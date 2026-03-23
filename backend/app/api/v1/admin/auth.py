from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.admin import EnterpriseAuthListItem, EnterpriseAuthAudit
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

router = APIRouter(prefix="/enterprise-auth", tags=["管理端-企业认证审核"])

@router.get("", summary="获取企业认证申请列表")
def get_enterprise_auth_list(
    status: int = Query(None, description="审核状态筛选 1-审核中 2-已通过 3-已拒绝"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有企业认证申请列表"""
    profiles, total = AdminService.get_enterprise_auth_list(db, status, page, page_size)
    return {
        "list": profiles,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.post("/{enterprise_id}/audit", summary="审核企业认证申请")
def audit_enterprise_auth(
    enterprise_id: int,
    audit_in: EnterpriseAuthAudit,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """审核企业认证申请，通过或拒绝"""
    AdminService.audit_enterprise_auth(db, enterprise_id, audit_in.status, audit_in.reason)
    return {"message": "审核完成"}
