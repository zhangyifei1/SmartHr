from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.job import Job, JobApplication
from app.models.resume import Resume
from app.models.user import JobseekerProfile, User
from app.core.dependencies import get_current_enterprise
from app.schemas.application import ApplicationProcess
from app.core.response import success_response
from app.services.job_service import JobService

router = APIRouter(prefix="/applications", tags=["企业-投递管理"])

@router.get("", summary="获取所有投递列表")
def get_all_applications(
    keyword: str = Query(None, description="搜索关键词"),
    status: int = Query(None, description="投递状态"),
    score_range: str = Query(None, description="AI分数范围筛选：80+, 60-80, 0-60"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_enterprise = Depends(get_current_enterprise)
):
    query = db.query(JobApplication).join(Job).filter(
        Job.enterprise_id == current_enterprise.id
    ).outerjoin(
        Resume, JobApplication.resume_id == Resume.id
    ).outerjoin(
        JobseekerProfile, JobApplication.jobseeker_id == JobseekerProfile.id
    ).outerjoin(
        User, JobseekerProfile.user_id == User.id
    )

    # 关键词搜索
    if keyword:
        query = query.filter(
            or_(
                Job.title.contains(keyword),
                Resume.title.contains(keyword),
                User.username.contains(keyword),
                User.phone.contains(keyword)
            )
        )

    # 状态筛选
    if status is not None:
        query = query.filter(JobApplication.status == status)

    # AI分数范围筛选
    if score_range:
        if score_range == "80+":
            query = query.filter(JobApplication.match_score >= 80)
        elif score_range == "60-80":
            query = query.filter(JobApplication.match_score >= 60, JobApplication.match_score < 80)
        elif score_range == "0-60":
            query = query.filter(JobApplication.match_score < 60)

    total = query.count()
    applications = query.order_by(JobApplication.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()

    # 手动转换字典，兼容缺少to_dict方法的情况
    result = []
    for app in applications:
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": app.job.title,
            "resume_id": app.resume_id,
            "resume_title": app.resume.title if app.resume else "未命名简历",
            "jobseeker_name": app.resume.jobseeker.user.username if app.resume and app.resume.jobseeker and app.resume.jobseeker.user else "匿名",
            "phone": app.resume.jobseeker.user.phone if app.resume and app.resume.jobseeker and app.resume.jobseeker.user else "",
            "email": app.resume.jobseeker.user.email if app.resume and app.resume.jobseeker and app.resume.jobseeker.user else "",
            "match_score": app.match_score,
            "match_analysis": app.match_analysis,
            "status": app.status,
            "created_at": app.created_at.strftime("%Y-%m-%d %H:%M:%S") if app.created_at else "",
            "updated_at": app.updated_at.strftime("%Y-%m-%d %H:%M:%S") if app.updated_at else ""
        })

    return success_response(data={
        "list": result,
        "total": total,
        "page": page,
        "page_size": page_size
    })

@router.post("/{application_id}/process", summary="处理投递申请")
def process_application(
    application_id: int,
    data: ApplicationProcess,
    db: Session = Depends(get_db),
    current_enterprise = Depends(get_current_enterprise)
):
    application = db.query(JobApplication).join(Job).filter(
        JobApplication.id == application_id,
        Job.enterprise_id == current_enterprise.id
    ).first()

    if not application:
        return success_response(code=404, msg="投递记录不存在")

    application.status = data.status
    if hasattr(application, 'remark'):
        application.remark = data.remark
    db.commit()

    return success_response(msg="操作成功")

@router.post("/{application_id}/match", summary="触发AI匹配测评")
def trigger_ai_match(
    application_id: int,
    db: Session = Depends(get_db),
    current_enterprise = Depends(get_current_enterprise)
):
    """手动触发AI匹配测评，生成匹配分数和分析报告"""
    application = db.query(JobApplication).join(Job).filter(
        JobApplication.id == application_id,
        Job.enterprise_id == current_enterprise.id
    ).first()

    if not application:
        return success_response(code=404, msg="投递记录不存在")

    # 调用AI服务计算匹配度
    result = JobService.calculate_match_score(db, application.job_id, application.resume_id)

    # 更新投递记录的匹配信息
    application.match_score = result.get("match_score", 0)
    application.match_analysis = result.get("match_analysis", "")
    db.commit()

    return success_response(msg="测评完成", data={
        "match_score": application.match_score,
        "match_analysis": application.match_analysis
    })
