from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8")

    # 基础配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SmartHr"
    DEBUG: bool = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///../database/smarthr.db"
    SQLALCHEMY_ECHO: bool = DEBUG

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 上传配置
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"}

    # 火山引擎大模型配置
    VOLCENGINE_API_KEY: Optional[str] = None
    VOLCENGINE_MODEL: str = "doubao-1.5-pro-250115"
    VOLCENGINE_API_URL: str = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    # 系统配置
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

settings = Settings()

# 确保上传目录存在
os.makedirs(os.path.join(settings.UPLOAD_DIR, "resumes"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "logos"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "avatars"), exist_ok=True)
