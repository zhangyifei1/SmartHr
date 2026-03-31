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
from app.services.job_service import JobService
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
    status: int = Query(None, description="新状态 0-关闭 1-开放 2-暂停"),
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """更新岗位的状态（开放/关闭/暂停）"""
    enterprise = EnterpriseService.get_profile(db, current_user.id)
    EnterpriseService.update_job_status(db, job_id, enterprise.id, status)
    return {"message": "状态更新成功"}


@router.post("/{job_id}/status", summary="更新岗位状态(POST)")
def update_job_status_post(
    job_id: int,
    data: dict,
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """更新岗位的状态（开放/关闭/暂停） - 支持POST方式"""
    status = data.get("status")
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

@router.post("/{job_id}/analyze-all", summary="一键分析所有投递简历")
def analyze_all_applications(
    job_id: int,
    current_user: User = Depends(requires_role(ROLE_ENTERPRISE)),
    db: Session = Depends(get_db)
):
    """一键分析指定岗位的所有投递简历，生成AI匹配报告"""
    import asyncio
    import json
    from app.services.volcengine_service import volcengine_ai_service

    enterprise = EnterpriseService.get_profile(db, current_user.id)

    # 获取该岗位的所有投递记录
    from app.models.job import JobApplication, Job
    from app.models.resume import Resume
    job = db.query(Job).filter(Job.id == job_id, Job.enterprise_id == enterprise.id).first()
    if not job:
        raise BusinessException(code=404001, message="岗位不存在")

    applications = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()

    results = []
    resume_summaries = []

    for app in applications:
        try:
            # 计算匹配度
            match_result = JobService.calculate_match_score(db, job_id, app.resume_id)

            # 更新投递记录
            app.match_score = match_result.get("match_score", 0)
            app.match_analysis = match_result.get("match_analysis", "")

            # 获取简历信息用于综合分析
            resume = db.query(Resume).filter(Resume.id == app.resume_id).first()
            if resume and resume.content:
                try:
                    resume_data = json.loads(resume.content)
                    personal_info = resume_data.get("personal_info", {})
                    resume_summaries.append({
                        "application_id": app.id,
                        "match_score": app.match_score,
                        "match_analysis": app.match_analysis,
                        "name": personal_info.get("姓名", "未知"),
                        "education": personal_info.get("学历", ""),
                        "work_experience": resume_data.get("work_experience", []),
                        "skills": resume_data.get("skills", [])
                    })
                except:
                    pass

            results.append({
                "application_id": app.id,
                "resume_id": app.resume_id,
                "match_score": app.match_score,
                "success": True
            })
        except Exception as e:
            results.append({
                "application_id": app.id,
                "resume_id": app.resume_id,
                "success": False,
                "error": str(e)
            })

    db.commit()

    success_count = sum(1 for r in results if r["success"])

    # 生成综合分析报告
    comprehensive_analysis = None
    if success_count > 0:
        try:
            # 提取岗位信息
            work_year = job.work_year_requirement
            if work_year:
                if work_year == 0:
                    work_year_str = "应届生"
                else:
                    work_year_str = f"{work_year}年及以上"
            else:
                work_year_str = "不限"

            job_info = f"""
岗位名称：{job.title}
工作城市：{job.work_city}
薪资范围：{job.salary_min}-{job.salary_max}K
学历要求：{job.education_requirement or '不限'}
工作经验要求：{work_year_str}
岗位职责：
{job.job_description}

任职要求：
{job.job_requirement}
"""

            # 构建简历概况
            resumes_overview = json.dumps(resume_summaries, ensure_ascii=False, indent=2)

            prompt = f"""
你是专业的招聘分析专家，请根据以下岗位信息和已分析的简历数据，生成一份综合分析报告。

【岗位信息】
{job_info}

【已分析的简历概况】
{resumes_overview}

请生成一份全面的分析报告，以JSON格式返回，包含以下字段：
1. overview: 整体概况分析（200字以内，包含总投递数、平均匹配度等）
2. candidates_summary: 候选人概况分析（300字以内，分析学历分布、工作经验分布、技能特点等）
3. suitable_candidates: 符合要求的候选人推荐（数组，每个对象包含application_id、name、match_score、reason，推荐匹配度前3-5名）
4. hiring_suggestions: 招聘建议（数组，3-5条具体建议，包含面试重点、考察方向、薪资谈判建议等）
5. risk_warnings: 风险提示（数组，2-3条可能存在的风险或需要注意的问题）

请严格返回JSON格式，不要任何其他解释文字。
"""

            messages = [{"role": "user", "content": prompt}]
            result = asyncio.run(volcengine_ai_service._chat_completion(messages, temperature=0.7))

            # 清理并解析JSON
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.endswith("```"):
                result = result[:-3]

            comprehensive_analysis = json.loads(result)
        except Exception as e:
            print(f"生成综合分析失败: {str(e)}")
            comprehensive_analysis = {
                "overview": f"共收到 {len(results)} 份简历，成功分析 {success_count} 份。",
                "candidates_summary": "请查看各简历的详细匹配分析。",
                "suitable_candidates": [],
                "hiring_suggestions": ["建议优先查看匹配度较高的简历", "面试时重点考察岗位相关技能"],
                "risk_warnings": []
            }

    return {
        "message": f"分析完成，成功分析 {success_count}/{len(results)} 份简历",
        "total": len(results),
        "success": success_count,
        "results": results,
        "comprehensive_analysis": comprehensive_analysis
    }
