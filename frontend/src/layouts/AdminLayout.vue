<template>
  <div class="admin-layout">
    <el-container style="height: 100vh">
      <el-aside width="200px" class="aside">
        <div class="logo">
          <h3>SmartHr 管理端</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="aside-menu"
          background-color="#304156"
          text-color="#fff"
          active-text-color="#409eff"
          :router="true"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据看板</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/enterprise-auth">
            <el-icon><OfficeBuilding /></el-icon>
            <span>企业认证</span>
          </el-menu-item>
          <el-menu-item index="/admin/system">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <el-avatar :size="32" icon="UserFilled" />
                <span class="username">管理员</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import { DataAnalysis, User, OfficeBuilding, Setting, UserFilled } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const handleCommand = (command) => {
  if (command === 'logout') {
    authStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.aside {
  background-color: #304156;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #263444;
}

.logo h3 {
  color: #fff;
  margin: 0;
  font-size: 16px;
}

.aside-menu {
  border-right: none;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.username {
  margin: 0 10px;
}

.main {
  background-color: #f5f7fa;
  overflow-y: auto;
}
</style>
