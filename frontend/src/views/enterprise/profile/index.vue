<template>
  <div class="enterprise-profile-page">
    <el-page-header content="企业信息管理" @back="$router.go(-1)" />

    <!-- 认证状态卡片 -->
    <div class="auth-status-card mt-20">
      <el-card>
        <template #header>
          <span>认证状态</span>
        </template>
        <div class="auth-status-content">
          <el-tag
            v-if="profileForm.auth_status === 0"
            type="info"
            size="large"
          >
            未提交认证
          </el-tag>
          <el-tag
            v-else-if="profileForm.auth_status === 1"
            type="warning"
            size="large"
          >
            审核中
          </el-tag>
          <el-tag
            v-else-if="profileForm.auth_status === 2"
            type="success"
            size="large"
          >
            已认证
          </el-tag>
          <el-tag
            v-else-if="profileForm.auth_status === 3"
            type="danger"
            size="large"
          >
            审核未通过
          </el-tag>

          <div class="auth-info" style="margin-top: 15px;">
            <p v-if="profileForm.auth_status === 0">
              请完善企业信息后提交认证申请，审核通过后即可使用全部功能。
            </p>
            <p v-if="profileForm.auth_status === 1">
              您的认证申请正在审核中，审核通过后即可使用全部功能。
            </p>
            <p v-else-if="profileForm.auth_status === 3" class="text-danger">
              审核未通过原因：{{ profileForm.auth_reason || '请检查您的认证信息并重新提交' }}
            </p>
          </div>

          <!-- 提交认证按钮 -->
          <el-button
            v-if="profileForm.auth_status === 0 || profileForm.auth_status === 3"
            type="primary"
            style="margin-top: 15px;"
            @click="handleSubmitAuth"
            :loading="submitting"
          >
            提交认证申请
          </el-button>
        </div>
      </el-card>
    </div>

    <div class="profile-form-container mt-20">
      <el-card>
        <template #header>
          <span>企业基本信息</span>
        </template>
        <el-form ref="profileFormRef" :model="profileForm" label-width="120px">
          <el-row :gutter="20">
            <el-col :span="24">
              <el-form-item label="企业名称" prop="name" :rules="[
                { required: true, message: '请输入企业名称', trigger: 'blur' }
              ]">
                <el-input v-model="profileForm.name" placeholder="请输入企业名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="行业" prop="industry">
                <el-input v-model="profileForm.industry" placeholder="请输入所属行业" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="企业规模" prop="scale">
                <el-select v-model="profileForm.scale" placeholder="请选择企业规模">
                  <el-option label="少于50人" value="少于50人" />
                  <el-option label="50-150人" value="50-150人" />
                  <el-option label="150-500人" value="150-500人" />
                  <el-option label="500-1000人" value="500-1000人" />
                  <el-option label="1000人以上" value="1000人以上" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="所在城市" prop="city">
                <el-input v-model="profileForm.city" placeholder="请输入所在城市" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="企业地址" prop="address">
                <el-input v-model="profileForm.address" placeholder="请输入详细地址" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="企业简介" prop="description">
                <el-input
                  v-model="profileForm.description"
                  type="textarea"
                  :rows="5"
                  placeholder="请输入企业简介"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系人" prop="contact_name">
                <el-input v-model="profileForm.contact_name" placeholder="请输入联系人姓名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系电话" prop="contact_phone">
                <el-input v-model="profileForm.contact_phone" placeholder="请输入联系电话" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系邮箱" prop="contact_email">
                <el-input v-model="profileForm.contact_email" placeholder="请输入联系邮箱" />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item>
            <el-button type="primary" @click="handleSave" :loading="saving">保存信息</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProfile, updateProfile, submitAuth } from '@/api/enterprise/profile'

const saving = ref(false)
const submitting = ref(false)
const profileFormRef = ref()

const profileForm = ref({
  name: '',
  company_name: '',
  industry: '',
  scale: '',
  city: '',
  address: '',
  description: '',
  contact_name: '',
  contact_phone: '',
  contact_email: '',
  auth_status: 0,
  auth_reason: '',
  unified_social_credit_code: '',
  legal_person: '',
  business_license: ''
})

// 获取企业信息
const fetchProfile = async () => {
  try {
    const res = await getProfile()
    profileForm.value = {
      ...profileForm.value,
      ...res,
      name: res.company_name || res.name
    }
  } catch (error) {
    console.error('获取企业信息失败:', error)
    ElMessage.error('获取企业信息失败')
  }
}

// 保存企业信息
const handleSave = async () => {
  if (!profileFormRef.value) return
  await profileFormRef.value.validate()

  try {
    saving.value = true
    const submitData = {
      ...profileForm.value,
      company_name: profileForm.value.name
    }
    await updateProfile(submitData)
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

// 提交认证申请
const handleSubmitAuth = async () => {
  if (!profileForm.value.name) {
    ElMessage.error('请先填写企业名称')
    return
  }

  try {
    submitting.value = true
    await submitAuth({
      company_name: profileForm.value.name
    })
    ElMessage.success('认证申请提交成功，请等待管理员审核')
    // 刷新页面状态
    await fetchProfile()
  } catch (error) {
    console.error('提交认证失败:', error)
    ElMessage.error('提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-form-container,
.auth-status-card,
.auth-info-card {
  max-width: 800px;
  margin: 0 auto;
}

.auth-status-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.text-danger {
  color: #f56c6c;
}
</style>
