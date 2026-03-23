from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, min_length=11, max_length=11, description="手机号")
    user_type: int = Field(..., ge=1, le=3, description="用户类型 1-求职者 2-企业 3-管理员")
    company_name: Optional[str] = Field(None, description="企业名称（企业用户注册时必填）")
    unified_social_credit_code: Optional[str] = Field(None, description="统一社会信用代码（企业用户注册时必填）")
    legal_person: Optional[str] = Field(None, description="法人姓名（企业用户注册时必填）")
    business_license: Optional[str] = Field(None, description="营业执照图片地址（企业用户注册时必填）")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50, description="密码")

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    phone: Optional[str]
    user_type: int
    status: int
    avatar: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: int

class TokenData(BaseModel):
    user_id: Optional[int] = None
