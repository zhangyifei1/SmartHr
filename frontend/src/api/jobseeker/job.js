import request from '@/utils/request'

// 获取岗位列表
export function getJobList(params) {
  return request({
    url: '/jobseeker/jobs',
    method: 'get',
    params
  })
}

// 获取岗位详情
export function getJobDetail(jobId) {
  return request({
    url: `/jobseeker/jobs/${jobId}`,
    method: 'get'
  })
}

// 投递岗位
export function applyJob(jobId, resumeId) {
  return request({
    url: `/jobseeker/jobs/${jobId}/apply`,
    method: 'post',
    data: { resume_id: resumeId }
  })
}

// 获取我的投递记录
export function getMyApplications(params) {
  return request({
    url: '/jobseeker/jobs/applications/my',
    method: 'get',
    params
  })
}
