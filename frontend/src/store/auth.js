import { defineStore } from 'pinia'
import { login as loginApi, register as registerApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    userType: parseInt(localStorage.getItem('userType')) || 0
  }),

  actions: {
    // 登录
    async login(loginForm) {
      const res = await loginApi(loginForm)
      this.token = res.access_token
      this.userType = res.user_type

      localStorage.setItem('token', res.access_token)
      localStorage.setItem('userType', res.user_type)

      // 根据用户类型跳转到对应首页
      if (res.user_type === 1) {
        return '/jobseeker/home'
      } else if (res.user_type === 2) {
        return '/enterprise/home'
      } else if (res.user_type === 3) {
        return '/admin/dashboard'
      }
      return '/'
    },

    // 注册
    async register(registerForm) {
      await registerApi(registerForm)
    },

    // 登出
    logout() {
      this.token = ''
      this.userInfo = {}
      this.userType = 0
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('userType')
    }
  }
})
