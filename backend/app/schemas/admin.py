from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class UserListItem(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone: Optional[str]
    user_type: int
    status: int
    created_at: datetime

    class Config:
        from_attributes = True

class EnterpriseAuthListItem(BaseModel):
    id: int
    user_id: int
    company_name: str
    unified_social_credit_code: Optional[str] = None
    legal_person: Optional[str] = None
    business_license: Optional[str] = None
    auth_status: int
    auth_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class EnterpriseAuthAudit(BaseModel):
    status: int = Field(..., ge=2, le=3, description="审核结果 2-通过 3-拒绝")
    reason: Optional[str] = Field(None, description="拒绝原因")

class ContentAuditListItem(BaseModel):
    id: int
    content_type: str  # job/resume/enterprise
    title: str
    content: str
    creator_id: int
    creator_name: str
    status: int  # 0-待审核 1-已通过 2-已拒绝
    created_at: datetime

class ContentAuditRequest(BaseModel):
    status: int = Field(..., ge=1, le=2, description="审核结果 1-通过 2-拒绝")
    reason: Optional[str] = Field(None, description="拒绝原因")

class SystemConfigItem(BaseModel):
    id: int
    config_key: str
    config_value: Any
    config_type: str
    description: Optional[str]
    updated_at: datetime

    class Config:
        from_attributes = True

class SystemConfigUpdate(BaseModel):
    config_value: Any = Field(..., description="配置值")

class DashboardStats(BaseModel):
    total_users: int
    total_jobseekers: int
    total_enterprises: int
    total_jobs: int
    total_applications: int
    today_new_users: int
    today_new_jobs: int
    today_new_applications: int

class BusinessStats(BaseModel):
    user_growth: List[dict]
    job_growth: List[dict]
    application_growth: List[dict]
    retention_rate: float
    match_success_rate: float

class SystemMonitorStats(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    api_response_time: float
    api_request_count: int
    error_rate: float
