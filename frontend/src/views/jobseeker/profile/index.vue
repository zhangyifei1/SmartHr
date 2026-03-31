<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人中心</h1>
      <p class="subtitle">管理您的个人信息和账户设置</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <template v-else>
      <!-- 基本信息卡片 -->
      <el-card class="profile-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <el-icon><User /></el-icon>
              <span>基本信息</span>
            </div>
            <el-button
              v-if="!isEditing"
              type="primary"
              plain
              size="small"
              @click="startEdit"
            >
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
          </div>
        </template>

        <div v-if="isEditing" class="edit-form">
          <el-form :model="editForm" label-width="100px" :rules="rules" ref="formRef">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="姓名" prop="name">
                  <el-input
                    v-model="editForm.name"
                    placeholder="请输入姓名"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="手机号码" prop="phone">
                  <el-input
                    v-model="editForm.phone"
                    placeholder="请输入手机号码"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="editForm.email"
                type="email"
                placeholder="请输入邮箱地址"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="isSaving" @click="handleSave">
                <el-icon><Check /></el-icon>
                保存
              </el-button>
              <el-button @click="handleCancel">
                <el-icon><Close /></el-icon>
                取消
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <div v-else class="info-display">
          <el-row :gutter="40">
            <el-col :span="12" v-for="item in infoItems" :key="item.key">
              <div class="info-item">
                <div class="info-icon" :style="{ backgroundColor: item.bgColor }">
                  <el-icon :size="20" :color="item.iconColor">
                    <component :is="item.icon" />
                  </el-icon>
                </div>
                <div class="info-content">
                  <span class="info-label">{{ item.label }}</span>
                  <span class="info-value">{{ item.value || '-' }}</span>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User,
  Edit,
  Check,
  Close,
  Message,
  Phone,
  Calendar
} from '@element-plus/icons-vue'
import { getUserInfo, updateUserInfo } from '@/api/jobseeker/profile'

// 加载状态
const isLoading = ref(false)
const isSaving = ref(false)
const isEditing = ref(false)
const formRef = ref(null)

// 用户信息
const userInfo = ref(null)

// 编辑表单
const editForm = reactive({
  name: '',
  phone: '',
  email: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 信息项配置
const infoItems = computed(() => [
  {
    key: 'name',
    label: '姓名',
    value: userInfo.value?.name,
    icon: 'User',
    bgColor: '#ecf5ff',
    iconColor: '#409eff'
  },
  {
    key: 'email',
    label: '邮箱',
    value: userInfo.value?.email,
    icon: 'Message',
    bgColor: '#f0f9ff',
    iconColor: '#10b981'
  },
  {
    key: 'phone',
    label: '手机号码',
    value: userInfo.value?.phone,
    icon: 'Phone',
    bgColor: '#f5f3ff',
    iconColor: '#8b5cf6'
  },
  {
    key: 'createdAt',
    label: '注册时间',
    value: userInfo.value?.createdAt
      ? new Date(userInfo.value.createdAt).toLocaleDateString('zh-CN')
      : '-',
    icon: 'Calendar',
    bgColor: '#fff7ed',
    iconColor: '#f97316'
  }
])

// 加载用户信息
const loadUserInfo = async () => {
  try {
    isLoading.value = true
    const res = await getUserInfo()
    userInfo.value = res.data || res
    // 同步编辑表单
    editForm.name = userInfo.value?.name || ''
    editForm.phone = userInfo.value?.phone || ''
    editForm.email = userInfo.value?.email || ''
  } catch (error) {
    ElMessage.error('加载用户信息失败')
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

// 开始编辑
const startEdit = () => {
  if (userInfo.value) {
    editForm.name = userInfo.value.name || ''
    editForm.phone = userInfo.value.phone || ''
    editForm.email = userInfo.value.email || ''
  }
  isEditing.value = true
}

// 保存修改
const handleSave = async () => {
  // 表单验证
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch (error) {
    return
  }

  try {
    isSaving.value = true
    await updateUserInfo({
      name: editForm.name,
      phone: editForm.phone,
      email: editForm.email
    })
    ElMessage.success('个人信息更新成功')
    isEditing.value = false
    await loadUserInfo()
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '更新失败，请重试')
    console.error(error)
  } finally {
    isSaving.value = false
  }
}

// 取消编辑
const handleCancel = () => {
  isEditing.value = false
  // 重置表单
  if (userInfo.value) {
    editForm.name = userInfo.value.name || ''
    editForm.phone = userInfo.value.phone || ''
    editForm.email = userInfo.value.email || ''
  }
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped lang="scss">
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  margin-bottom: 24px;

  h1 {
    font-size: 28px;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 8px;
  }

  .subtitle {
    color: #6b7280;
    font-size: 14px;
    margin: 0;
  }
}

.loading-container {
  padding: 40px 0;
}

.profile-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;

  .el-icon {
    font-size: 18px;
    color: #409eff;
  }
}

.edit-form {
  padding: 20px 0;
}

.info-display {
  padding: 20px 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f3f4f6;

  &:last-child {
    border-bottom: none;
  }
}

.info-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.info-label {
  font-size: 13px;
  color: #6b7280;
}

.info-value {
  font-size: 15px;
  font-weight: 500;
  color: #1f2937;
  word-break: break-all;
}

.security-list {
  padding: 10px 0;
}

.security-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
  border-bottom: 1px solid #f3f4f6;

  &:last-child {
    border-bottom: none;
  }
}

.security-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.security-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.security-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.security-title {
  font-size: 15px;
  font-weight: 500;
  color: #1f2937;
}

.security-desc {
  font-size: 13px;
  color: #6b7280;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 16px;
  }

  .profile-header h1 {
    font-size: 24px;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .security-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .security-info {
    width: 100%;
  }
}
</style>
