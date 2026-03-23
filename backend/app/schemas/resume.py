from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class EducationExperienceBase(BaseModel):
    school_name: str = Field(..., description="学校名称")
    major: str = Field(..., description="专业")
    education: str = Field(..., description="学历")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    description: Optional[str] = Field(None, description="经历描述")

class EducationExperienceCreate(EducationExperienceBase):
    pass

class EducationExperience(EducationExperienceBase):
    id: int
    resume_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WorkExperienceBase(BaseModel):
    company_name: str = Field(..., description="公司名称")
    position: str = Field(..., description="职位")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    description: Optional[str] = Field(None, description="工作描述")
    achievements: Optional[str] = Field(None, description="工作业绩")

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperience(WorkExperienceBase):
    id: int
    resume_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectExperienceBase(BaseModel):
    project_name: str = Field(..., description="项目名称")
    role: str = Field(..., description="项目角色")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    description: Optional[str] = Field(None, description="项目描述")
    achievements: Optional[str] = Field(None, description="项目成果")

class ProjectExperienceCreate(ProjectExperienceBase):
    pass

class ProjectExperience(ProjectExperienceBase):
    id: int
    resume_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    title: str = Field(..., description="简历标题")
    content: Optional[str] = Field(None, description="简历完整内容JSON")
    is_default: Optional[bool] = Field(False, description="是否为默认简历")

class ResumeCreate(ResumeBase):
    education_experiences: Optional[List[EducationExperienceCreate]] = Field(None, description="教育经历")
    work_experiences: Optional[List[WorkExperienceCreate]] = Field(None, description="工作经历")
    project_experiences: Optional[List[ProjectExperienceCreate]] = Field(None, description="项目经历")

class ResumeUpdate(ResumeBase):
    education_experiences: Optional[List[EducationExperienceCreate]] = Field(None, description="教育经历")
    work_experiences: Optional[List[WorkExperienceCreate]] = Field(None, description="工作经历")
    project_experiences: Optional[List[ProjectExperienceCreate]] = Field(None, description="项目经历")

class Resume(ResumeBase):
    id: int
    user_id: int
    jobseeker_id: int
    original_file: Optional[str]
    parse_status: int
    score: Optional[int]
    evaluation: Optional[str]
    created_at: datetime
    updated_at: datetime
    education_experiences: List[EducationExperience] = []
    work_experiences: List[WorkExperience] = []
    project_experiences: List[ProjectExperience] = []

    class Config:
        from_attributes = True

class ResumeListItem(BaseModel):
    id: int
    title: str
    is_default: bool
    parse_status: int
    score: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResumeEvaluateResult(BaseModel):
    score: int
    evaluation: str
    suggestions: List[str]
