from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple
from datetime import datetime, timedelta
from app.models.user import User, EnterpriseProfile, JobseekerProfile
from app.models.job import Job, JobApplication
from app.models.system import SystemConfig, OperationLog
from app.core.exceptions import ResourceNotFoundException, BusinessException
import json
from typing import Any, Dict

class AdminService:
    @staticmethod
    def get_user_list(db: Session, user_type: int = None, status: int = None, page: int = 1, page_size: int = 10) -> Tuple[List[User], int]:
        """获取用户列表"""
        query = db.query(User)

        if user_type is not None:
            query = query.filter(User.user_type == user_type)
        if status is not None:
            query = query.filter(User.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        users = query.order_by(User.created_at.desc()).offset(offset).limit(page_size).all()
        return users, total

    @staticmethod
    def update_user_status(db: Session, user_id: int, status: int):
        """更新用户状态"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundException(message="用户不存在")
        if user.user_type == 3:
            raise BusinessException(code=400008, message="不能修改管理员账号状态")
        user.status = status
        db.commit()

    @staticmethod
    def get_enterprise_auth_list(db: Session, status: int = None, page: int = 1, page_size: int = 10) -> Tuple[List[EnterpriseProfile], int]:
        """获取企业认证申请列表"""
        query = db.query(EnterpriseProfile).filter(EnterpriseProfile.auth_status != 0)

        if status is not None:
            query = query.filter(EnterpriseProfile.auth_status == status)

        total = query.count()
        offset = (page - 1) * page_size
        profiles = query.order_by(EnterpriseProfile.updated_at.desc()).offset(offset).limit(page_size).all()
        return profiles, total

    @staticmethod
    def audit_enterprise_auth(db: Session, enterprise_id: int, status: int, reason: str = None):
        """审核企业认证"""
        enterprise = db.query(EnterpriseProfile).filter(EnterpriseProfile.id == enterprise_id).first()
        if not enterprise:
            raise ResourceNotFoundException(message="企业不存在")
        if enterprise.auth_status != 1:
            raise BusinessException(code=400009, message="该企业不是待审核状态")

        # 如果是审核通过，需要检查企业名称是否已被其他已认证企业使用
        if status == 2:
            existing_enterprise = db.query(EnterpriseProfile).filter(
                EnterpriseProfile.company_name == enterprise.company_name,
                EnterpriseProfile.id != enterprise_id,
                EnterpriseProfile.auth_status == 2
            ).first()
            if existing_enterprise:
                raise BusinessException(code=400010, message="该企业名称已被其他企业注册，无法通过审核")

        enterprise.auth_status = status
        enterprise.auth_reason = reason
        db.commit()

    @staticmethod
    def get_system_config_list(db: Session) -> List[SystemConfig]:
        """获取系统配置列表"""
        return db.query(SystemConfig).all()

    @staticmethod
    def update_system_config(db: Session, config_key: str, config_value: Any):
        """更新系统配置"""
        config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
        if not config:
            # 如果不存在则创建
            config = SystemConfig(
                config_key=config_key,
                config_value=json.dumps(config_value) if isinstance(config_value, (dict, list)) else str(config_value),
                config_type=type(config_value).__name__
            )
            db.add(config)
        else:
            config.config_value = json.dumps(config_value) if isinstance(config_value, (dict, list)) else str(config_value)
            config.config_type = type(config_value).__name__
        db.commit()
        db.refresh(config)
        return config

    @staticmethod
    def get_dashboard_stats(db: Session) -> dict:
        """获取数据看板统计数据"""
        # 总数统计
        total_users = db.query(User).count()
        total_jobseekers = db.query(JobseekerProfile).count()
        total_enterprises = db.query(EnterpriseProfile).count()
        total_jobs = db.query(Job).count()
        total_applications = db.query(JobApplication).count()

        # 今日新增
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_new_users = db.query(User).filter(User.created_at >= today_start).count()
        today_new_jobs = db.query(Job).filter(Job.created_at >= today_start).count()
        today_new_applications = db.query(JobApplication).filter(JobApplication.created_at >= today_start).count()

        return {
            "total_users": total_users,
            "total_jobseekers": total_jobseekers,
            "total_enterprises": total_enterprises,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "today_new_users": today_new_users,
            "today_new_jobs": today_new_jobs,
            "today_new_applications": today_new_applications
        }

    @staticmethod
    def get_business_stats(db: Session) -> dict:
        """获取业务统计数据"""
        # 最近7天的增长数据
        days = 7
        user_growth = []
        job_growth = []
        application_growth = []

        for i in range(days-1, -1, -1):
            date = datetime.now().date() - timedelta(days=i)
            date_start = datetime.combine(date, datetime.min.time())
            date_end = date_start + timedelta(days=1)

            user_count = db.query(User).filter(
                User.created_at >= date_start,
                User.created_at < date_end
            ).count()
            job_count = db.query(Job).filter(
                Job.created_at >= date_start,
                Job.created_at < date_end
            ).count()
            application_count = db.query(JobApplication).filter(
                JobApplication.created_at >= date_start,
                JobApplication.created_at < date_end
            ).count()

            user_growth.append({"date": date.strftime("%Y-%m-%d"), "count": user_count})
            job_growth.append({"date": date.strftime("%Y-%m-%d"), "count": job_count})
            application_growth.append({"date": date.strftime("%Y-%m-%d"), "count": application_count})

        # 留存率和匹配成功率暂时模拟
        retention_rate = 68.5
        match_success_rate = 23.2

        return {
            "user_growth": user_growth,
            "job_growth": job_growth,
            "application_growth": application_growth,
            "retention_rate": retention_rate,
            "match_success_rate": match_success_rate
        }

    @staticmethod
    def get_system_monitor_stats() -> dict:
        """获取系统监控数据，暂时返回模拟数据"""
        return {
            "cpu_usage": 32.5,
            "memory_usage": 45.2,
            "disk_usage": 68.7,
            "api_response_time": 235,
            "api_request_count": 12568,
            "error_rate": 0.12
        }
