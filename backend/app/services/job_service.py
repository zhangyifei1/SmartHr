from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Tuple
from app.models.job import Job, JobApplication
from app.models.user import EnterpriseProfile
from app.models.resume import Resume
from app.schemas.job import JobFilterParams, JobApplicationCreate
from app.core.exceptions import ResourceNotFoundException, BusinessException
import json
from datetime import datetime

class JobService:
    @staticmethod
    def get_job_list(db: Session, filter_params: JobFilterParams) -> Tuple[List[Job], int]:
        """获取岗位列表，支持多条件筛选"""
        query = db.query(Job).filter(Job.status == 1)

        # 关键词搜索
        if filter_params.keyword:
            keyword = f"%{filter_params.keyword}%"
            query = query.filter(
                or_(
                    Job.title.like(keyword),
                    Job.job_description.like(keyword),
                    Job.job_requirement.like(keyword)
                )
            )

        # 城市筛选
        if filter_params.city:
            query = query.filter(Job.work_city == filter_params.city)

        # 薪资筛选
        if filter_params.salary_min is not None:
            query = query.filter(Job.salary_max >= filter_params.salary_min)
        if filter_params.salary_max is not None:
            query = query.filter(Job.salary_min <= filter_params.salary_max)

        # 学历筛选
        if filter_params.education:
            query = query.filter(Job.education_requirement == filter_params.education)

        # 工作年限筛选
        if filter_params.work_years is not None:
            query = query.filter(Job.work_year_requirement <= filter_params.work_years)

        # 行业筛选
        if filter_params.industry:
            query = query.join(EnterpriseProfile).filter(EnterpriseProfile.industry == filter_params.industry)

        # 计算总数
        total = query.count()

        # 分页
        offset = (filter_params.page - 1) * filter_params.page_size
        jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(filter_params.page_size).all()

        # 补充企业信息
        for job in jobs:
            enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.id == job.enterprise_id).first()
            if enterprise:
                job.company_name = enterprise.company_name
                job.company_logo = enterprise.company_logo
                job.company_size = enterprise.company_size
                job.industry = enterprise.industry
            # 解析标签
            if job.tags:
                job.tags = json.loads(job.tags)

        return jobs, total

    @staticmethod
    def get_job_detail(db: Session, job_id: int, increase_view: bool = True) -> Job:
        """获取岗位详情"""
        job = db.query(Job).filter(Job.id == job_id, Job.status == 1).first()
        if not job:
            raise ResourceNotFoundException(message="岗位不存在或已关闭")

        # 增加浏览量
        if increase_view:
            job.view_count += 1
            db.commit()
            db.refresh(job)

        # 补充企业信息
        enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.id == job.enterprise_id).first()
        if enterprise:
            job.company_name = enterprise.company_name
            job.company_logo = enterprise.company_logo
            job.company_size = enterprise.company_size
            job.industry = enterprise.industry
        # 解析标签
        if job.tags:
            job.tags = json.loads(job.tags)

        return job

    @staticmethod
    def get_recommended_jobs(db: Session, jobseeker_id: int, limit: int = 10) -> List[Job]:
        """获取推荐岗位，暂时返回最新发布的岗位"""
        # TODO: 后续实现基于用户画像和行为的个性化推荐
        jobs = db.query(Job).filter(Job.status == 1).order_by(Job.created_at.desc()).limit(limit).all()

        # 补充企业信息
        for job in jobs:
            enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.id == job.enterprise_id).first()
            if enterprise:
                job.company_name = enterprise.company_name
                job.company_logo = enterprise.company_logo
            if job.tags:
                job.tags = json.loads(job.tags)

        return jobs

    @staticmethod
    def apply_job(db: Session, job_id: int, jobseeker_id: int, resume_id: int) -> JobApplication:
        """投递简历"""
        # 检查岗位是否存在
        job = JobService.get_job_detail(db, job_id, increase_view=False)
        if not job:
            raise ResourceNotFoundException(message="岗位不存在或已关闭")

        # 检查是否已经投递过
        existing_apply = db.query(JobApplication).filter(
            JobApplication.job_id == job_id,
            JobApplication.jobseeker_id == jobseeker_id
        ).first()
        if existing_apply:
            raise BusinessException(code=400005, message="您已经投递过该岗位了")

        # 创建投递记录
        application = JobApplication(
            job_id=job_id,
            jobseeker_id=jobseeker_id,
            resume_id=resume_id,
            status=1
        )
        db.add(application)

        # 增加岗位投递量
        job.apply_count += 1

        db.commit()
        db.refresh(application)

        return application

    @staticmethod
    def get_application_list(db: Session, jobseeker_id: int, status: int = None, page: int = 1, page_size: int = 10) -> Tuple[List[JobApplication], int]:
        """获取我的投递记录"""
        query = db.query(JobApplication).filter(JobApplication.jobseeker_id == jobseeker_id)

        if status is not None:
            query = query.filter(JobApplication.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        applications = query.order_by(JobApplication.created_at.desc()).offset(offset).limit(page_size).all()

        # 补充岗位和企业信息
        result = []
        for app in applications:
            job = db.query(Job).filter(Job.id == app.job_id).first()
            if job:
                enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.id == job.enterprise_id).first()

                # 构建返回数据，字段名与前端对齐
                app_data = {
                    "id": app.id,
                    "job_id": app.job_id,
                    "jobseeker_id": app.jobseeker_id,
                    "resume_id": app.resume_id,
                    "status": app.status,
                    "created_at": app.created_at.isoformat() if app.created_at else None,
                    "updated_at": app.updated_at.isoformat() if app.updated_at else None,
                    # 岗位信息
                    "job_title": job.title,
                    "salary_min": float(job.salary_min) if job.salary_min else 0,
                    "salary_max": float(job.salary_max) if job.salary_max else 0,
                    "work_city": job.work_city,
                    # 企业信息
                    "enterprise_name": enterprise.company_name if enterprise else "",
                    "company_name": enterprise.company_name if enterprise else "",
                    "company_logo": enterprise.company_logo if enterprise else "",
                    # 投递时间
                    "apply_time": app.created_at.strftime("%Y-%m-%d %H:%M") if app.created_at else ""
                }
                result.append(app_data)

        return result, total

    @staticmethod
    def calculate_match_score(db: Session, job_id: int, resume_id: int) -> dict:
        """计算简历与岗位的匹配度"""
        import json

        job = JobService.get_job_detail(db, job_id, increase_view=False)
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume or not resume.content:
            return {
                "match_score": 0,
                "match_analysis": "简历内容为空，无法进行匹配分析，请检查简历是否已正确解析。"
            }

        try:
            # 提取岗位核心信息
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

岗位福利：
{getattr(job, 'benefits', '无') or '无'}
"""

            # 提取简历内容（JSON转格式化文本）
            try:
                import json
                resume_data = json.loads(resume.content)
                # 格式化简历内容为易读的文本
                resume_content = json.dumps(resume_data, ensure_ascii=False, indent=2)
            except:
                # 如果JSON解析失败，直接使用原始内容
                resume_content = resume.content

            # 构造大模型prompt
            prompt = f"""
你是专业的招聘AI助手，现在需要分析简历与岗位的匹配度。

【岗位详细信息】：
{job_info}

【简历详细内容】：
{resume_content}

请严格按照以下要求返回结果：
1. 综合评估简历与岗位的匹配度，给出0-100的整数分数（match_score）
2. 撰写简洁专业的匹配分析（match_analysis），500字以内，包含：
   - 总体匹配评价
   - 候选人核心优势
   - 候选人不足
   - 招聘建议

返回格式要求：
- 严格返回JSON格式，不要任何其他内容
- JSON包含两个字段：match_score（整数）、match_analysis（字符串）
- 确保JSON格式正确，没有语法错误
"""

            # 调用火山引擎大模型
            import asyncio
            from app.services.volcengine_service import volcengine_ai_service
            messages = [{"role": "user", "content": prompt}]
            # 在同步方法中运行异步调用
            result = asyncio.run(volcengine_ai_service._chat_completion(messages, temperature=0.7))

            # 解析JSON结果
            match_result = json.loads(result)

            # 验证返回格式
            if not isinstance(match_result.get("match_score"), int) or not isinstance(match_result.get("match_analysis"), str):
                raise ValueError("大模型返回格式不正确")

            # 分数范围校验
            match_result["match_score"] = max(0, min(100, match_result["match_score"]))

            return match_result

        except Exception as e:
            print(f"AI匹配失败: {str(e)}")
            # 失败时返回友好提示
            return {
                "match_score": None,
                "match_analysis": f"AI测评暂时失败，请稍后重试。错误信息：{str(e)[:100]}..."
            }

    @staticmethod
    def generate_interview_questions(db: Session, job_id: int, resume_id: int) -> List[dict]:
        """生成面试题"""
        job = JobService.get_job_detail(db, job_id, increase_view=False)
        # TODO: 调用AI服务生成面试题
        # 暂时返回模拟数据
        return [
            {
                "question": "请介绍一下你之前做过的最有挑战性的项目？",
                "examination_point": "考察项目经验和解决问题的能力",
                "reference_answer": "可以从项目背景、遇到的挑战、解决方案、最终成果几个方面介绍，突出自己的贡献。"
            },
            {
                "question": "请解释一下Python中的GIL是什么，它对多线程程序有什么影响？",
                "examination_point": "考察Python基础知识掌握程度",
                "reference_answer": "GIL是全局解释器锁，同一时间只能有一个线程执行Python字节码，所以CPU密集型任务不适合用多线程，适合用多进程。"
            },
            {
                "question": "在FastAPI中如何实现接口的权限控制？",
                "examination_point": "考察FastAPI框架使用经验",
                "reference_answer": "可以通过依赖注入的方式，在路由中添加权限校验依赖，验证用户的JWT token和角色权限。"
            }
        ]

    @staticmethod
    def generate_interview_preparation(db: Session, job_id: int) -> dict:
        """生成面试准备：10个面试问题、参考答案和知识点梳理"""
        import asyncio
        from app.services.volcengine_service import volcengine_ai_service

        job = JobService.get_job_detail(db, job_id, increase_view=False)

        job_content = {
            "title": job.title,
            "job_description": job.job_description,
            "job_requirement": job.job_requirement,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "education_requirement": job.education_requirement,
            "work_year_requirement": job.work_year_requirement
        }

        try:
            result = asyncio.run(volcengine_ai_service.generate_interview_preparation(job_content))
            return result
        except Exception as e:
            print(f"AI生成面试准备失败: {str(e)}")
            # 返回模拟数据
            return {
                "interview_questions": [
                    {
                        "question": "请简单介绍一下你自己？",
                        "reference_answer": "可以从教育背景、工作经历、技能特长和职业规划几个方面简要介绍，控制在2-3分钟。",
                        "key_points": ["自我介绍的结构", "时间控制", "重点突出"]
                    },
                    {
                        "question": "你为什么对这个岗位感兴趣？",
                        "reference_answer": "结合岗位要求和自己的职业规划，说明对公司和岗位的了解，以及自己为什么适合这个岗位。",
                        "key_points": ["对公司的了解", "岗位匹配度", "职业规划"]
                    }
                ]
            }
