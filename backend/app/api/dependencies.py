from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import InvalidTokenException, PermissionDeniedException
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

class TokenData(BaseModel):
    user_id: Optional[int] = None

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """获取当前登录用户"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException()
        token_data = TokenData(user_id=int(user_id))
    except JWTError:
        raise InvalidTokenException()

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise InvalidTokenException()
    if user.status == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户已被禁用")
    return user

def requires_role(required_role: int):
    """角色权限校验装饰器"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.user_type != required_role:
            raise PermissionDeniedException()
        return current_user
    return role_checker

# 角色常量
ROLE_JOBSEEKER = 1
ROLE_ENTERPRISE = 2
ROLE_ADMIN = 3
