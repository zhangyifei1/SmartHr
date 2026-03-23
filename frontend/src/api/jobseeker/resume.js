import request from '@/utils/request'

// 获取简历列表
export function getResumeList() {
  return request({
    url: '/jobseeker/resumes',
    method: 'get'
  })
}

// 获取简历详情
export function getResumeDetail(resumeId) {
  return request({
    url: `/jobseeker/resumes/${resumeId}`,
    method: 'get'
  })
}

// 创建简历
export function createResume(data) {
  return request({
    url: '/jobseeker/resumes',
    method: 'post',
    data
  })
}

// 更新简历
export function updateResume(resumeId, data) {
  return request({
    url: `/jobseeker/resumes/${resumeId}`,
    method: 'put',
    data
  })
}

// 删除简历
export function deleteResume(resumeId) {
  return request({
    url: `/jobseeker/resumes/${resumeId}`,
    method: 'delete'
  })
}

// 设置默认简历
export function setDefaultResume(resumeId) {
  return request({
    url: `/jobseeker/resumes/${resumeId}/set-default`,
    method: 'post'
  })
}

// 上传并解析简历
export function uploadResume(file, title) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: `/jobseeker/resumes/upload?title=${encodeURIComponent(title)}`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// AI评测简历
export function evaluateResume(resumeId) {
  return request({
    url: `/jobseeker/resumes/${resumeId}/evaluate`,
    method: 'post'
  })
}
