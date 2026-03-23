<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>SmartHr</h2>
        <p>智能人力资源管理系统</p>
      </div>
      <el-form ref="loginFormRef" :model="loginForm" label-width="80px" class="login-form">
        <el-form-item label="账号" prop="username" :rules="[
          { required: true, message: '请输入用户名/手机号/邮箱', trigger: 'blur' }
        ]">
          <el-input v-model="loginForm.username" placeholder="请输入用户名/手机号/邮箱" />
        </el-form-item>
        <el-form-item label="密码" prop="password" :rules="[
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" @click="handleLogin" :loading="loading">登录</el-button>
          <el-button @click="$router.push('/register')">去注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate()
  try {
    loading.value = true
    const redirectUrl = await authStore.login(loginForm.value)
    ElMessage.success('登录成功')
    router.push(redirectUrl)
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  width: 450px;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 32px;
  color: #409eff;
  margin-bottom: 10px;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.login-form {
  width: 100%;
}

.login-btn {
  width: 100%;
  margin-bottom: 10px;
}
</style>
