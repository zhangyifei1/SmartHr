from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job, JobApplication
from app.core.dependencies import get_current_jobseeker

router = APIRouter(prefix="", tags=["求职者-首页"])

@router.get("/statistics", summary="获取首页统计数据")
def get_statistics(
    db: Session = Depends(get_db),
    current_jobseeker = Depends(get_current_jobseeker)
):
    # 统计在招岗位总数
    job_count = db.query(Job).filter(Job.status == 1).count()

    # 统计我的投递总数
    application_count = db.query(JobApplication).filter(
        JobApplication.jobseeker_id == current_jobseeker.id
    ).count()

    # 统计我的面试邀请数量
    interview_count = db.query(JobApplication).filter(
        JobApplication.jobseeker_id == current_jobseeker.id,
        JobApplication.status == 3
    ).count()

    return {
        "job_count": job_count,
        "application_count": application_count,
        "interview_count": interview_count
    }
