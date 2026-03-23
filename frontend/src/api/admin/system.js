import request from '@/utils/request'

// 获取系统配置列表
export function getSystemConfig() {
  return request({
    url: '/admin/system/config',
    method: 'get'
  })
}

// 更新系统配置
export function updateSystemConfig(configKey, configValue) {
  return request({
    url: `/admin/system/config/${configKey}`,
    method: 'put',
    data: { config_value: configValue }
  })
}
