from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.exceptions import UserNotFoundException, IncorrectUsernameOrPasswordException, UserAlreadyExistsException
from app.models.user import User, JobseekerProfile, EnterpriseProfile
from app.schemas.user import UserCreate, Token, UserOut

router = APIRouter()

@router.post("/register", response_model=UserOut, summary="用户注册")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    - user_type: 1-求职者 2-企业
    """
    # 检查用户名是否存在
    db_user = db.query(User).filter(User.username == user_in.username).first()
    if db_user:
        raise UserAlreadyExistsException(message="用户名已存在")

    # 检查手机号是否存在
    if user_in.phone:
        db_user = db.query(User).filter(User.phone == user_in.phone).first()
        if db_user:
            raise UserAlreadyExistsException(message="手机号已被注册")

    # 检查邮箱是否存在
    if user_in.email:
        db_user = db.query(User).filter(User.email == user_in.email).first()
        if db_user:
            raise UserAlreadyExistsException(message="邮箱已被注册")

    # 创建用户
    user = User(
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        email=user_in.email,
        phone=user_in.phone,
        user_type=user_in.user_type
    )
    db.add(user)
    db.flush()

    # 创建对应角色的profile
    if user_in.user_type == 1:
        profile = JobseekerProfile(user_id=user.id)
        db.add(profile)
    elif user_in.user_type == 2:
        # 企业用户注册，默认未认证状态
        profile = EnterpriseProfile(
            user_id=user.id,
            company_name=user_in.company_name or "",
            unified_social_credit_code=user_in.unified_social_credit_code or "",
            legal_person=user_in.legal_person or "",
            business_license=user_in.business_license or "",
            auth_status=0  # 0-未提交认证
        )
        db.add(profile)

    db.commit()
    db.refresh(user)

    return user

@router.post("/login", response_model=Token, summary="用户登录")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录，支持用户名/手机号/邮箱登录
    """
    # 尝试用用户名、手机号、邮箱分别查询
    user = db.query(User).filter(
        (User.username == form_data.username) |
        (User.phone == form_data.username) |
        (User.email == form_data.username)
    ).first()

    if not user:
        raise UserNotFoundException()

    if not verify_password(form_data.password, user.password_hash):
        raise IncorrectUsernameOrPasswordException()

    if user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被禁用"
        )

    # 生成token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.user_type
    }
