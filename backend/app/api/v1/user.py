from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.response import success_response, error_response
from app.models.user import User
from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserInfoOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    role: str = "user"
    createdAt: str

    class Config:
        from_attributes = True


class UserInfoUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


@router.get("/info", summary="获取用户信息")
async def get_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前登录用户的详细信息
    """
    user_data = UserInfoOut(
        id=current_user.id,
        name=current_user.username,
        email=current_user.email,
        phone=current_user.phone,
        role="user" if current_user.user_type == 1 else "enterprise" if current_user.user_type == 2 else "admin",
        createdAt=current_user.created_at.isoformat() if current_user.created_at else ""
    )
    return success_response(data=user_data.dict())


@router.put("/info", summary="更新用户信息")
async def update_user_info(
    user_update: UserInfoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前登录用户的信息
    """
    try:
        # 更新用户信息
        if user_update.name is not None:
            current_user.username = user_update.name
        if user_update.email is not None:
            current_user.email = user_update.email
        if user_update.phone is not None:
            current_user.phone = user_update.phone

        db.commit()
        db.refresh(current_user)

        user_data = UserInfoOut(
            id=current_user.id,
            name=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
            role="user" if current_user.user_type == 1 else "enterprise" if current_user.user_type == 2 else "admin",
            createdAt=current_user.created_at.isoformat() if current_user.created_at else ""
        )
        return success_response(data=user_data.dict())
    except Exception as e:
        db.rollback()
        return error_response(msg=f"更新失败: {str(e)}")
