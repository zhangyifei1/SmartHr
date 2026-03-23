from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
from .config import settings
from .database import get_db
from app.models.user import User, JobseekerProfile, EnterpriseProfile

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_jobseeker(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> JobseekerProfile:
    """获取当前求职者用户"""
    jobseeker = db.query(JobseekerProfile).filter(JobseekerProfile.user_id == current_user.id).first()
    if not jobseeker:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a jobseeker user"
        )
    return jobseeker

async def get_current_enterprise(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EnterpriseProfile:
    """获取当前企业用户，会校验认证状态"""
    enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="不是企业用户"
        )

    # 检查企业认证状态
    if enterprise.auth_status == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请先完善企业信息并提交认证申请"
        )
    if enterprise.auth_status == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="企业资质正在审核中，暂时无法使用该功能"
        )
    if enterprise.auth_status == 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"企业资质审核未通过：{enterprise.auth_reason or '请重新提交认证信息'}"
        )
    if enterprise.auth_status != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="企业未通过认证，无法使用该功能"
        )

    return enterprise
