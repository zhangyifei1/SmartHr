import request from '@/utils/request'

// 获取所有投递列表
export function getAllApplications(params) {
  return request({
    url: '/enterprise/applications',
    method: 'get',
    params
  })
}

// 处理投递申请
export function processApplication(applicationId, status, remark) {
  return request({
    url: `/enterprise/applications/${applicationId}/process`,
    method: 'post',
    data: { status, remark }
  })
}

// 触发AI匹配测评
export function triggerAIMatch(applicationId) {
  return request({
    url: `/enterprise/applications/${applicationId}/match`,
    method: 'post',
    timeout: 120000
  })
}
