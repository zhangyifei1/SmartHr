import request from '@/utils/request'

// 获取岗位列表
export function getJobList(params) {
  return request({
    url: '/enterprise/jobs',
    method: 'get',
    params
  })
}

// 获取岗位详情
export function getJobDetail(jobId) {
  return request({
    url: `/enterprise/jobs/${jobId}`,
    method: 'get'
  })
}

// 创建岗位
export function createJob(data) {
  return request({
    url: '/enterprise/jobs',
    method: 'post',
    data
  })
}

// 更新岗位
export function updateJob(jobId, data) {
  return request({
    url: `/enterprise/jobs/${jobId}`,
    method: 'put',
    data
  })
}

// 删除岗位
export function deleteJob(jobId) {
  return request({
    url: `/enterprise/jobs/${jobId}`,
    method: 'delete'
  })
}

// 上下架岗位
export function updateJobStatus(jobId, status) {
  return request({
    url: `/enterprise/jobs/${jobId}/status`,
    method: 'post',
    data: { status }
  })
}

// 获取岗位投递列表
export function getJobApplications(jobId, params) {
  return request({
    url: `/enterprise/jobs/${jobId}/applications`,
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

// 一键分析所有投递简历
export function analyzeAllApplications(jobId) {
  return request({
    url: `/enterprise/jobs/${jobId}/analyze-all`,
    method: 'post'
  })
}
