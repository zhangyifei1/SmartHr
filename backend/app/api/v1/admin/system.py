from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.admin import SystemConfigItem, SystemConfigUpdate, DashboardStats, BusinessStats, SystemMonitorStats
from app.services.admin_service import AdminService

# 角色常量
ROLE_ADMIN = 3

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if current_user.user_type != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

router = APIRouter(prefix="/system", tags=["管理端-系统管理"])

@router.get("/config", summary="获取系统配置列表")
def get_system_config(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有系统配置项"""
    configs = AdminService.get_system_config_list(db)
    return {"list": configs}

@router.put("/config/{config_key}", summary="更新系统配置")
def update_system_config(
    config_key: str,
    config_in: SystemConfigUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新指定的系统配置项"""
    config = AdminService.update_system_config(db, config_key, config_in.config_value)
    return {"message": "更新成功", "config": config}

@router.get("/dashboard/stats", response_model=DashboardStats, summary="获取数据看板核心指标")
def get_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取管理后台首页核心统计指标"""
    return AdminService.get_dashboard_stats(db)

@router.get("/dashboard/business", response_model=BusinessStats, summary="获取业务统计数据")
def get_business_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取业务增长、转化率等统计数据"""
    return AdminService.get_business_stats(db)

@router.get("/dashboard/monitor", response_model=SystemMonitorStats, summary="获取系统监控数据")
def get_system_monitor_stats(
    current_user: User = Depends(get_current_admin)
):
    """获取服务器性能、API监控等系统指标"""
    return AdminService.get_system_monitor_stats()
