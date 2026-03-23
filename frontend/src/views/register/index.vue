<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>用户注册</h2>
        <p>SmartHr 智能人力资源管理系统</p>
      </div>
      <el-form ref="registerFormRef" :model="registerForm" label-width="100px" class="register-form">
        <el-form-item label="用户名" prop="username" :rules="[
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
        ]">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" :rules="[
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
        ]">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword" :rules="[
          { required: true, message: '请确认密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请确认密码" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="registerForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="用户类型" prop="userType" :rules="[
          { required: true, message: '请选择用户类型', trigger: 'change' }
        ]">
          <el-radio-group v-model="registerForm.userType">
            <el-radio :label="1">求职者</el-radio>
            <el-radio :label="2">企业</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="registerForm.userType === 2" label="企业名称" prop="companyName" :rules="[
          { required: true, message: '请输入企业名称', trigger: 'blur' }
        ]">
          <el-input v-model="registerForm.companyName" placeholder="请输入企业名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="register-btn" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="$router.push('/login')">去登录</el-button>
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
const registerFormRef = ref()
const loading = ref(false)

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  phone: '',
  email: '',
  userType: 1,
  companyName: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate()
  try {
    loading.value = true
    const params = {
      username: registerForm.value.username,
      password: registerForm.value.password,
      phone: registerForm.value.phone || undefined,
      email: registerForm.value.email || undefined,
      user_type: registerForm.value.userType,
      company_name: registerForm.value.userType === 2 ? registerForm.value.companyName : undefined
    }
    await authStore.register(params)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-card {
  width: 550px;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  font-size: 28px;
  color: #409eff;
  margin-bottom: 10px;
}

.register-header p {
  color: #909399;
  font-size: 14px;
}

.register-form {
  width: 100%;
}

.register-btn {
  width: 100%;
  margin-bottom: 10px;
}
</style>
