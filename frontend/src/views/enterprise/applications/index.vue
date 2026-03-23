<template>
  <div class="application-management-page">
    <el-page-header content="投递管理" @back="$router.go(-1)" />

    <!-- 筛选栏 -->
    <div class="filter-bar mt-20">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索岗位名称、求职者姓名"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.status" placeholder="投递状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="已投递" :value="1" />
            <el-option label="已查看" :value="2" />
            <el-option label="面试中" :value="3" />
            <el-option label="已录用" :value="4" />
            <el-option label="不合适" :value="5" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.score_range" placeholder="AI分数筛选" clearable>
            <el-option label="全部" value="" />
            <el-option label="80分以上" value="80+" />
            <el-option label="60-80分" value="60-80" />
            <el-option label="60分以下" value="0-60" />
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 投递列表 -->
    <div class="application-list mt-20">
      <el-table :data="applicationList" v-loading="loading" border>
        <el-table-column prop="job_title" label="岗位名称" width="200" />
        <el-table-column prop="resume_title" label="简历名称" width="200" />
        <el-table-column prop="jobseeker_name" label="求职者姓名" width="120" />
        <el-table-column prop="phone" label="联系方式" width="130" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="match_score" label="AI匹配分数" width="130">
          <template #default="{ row }">
            <div class="score-container">
              <el-progress
                type="circle"
                :percentage="row.match_score || 0"
                :width="50"
                :stroke-width="8"
                :color="getScoreColor(row.match_score)"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="AI测评报告" width="150">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              size="small"
              @click="viewMatchReport(row)"
              :disabled="!row.match_analysis"
            >
              查看报告
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="投递状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="投递时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="success"
              size="small"
              :loading="row.matchingLoading"
              @click="handleAIMatch(row)"
              :disabled="row.match_score !== null"
              style="margin-right: 5px;"
            >
              {{ row.match_score !== null ? '已测评' : 'AI测评' }}
            </el-button>
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

    <!-- AI测评报告弹窗 -->
    <el-dialog v-model="reportDialogVisible" title="AI匹配度分析报告" width="700px">
      <div v-if="currentReport" class="report-content">
        <div class="report-header">
          <div class="report-score">
            <span class="score-label">匹配度</span>
            <el-progress
              type="circle"
              :percentage="currentReport.match_score || 0"
              :width="80"
              :color="getScoreColor(currentReport.match_score)"
            />
          </div>
          <div class="report-info">
            <p><strong>岗位：</strong>{{ currentReport.job_title }}</p>
            <p><strong>求职者：</strong>{{ currentReport.jobseeker_name }}</p>
            <p><strong>简历：</strong>{{ currentReport.resume_title }}</p>
          </div>
        </div>
        <el-divider />
        <div class="report-body">
          <h4>匹配分析</h4>
          <p class="analysis-text">{{ currentReport.match_analysis }}</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="reportDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getAllApplications,
  processApplication,
  triggerAIMatch
} from '@/api/enterprise/application'

const route = useRoute()

const loading = ref(false)
const applicationList = ref([])
const total = ref(0)
const pageSize = ref(10)
const reportDialogVisible = ref(false)
const currentReport = ref(null)

const searchParams = ref({
  keyword: '',
  status: '',
  score_range: '',
  page: 1,
  page_size: 10
})

// 获取投递列表
const fetchApplicationList = async () => {
  try {
    loading.value = true
    // 过滤空值参数，避免后端类型校验错误
    const params = Object.fromEntries(
      Object.entries(searchParams.value).filter(([_, value]) => value !== '' && value != null)
    )
    const res = await getAllApplications(params)
    applicationList.value = res.list || res || []
    total.value = res.total || applicationList.value.length
  } catch (error) {
    console.error('获取投递列表失败:', error)
    ElMessage.error('获取投递列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.value.page = 1
  fetchApplicationList()
}

// 重置
const handleReset = () => {
  searchParams.value = {
    keyword: '',
    status: '',
    score_range: '',
    page: 1,
    page_size: 10
  }
  fetchApplicationList()
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
    fetchApplicationList()
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

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

// 获取分数颜色
const getScoreColor = (score) => {
  if (!score) return '#909399'
  if (score >= 80) return '#67c23a'
  if (score >= 60) return '#e6a23c'
  return '#f56c6c'
}

// 查看匹配报告
const viewMatchReport = (row) => {
  currentReport.value = row
  reportDialogVisible.value = true
}

// 触发AI匹配测评
const handleAIMatch = async (row) => {
  try {
    // 设置当前行的加载状态
    row.matchingLoading = true
    ElMessage.info('AI测评中，请稍候，预计需要10-20秒...')

    await triggerAIMatch(row.id)
    ElMessage.success('AI测评完成')

    // 刷新列表获取最新的匹配分数
    await fetchApplicationList()
  } catch (error) {
    console.error('AI测评失败:', error)
    ElMessage.error('AI测评失败，请稍后重试')
  } finally {
    row.matchingLoading = false
  }
}

onMounted(() => {
  // 从路由参数获取筛选条件
  if (route.query.status) {
    searchParams.value.status = parseInt(route.query.status)
  }
  fetchApplicationList()
})

// 监听路由参数变化
watch(() => route.query.status, (newStatus) => {
  if (newStatus) {
    searchParams.value.status = parseInt(newStatus)
    fetchApplicationList()
  }
})
</script>

<style scoped>
.filter-bar {
  padding: 15px;
  background: #fff;
  border-radius: 4px;
}

.pagination {
  display: flex;
  justify-content: center;
}

.score-container {
  display: flex;
  justify-content: center;
  padding: 10px 0;
}

.report-content .report-header {
  display: flex;
  align-items: center;
  gap: 30px;
}

.report-score {
  text-align: center;
}

.score-label {
  display: block;
  margin-bottom: 10px;
  font-weight: 500;
  color: #606266;
}

.report-info p {
  margin: 8px 0;
  color: #606266;
}

.report-body h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.analysis-text {
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}
</style>
