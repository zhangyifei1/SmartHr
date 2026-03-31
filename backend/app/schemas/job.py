from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class JobBase(BaseModel):
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

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    status: Optional[int] = Field(None, description="状态 0-关闭 1-开放 2-暂停")

class Job(JobBase):
    id: int
    enterprise_id: int
    status: int
    view_count: int
    apply_count: int
    created_at: datetime
    updated_at: datetime
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None

    class Config:
        from_attributes = True

class JobListItem(BaseModel):
    id: int
    title: str
    work_city: str
    salary_min: int
    salary_max: int
    salary_type: int
    education_requirement: Optional[str]
    work_year_requirement: Optional[int]
    tags: Optional[List[str]]
    company_name: Optional[str]
    company_logo: Optional[str]
    match_score: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class JobFilterParams(BaseModel):
    keyword: Optional[str] = Field(None, description="搜索关键词")
    city: Optional[str] = Field(None, description="工作城市")
    salary_min: Optional[int] = Field(None, description="最低薪资")
    salary_max: Optional[int] = Field(None, description="最高薪资")
    education: Optional[str] = Field(None, description="学历要求")
    work_years: Optional[int] = Field(None, description="工作年限要求")
    industry: Optional[str] = Field(None, description="行业")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")

class JobApplicationCreate(BaseModel):
    resume_id: int = Field(..., description="投递使用的简历ID")

class JobApplication(BaseModel):
    id: int
    job_id: int
    resume_id: int
    match_score: Optional[int]
    match_analysis: Optional[str]
    status: int
    current_stage: Optional[str]
    interview_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    job_title: Optional[str]
    company_name: Optional[str]
    company_logo: Optional[str]

    class Config:
        from_attributes = True

class MatchResult(BaseModel):
    match_score: int
    match_analysis: str
    advantages: List[str]
    disadvantages: List[str]
    suggestions: List[str]

class InterviewQuestion(BaseModel):
    question: str
    examination_point: str
    reference_answer: str

class InterviewPreparationQuestion(BaseModel):
    question: str
    reference_answer: str
    key_points: List[str]

class InterviewPreparationResult(BaseModel):
    interview_questions: List[InterviewPreparationQuestion]
