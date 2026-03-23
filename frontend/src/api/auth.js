import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    transformRequest: [function (data) {
      let ret = ''
      for (let it in data) {
        ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
      }
      return ret
    }]
  })
}

// 注册
export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

// 文件上传
export function uploadFile(file, fileType = 'common') {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('file_type', fileType)
  return request({
    url: '/common/upload/file',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
