from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.api.dependencies import requires_role, ROLE_ENTERPRISE
from app.models.user import User, EnterpriseProfile
from app.schemas.enterprise import EnterpriseProfileUpdate, EnterpriseAuthSubmit, EnterpriseProfileOut
from app.services.enterprise_service import EnterpriseService

router = APIRouter(prefix="/profile", tags=["企业端-企业信息"])

@router.get("/auth-status", summary="获取企业认证状态")
def get_auth_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前企业的认证状态，不需要通过认证校验"""
    enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.user_id == current_user.id).first()
    return {
        "auth_status": enterprise.auth_status,
        "auth_reason": enterprise.auth_reason
    }

@router.get("", response_model=EnterpriseProfileOut, summary="获取企业信息")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前企业的信息"""
    return EnterpriseService.get_profile(db, current_user.id)

@router.put("", response_model=EnterpriseProfileOut, summary="更新企业信息")
def update_profile(
    profile_in: EnterpriseProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新企业基本信息"""
    return EnterpriseService.update_profile(db, current_user.id, profile_in)

@router.post("/auth", response_model=EnterpriseProfileOut, summary="提交企业认证")
def submit_auth(
    auth_in: EnterpriseAuthSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交企业认证申请"""
    return EnterpriseService.submit_auth(db, current_user.id, auth_in)
