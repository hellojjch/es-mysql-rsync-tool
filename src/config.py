from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # ES配置
    ES_HOST: str
    ES_PORT: int
    ES_USERNAME: Optional[str] = None
    ES_PASSWORD: Optional[str] = None
    
    # MySQL配置
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    
    # 同步配置
    BATCH_SIZE: int
    SCROLL_TIMEOUT: str
    CHECKPOINT_FILE: str
    
    # 索引配置
    INDEX_PREFIX: str
    SYNC_TIME: str
    TIMEZONE: str
    
    class Config:
        env_file = ".env"

settings = Settings() 