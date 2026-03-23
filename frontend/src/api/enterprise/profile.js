import request from '@/utils/request'

// 获取企业认证状态
export function getAuthStatus() {
  return request({
    url: '/enterprise/profile/auth-status',
    method: 'get'
  })
}

// 获取企业信息
export function getProfile() {
  return request({
    url: '/enterprise/profile',
    method: 'get'
  })
}

// 更新企业信息
export function updateProfile(data) {
  return request({
    url: '/enterprise/profile',
    method: 'put',
    data
  })
}

// 提交认证申请
export function submitAuth(data) {
  return request({
    url: '/enterprise/profile/auth',
    method: 'post',
    data
  })
}
