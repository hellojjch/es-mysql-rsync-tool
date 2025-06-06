from elasticsearch import Elasticsearch
from loguru import logger
from src.config import settings

class ESClient:
    def __init__(self):
        self.client = Elasticsearch(
            hosts=[f"http://{settings.ES_HOST}:{settings.ES_PORT}"],
            basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD) if settings.ES_USERNAME else None
        )
    
    def get_index_mapping(self, index_name: str) -> dict:
        """获取索引的mapping信息"""
        try:
            response = self.client.indices.get_mapping(index=index_name)
            return response[index_name]['mappings']
        except Exception as e:
            logger.error(f"获取索引mapping失败: {str(e)}")
            raise
    
    def scroll_search(self, index_name: str, scroll_id: str = None):
        """使用scroll API进行分页查询"""
        try:
            if scroll_id:
                response = self.client.scroll(
                    scroll_id=scroll_id,
                    scroll=settings.SCROLL_TIMEOUT
                )
            else:
                response = self.client.search(
                    index=index_name,
                    scroll=settings.SCROLL_TIMEOUT,
                    size=settings.BATCH_SIZE,
                    body={"query": {"match_all": {}}}
                )
            
            return response
        except Exception as e:
            logger.error(f"Scroll查询失败: {str(e)}")
            raise
    
    def close(self):
        """关闭ES连接"""
        self.client.close()

    def get_all_indices(self) -> list:
        """获取所有索引列表"""
        try:
            response = self.client.indices.get_alias().keys()
            return list(response)
        except Exception as e:
            logger.error(f"获取索引列表失败: {str(e)}")
            raise 