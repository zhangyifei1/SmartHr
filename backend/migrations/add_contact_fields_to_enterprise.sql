-- 为企业表添加联系人字段
-- 执行日期: 2026-03-31

ALTER TABLE enterprise_profiles
ADD COLUMN contact_name VARCHAR(50) COMMENT '联系人姓名' AFTER auth_reason;

ALTER TABLE enterprise_profiles
ADD COLUMN contact_phone VARCHAR(20) COMMENT '联系电话' AFTER contact_name;

ALTER TABLE enterprise_profiles
ADD COLUMN contact_email VARCHAR(100) COMMENT '联系邮箱' AFTER contact_phone;
