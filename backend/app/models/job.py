from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Job(Base):
    """岗位表"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enterprise_id = Column(Integer, ForeignKey("enterprise_profiles.id"), nullable=False)
    title = Column(String(100), nullable=False)
    department = Column(String(100))
    work_city = Column(String(50), nullable=False)
    salary_min = Column(Integer, nullable=False)
    salary_max = Column(Integer, nullable=False)
    salary_type = Column(Integer, default=1, comment="1-月薪 2-年薪")
    education_requirement = Column(String(50))
    work_year_requirement = Column(Integer)
    job_description = Column(Text, nullable=False)
    job_requirement = Column(Text, nullable=False)
    tags = Column(Text, comment="岗位标签JSON")
    status = Column(Integer, default=1, comment="0-关闭 1-开放 2-暂停")
    view_count = Column(Integer, default=0)
    apply_count = Column(Integer, default=0)
    expire_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    enterprise = relationship("EnterpriseProfile", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")

class JobApplication(Base):
    """投递记录表"""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    jobseeker_id = Column(Integer, ForeignKey("jobseeker_profiles.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    match_score = Column(Integer, comment="匹配度分数")
    match_analysis = Column(Text, comment="匹配度分析结果")
    status = Column(Integer, default=1, comment="1-已投递 2-已查看 3-面试中 4-已录用 5-已拒绝")
    current_stage = Column(String(50), comment="当前面试阶段")
    interview_time = Column(DateTime(timezone=True))
    interview_notes = Column(Text)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume")
