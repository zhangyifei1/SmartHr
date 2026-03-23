from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job, JobApplication
from app.core.dependencies import get_current_enterprise

router = APIRouter(prefix="", tags=["企业-首页"])

@router.get("/statistics", summary="获取企业首页统计数据")
def get_statistics(
    db: Session = Depends(get_db),
    current_enterprise = Depends(get_current_enterprise)
):
    # 统计在招岗位数
    job_count = db.query(Job).filter(
        Job.enterprise_id == current_enterprise.id,
        Job.status == 1
    ).count()

    # 统计收到的简历总数
    application_count = db.query(JobApplication).join(Job).filter(
        Job.enterprise_id == current_enterprise.id
    ).count()

    # 统计面试中数量
    interview_count = db.query(JobApplication).join(Job).filter(
        Job.enterprise_id == current_enterprise.id,
        JobApplication.status == 3
    ).count()

    # 统计已录用数量
    hire_count = db.query(JobApplication).join(Job).filter(
        Job.enterprise_id == current_enterprise.id,
        JobApplication.status == 4
    ).count()

    return {
        "job_count": job_count,
        "application_count": application_count,
        "interview_count": interview_count,
        "hire_count": hire_count
    }
