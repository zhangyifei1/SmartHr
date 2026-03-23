import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/login/index.vue'
import Register from '@/views/register/index.vue'
import JobseekerLayout from '@/layouts/JobseekerLayout.vue'
import JobseekerHome from '@/views/jobseeker/home/index.vue'
import JobseekerResume from '@/views/jobseeker/resume/index.vue'
import JobseekerJobs from '@/views/jobseeker/jobs/index.vue'
import JobseekerJobDetail from '@/views/jobseeker/jobs/detail.vue'
import JobseekerApplications from '@/views/jobseeker/applications/index.vue'
import JobseekerProfile from '@/views/jobseeker/profile/index.vue'
import EnterpriseLayout from '@/layouts/EnterpriseLayout.vue'
import EnterpriseHome from '@/views/enterprise/home/index.vue'
import EnterpriseJobs from '@/views/enterprise/jobs/index.vue'
import EnterpriseApplications from '@/views/enterprise/applications/index.vue'
import EnterpriseProfile from '@/views/enterprise/profile/index.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import AdminDashboard from '@/views/admin/dashboard/index.vue'
import AdminUsers from '@/views/admin/users/index.vue'
import AdminEnterpriseAuth from '@/views/admin/enterprise-auth/index.vue'
import AdminSystem from '@/views/admin/system/index.vue'
import NotFound from '@/views/404.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册' }
  },
  // 求职者端路由
  {
    path: '/jobseeker',
    component: JobseekerLayout,
    meta: { requiresAuth: true, userType: 1 },
    children: [
      {
        path: '',
        redirect: '/jobseeker/home'
      },
      {
        path: 'home',
        name: 'JobseekerHome',
        component: JobseekerHome,
        meta: { title: '首页' }
      },
      {
        path: 'resume',
        name: 'JobseekerResume',
        component: JobseekerResume,
        meta: { title: '我的简历' }
      },
      {
        path: 'jobs',
        name: 'JobseekerJobs',
        component: JobseekerJobs,
        meta: { title: '找工作' }
      },
      {
        path: 'jobs/:id',
        name: 'JobseekerJobDetail',
        component: JobseekerJobDetail,
        meta: { title: '岗位详情' }
      },
      {
        path: 'applications',
        name: 'JobseekerApplications',
        component: JobseekerApplications,
        meta: { title: '申请记录' }
      },
      {
        path: 'profile',
        name: 'JobseekerProfile',
        component: JobseekerProfile,
        meta: { title: '个人中心' }
      }
    ]
  },
  // 企业端路由
  {
    path: '/enterprise',
    component: EnterpriseLayout,
    meta: { requiresAuth: true, userType: 2 },
    children: [
      {
        path: '',
        redirect: '/enterprise/home'
      },
      {
        path: 'home',
        name: 'EnterpriseHome',
        component: EnterpriseHome,
        meta: { title: '企业首页' }
      },
      {
        path: 'jobs',
        name: 'EnterpriseJobs',
        component: EnterpriseJobs,
        meta: { title: '岗位管理' }
      },
      {
        path: 'applications',
        name: 'EnterpriseApplications',
        component: EnterpriseApplications,
        meta: { title: '简历管理' }
      },
      {
        path: 'profile',
        name: 'EnterpriseProfile',
        component: EnterpriseProfile,
        meta: { title: '企业信息' }
      }
    ]
  },
  // 管理端路由
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, userType: 3 },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { title: '数据看板' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: { title: '用户管理' }
      },
      {
        path: 'enterprise-auth',
        name: 'AdminEnterpriseAuth',
        component: AdminEnterpriseAuth,
        meta: { title: '企业认证审核' }
      },
      {
        path: 'system',
        name: 'AdminSystem',
        component: AdminSystem,
        meta: { title: '系统设置' }
      }
    ]
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '页面不存在' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - SmartHr`
  }

  const token = localStorage.getItem('token')
  const userType = localStorage.getItem('userType')

  // 需要登录的路由
  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
      return
    }
    // 检查用户类型
    if (to.meta.userType && parseInt(userType) !== to.meta.userType) {
      next('/login')
      return
    }
  }

  next()
})

export default router
