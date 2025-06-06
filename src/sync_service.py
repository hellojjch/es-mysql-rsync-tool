import json
from loguru import logger
from src.es_client import ESClient
from src.mysql_client import MySQLClient
from src.config import settings

class SyncService:
    def __init__(self):
        self.es_client = ESClient()
        self.mysql_client = MySQLClient()
    
    def sync_index(self, index_name: str):
        """同步指定索引的数据到MySQL"""
        try:
            # 获取ES索引mapping
            mapping = self.es_client.get_index_mapping(index_name)
            
            # 创建MySQL表
            self.mysql_client.create_table_from_mapping(index_name, mapping)
            
            # 加载检查点
            checkpoint = self._load_checkpoint(index_name)
            scroll_id = checkpoint.get('scroll_id')
            
            while True:
                # 使用scroll API获取数据
                response = self.es_client.scroll_search(index_name, scroll_id)
                scroll_id = response['_scroll_id']
                hits = response['hits']['hits']
                
                if not hits:
                    break
                
                # 处理数据
                data = []
                for hit in hits:
                    doc = hit['_source']
                    doc['id'] = hit['_id']
                    data.append(doc)
                
                # 批量插入MySQL
                self.mysql_client.bulk_insert(index_name, data)
                
                # 保存检查点
                self._save_checkpoint(index_name, {
                    'scroll_id': scroll_id,
                    'processed_count': checkpoint.get('processed_count', 0) + len(data)
                })
                
                logger.info(f"已处理 {len(data)} 条数据")
            
            logger.info(f"索引 {index_name} 同步完成")
            
        except Exception as e:
            logger.error(f"同步失败: {str(e)}")
            raise
        finally:
            self.es_client.close()
            self.mysql_client.close()
    
    def _load_checkpoint(self, index_name: str) -> dict:
        """加载检查点"""
        try:
            with open(f"{settings.CHECKPOINT_FILE}", 'r') as f:
                checkpoints = json.load(f)
                return checkpoints.get(index_name, {})
        except FileNotFoundError:
            return {}
    
    def _save_checkpoint(self, index_name: str, checkpoint: dict):
        """保存检查点"""
        try:
            try:
                with open(settings.CHECKPOINT_FILE, 'r') as f:
                    checkpoints = json.load(f)
            except FileNotFoundError:
                checkpoints = {}
            
            checkpoints[index_name] = checkpoint
            
            with open(settings.CHECKPOINT_FILE, 'w') as f:
                json.dump(checkpoints, f)
        except Exception as e:
            logger.error(f"保存检查点失败: {str(e)}")
            raise 