<template>
  <div class="job-management-page">
    <el-page-header content="岗位管理" @back="$router.go(-1)" />

    <!-- 操作栏 -->
    <div class="action-bar mt-20">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        发布新岗位
      </el-button>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar mt-20">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索岗位名称"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.status" placeholder="岗位状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="招聘中" :value="1" />
            <el-option label="已关闭" :value="0" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 岗位列表 -->
    <div class="job-list mt-20">
      <el-table :data="jobList" v-loading="loading" border>
        <el-table-column prop="title" label="岗位名称" width="200" />
        <el-table-column label="薪资范围" width="120">
          <template #default="{ row }">
            {{ row.salary || `${row.salary_min || 0}-${row.salary_max || 0}K` }}
          </template>
        </el-table-column>
        <el-table-column prop="work_city" label="工作城市" width="100" />
        <el-table-column prop="education_requirement" label="学历要求" width="100" />
        <el-table-column label="经验要求" width="120">
          <template #default="{ row }">
            {{ row.work_year_requirement === null ? '不限' :
               row.work_year_requirement === 0 ? '应届生' :
               row.work_year_requirement === 1 ? '1-3年' :
               row.work_year_requirement === 3 ? '3-5年' :
               row.work_year_requirement === 5 ? '5-10年' :
               row.work_year_requirement === 10 ? '10年以上' : '不限' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '招聘中' : '已关闭' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="apply_count" label="投递人数" width="100" />
        <el-table-column prop="updated_at" label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="400" fixed="right">
          <template #default="{ row }">
            <el-button type="success" size="small" @click="handleAnalyzeAll(row)" :loading="analyzingJobId === row.id">
              一键分析
            </el-button>
            <el-button size="small" @click="handleViewApplications(row)">
              投递记录({{ row.apply_count || 0 }})
            </el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" @click="handleToggleStatus(row)">
              {{ row.status === 1 ? '关闭' : '开启' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination mt-20" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="searchParams.page"
          v-model:page-size="searchParams.page_size"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSearch"
          @current-change="handleSearch"
        />
      </div>
    </div>

    <!-- 新增/编辑岗位弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑岗位' : '发布新岗位'" width="800px" :close-on-click-modal="false">
      <el-form ref="jobFormRef" :model="jobForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="岗位名称" prop="title" :rules="[
              { required: true, message: '请输入岗位名称', trigger: 'blur' }
            ]">
              <el-input v-model="jobForm.title" placeholder="请输入岗位名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="薪资范围" prop="salary" :rules="[
              { required: true, message: '请输入薪资范围', trigger: 'blur' }
            ]">
              <el-input v-model="jobForm.salary" placeholder="例如：15-25K" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="工作城市" prop="city" :rules="[
              { required: true, message: '请输入工作城市', trigger: 'blur' }
            ]">
              <el-input v-model="jobForm.city" placeholder="请输入工作城市" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="学历要求" prop="education">
              <el-select v-model="jobForm.education" placeholder="请选择学历要求">
                <el-option label="不限" value="不限" />
                <el-option label="大专" value="大专" />
                <el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" />
                <el-option label="博士" value="博士" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="经验要求" prop="experience">
              <el-select v-model="jobForm.experience" placeholder="请选择经验要求">
                <el-option label="不限" value="不限" />
                <el-option label="应届生" value="应届生" />
                <el-option label="1-3年" value="1-3年" />
                <el-option label="3-5年" value="3-5年" />
                <el-option label="5-10年" value="5-10年" />
                <el-option label="10年以上" value="10年以上" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="岗位职责" prop="responsibilities" :rules="[
          { required: true, message: '请输入岗位职责', trigger: 'blur' }
        ]">
          <el-input
            v-model="jobForm.responsibilities"
            type="textarea"
            :rows="5"
            placeholder="请输入岗位职责，每行一条"
          />
        </el-form-item>

        <el-form-item label="任职要求" prop="requirements" :rules="[
          { required: true, message: '请输入任职要求', trigger: 'blur' }
        ]">
          <el-input
            v-model="jobForm.requirements"
            type="textarea"
            :rows="5"
            placeholder="请输入任职要求，每行一条"
          />
        </el-form-item>

        <el-form-item label="岗位福利" prop="benefits">
          <el-input
            v-model="jobForm.benefits"
            type="textarea"
            :rows="3"
            placeholder="请输入岗位福利，每行一条"
          />
        </el-form-item>

        <el-form-item label="立即发布">
          <el-switch v-model="jobForm.publish_now" />
          <span class="ml-10">开启后立即发布，否则保存为草稿</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 一键分析弹窗 -->
    <el-dialog v-model="analyzeDialogVisible" title="AI简历分析" width="900px" :close-on-click-modal="false">
      <div class="analyze-content">
        <div v-if="analyzing" class="analyzing-container">
          <el-icon :size="60" color="#409eff" class="is-loading">
            <Loading />
          </el-icon>
          <p style="margin-top: 20px; font-size: 16px; color: #606266;">AI正在分析简历...</p>
          <p style="margin-top: 10px; font-size: 14px; color: #909399;">已完成 {{ analyzedCount }}/{{ totalCount }} 份</p>
          <el-progress
            :percentage="totalCount > 0 ? Math.round((analyzedCount / totalCount) * 100) : 0"
            style="width: 60%; margin-top: 20px;"
          />
        </div>
        <div v-else-if="analyzeResult" class="analyze-result">
          <el-alert
            :title="analyzeResult.message"
            type="success"
            :closable="false"
            show-icon
            style="margin-bottom: 20px;"
          />
          <el-descriptions :column="2" border style="margin-bottom: 20px;">
            <el-descriptions-item label="总份数">{{ analyzeResult.total }}</el-descriptions-item>
            <el-descriptions-item label="成功分析">{{ analyzeResult.success }}</el-descriptions-item>
            <el-descriptions-item label="失败份数">{{ analyzeResult.total - analyzeResult.success }}</el-descriptions-item>
          </el-descriptions>

          <!-- 综合分析报告 -->
          <div v-if="analyzeResult.comprehensive_analysis" class="comprehensive-analysis">
            <el-divider content-position="left">
              <span class="divider-title">📊 综合分析报告</span>
            </el-divider>

            <!-- 整体概况 -->
            <el-card class="analysis-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>整体概况</span>
                </div>
              </template>
              <p>{{ analyzeResult.comprehensive_analysis.overview }}</p>
            </el-card>

            <!-- 候选人概况 -->
            <el-card class="analysis-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>候选人概况分析</span>
                </div>
              </template>
              <p>{{ analyzeResult.comprehensive_analysis.candidates_summary }}</p>
            </el-card>

            <!-- 推荐候选人 -->
            <el-card v-if="analyzeResult.comprehensive_analysis.suitable_candidates && analyzeResult.comprehensive_analysis.suitable_candidates.length > 0" class="analysis-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>🌟 推荐候选人</span>
                </div>
              </template>
              <el-table :data="analyzeResult.comprehensive_analysis.suitable_candidates" border size="small">
                <el-table-column prop="name" label="姓名" width="120" />
                <el-table-column label="匹配度" width="100">
                  <template #default="{ row }">
                    <el-tag :type="getMatchScoreType(row.match_score)">
                      {{ row.match_score }}分
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="reason" label="推荐理由" />
              </el-table>
            </el-card>

            <!-- 招聘建议 -->
            <el-card v-if="analyzeResult.comprehensive_analysis.hiring_suggestions && analyzeResult.comprehensive_analysis.hiring_suggestions.length > 0" class="analysis-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>💡 招聘建议</span>
                </div>
              </template>
              <ol>
                <li v-for="(suggestion, index) in analyzeResult.comprehensive_analysis.hiring_suggestions" :key="index" style="margin-bottom: 8px;">
                  {{ suggestion }}
                </li>
              </ol>
            </el-card>

            <!-- 风险提示 -->
            <el-card v-if="analyzeResult.comprehensive_analysis.risk_warnings && analyzeResult.comprehensive_analysis.risk_warnings.length > 0" class="analysis-card risk-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>⚠️ 风险提示</span>
                </div>
              </template>
              <ul>
                <li v-for="(warning, index) in analyzeResult.comprehensive_analysis.risk_warnings" :key="index" style="margin-bottom: 8px;">
                  {{ warning }}
                </li>
              </ul>
            </el-card>
          </div>

          <div style="margin-top: 20px;">
            <el-button type="primary" @click="handleViewApplications(currentAnalyzeJob)">
              查看投递记录
            </el-button>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="analyzeDialogVisible = false" :disabled="analyzing">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 投递记录弹窗 -->
    <el-dialog v-model="applicationsDialogVisible" title="投递记录" width="1000px">
      <el-table :data="applicationList" v-loading="applicationsLoading" border>
        <el-table-column prop="resume_title" label="简历名称" width="150" />
        <el-table-column prop="jobseeker_name" label="求职者姓名" width="100" />
        <el-table-column label="匹配度" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.match_score !== null && row.match_score !== undefined" :type="getMatchScoreType(row.match_score)">
              {{ row.match_score }}分
            </el-tag>
            <span v-else>未分析</span>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="联系方式" width="120" />
        <el-table-column prop="email" label="邮箱" width="160" />
        <el-table-column label="投递状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="投递时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-dropdown @command="(command) => handleProcessApplication(row, command)">
              <el-button type="primary" size="small">
                处理 <i class="el-icon-arrow-down el-icon--right" />
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="2">标记为已查看</el-dropdown-item>
                  <el-dropdown-item command="3">进入面试</el-dropdown-item>
                  <el-dropdown-item command="4">已录用</el-dropdown-item>
                  <el-dropdown-item command="5">不合适</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  getJobList,
  createJob,
  updateJob,
  deleteJob,
  updateJobStatus,
  getJobApplications,
  processApplication,
  analyzeAllApplications
} from '@/api/enterprise/job'
import { Loading } from '@element-plus/icons-vue'

const loading = ref(false)
const saving = ref(false)
const applicationsLoading = ref(false)
const jobList = ref([])
const applicationList = ref([])
const total = ref(0)
const pageSize = ref(10)
const dialogVisible = ref(false)
const applicationsDialogVisible = ref(false)
const analyzeDialogVisible = ref(false)
const jobFormRef = ref()
const editingId = ref(null)
const currentJobId = ref(null)
const analyzingJobId = ref(null)
const analyzing = ref(false)
const analyzedCount = ref(0)
const totalCount = ref(0)
const analyzeResult = ref(null)
const currentAnalyzeJob = ref(null)

const searchParams = ref({
  keyword: '',
  status: '',
  page: 1,
  page_size: 10
})

const jobForm = ref({
  title: '',
  salary: '',
  city: '',
  education: '',
  experience: '',
  responsibilities: '',
  requirements: '',
  benefits: '',
  publish_now: true
})

// 获取岗位列表
const fetchJobList = async () => {
  try {
    loading.value = true
    // 过滤空值参数，避免后端类型校验错误
    const params = Object.fromEntries(
      Object.entries(searchParams.value).filter(([_, value]) => value !== '' && value != null)
    )
    const res = await getJobList(params)
    jobList.value = res.list || res || []
    total.value = res.total || jobList.value.length
  } catch (error) {
    console.error('获取岗位列表失败:', error)
    ElMessage.error('获取岗位列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.value.page = 1
  fetchJobList()
}

// 重置
const handleReset = () => {
  searchParams.value = {
    keyword: '',
    status: '',
    page: 1,
    page_size: 10
  }
  fetchJobList()
}

// 新增岗位
const handleCreate = () => {
  editingId.value = null
  jobForm.value = {
    title: '',
    salary: '',
    city: '',
    education: '',
    experience: '',
    responsibilities: '',
    requirements: '',
    benefits: '',
    publish_now: true
  }
  dialogVisible.value = true
}

// 编辑岗位
const handleEdit = (job) => {
  editingId.value = job.id
  // 拼接薪资显示
  let salary = job.salary
  if (job.salary_min && job.salary_max) {
    salary = `${job.salary_min}-${job.salary_max}K`
  }
  jobForm.value = {
    title: job.title,
    salary: salary,
    city: job.work_city,
    education: job.education_requirement,
    experience: job.work_year_requirement === null ? '不限' :
                job.work_year_requirement === 0 ? '应届生' :
                job.work_year_requirement === 1 ? '1-3年' :
                job.work_year_requirement === 3 ? '3-5年' :
                job.work_year_requirement === 5 ? '5-10年' :
                job.work_year_requirement === 10 ? '10年以上' : '不限',
    responsibilities: job.job_description,
    requirements: job.job_requirement,
    benefits: '',
    publish_now: job.status === 1
  }
  dialogVisible.value = true
}

// 解析薪资范围
const parseSalary = (salaryStr) => {
  if (!salaryStr) return { min: 0, max: 0 }
  // 处理类似 "15-25K" 格式
  const match = salaryStr.match(/(\d+)-(\d+)/)
  if (match) {
    return {
      min: parseInt(match[1]),
      max: parseInt(match[2])
    }
  }
  // 处理类似 "20K以上" 格式
  const matchAbove = salaryStr.match(/(\d+)K以上/)
  if (matchAbove) {
    return {
      min: parseInt(matchAbove[1]),
      max: parseInt(matchAbove[1]) * 2
    }
  }
  return { min: 0, max: 0 }
}

// 保存岗位
const handleSave = async () => {
  if (!jobFormRef.value) return
  await jobFormRef.value.validate()

  try {
    saving.value = true
    const salary = parseSalary(jobForm.value.salary)
    const submitData = {
      title: jobForm.value.title,
      work_city: jobForm.value.city,
      salary_min: salary.min,
      salary_max: salary.max,
      education_requirement: jobForm.value.education,
      work_year_requirement: jobForm.value.experience === '不限' ? null :
                               jobForm.value.experience === '应届生' ? 0 :
                               jobForm.value.experience === '1-3年' ? 1 :
                               jobForm.value.experience === '3-5年' ? 3 :
                               jobForm.value.experience === '5-10年' ? 5 :
                               jobForm.value.experience === '10年以上' ? 10 : null,
      job_description: jobForm.value.responsibilities,
      job_requirement: jobForm.value.requirements,
      status: jobForm.value.publish_now ? 1 : 0
    }

    if (editingId.value) {
      await updateJob(editingId.value, submitData)
      ElMessage.success('岗位更新成功')
    } else {
      await createJob(submitData)
      ElMessage.success('岗位创建成功')
    }
    dialogVisible.value = false
    fetchJobList()
  } catch (error) {
    console.error('保存岗位失败:', error)
  } finally {
    saving.value = false
  }
}

// 切换岗位状态
const handleToggleStatus = async (job) => {
  const newStatus = job.status === 1 ? 0 : 1
  const actionText = newStatus === 1 ? '开启' : '关闭'
  try {
    await ElMessageBox.confirm(
      `确定要${actionText}该岗位吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await updateJobStatus(job.id, newStatus)
    ElMessage.success(`${actionText}成功`)
    fetchJobList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
    }
  }
}

// 删除岗位
const handleDelete = async (job) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该岗位吗？删除后无法恢复',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteJob(job.id)
    ElMessage.success('删除成功')
    fetchJobList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

// 一键分析所有简历
const handleAnalyzeAll = async (job) => {
  if (!job.apply_count || job.apply_count === 0) {
    ElMessage.warning('该岗位暂无投递简历')
    return
  }

  try {
    currentAnalyzeJob.value = job
    analyzingJobId.value = job.id
    analyzing.value = true
    analyzedCount.value = 0
    totalCount.value = job.apply_count
    analyzeResult.value = null
    analyzeDialogVisible.value = true

    const res = await analyzeAllApplications(job.id)
    analyzeResult.value = res
    analyzedCount.value = res.success
    totalCount.value = res.total

    ElMessage.success(res.message)
    // 刷新岗位列表
    fetchJobList()
  } catch (error) {
    console.error('分析失败:', error)
    ElMessage.error('分析失败，请稍后重试')
  } finally {
    analyzing.value = false
    analyzingJobId.value = null
  }
}

// 查看投递记录
const handleViewApplications = async (job) => {
  currentJobId.value = job.id
  applicationsDialogVisible.value = true
  try {
    applicationsLoading.value = true
    const res = await getJobApplications(job.id)
    applicationList.value = res.list || res || []
  } catch (error) {
    console.error('获取投递记录失败:', error)
    ElMessage.error('获取投递记录失败')
  } finally {
    applicationsLoading.value = false
  }
}

// 处理投递申请
const handleProcessApplication = async (application, status) => {
  const statusText = getStatusText(status)
  try {
    await ElMessageBox.confirm(
      `确定要将该申请标记为【${statusText}】吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await processApplication(application.id, status, '')
    ElMessage.success('操作成功')
    // 刷新列表
    handleViewApplications({ id: currentJobId.value })
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
    }
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    1: 'info',
    2: 'primary',
    3: 'warning',
    4: 'success',
    5: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    1: '已投递',
    2: '已查看',
    3: '面试中',
    4: '已录用',
    5: '不合适'
  }
  return textMap[status] || '已投递'
}

// 获取匹配度分数类型
const getMatchScoreType = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchJobList()
})
</script>

<style scoped>
.action-bar {
  display: flex;
  justify-content: flex-end;
}

.filter-bar {
  padding: 15px;
  background: #fff;
  border-radius: 4px;
}

.pagination {
  display: flex;
  justify-content: center;
}

.ml-10 {
  margin-left: 10px;
}

.analyze-content {
  min-height: 200px;
  max-height: 70vh;
  overflow-y: auto;
}

.analyzing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.analyzing-container .el-icon.is-loading {
  animation: rotating 2s linear infinite;
}

.analyze-result {
  padding: 10px 0;
}

.comprehensive-analysis {
  margin-top: 20px;
}

.divider-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.analysis-card {
  margin-bottom: 15px;
}

.analysis-card :deep(.el-card__header) {
  background: #f5f7fa;
  padding: 12px 16px;
}

.analysis-card :deep(.el-card__body) {
  padding: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #409eff;
}

.risk-card :deep(.el-card__header) {
  background: #fef0f0;
}

.risk-card :deep(.card-header) {
  color: #f56c6c;
}

.analysis-card p,
.analysis-card ol,
.analysis-card ul {
  margin: 0;
  line-height: 1.6;
  color: #606266;
}

.analysis-card ol,
.analysis-card ul {
  padding-left: 20px;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
