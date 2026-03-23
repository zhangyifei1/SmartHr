from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, JobseekerProfile, EnterpriseProfile
from app.models.job import Job, JobApplication

# 角色常量
ROLE_JOBSEEKER = 1
ROLE_ENTERPRISE = 2
ROLE_ADMIN = 3

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if current_user.user_type != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

router = APIRouter(prefix="/dashboard", tags=["管理端-数据看板"])

@router.get("/statistics", summary="获取系统统计数据")
def get_statistics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """获取系统整体统计数据"""
    # 总用户数
    total_users = db.query(User).count()

    # 求职者数
    jobseeker_count = db.query(JobseekerProfile).count()

    # 企业数
    enterprise_count = db.query(EnterpriseProfile).count()

    # 岗位总数
    total_jobs = db.query(Job).count()

    # 投递总数
    total_applications = db.query(JobApplication).count()

    # 待认证企业数
    pending_enterprise_auth = db.query(EnterpriseProfile).filter(
        EnterpriseProfile.auth_status == 1
    ).count()

    return {
        "total_users": total_users,
        "jobseeker_count": jobseeker_count,
        "enterprise_count": enterprise_count,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "pending_enterprise_auth": pending_enterprise_auth
    }

@router.get("/recent-users", summary="获取最近注册用户")
def get_recent_users(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """获取最近注册的用户列表"""
    users = db.query(User).order_by(User.created_at.desc()).limit(limit).all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "phone": user.phone,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else ""
        })

    return result

@router.get("/recent-jobs", summary="获取最新发布岗位")
def get_recent_jobs(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """获取最新发布的岗位列表"""
    jobs = db.query(Job).join(EnterpriseProfile).order_by(Job.created_at.desc()).limit(limit).all()

    result = []
    for job in jobs:
        result.append({
            "id": job.id,
            "title": job.title,
            "enterprise_name": job.enterprise.company_name if job.enterprise else "",
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "work_city": job.work_city,
            "education_requirement": job.education_requirement,
            "status": job.status,
            "created_at": job.created_at.strftime("%Y-%m-%d %H:%M:%S") if job.created_at else ""
        })

    return result

@router.get("/recent-applications", summary="获取最新投递记录")
def get_recent_applications(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """获取最新的投递记录列表"""
    applications = db.query(JobApplication).join(Job).order_by(JobApplication.created_at.desc()).limit(limit).all()

    result = []
    for app in applications:
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": app.job.title if app.job else "",
            "jobseeker_id": app.jobseeker_id,
            "jobseeker_name": app.resume.jobseeker.user.username if app.resume and app.resume.jobseeker and app.resume.jobseeker.user else "匿名",
            "resume_id": app.resume_id,
            "resume_title": app.resume.title if app.resume else "未命名简历",
            "status": app.status,
            "match_score": app.match_score,
            "created_at": app.created_at.strftime("%Y-%m-%d %H:%M:%S") if app.created_at else ""
        })

    return result
