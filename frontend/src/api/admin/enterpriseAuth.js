import request from '@/utils/request'

// 获取企业认证申请列表
export function getEnterpriseAuthList(params) {
  return request({
    url: '/admin/enterprise-auth',
    method: 'get',
    params
  })
}

// 审核企业认证申请
export function auditEnterpriseAuth(enterpriseId, status, reason = '') {
  return request({
    url: `/admin/enterprise-auth/${enterpriseId}/audit`,
    method: 'post',
    data: { status, reason }
  })
}
