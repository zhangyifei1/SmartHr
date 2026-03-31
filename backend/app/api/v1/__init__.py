from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as user_router
from .jobseeker import router as jobseeker_router
from .enterprise import router as enterprise_router
from .admin import router as admin_router
from .common import router as common_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["认证相关"])
api_router.include_router(user_router, prefix="/user", tags=["用户相关"])
api_router.include_router(common_router, prefix="/common", tags=["公共接口"])
api_router.include_router(jobseeker_router, prefix="/jobseeker", tags=["求职者端接口"])
api_router.include_router(enterprise_router, prefix="/enterprise", tags=["企业端接口"])
api_router.include_router(admin_router, prefix="/admin", tags=["管理端接口"])
