<template>
  <div class="resume-page">
    <el-page-header content="我的简历" @back="$router.go(-1)" />

    <div class="action-bar mt-20">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建简历
      </el-button>
      <el-button @click="handleUpload">
        <el-icon><Upload /></el-icon>
        上传简历
      </el-button>
    </div>

    <div class="resume-list mt-20">
      <el-row :gutter="20">
        <el-col :span="8" v-for="resume in resumeList" :key="resume.id">
          <el-card shadow="hover" class="resume-card" :class="{ 'default-card': resume.is_default }">
            <template #header>
              <div class="card-header">
                <span class="resume-title">{{ resume.title }}</span>
                <el-tag v-if="resume.is_default" type="success" size="small">默认</el-tag>
              </div>
            </template>
            <div class="resume-info">
              <div class="info-item">
                <span class="label">解析状态：</span>
                <el-tag :type="resume.parse_status === 2 ? 'success' : resume.parse_status === 3 ? 'danger' : 'warning'" size="small">
                  {{ parseStatusText(resume.parse_status) }}
                </el-tag>
              </div>
              <div class="info-item" v-if="resume.score">
                <span class="label">AI评分：</span>
                <el-progress :percentage="resume.score" :show-text="false" style="width: 120px; display: inline-block; vertical-align: middle;" />
                <span class="score-text" :style="{ color: getScoreColor(resume.score) }">{{ resume.score }}分</span>
              </div>
              <div class="info-item">
                <span class="label">更新时间：</span>
                <span>{{ formatDate(resume.updated_at) }}</span>
              </div>
            </div>
            <div class="card-actions">
              <el-button size="small" @click="handleEdit(resume)">编辑</el-button>
              <el-button size="small" @click="handleEvaluate(resume)" :disabled="resume.parse_status !== 2" :loading="evaluating">AI评测</el-button>
              <el-button size="small" @click="handleSetDefault(resume)" :disabled="resume.is_default">设为默认</el-button>
              <el-button size="small" type="danger" @click="handleDelete(resume)" :disabled="resume.is_default">删除</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-if="resumeList.length === 0" description="暂无简历，点击上方按钮创建或上传简历" />
    </div>

    <!-- 新建/编辑简历弹窗 -->
    <el-dialog v-model="dialogVisible" title="编辑简历" width="800px" :close-on-click-modal="false">
      <el-form ref="resumeFormRef" :model="resumeForm" label-width="100px">
        <el-form-item label="简历标题" prop="title" :rules="[
          { required: true, message: '请输入简历标题', trigger: 'blur' }
        ]">
          <el-input v-model="resumeForm.title" placeholder="请输入简历标题，如：Java开发工程师简历" />
        </el-form-item>
        <el-form-item label="设为默认">
          <el-switch v-model="resumeForm.is_default" />
        </el-form-item>

        <el-divider content-position="left">教育经历</el-divider>
        <div v-for="(edu, index) in resumeForm.education_experiences" :key="index" class="experience-item">
          <div class="experience-header">
            <h4>教育经历 {{ index + 1 }}</h4>
            <el-button type="danger" size="small" @click="removeEducation(index)">删除</el-button>
          </div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="学校名称" :prop="`education_experiences.${index}.school_name`" :rules="[
                { required: true, message: '请输入学校名称', trigger: 'blur' }
              ]">
                <el-input v-model="edu.school_name" placeholder="请输入学校名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="专业" :prop="`education_experiences.${index}.major`" :rules="[
                { required: true, message: '请输入专业', trigger: 'blur' }
              ]">
                <el-input v-model="edu.major" placeholder="请输入专业" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="学历" :prop="`education_experiences.${index}.education`" :rules="[
                { required: true, message: '请选择学历', trigger: 'change' }
              ]">
                <el-select v-model="edu.education" placeholder="请选择学历">
                  <el-option label="大专" value="大专" />
                  <el-option label="本科" value="本科" />
                  <el-option label="硕士" value="硕士" />
                  <el-option label="博士" value="博士" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="开始时间" :prop="`education_experiences.${index}.start_date`" :rules="[
                { required: true, message: '请选择开始时间', trigger: 'change' }
              ]">
                <el-date-picker v-model="edu.start_date" type="date" placeholder="选择开始时间" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="结束时间" :prop="`education_experiences.${index}.end_date`">
                <el-date-picker v-model="edu.end_date" type="date" placeholder="选择结束时间，至今可不填" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        <el-button type="primary" plain size="small" @click="addEducation">
          <el-icon><Plus /></el-icon>
          添加教育经历
        </el-button>

        <el-divider content-position="left">工作经历</el-divider>
        <div v-for="(work, index) in resumeForm.work_experiences" :key="index" class="experience-item">
          <div class="experience-header">
            <h4>工作经历 {{ index + 1 }}</h4>
            <el-button type="danger" size="small" @click="removeWork(index)">删除</el-button>
          </div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="公司名称" :prop="`work_experiences.${index}.company_name`" :rules="[
                { required: true, message: '请输入公司名称', trigger: 'blur' }
              ]">
                <el-input v-model="work.company_name" placeholder="请输入公司名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="职位" :prop="`work_experiences.${index}.position`" :rules="[
                { required: true, message: '请输入职位', trigger: 'blur' }
              ]">
                <el-input v-model="work.position" placeholder="请输入职位" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="开始时间" :prop="`work_experiences.${index}.start_date`" :rules="[
                { required: true, message: '请选择开始时间', trigger: 'change' }
              ]">
                <el-date-picker v-model="work.start_date" type="date" placeholder="选择开始时间" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="结束时间" :prop="`work_experiences.${index}.end_date`">
                <el-date-picker v-model="work.end_date" type="date" placeholder="选择结束时间，至今可不填" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="工作描述">
                <el-input v-model="work.description" type="textarea" :rows="3" placeholder="请描述你的工作职责" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="工作业绩">
                <el-input v-model="work.achievements" type="textarea" :rows="2" placeholder="请描述你的工作业绩，建议使用量化数据" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        <el-button type="primary" plain size="small" @click="addWork">
          <el-icon><Plus /></el-icon>
          添加工作经历
        </el-button>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveResume" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 上传简历弹窗 -->
    <el-dialog v-model="uploadDialogVisible" title="上传简历" width="500px">
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :show-file-list="true"
        :limit="1"
        accept=".doc,.docx,.pdf"
        :on-exceed="handleExceed"
        :before-upload="beforeUpload"
        @change="handleFileChange"
      >
        <el-button type="primary" icon="Upload">选择文件</el-button>
        <template #tip>
          <div class="el-upload__tip">
            支持doc、docx、pdf格式，文件大小不超过10MB
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUploadResume" :loading="uploading">{{ uploading ? uploadingText : '开始上传' }}</el-button>
      </template>
    </el-dialog>

    <!-- AI评测结果弹窗 -->
    <el-dialog v-model="evaluateDialogVisible" title="AI简历评测结果" width="700px">
      <div v-if="evaluateResult" class="evaluate-result">
        <div class="score-section">
          <div class="score-circle" :style="{ background: getScoreColor(evaluateResult.score, true) }">
            {{ evaluateResult.score }}分
          </div>
          <div class="score-desc">
            <h3>简历综合评分</h3>
            <p>{{ evaluateResult.evaluation }}</p>
          </div>
        </div>
        <el-divider />
        <div class="suggestion-section">
          <h4>优化建议</h4>
          <el-list>
            <el-list-item v-for="(suggestion, index) in evaluateResult.suggestions" :key="index">
              <el-icon style="color: #409eff; margin-right: 8px;"><Help /></el-icon>
              {{ suggestion }}
            </el-list-item>
          </el-list>
        </div>
      </div>
      <template #footer>
        <el-button @click="evaluateDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, Help } from '@element-plus/icons-vue'
import {
  getResumeList,
  getResumeDetail,
  createResume,
  updateResume,
  deleteResume,
  setDefaultResume,
  uploadResume,
  evaluateResume
} from '@/api/jobseeker/resume'

const resumeList = ref([])
const dialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const evaluateDialogVisible = ref(false)
const resumeFormRef = ref()
const uploadRef = ref()
const saving = ref(false)
const uploading = ref(false)
const uploadingText = ref('正在上传中')
const uploadCountdown = ref(0)
const countdownTimer = ref(null)
const editingId = ref(null)
const evaluating = ref(false)

const resumeForm = ref({
  title: '',
  is_default: false,
  education_experiences: [],
  work_experiences: [],
  project_experiences: []
})

// 上传表单已移除，标题自动从文件名解析

const evaluateResult = ref(null)
const selectedFile = ref(null)

// 获取简历列表
const fetchResumeList = async () => {
  try {
    const res = await getResumeList()
    resumeList.value = res
  } catch (error) {
    console.error('获取简历列表失败:', error)
  }
}

// 解析状态文本
const parseStatusText = (status) => {
  const statusMap = {
    0: '未解析',
    1: '解析中',
    2: '解析成功',
    3: '解析失败'
  }
  return statusMap[status] || '未知'
}

// 获取分数颜色
const getScoreColor = (score, isBg = false) => {
  if (score >= 80) return isBg ? 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' : '#67c23a'
  if (score >= 60) return isBg ? 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' : '#e6a23c'
  return isBg ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' : '#f56c6c'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

// 新建简历
const handleCreate = () => {
  editingId.value = null
  resumeForm.value = {
    title: '',
    is_default: false,
    education_experiences: [],
    work_experiences: [],
    project_experiences: []
  }
  dialogVisible.value = true
}

// 编辑简历
const handleEdit = async (resume) => {
  try {
    // 调用详情接口获取完整的简历信息，包含经历字段
    const detail = await getResumeDetail(resume.id)
    editingId.value = resume.id
    resumeForm.value = {
      title: detail.title,
      is_default: detail.is_default,
      education_experiences: [...(detail.education_experiences || [])],
      work_experiences: [...(detail.work_experiences || [])],
      project_experiences: [...(detail.project_experiences || [])]
    }
    dialogVisible.value = true
  } catch (error) {
    console.error('获取简历详情失败:', error)
  }
}

// 保存简历
const handleSaveResume = async () => {
  if (!resumeFormRef.value) return
  await resumeFormRef.value.validate()

  try {
    saving.value = true
    if (editingId.value) {
      await updateResume(editingId.value, resumeForm.value)
      ElMessage.success('简历更新成功')
    } else {
      await createResume(resumeForm.value)
      ElMessage.success('简历创建成功')
    }
    dialogVisible.value = false
    fetchResumeList()
  } catch (error) {
    console.error('保存简历失败:', error)
  } finally {
    saving.value = false
  }
}

// 删除简历
const handleDelete = async (resume) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这份简历吗？删除后无法恢复',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteResume(resume.id)
    ElMessage.success('删除成功')
    fetchResumeList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

// 设置默认简历
const handleSetDefault = async (resume) => {
  try {
    await setDefaultResume(resume.id)
    ElMessage.success('设置成功')
    fetchResumeList()
  } catch (error) {
    console.error('设置默认简历失败:', error)
  }
}

// 文件选择变化
const handleFileChange = (uploadFile, uploadFiles) => {
  selectedFile.value = uploadFile.raw
  if (uploadFiles.length > 0) {
    // 简单判断：PDF按每页30秒估算，docx按10秒估算
    const ext = uploadFile.name.split('.').pop().toLowerCase()
    if (ext === 'pdf') {
      // 暂时按平均3页估算，后续可以根据实际页数调整
      uploadingText.value = '正在大模型多模态解析简历，请稍后，预计需要60秒'
    } else {
      uploadingText.value = '正在大模型解析简历，请稍后，预计需要10秒'
    }
  }
}

// 上传简历
const handleUpload = () => {
  selectedFile.value = null
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  // 重置倒计时
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
    countdownTimer.value = null
  }
  uploadCountdown.value = 0
  uploadingText.value = '正在上传中'
  uploadDialogVisible.value = true
}

// 组件卸载时清理定时器
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
  }
})

// 文件超出数量限制
const handleExceed = (files) => {
  ElMessage.warning('只能上传一个文件')
}

// 上传前校验
const beforeUpload = (file) => {
  const fileType = file.name.split('.').pop().toLowerCase()
  if (!['doc', 'docx', 'pdf'].includes(fileType)) {
    ElMessage.error('仅支持doc、docx、pdf格式文件')
    return false
  }
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过10MB')
    return false
  }
  return true
}

// 提交上传
const handleUploadResume = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择要上传的文件')
    return
  }

  try {
    uploading.value = true
    const file = selectedFile.value
    // 自动从文件名提取标题，去掉扩展名
    const title = file.name.replace(/\.[^/.]+$/, '')

    // 启动倒计时，PDF按每页20秒估算
    const ext = file.name.split('.').pop().toLowerCase()
    if (ext === 'pdf') {
      // 简单估算：每页20秒，最少60秒，最多120秒
      // 后续如果能获取实际页数可以替换为页数*20
      uploadCountdown.value = 60 // 默认3页=3*20
    } else {
      uploadCountdown.value = 15 // 其他文档15秒
    }
    // 每秒更新倒计时
    if (countdownTimer.value) clearInterval(countdownTimer.value)
    countdownTimer.value = setInterval(() => {
      uploadCountdown.value--
      if (uploadCountdown.value <= 0) {
        uploadCountdown.value = 0
        clearInterval(countdownTimer.value)
      }
      uploadingText.value = `正在大模型多模态解析简历，请稍后，预计还需要${uploadCountdown.value}秒`
    }, 1000)

    await uploadResume(file, title)
    ElMessage.success('简历上传成功，解析完成')
    uploadDialogVisible.value = false
    fetchResumeList()
  } catch (error) {
    console.error('上传失败:', error)
  } finally {
    uploading.value = false
    // 清除倒计时
    if (countdownTimer.value) {
      clearInterval(countdownTimer.value)
      countdownTimer.value = null
    }
    uploadCountdown.value = 0
    uploadingText.value = '正在上传中'
  }
}

// AI评测
const handleEvaluate = async (resume) => {
  if (evaluating.value) return
  try {
    evaluating.value = true
    ElMessage.info('正在进行AI评测，请稍候，预计需要30秒左右')
    const res = await evaluateResume(resume.id)
    evaluateResult.value = res
    evaluateDialogVisible.value = true
    // 刷新简历列表，更新评分显示
    await fetchResumeList()
    ElMessage.success('AI评测完成')
  } catch (error) {
    console.error('评测失败:', error)
    ElMessage.error('AI评测失败，请稍后重试')
  } finally {
    evaluating.value = false
  }
}

// 添加教育经历
const addEducation = () => {
  resumeForm.value.education_experiences.push({
    school_name: '',
    major: '',
    education: '',
    start_date: '',
    end_date: '',
    description: ''
  })
}

// 删除教育经历
const removeEducation = (index) => {
  resumeForm.value.education_experiences.splice(index, 1)
}

// 添加工作经历
const addWork = () => {
  resumeForm.value.work_experiences.push({
    company_name: '',
    position: '',
    start_date: '',
    end_date: '',
    description: '',
    achievements: ''
  })
}

// 删除工作经历
const removeWork = (index) => {
  resumeForm.value.work_experiences.splice(index, 1)
}

onMounted(() => {
  fetchResumeList()
})
</script>

<style scoped>
.action-bar {
  display: flex;
  gap: 10px;
}

.resume-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.resume-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.default-card {
  border: 1px solid #67c23a;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resume-title {
  font-weight: bold;
  font-size: 16px;
}

.resume-info {
  padding: 10px 0;
}

.info-item {
  margin-bottom: 8px;
  font-size: 14px;
}

.label {
  color: #909399;
  margin-right: 8px;
}

.score-text {
  margin-left: 8px;
  font-weight: bold;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.experience-item {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
}

.experience-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.experience-header h4 {
  margin: 0;
}

.score-section {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 20px 0;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 32px;
  font-weight: bold;
  flex-shrink: 0;
}

.score-desc h3 {
  margin: 0 0 12px;
  font-size: 20px;
}

.score-desc p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

.suggestion-section h4 {
  margin: 0 0 16px;
  font-size: 16px;
}
</style>
