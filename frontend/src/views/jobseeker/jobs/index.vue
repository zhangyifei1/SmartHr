<template>
  <div class="jobs-page">
    <el-page-header content="找工作" @back="$router.go(-1)" />

    <!-- 搜索栏 -->
    <div class="search-bar mt-20">
      <el-input
        v-model="searchParams.keyword"
        placeholder="搜索岗位名称、公司名称"
        clearable
        style="width: 400px;"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button type="primary" @click="handleSearch" :loading="loading">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-bar mt-20">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-select v-model="searchParams.city" placeholder="工作城市" clearable>
            <el-option label="全国" value="" />
            <el-option label="北京" value="北京" />
            <el-option label="上海" value="上海" />
            <el-option label="广州" value="广州" />
            <el-option label="深圳" value="深圳" />
            <el-option label="杭州" value="杭州" />
            <el-option label="郑州" value="郑州" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.salary" placeholder="薪资范围" clearable>
            <el-option label="不限" value="" />
            <el-option label="3k以下" value="0-3" />
            <el-option label="3-5k" value="3-5" />
            <el-option label="5-10k" value="5-10" />
            <el-option label="10-15k" value="10-15" />
            <el-option label="15-20k" value="15-20" />
            <el-option label="20k以上" value="20+" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.education" placeholder="学历要求" clearable>
            <el-option label="不限" value="" />
            <el-option label="大专" value="大专" />
            <el-option label="本科" value="本科" />
            <el-option label="硕士" value="硕士" />
            <el-option label="博士" value="博士" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.experience" placeholder="工作经验" clearable>
            <el-option label="不限" value="" />
            <el-option label="应届生" value="应届生" />
            <el-option label="1-3年" value="1-3" />
            <el-option label="3-5年" value="3-5" />
            <el-option label="5-10年" value="5-10" />
            <el-option label="10年以上" value="10+" />
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" plain @click="handleReset">重置筛选</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 岗位列表 -->
    <div class="job-list mt-20">
      <el-card v-for="job in jobList" :key="job.id" class="job-card" shadow="hover">
        <div class="job-header">
          <div class="job-info">
            <h3 class="job-title clickable" @click="router.push(`/jobseeker/jobs/${job.id}`)">{{ job.title }}</h3>
            <div class="job-tags mt-10">
              <el-tag size="small" type="success" class="salary-tag">
                {{ job.salary || `${job.salary_min || 0}-${job.salary_max || 0}K` }}
              </el-tag>
              <el-tag size="small" v-if="job.work_city || job.city">{{ job.work_city || job.city }}</el-tag>
              <el-tag size="small" v-if="job.education">{{ job.education }}</el-tag>
              <el-tag size="small" v-if="job.experience">{{ job.experience }}</el-tag>
            </div>
          </div>
          <div class="company-info">
            <h4 class="company-name">{{ job.company_name }}</h4>
            <p class="company-desc mt-5">{{ job.company_scale }} · {{ job.industry }}</p>
          </div>
          <div class="job-actions">
            <el-button type="primary" size="small" @click="handleApply(job)" :loading="applyingJobId === job.id">
              立即投递
            </el-button>
          </div>
        </div>
        <div class="job-footer mt-15">
          <span class="update-time">更新时间: {{ formatDate(job.updated_at) }}</span>
        </div>
      </el-card>

      <el-empty v-if="jobList.length === 0 && !loading" description="暂无符合条件的岗位" />

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

    <!-- 投递简历弹窗 -->
    <el-dialog v-model="applyDialogVisible" title="投递简历" width="500px">
      <el-form label-width="100px">
        <el-form-item label="选择简历">
          <el-select v-model="selectedResumeId" placeholder="请选择要投递的简历">
            <el-option
              v-for="resume in resumeList"
              :key="resume.id"
              :label="resume.title + (resume.is_default ? ' (默认)' : '')"
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getJobList, applyJob } from '@/api/jobseeker/job'
import { getResumeList } from '@/api/jobseeker/resume'

const router = useRouter()

const loading = ref(false)
const applying = ref(false)
const applyingJobId = ref(null)
const jobList = ref([])
const resumeList = ref([])
const total = ref(0)
const pageSize = ref(10)
const applyDialogVisible = ref(false)
const selectedResumeId = ref(null)
const currentJob = ref(null)

const searchParams = ref({
  keyword: '',
  city: '',
  salary: '',
  education: '',
  experience: '',
  page: 1,
  page_size: 10
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

// 获取我的简历列表
const fetchResumeList = async () => {
  try {
    resumeList.value = await getResumeList()
  } catch (error) {
    console.error('获取简历列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  searchParams.value.page = 1
  fetchJobList()
}

// 重置筛选
const handleReset = () => {
  searchParams.value = {
    keyword: '',
    city: '',
    salary: '',
    education: '',
    experience: '',
    page: 1,
    page_size: 10
  }
  fetchJobList()
}

// 投递岗位
const handleApply = async (job) => {
  currentJob.value = job
  await fetchResumeList()

  if (resumeList.value.length === 0) {
    ElMessageBox.confirm(
      '您还没有创建简历，请先创建简历后再投递',
      '提示',
      {
        confirmButtonText: '去创建简历',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push('/jobseeker/resume')
    }).catch(() => {})
    return
  }

  // 默认选择第一个简历
  selectedResumeId.value = resumeList.value[0].id
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
    applyingJobId.value = currentJob.value.id
    await applyJob(currentJob.value.id, selectedResumeId.value)
    ElMessage.success('投递成功')
    applyDialogVisible.value = false
  } catch (error) {
    console.error('投递失败:', error)
  } finally {
    applying.value = false
    applyingJobId.value = null
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

onMounted(() => {
  fetchJobList()
})
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: center;
}

.filter-bar {
  padding: 15px;
  background: #fff;
  border-radius: 4px;
}

.job-card {
  margin-bottom: 15px;
  transition: all 0.3s;
}

.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.job-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.job-info {
  flex: 1;
}

.job-title {
  margin: 0;
  font-size: 18px;
  color: #303133;
  transition: color 0.3s;
}

.job-title.clickable {
  cursor: pointer;
  color: #409eff;
}

.job-title.clickable:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.salary-tag {
  font-weight: bold;
}

.company-info {
  flex: 1;
  padding: 0 20px;
}

.company-name {
  margin: 0;
  font-size: 16px;
  color: #606266;
}

.company-desc {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.job-actions {
  flex-shrink: 0;
}

.job-footer {
  border-top: 1px solid #f0f0f0;
  padding-top: 10px;
  font-size: 12px;
  color: #909399;
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>
