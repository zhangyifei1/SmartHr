import request from '@/utils/request'

// 获取系统统计数据
export function getStatistics() {
  return request({
    url: '/admin/dashboard/statistics',
    method: 'get'
  })
}

// 获取最近注册用户
export function getRecentUsers(limit = 10) {
  return request({
    url: '/admin/dashboard/recent-users',
    method: 'get',
    params: { limit }
  })
}

// 获取最近发布岗位
export function getRecentJobs(limit = 10) {
  return request({
    url: '/admin/dashboard/recent-jobs',
    method: 'get',
    params: { limit }
  })
}

// 获取最近投递记录
export function getRecentApplications(limit = 10) {
  return request({
    url: '/admin/dashboard/recent-applications',
    method: 'get',
    params: { limit }
  })
}
