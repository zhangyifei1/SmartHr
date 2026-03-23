from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.models.resume import Resume, ResumeEducationExperience, ResumeWorkExperience, ResumeProjectExperience
from app.models.user import JobseekerProfile
from app.schemas.resume import ResumeCreate, ResumeUpdate
from app.core.exceptions import ResourceNotFoundException, PermissionDeniedException
import json

class ResumeService:
    @staticmethod
    def get_resume_list(db: Session, user_id: int, jobseeker_id: int) -> List[Resume]:
        """获取用户的简历列表"""
        return db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.jobseeker_id == jobseeker_id
        ).order_by(Resume.is_default.desc(), Resume.updated_at.desc()).all()

    @staticmethod
    def get_resume_by_id(db: Session, resume_id: int, user_id: int = None) -> Resume:
        """根据ID获取简历，包含关联的经历信息"""
        from sqlalchemy.orm import joinedload
        resume = db.query(Resume)\
            .options(
                joinedload(Resume.education_experiences),
                joinedload(Resume.work_experiences),
                joinedload(Resume.project_experiences)
            )\
            .filter(Resume.id == resume_id).first()
        if not resume:
            raise ResourceNotFoundException(message="简历不存在")

        if user_id and resume.user_id != user_id:
            raise PermissionDeniedException(message="无权限访问该简历")

        return resume

    @staticmethod
    def create_resume(db: Session, user_id: int, jobseeker_id: int, resume_in: ResumeCreate) -> Resume:
        """创建新简历"""
        # 如果是默认简历，先取消其他简历的默认状态
        if resume_in.is_default:
            db.query(Resume).filter(
                Resume.user_id == user_id,
                Resume.jobseeker_id == jobseeker_id
            ).update({"is_default": False})

        # 创建简历基本信息
        db_resume = Resume(
            user_id=user_id,
            jobseeker_id=jobseeker_id,
            title=resume_in.title,
            content=resume_in.content or json.dumps({}),
            is_default=resume_in.is_default,
            parse_status=2  # 手动创建的直接标记为解析成功
        )
        db.add(db_resume)
        db.flush()

        # 添加教育经历
        if resume_in.education_experiences:
            for exp in resume_in.education_experiences:
                db_exp = ResumeEducationExperience(
                    resume_id=db_resume.id,
                    **exp.model_dump()
                )
                db.add(db_exp)

        # 添加工作经历
        if resume_in.work_experiences:
            for exp in resume_in.work_experiences:
                db_exp = ResumeWorkExperience(
                    resume_id=db_resume.id,
                    **exp.model_dump()
                )
                db.add(db_exp)

        # 添加项目经历
        if resume_in.project_experiences:
            for exp in resume_in.project_experiences:
                exp_data = exp.model_dump()
                # 处理空字段，避免数据库非空约束报错
                if not exp_data.get('role'):
                    exp_data['role'] = '未填写'
                if not exp_data.get('start_date'):
                    exp_data['start_date'] = date.today()  # 默认使用当前日期填充
                db_exp = ResumeProjectExperience(
                    resume_id=db_resume.id,
                    **exp_data
                )
                db.add(db_exp)

        db.commit()
        db.refresh(db_resume)
        return db_resume

    @staticmethod
    def update_resume(db: Session, resume_id: int, user_id: int, resume_in: ResumeUpdate) -> Resume:
        """更新简历"""
        resume = ResumeService.get_resume_by_id(db, resume_id, user_id)

        # 如果要设置为默认简历，先取消其他简历的默认状态
        if resume_in.is_default and not resume.is_default:
            db.query(Resume).filter(
                Resume.user_id == user_id,
                Resume.jobseeker_id == resume.jobseeker_id
            ).update({"is_default": False})

        # 更新基本信息
        update_data = resume_in.model_dump(exclude_unset=True, exclude={"education_experiences", "work_experiences", "project_experiences"})
        for field, value in update_data.items():
            setattr(resume, field, value)

        # 更新教育经历 - 先删后加
        if resume_in.education_experiences is not None:
            db.query(ResumeEducationExperience).filter(ResumeEducationExperience.resume_id == resume_id).delete()
            for exp in resume_in.education_experiences:
                db_exp = ResumeEducationExperience(
                    resume_id=resume_id,
                    **exp.model_dump()
                )
                db.add(db_exp)

        # 更新工作经历
        if resume_in.work_experiences is not None:
            db.query(ResumeWorkExperience).filter(ResumeWorkExperience.resume_id == resume_id).delete()
            for exp in resume_in.work_experiences:
                db_exp = ResumeWorkExperience(
                    resume_id=resume_id,
                    **exp.model_dump()
                )
                db.add(db_exp)

        # 更新项目经历
        if resume_in.project_experiences is not None:
            db.query(ResumeProjectExperience).filter(ResumeProjectExperience.resume_id == resume_id).delete()
            for exp in resume_in.project_experiences:
                db_exp = ResumeProjectExperience(
                    resume_id=resume_id,
                    **exp.model_dump()
                )
                db.add(db_exp)

        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def delete_resume(db: Session, resume_id: int, user_id: int):
        """删除简历"""
        resume = ResumeService.get_resume_by_id(db, resume_id, user_id)

        # 不能删除默认简历
        if resume.is_default:
            raise PermissionDeniedException(message="默认简历不能删除，请先设置其他简历为默认")

        db.delete(resume)
        db.commit()

    @staticmethod
    def set_default_resume(db: Session, resume_id: int, user_id: int, jobseeker_id: int):
        """设置默认简历"""
        resume = ResumeService.get_resume_by_id(db, resume_id, user_id)

        # 取消其他简历的默认状态
        db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.jobseeker_id == jobseeker_id
        ).update({"is_default": False})

        resume.is_default = True
        db.commit()
