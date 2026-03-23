<template>
  <div class="enterprise-layout">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <div class="logo">
            <h2>SmartHr 企业端</h2>
          </div>
          <el-menu :default-active="$route.path" mode="horizontal" class="header-menu" :router="true">
            <el-menu-item index="/enterprise/home">首页</el-menu-item>
            <el-menu-item index="/enterprise/jobs" :disabled="authStatus !== 2">岗位管理</el-menu-item>
            <el-menu-item index="/enterprise/applications" :disabled="authStatus !== 2">简历管理</el-menu-item>
          </el-menu>
          <div class="user-info">
            <!-- 认证状态提示 -->
            <el-tag
              v-if="authStatus === 1"
              type="warning"
              size="small"
              style="margin-right: 20px;"
            >
              审核中
            </el-tag>
            <el-tag
              v-else-if="authStatus === 3"
              type="danger"
              size="small"
              style="margin-right: 20px;"
            >
              审核未通过
            </el-tag>
            <el-tag
              v-else-if="authStatus === 2"
              type="success"
              size="small"
              style="margin-right: 20px;"
            >
              已认证
            </el-tag>

            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <el-avatar :size="32" icon="OfficeBuilding" />
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">企业信息</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main class="main">
        <!-- 企业信息页面总是可以访问 -->
        <router-view v-if="$route.path === '/enterprise/profile'" />

        <!-- 其他页面的认证提示 -->
        <div v-else>
          <!-- 未提交认证提示 -->
          <div v-if="authStatus === 0" class="auth-tip info">
            <el-icon size="48" style="margin-right: 20px;"><InfoFilled /></el-icon>
            <div class="tip-content">
              <h3>请先完善企业信息</h3>
              <p>您还没有提交企业认证申请，请先完善企业信息并提交审核。</p>
              <p>审核通过后即可使用全部招聘功能。</p>
              <el-button type="primary" @click="router.push('/enterprise/profile')" style="margin-top: 10px;">
                去完善企业信息
              </el-button>
            </div>
          </div>

          <!-- 审核中提示 -->
          <div v-else-if="authStatus === 1" class="auth-tip warning">
            <el-icon size="48" style="margin-right: 20px;"><Warning /></el-icon>
            <div class="tip-content">
              <h3>企业资质正在审核中</h3>
              <p>您提交的企业资质正在由系统管理员审核，审核通过后即可使用全部功能。</p>
              <p>审核通常会在1-3个工作日内完成，请耐心等待。</p>
            </div>
          </div>

          <!-- 审核未通过提示 -->
          <div v-else-if="authStatus === 3" class="auth-tip danger">
            <el-icon size="48" style="margin-right: 20px;"><CircleClose /></el-icon>
            <div class="tip-content">
              <h3>企业资质审核未通过</h3>
              <p>原因：{{ authReason || '请重新提交认证信息' }}</p>
              <p>请前往企业信息页面修改并重新提交认证申请。</p>
              <el-button type="primary" @click="router.push('/enterprise/profile')" style="margin-top: 10px;">
                去修改认证信息
              </el-button>
            </div>
          </div>

          <!-- 正常显示内容 -->
          <router-view v-else-if="authStatus === 2" />
        </div>
      </el-main>
      <el-footer class="footer">
        <p>SmartHr © 2026 智能人力资源管理系统</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Warning, CircleClose, InfoFilled } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { getAuthStatus } from '@/api/enterprise/profile'

const router = useRouter()
const authStore = useAuthStore()

const authStatus = ref(0)
const authReason = ref('')

const fetchAuthStatus = async () => {
  try {
    const res = await getAuthStatus()
    authStatus.value = res.auth_status
    authReason.value = res.auth_reason
  } catch (error) {
    console.error('获取认证状态失败:', error)
  }
}

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/enterprise/profile')
  } else if (command === 'logout') {
    authStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  }
}

onMounted(() => {
  fetchAuthStatus()
})
</script>

<style scoped>
.enterprise-layout {
  min-height: 100vh;
}

.auth-tip {
  display: flex;
  align-items: flex-start;
  padding: 40px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.auth-tip.warning {
  background: #fff7e6;
  border: 1px solid #ffd591;
  color: #d48806;
}

.auth-tip.danger {
  background: #fff1f0;
  border: 1px solid #ffccc7;
  color: #cf1322;
}

.auth-tip.info {
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.auth-tip .tip-content h3 {
  margin: 0 0 10px;
  font-size: 20px;
}

.auth-tip .tip-content p {
  margin: 5px 0;
  font-size: 14px;
  opacity: 0.9;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.logo h2 {
  color: #67c23a;
  margin: 0;
}

.header-menu {
  flex: 1;
  margin: 0 30px;
  border-bottom: none;
}

.user-info {
  cursor: pointer;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  width: 100%;
  min-height: calc(100vh - 120px);
}

.footer {
  text-align: center;
  line-height: 60px;
  color: #909399;
  font-size: 14px;
  border-top: 1px solid #e4e7ed;
}
</style>
