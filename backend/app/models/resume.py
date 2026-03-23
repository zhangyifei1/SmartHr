from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Resume(Base):
    """简历表"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    jobseeker_id = Column(Integer, ForeignKey("jobseeker_profiles.id"), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False, comment="简历完整内容JSON")
    original_file = Column(String(255), comment="原文件路径")
    parse_status = Column(Integer, default=0, comment="0-未解析 1-解析中 2-解析成功 3-解析失败")
    score = Column(Integer, comment="AI评分(0-100)")
    evaluation = Column(Text, comment="AI评测建议")
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    jobseeker = relationship("JobseekerProfile", back_populates="resumes")
    education_experiences = relationship("ResumeEducationExperience", back_populates="resume", cascade="all, delete-orphan")
    work_experiences = relationship("ResumeWorkExperience", back_populates="resume", cascade="all, delete-orphan")
    project_experiences = relationship("ResumeProjectExperience", back_populates="resume", cascade="all, delete-orphan")

class ResumeEducationExperience(Base):
    """教育经历表"""
    __tablename__ = "resume_education_experiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    school_name = Column(String(100), nullable=False)
    major = Column(String(100), nullable=False)
    education = Column(String(50), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联关系
    resume = relationship("Resume", back_populates="education_experiences")

class ResumeWorkExperience(Base):
    """工作经历表"""
    __tablename__ = "resume_work_experiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    achievements = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联关系
    resume = relationship("Resume", back_populates="work_experiences")

class ResumeProjectExperience(Base):
    """项目经历表"""
    __tablename__ = "resume_project_experiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    project_name = Column(String(100), nullable=False)
    role = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    achievements = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联关系
    resume = relationship("Resume", back_populates="project_experiences")
