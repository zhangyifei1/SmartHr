from sqlalchemy.orm import Session
from typing import List, Tuple
from app.models.user import EnterpriseProfile
from app.models.job import Job, JobApplication
from app.models.resume import Resume
from app.schemas.enterprise import EnterpriseProfileUpdate, EnterpriseAuthSubmit, EnterpriseJobCreate, EnterpriseJobUpdate
from app.core.exceptions import ResourceNotFoundException, PermissionDeniedException, BusinessException
import json
from datetime import datetime

class EnterpriseService:
    @staticmethod
    def get_profile(db: Session, user_id: int) -> EnterpriseProfile:
        """获取企业信息"""
        profile = db.query(EnterpriseProfile).filter(EnterpriseProfile.user_id == user_id).first()
        if not profile:
            raise ResourceNotFoundException(message="企业信息不存在")
        # 解析福利字段
        if profile.welfare:
            profile.welfare = json.loads(profile.welfare)
        return profile

    @staticmethod
    def update_profile(db: Session, user_id: int, profile_in: EnterpriseProfileUpdate) -> EnterpriseProfile:
        """更新企业信息"""
        profile = EnterpriseService.get_profile(db, user_id)

        update_data = profile_in.model_dump(exclude_unset=True)
        # 处理福利字段
        if "welfare" in update_data:
            update_data["welfare"] = json.dumps(update_data["welfare"]) if update_data["welfare"] else None

        for field, value in update_data.items():
            setattr(profile, field, value)

        db.commit()
        db.refresh(profile)

        if profile.welfare:
            profile.welfare = json.loads(profile.welfare)
        return profile

    @staticmethod
    def submit_auth(db: Session, user_id: int, auth_in: EnterpriseAuthSubmit) -> EnterpriseProfile:
        """提交企业认证"""
        profile = EnterpriseService.get_profile(db, user_id)

        if profile.auth_status == 2:
            raise BusinessException(code=400006, message="企业已认证，无需重复提交")
        if profile.auth_status == 1:
            raise BusinessException(code=400007, message="认证审核中，请耐心等待")

        # 检查企业名称是否已被其他已认证企业使用
        existing_enterprise = db.query(EnterpriseProfile).filter(
            EnterpriseProfile.company_name == auth_in.company_name,
            EnterpriseProfile.user_id != user_id,
            EnterpriseProfile.auth_status == 2
        ).first()
        if existing_enterprise:
            raise BusinessException(code=400008, message="该企业名称已被注册，请使用其他名称")

        profile.company_name = auth_in.company_name
        profile.unified_social_credit_code = auth_in.unified_social_credit_code
        profile.legal_person = auth_in.legal_person
        profile.business_license = auth_in.business_license
        profile.auth_status = 1
        profile.auth_reason = None

        db.commit()
        db.refresh(profile)

        if profile.welfare:
            profile.welfare = json.loads(profile.welfare)
        return profile

    @staticmethod
    def get_job_list(db: Session, enterprise_id: int, status: int = None, page: int = 1, page_size: int = 10) -> Tuple[List[Job], int]:
        """获取企业发布的岗位列表"""
        query = db.query(Job).filter(Job.enterprise_id == enterprise_id)

        if status is not None:
            query = query.filter(Job.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(page_size).all()

        return jobs, total

    @staticmethod
    def get_job_detail(db: Session, job_id: int, enterprise_id: int) -> Job:
        """获取岗位详情"""
        job = db.query(Job).filter(Job.id == job_id, Job.enterprise_id == enterprise_id).first()
        if not job:
            raise ResourceNotFoundException(message="岗位不存在")
        if job.tags:
            job.tags = json.loads(job.tags)
        return job

    @staticmethod
    def create_job(db: Session, enterprise_id: int, job_in: EnterpriseJobCreate) -> Job:
        """发布新岗位"""
        job_data = job_in.model_dump()
        # 处理标签
        if job_data.get("tags"):
            job_data["tags"] = json.dumps(job_data["tags"])

        job = Job(
            enterprise_id=enterprise_id,
            **job_data
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        if job.tags:
            job.tags = json.loads(job.tags)
        return job

    @staticmethod
    def update_job(db: Session, job_id: int, enterprise_id: int, job_in: EnterpriseJobUpdate) -> Job:
        """更新岗位信息"""
        job = EnterpriseService.get_job_detail(db, job_id, enterprise_id)

        update_data = job_in.model_dump(exclude_unset=True)
        # 处理标签
        if "tags" in update_data:
            update_data["tags"] = json.dumps(update_data["tags"]) if update_data["tags"] else None

        for field, value in update_data.items():
            setattr(job, field, value)

        db.commit()
        db.refresh(job)

        if job.tags:
            job.tags = json.loads(job.tags)
        return job

    @staticmethod
    def update_job_status(db: Session, job_id: int, enterprise_id: int, status: int):
        """更新岗位状态"""
        job = EnterpriseService.get_job_detail(db, job_id, enterprise_id)
        job.status = status
        db.commit()

    @staticmethod
    def get_job_applications(db: Session, enterprise_id: int, job_id: int = None, status: int = None, page: int = 1, page_size: int = 10) -> Tuple[List[JobApplication], int]:
        """获取岗位投递记录"""
        query = db.query(JobApplication).join(Job).filter(Job.enterprise_id == enterprise_id)

        if job_id is not None:
            query = query.filter(JobApplication.job_id == job_id)
        if status is not None:
            query = query.filter(JobApplication.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        applications = query.order_by(JobApplication.created_at.desc()).offset(offset).limit(page_size).all()

        # 补充求职者和岗位信息
        for app in applications:
            job = db.query(Job).filter(Job.id == app.job_id).first()
            if job:
                app.job_title = job.title
            # 暂时模拟求职者信息
            app.jobseeker_name = "求职者"
            app.jobseeker_education = "本科"
            app.jobseeker_work_years = 3

        return applications, total

    @staticmethod
    def get_application_detail(db: Session, application_id: int, enterprise_id: int) -> JobApplication:
        """获取投递详情"""
        application = db.query(JobApplication).join(Job).filter(
            JobApplication.id == application_id,
            Job.enterprise_id == enterprise_id
        ).first()
        if not application:
            raise ResourceNotFoundException(message="投递记录不存在")

        job = db.query(Job).filter(Job.id == application.job_id).first()
        if job:
            application.job_title = job.title

        resume = db.query(Resume).filter(Resume.id == application.resume_id).first()
        if resume:
            application.resume_content = json.loads(resume.content) if resume.content else {}

        # 补充求职者信息
        application.jobseeker_name = "求职者"
        application.jobseeker_phone = "13800138000"
        application.jobseeker_email = "jobseeker@example.com"
        application.jobseeker_education = "本科"
        application.jobseeker_work_years = 3

        return application

    @staticmethod
    def update_application_status(db: Session, application_id: int, enterprise_id: int, status: int, feedback: str = None):
        """更新投递状态"""
        application = EnterpriseService.get_application_detail(db, application_id, enterprise_id)
        application.status = status
        if feedback:
            application.feedback = feedback
        db.commit()

    @staticmethod
    def arrange_interview(db: Session, application_id: int, enterprise_id: int, interview_time: datetime, notes: str = None):
        """安排面试"""
        application = EnterpriseService.get_application_detail(db, application_id, enterprise_id)
        application.status = 3  # 面试中
        application.interview_time = interview_time
        application.interview_notes = notes
        application.current_stage = "初试"
        db.commit()
