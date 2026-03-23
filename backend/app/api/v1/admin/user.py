from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.admin import UserListItem
from app.services.admin_service import AdminService

# 角色常量
ROLE_JOBSEEKER = 1
ROLE_ENTERPRISE = 2
ROLE_ADMIN = 3

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if current_user.user_type != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

router = APIRouter(prefix="/users", tags=["管理端-用户管理"])

@router.get("", summary="获取用户列表")
def get_user_list(
    user_type: int = Query(None, description="用户类型筛选 1-求职者 2-企业 3-管理员"),
    status: int = Query(None, description="状态筛选 0-禁用 1-正常"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有用户列表，支持筛选和分页"""
    users, total = AdminService.get_user_list(db, user_type, status, page, page_size)
    return {
        "list": users,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.patch("/{user_id}/status", summary="更新用户状态")
def update_user_status(
    user_id: int,
    status: int = Query(..., description="新状态 0-禁用 1-正常"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """启用或禁用用户账号，管理员账号不能被修改"""
    AdminService.update_user_status(db, user_id, status)
    return {"message": "状态更新成功"}
