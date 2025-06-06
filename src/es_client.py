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
    
    def scroll_search(self, index_name: str, scroll_id: str = None, scroll_timeout: str = '5m'):
        """使用scroll API获取数据"""
        try:
            if scroll_id is None:
                # 初始搜索
                response = self.client.search(
                    index=index_name,
                    scroll=scroll_timeout,
                    size=1000,  # 每批次获取的数据量
                    body={
                        "query": {
                            "match_all": {}
                        }
                    }
                )
            else:
                # 继续滚动
                try:
                    response = self.client.scroll(
                        scroll_id=scroll_id,
                        scroll=scroll_timeout
                    )
                except Exception as e:
                    if "No search context found" in str(e):
                        # 如果scroll context已过期，重新开始搜索
                        logger.warning(f"Scroll context已过期，重新开始搜索: {str(e)}")
                        return self.scroll_search(index_name, None, scroll_timeout)
                    raise
            
            return response
        except Exception as e:
            logger.error(f"Scroll查询失败: {str(e)}")
            raise
    
    def close(self):
        """关闭ES客户端连接"""
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            logger.error(f"关闭ES连接失败: {str(e)}")

    def get_all_indices(self) -> list:
        """获取所有索引列表"""
        try:
            response = self.client.indices.get_alias().keys()
            return list(response)
        except Exception as e:
            logger.error(f"获取索引列表失败: {str(e)}")
            raise 