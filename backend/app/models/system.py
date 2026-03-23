from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class SystemConfig(Base):
    """系统配置表"""
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=False)
    config_type = Column(String(50), default="string")
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class OperationLog(Base):
    """操作日志表"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    operation_type = Column(String(50), nullable=False)
    operation_content = Column(Text, nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
