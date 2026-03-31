from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    """用户基础表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    user_type = Column(Integer, nullable=False, comment="1-求职者 2-企业 3-管理员")
    status = Column(Integer, default=1, comment="0-禁用 1-正常")
    avatar = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    jobseeker_profile = relationship("JobseekerProfile", back_populates="user", uselist=False)
    enterprise_profile = relationship("EnterpriseProfile", back_populates="user", uselist=False)

class JobseekerProfile(Base):
    """求职者信息表"""
    __tablename__ = "jobseeker_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    real_name = Column(String(50))
    gender = Column(Integer, comment="1-男 2-女")
    age = Column(Integer)
    work_years = Column(Integer)
    highest_education = Column(String(50))
    current_city = Column(String(50))
    expected_salary = Column(String(50))
    expected_position = Column(String(100))
    expected_city = Column(String(50))
    skills = Column(Text, comment="技能标签JSON")
    self_introduction = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    user = relationship("User", back_populates="jobseeker_profile")
    resumes = relationship("Resume", back_populates="jobseeker")

class EnterpriseProfile(Base):
    """企业信息表"""
    __tablename__ = "enterprise_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    company_name = Column(String(100), nullable=False)
    unified_social_credit_code = Column(String(50))
    legal_person = Column(String(50))
    business_license = Column(String(255))
    company_logo = Column(String(255))
    company_size = Column(String(50))
    industry = Column(String(50))
    location = Column(String(100))
    website = Column(String(255))
    company_introduction = Column(Text)
    welfare = Column(Text, comment="公司福利JSON")
    auth_status = Column(Integer, default=0, comment="0-未认证 1-审核中 2-已认证 3-认证失败")
    auth_reason = Column(String(255))
    contact_name = Column(String(50), comment="联系人姓名")
    contact_phone = Column(String(20), comment="联系电话")
    contact_email = Column(String(100), comment="联系邮箱")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    user = relationship("User", back_populates="enterprise_profile")
    jobs = relationship("Job", back_populates="enterprise")
