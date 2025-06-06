from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from loguru import logger
from .config import settings
import json

class MySQLClient:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@"
            f"{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
        )
        self.metadata = MetaData()
    
    def create_table_from_mapping(self, index_name: str, mapping: dict):
        """根据ES的mapping创建MySQL表"""
        try:
            columns = []
            properties = mapping.get('properties', {})
            
            # 添加id字段
            columns.append(Column('id', String(255), primary_key=True))
            
            # 根据mapping创建字段
            for field_name, field_info in properties.items():
                field_type = field_info.get('type', 'text')
                column = self._get_column_type(field_name, field_type)
                if column:
                    columns.append(column)
            
            # 创建表
            table = Table(index_name, self.metadata, *columns)
            table.create(self.engine, checkfirst=True)
            logger.info(f"表 {index_name} 创建成功")
            
        except Exception as e:
            logger.error(f"创建表失败: {str(e)}")
            raise
    
    def _get_column_type(self, field_name: str, field_type: str):
        """将ES字段类型转换为MySQL字段类型"""
        type_mapping = {
            'keyword': String(255),
            'text': LONGTEXT,
            'long': Integer,
            'integer': Integer,
            'float': Float,
            'double': Float,
            'date': DateTime,
            'object': JSON,
            'nested': JSON
        }
        
        return Column(field_name, type_mapping.get(field_type, LONGTEXT))
    
    def bulk_insert(self, table_name: str, data: list):
        """批量插入数据"""
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            with self.engine.begin() as conn:
                conn.execute(table.insert(), data)
            logger.info(f"成功插入 {len(data)} 条数据到表 {table_name}")
        except Exception as e:
            logger.error(f"批量插入数据失败: {str(e)}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        self.engine.dispose() 