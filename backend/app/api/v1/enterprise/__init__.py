from fastapi import APIRouter
from .profile import router as profile_router
from .job import router as job_router
from .home import router as home_router
from .application import router as application_router

router = APIRouter()

router.include_router(home_router)
router.include_router(profile_router)
router.include_router(job_router)
router.include_router(application_router)

# 后续添加其他子模块路由
# from . import talent, dashboard
# router.include_router(talent.router, prefix="/talent", tags=["企业端-人才库"])
# router.include_router(dashboard.router, prefix="/dashboard", tags=["企业端-数据看板"])
