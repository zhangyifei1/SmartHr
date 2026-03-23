from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user, requires_role, ROLE_ENTERPRISE
from app.models.user import User, EnterpriseProfile
from app.schemas.enterprise import (
    EnterpriseJobCreate, EnterpriseJobUpdate, EnterpriseJobListItem,
    JobApplicationListItem, JobApplicationDetail
)
from app.services.enterprise_service import EnterpriseService

router = APIRouter(prefix="/jobs", tags=["企业端-岗位管理"])

@router.get("", summary="获取企业发布的岗位列表")
def get_job_list(
    status: int = Query(None, description="岗位状态筛选 0-关闭 1-开放 2-暂停"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """获取当前企业发布的所有岗位列表"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    jobs, total = EnterpriseService.get_job_list(db, enterprise.id, status, page, page_size)
    return {
        "list": jobs,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{job_id}", summary="获取岗位详情")
def get_job_detail(
    job_id: int,
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """获取指定岗位的详细信息"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    return EnterpriseService.get_job_detail(db, job_id, enterprise.id)

@router.post("", summary="发布新岗位")
def create_job(
    job_in: EnterpriseJobCreate,
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """发布新的招聘岗位"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    job = EnterpriseService.create_job(db, enterprise.id, job_in)
    return {"message": "发布成功", "job_id": job.id, "job": job}

@router.put("/{job_id}", summary="更新岗位信息")
def update_job(
    job_id: int,
    job_in: EnterpriseJobUpdate,
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """更新已有岗位的信息"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    job = EnterpriseService.update_job(db, job_id, enterprise.id, job_in)
    return {"message": "更新成功", "job": job}

@router.patch("/{job_id}/status", summary="更新岗位状态")
def update_job_status(
    job_id: int,
    status: int = Query(..., description="新状态 0-关闭 1-开放 2-暂停"),
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """更新岗位的状态（开放/关闭/暂停）"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    EnterpriseService.update_job_status(db, job_id, enterprise.id, status)
    return {"message": "状态更新成功"}

@router.get("/{job_id}/applications", summary="获取岗位投递记录")
def get_job_applications(
    job_id: int,
    status: int = Query(None, description="投递状态筛选 1-已投递 2-已查看 3-面试中 4-已录用 5-已拒绝"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """获取指定岗位的所有投递记录"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    applications, total = EnterpriseService.get_job_applications(db, enterprise.id, job_id, status, page, page_size)
    return {
        "list": applications,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/applications/{application_id}", response_model=JobApplicationDetail, summary="获取投递详情")
def get_application_detail(
    application_id: int,
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """获取投递记录的详细信息和简历内容"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    return EnterpriseService.get_application_detail(db, application_id, enterprise.id)

@router.patch("/applications/{application_id}/status", summary="更新投递状态")
def update_application_status(
    application_id: int,
    status: int = Query(..., description="新状态 1-已投递 2-已查看 3-面试中 4-已录用 5-已拒绝"),
    feedback: str = Query(None, description="反馈信息"),
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """更新投递记录的状态（查看/面试/录用/拒绝）"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    EnterpriseService.update_application_status(db, application_id, enterprise.id, status, feedback)
    return {"message": "状态更新成功"}

@router.post("/applications/{application_id}/arrange-interview", summary="安排面试")
def arrange_interview(
    application_id: int,
    interview_time: datetime = Query(..., description="面试时间"),
    notes: str = Query(None, description="面试备注"),
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """为候选人安排面试时间"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    EnterpriseService.arrange_interview(db, application_id, enterprise.id, interview_time, notes)
    return {"message": "面试安排成功"}
