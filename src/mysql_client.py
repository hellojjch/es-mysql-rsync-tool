from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, DateTime, JSON, text
from sqlalchemy.dialects.mysql import LONGTEXT
from loguru import logger
from src.config import settings
import json
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
from typing import Dict, Any, Optional
from datetime import datetime

class MySQLClient:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        # URL 编码密码，处理特殊字符
        encoded_password = quote_plus(password)
        self.engine = create_engine(
            f'mysql+mysqlconnector://{user}:{encoded_password}@{host}:{port}/{database}',
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
        self.metadata = MetaData()
        self.connection = None
    
    def create_table_from_mapping(self, index_name: str, mapping: dict):
        """根据ES的mapping创建MySQL表"""
        try:
            # 检查表是否已存在
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SHOW TABLES LIKE '{index_name}'"))
                if result.fetchone():
                    logger.info(f"表 {index_name} 已存在")
                    return

            # 构建建表SQL
            columns = []
            properties = mapping.get('properties', {})
            
            # 根据mapping创建字段
            for field_name, field_info in properties.items():
                field_type = field_info.get('type', 'text')
                # 如果是id字段，强制使用VARCHAR类型
                if field_name == 'id':
                    columns.append("`id` VARCHAR(255)")
                else:
                    column_def = self._get_column_definition(field_name, field_type)
                    if column_def:
                        columns.append(column_def)
            
            # 添加主键约束
            if 'id' in properties:
                columns.append("PRIMARY KEY (`id`)")
            
            # 创建表
            create_table_sql = f"CREATE TABLE `{index_name}` ({', '.join(columns)})"
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
            
            logger.info(f"表 {index_name} 创建成功")
            
        except Exception as e:
            logger.error(f"创建表失败: {str(e)}")
            raise
    
    def _get_column_definition(self, field_name: str, field_type: str) -> str:
        """将ES字段类型转换为MySQL字段定义"""
        type_mapping = {
            'keyword': 'VARCHAR(255)',
            'text': 'LONGTEXT',
            'long': 'BIGINT',
            'integer': 'INT',
            'float': 'FLOAT',
            'double': 'DOUBLE',
            'date': 'DATETIME',
            'object': 'JSON',
            'nested': 'JSON'
        }
        
        mysql_type = type_mapping.get(field_type, 'LONGTEXT')
        return f"`{field_name}` {mysql_type}"
    
    def bulk_insert(self, table_name: str, data: list):
        """批量插入数据"""
        try:
            if not data:
                return
                
            # 获取表结构
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            
            # 批量插入数据
            with self.engine.begin() as conn:
                conn.execute(table.insert(), data)
            
            logger.info(f"成功插入 {len(data)} 条数据到表 {table_name}")
        except Exception as e:
            logger.error(f"批量插入数据失败: {str(e)}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        self.engine.dispose() 