"""
应用配置管理
"""
import os
from typing import Optional

class Settings:
    """应用配置类"""
    
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "销售数据分析系统"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./sales_analyzer.db"
    
    # 文件上传配置
    UPLOAD_DIR: str = "data/uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".csv", ".xlsx", ".xls"]
    
    # 数据处理配置
    BATCH_SIZE: int = 1000
    CHUNK_SIZE: int = 10000
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局配置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 