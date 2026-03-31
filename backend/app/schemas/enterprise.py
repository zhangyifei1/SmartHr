from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date

class EnterpriseProfileBase(BaseModel):
    company_name: str = Field(..., description="公司名称")
    unified_social_credit_code: Optional[str] = Field(None, description="统一社会信用代码")
    legal_person: Optional[str] = Field(None, description="法人姓名")
    company_size: Optional[str] = Field(None, description="公司规模")
    industry: Optional[str] = Field(None, description="所属行业")
    location: Optional[str] = Field(None, description="公司地址")
    website: Optional[str] = Field(None, description="公司官网")
    company_introduction: Optional[str] = Field(None, description="公司介绍")
    welfare: Optional[List[str]] = Field(None, description="公司福利")
    contact_name: Optional[str] = Field(None, description="联系人姓名")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    contact_email: Optional[str] = Field(None, description="联系邮箱")

class EnterpriseProfileUpdate(EnterpriseProfileBase):
    pass

class EnterpriseAuthSubmit(BaseModel):
    company_name: str = Field(..., description="公司名称")
    unified_social_credit_code: Optional[str] = Field(None, description="统一社会信用代码")
    legal_person: Optional[str] = Field(None, description="法人姓名")
    business_license: Optional[str] = Field(None, description="营业执照路径")

class EnterpriseProfileOut(BaseModel):
    id: int
    user_id: int
    company_name: str
    unified_social_credit_code: Optional[str]
    legal_person: Optional[str]
    business_license: Optional[str]
    company_logo: Optional[str]
    company_size: Optional[str]
    industry: Optional[str]
    location: Optional[str]
    website: Optional[str]
    company_introduction: Optional[str]
    welfare: Optional[List[str]]
    auth_status: int
    auth_reason: Optional[str]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EnterpriseJobBase(BaseModel):
    title: str = Field(..., description="岗位名称")
    department: Optional[str] = Field(None, description="所属部门")
    work_city: str = Field(..., description="工作城市")
    salary_min: int = Field(..., ge=0, description="薪资下限")
    salary_max: int = Field(..., ge=0, description="薪资上限")
    salary_type: Optional[int] = Field(1, description="薪资类型 1-月薪 2-年薪")
    education_requirement: Optional[str] = Field(None, description="学历要求")
    work_year_requirement: Optional[int] = Field(None, description="工作年限要求")
    job_description: str = Field(..., description="岗位描述")
    job_requirement: str = Field(..., description="岗位要求")
    tags: Optional[List[str]] = Field(None, description="岗位标签")
    expire_date: Optional[date] = Field(None, description="过期时间")

class EnterpriseJobCreate(EnterpriseJobBase):
    pass

class EnterpriseJobUpdate(EnterpriseJobBase):
    status: Optional[int] = Field(None, description="状态 0-关闭 1-开放 2-暂停")

class EnterpriseJobListItem(BaseModel):
    id: int
    title: str
    work_city: str
    salary_min: int
    salary_max: int
    salary_type: int
    education_requirement: Optional[str]
    work_year_requirement: Optional[int]
    status: int
    view_count: int
    apply_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JobApplicationListItem(BaseModel):
    id: int
    job_id: int
    job_title: str
    resume_id: int
    match_score: Optional[int]
    status: int
    current_stage: Optional[str]
    jobseeker_name: Optional[str]
    jobseeker_education: Optional[str]
    jobseeker_work_years: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class JobApplicationDetail(BaseModel):
    id: int
    job_id: int
    job_title: str
    resume_id: int
    resume_content: Optional[dict]
    match_score: Optional[int]
    match_analysis: Optional[str]
    status: int
    current_stage: Optional[str]
    interview_time: Optional[datetime]
    interview_notes: Optional[str]
    feedback: Optional[str]
    jobseeker_name: Optional[str]
    jobseeker_phone: Optional[str]
    jobseeker_email: Optional[str]
    jobseeker_education: Optional[str]
    jobseeker_work_years: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
