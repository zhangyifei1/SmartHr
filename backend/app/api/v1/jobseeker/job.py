from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user, requires_role, ROLE_JOBSEEKER
from app.models.user import User, JobseekerProfile
from app.schemas.job import JobFilterParams, Job, JobListItem, JobApplicationCreate, JobApplication, MatchResult, InterviewQuestion
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["求职者-岗位服务"])

@router.get("/recommend", response_model=List[JobListItem], summary="获取推荐岗位")
def get_recommended_jobs(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """获取个性化推荐岗位"""
    jobseeker = db.query(JobseekerProfile).filter(JobseekerProfile.user_id == current_user.id).first()
    return JobService.get_recommended_jobs(db, jobseeker.id, limit)

@router.get("", summary="搜索岗位列表")
def search_jobs(
    filter_params: JobFilterParams = Depends(),
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """搜索岗位，支持多条件筛选和分页"""
    jobs, total = JobService.get_job_list(db, filter_params)
    return {
        "list": jobs,
        "total": total,
        "page": filter_params.page,
        "page_size": filter_params.page_size
    }

@router.get("/{job_id}", response_model=Job, summary="获取岗位详情")
def get_job_detail(
    job_id: int,
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """获取岗位详细信息，同时增加浏览量"""
    return JobService.get_job_detail(db, job_id)

@router.post("/{job_id}/apply", summary="投递简历")
def apply_job(
    job_id: int,
    application_in: JobApplicationCreate,
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """投递简历到指定岗位"""
    jobseeker = db.query(JobseekerProfile).filter(JobseekerProfile.user_id == current_user.id).first()
    application = JobService.apply_job(db, job_id, jobseeker.id, application_in.resume_id)
    return {"message": "投递成功", "application_id": application.id}

@router.get("/{job_id}/match", response_model=MatchResult, summary="获取简历与岗位匹配度")
def get_job_match(
    job_id: int,
    resume_id: int = Query(..., description="简历ID"),
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """计算并返回指定简历与岗位的匹配度分析"""
    return JobService.calculate_match_score(db, job_id, resume_id)

@router.get("/{job_id}/interview-questions", response_model=List[InterviewQuestion], summary="生成面试题")
def get_interview_questions(
    job_id: int,
    resume_id: int = Query(..., description="简历ID"),
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """根据岗位和简历生成面试题和参考答案"""
    return JobService.generate_interview_questions(db, job_id, resume_id)

@router.get("/applications/my", summary="获取我的投递记录")
def get_my_applications(
    status: int = Query(None, description="投递状态筛选 1-已投递 2-已查看 3-面试中 4-已录用 5-已拒绝"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(requires_role(ROLE_JOBSEEKER)),
    db: Session = Depends(get_db)
):
    """获取我的投递记录列表"""
    jobseeker = db.query(JobseekerProfile).filter(JobseekerProfile.user_id == current_user.id).first()
    applications, total = JobService.get_application_list(db, jobseeker.id, status, page, page_size)
    return {
        "list": applications,
        "total": total,
        "page": page,
        "page_size": page_size
    }
