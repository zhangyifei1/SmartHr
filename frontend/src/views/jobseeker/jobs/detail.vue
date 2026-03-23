<template>
  <div class="job-detail-page">
    <el-page-header @back="goBack" content="岗位详情" />

    <div v-loading="loading" class="detail-container mt-20">
      <!-- 岗位基本信息 -->
      <el-card class="job-base-card">
        <div class="job-header">
          <div>
            <h1 class="job-title">{{ jobDetail.title }}</h1>
            <div class="job-meta mt-10">
              <span class="salary">{{ jobDetail.salary_min }}-{{ jobDetail.salary_max }}K</span>
              <span class="meta-item">{{ jobDetail.work_city }}</span>
              <span class="meta-item">{{ jobDetail.experience }}</span>
              <span class="meta-item">{{ jobDetail.education }}</span>
            </div>
          </div>
          <el-button
            type="primary"
            size="large"
            :disabled="hasApplied"
            @click="handleApply"
          >
            {{ hasApplied ? '已投递' : '立即投递' }}
          </el-button>
        </div>
        <el-divider />
        <div class="company-info">
          <div class="company-name">{{ jobDetail.enterprise_name }}</div>
          <div class="company-meta mt-5">
            <span class="meta-item">{{ jobDetail.industry }}</span>
            <span class="meta-item">{{ jobDetail.staff_size }}</span>
            <span class="meta-item">{{ jobDetail.financing_stage }}</span>
          </div>
        </div>
      </el-card>

      <!-- 岗位详情 -->
      <el-card class="job-detail-card mt-20">
        <template #header>
          <span class="card-title">岗位职责</span>
        </template>
        <div class="content-text" v-html="formatText(jobDetail.job_description)"></div>
      </el-card>

      <el-card class="job-detail-card mt-20">
        <template #header>
          <span class="card-title">任职要求</span>
        </template>
        <div class="content-text" v-html="formatText(jobDetail.job_requirement)"></div>
      </el-card>

      <el-card class="job-detail-card mt-20" v-if="jobDetail.benefits">
        <template #header>
          <span class="card-title">福利待遇</span>
        </template>
        <div class="content-text" v-html="formatText(jobDetail.benefits)"></div>
      </el-card>
    </div>

    <!-- 投递弹窗 -->
    <el-dialog v-model="applyDialogVisible" title="选择投递简历" width="500px">
      <el-form>
        <el-form-item label="选择简历">
          <el-select v-model="selectedResumeId" placeholder="请选择要投递的简历">
            <el-option
              v-for="resume in resumeList"
              :key="resume.id"
              :label="resume.title"
              :value="resume.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="applyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmApply" :loading="applying">确认投递</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getJobDetail, applyJob } from '@/api/jobseeker/job'
import { getResumeList } from '@/api/jobseeker/resume'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const applying = ref(false)
const applyDialogVisible = ref(false)
const jobDetail = ref({})
const resumeList = ref([])
const selectedResumeId = ref(null)
const hasApplied = ref(false)

// 获取岗位详情
const fetchJobDetail = async () => {
  try {
    loading.value = true
    const res = await getJobDetail(route.params.id)
    jobDetail.value = res
    // 这里可以加判断是否已经投递
    // hasApplied.value = res.has_applied
  } catch (error) {
    console.error('获取岗位详情失败:', error)
    ElMessage.error('获取岗位详情失败')
  } finally {
    loading.value = false
  }
}

// 获取简历列表
const fetchResumeList = async () => {
  try {
    const res = await getResumeList()
    resumeList.value = res
    if (res.length > 0) {
      selectedResumeId.value = res[0].id
    }
  } catch (error) {
    console.error('获取简历列表失败:', error)
  }
}

// 处理投递
const handleApply = async () => {
  await fetchResumeList()
  if (resumeList.value.length === 0) {
    ElMessageBox.confirm(
      '您还没有创建简历，是否先去创建简历？',
      '提示',
      {
        confirmButtonText: '去创建',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push('/jobseeker/resume')
    })
    return
  }
  applyDialogVisible.value = true
}

// 确认投递
const confirmApply = async () => {
  if (!selectedResumeId.value) {
    ElMessage.warning('请选择要投递的简历')
    return
  }
  try {
    applying.value = true
    await applyJob(route.params.id, selectedResumeId.value)
    ElMessage.success('投递成功')
    applyDialogVisible.value = false
    hasApplied.value = true
  } catch (error) {
    console.error('投递失败:', error)
    ElMessage.error('投递失败，请稍后重试')
  } finally {
    applying.value = false
  }
}

// 格式化文本，将换行转换为br
const formatText = (text) => {
  if (!text) return ''
  return text.replace(/\n/g, '<br>')
}

// 返回上一页
const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchJobDetail()
})
</script>

<style scoped>
.job-detail-page {
  padding-bottom: 40px;
}

.detail-container {
  max-width: 900px;
  margin: 0 auto;
}

.job-base-card .job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.job-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  color: #303133;
}

.job-meta .salary {
  color: #f56c6c;
  font-size: 24px;
  font-weight: bold;
  margin-right: 20px;
}

.job-meta .meta-item {
  color: #606266;
  margin-right: 20px;
  padding: 2px 8px;
  background: #f5f7fa;
  border-radius: 4px;
}

.company-info .company-name {
  font-size: 20px;
  font-weight: 500;
  color: #303133;
}

.company-meta .meta-item {
  color: #909399;
  margin-right: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 500;
}

.content-text {
  line-height: 2;
  color: #606266;
  white-space: pre-wrap;
}
</style>
