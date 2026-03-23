from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .system import router as system_router
from .dashboard import router as dashboard_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(system_router)
router.include_router(dashboard_router)

# 后续添加其他子模块路由
# from . import content, ai
# router.include_router(content.router, prefix="/content", tags=["管理端-内容审核"])
# router.include_router(ai.router, prefix="/ai", tags=["管理端-AI模型管理"])
