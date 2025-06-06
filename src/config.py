from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Elasticsearch配置
    ES_HOST: str = "localhost"
    ES_PORT: int = 9200
    ES_USERNAME: Optional[str] = None
    ES_PASSWORD: Optional[str] = None
    
    # MySQL配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "es_sync"
    
    # 同步配置
    BATCH_SIZE: int = 1000
    SCROLL_TIMEOUT: str = "5m"
    CHECKPOINT_FILE: str = "checkpoint.json"
    
    class Config:
        env_file = ".env"

settings = Settings() 