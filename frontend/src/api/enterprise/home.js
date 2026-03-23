import request from '@/utils/request'

// 获取企业首页统计数据
export function getStatistics() {
  return request({
    url: '/enterprise/statistics',
    method: 'get'
  })
}
