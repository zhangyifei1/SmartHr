<template>
  <div class="jobseeker-layout">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <div class="logo">
            <h2>SmartHr 求职者端</h2>
          </div>
          <el-menu :default-active="$route.path" mode="horizontal" class="header-menu" :router="true">
            <el-menu-item index="/jobseeker/home">首页</el-menu-item>
            <el-menu-item index="/jobseeker/jobs">找工作</el-menu-item>
            <el-menu-item index="/jobseeker/resume">我的简历</el-menu-item>
            <el-menu-item index="/jobseeker/applications">申请记录</el-menu-item>
          </el-menu>
          <div class="user-info">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <el-avatar :size="32" icon="User" />
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
      <el-footer class="footer">
        <p>SmartHr © 2026 智能人力资源管理系统</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/jobseeker/profile')
  } else if (command === 'logout') {
    authStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  }
}
</script>

<style scoped>
.jobseeker-layout {
  min-height: 100vh;
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
  color: #409eff;
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
