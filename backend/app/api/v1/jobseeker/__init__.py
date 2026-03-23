from fastapi import APIRouter
from .resume import router as resume_router
from .job import router as job_router
from .home import router as home_router

router = APIRouter()

router.include_router(home_router)
router.include_router(resume_router)
router.include_router(job_router)

# 后续添加其他子模块路由
# from . import application, ai
# router.include_router(application.router, prefix="/applications", tags=["求职者-申请管理"])
# router.include_router(ai.router, prefix="/ai", tags=["求职者-AI助手"])
