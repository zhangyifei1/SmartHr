import request from '@/utils/request'

// 获取用户列表
export function getUserList(params) {
  return request({
    url: '/admin/users',
    method: 'get',
    params
  })
}

// 更新用户状态
export function updateUserStatus(userId, status) {
  return request({
    url: `/admin/users/${userId}/status`,
    method: 'patch',
    params: { status }
  })
}
