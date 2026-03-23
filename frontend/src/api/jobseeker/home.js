import request from '@/utils/request'

// 获取求职者首页统计数据
export function getStatistics() {
  return request({
    url: '/jobseeker/statistics',
    method: 'get'
  })
}
