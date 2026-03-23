<template>
  <div class="admin-dashboard">
    <el-page-header content="数据看板" />
    <div class="stat-cards mt-20">
      <el-row :gutter="20">
        <el-col :span="4.8">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon blue">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">总用户数</div>
                <div class="stat-value">{{ statistics.total_users }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4.8">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon cyan">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">求职者数</div>
                <div class="stat-value">{{ statistics.jobseeker_count }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4.8">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon green">
                <el-icon><OfficeBuilding /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">企业数</div>
                <div class="stat-value">{{ statistics.enterprise_count }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4.8">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon orange">
                <el-icon><Position /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">岗位数</div>
                <div class="stat-value">{{ statistics.total_jobs }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4.8">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon purple">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">投递数</div>
                <div class="stat-value">{{ statistics.total_applications }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 最近数据Tabs -->
    <div class="mt-20">
      <el-card>
        <template #header>
          <span>最近动态</span>
        </template>
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="最近注册用户" name="users">
            <el-table :data="recentUsers" v-loading="loading" border stripe>
              <el-table-column prop="username" label="用户名" min-width="150" />
              <el-table-column label="用户类型" min-width="100">
                <template #default="{ row }">
                  <el-tag :type="getUserTypeTag(row.user_type)">
                    {{ getUserTypeText(row.user_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="phone" label="手机号" min-width="130" />
              <el-table-column prop="email" label="邮箱" min-width="180" />
              <el-table-column prop="created_at" label="注册时间" min-width="180" />
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="最新发布岗位" name="jobs">
            <el-table :data="recentJobs" v-loading="loading" border stripe>
              <el-table-column prop="title" label="岗位名称" min-width="200" />
              <el-table-column prop="enterprise_name" label="企业名称" min-width="200" />
              <el-table-column label="薪资" min-width="120">
                <template #default="{ row }">
                  <span class="salary-text">{{ row.salary_min }}-{{ row.salary_max }}K</span>
                </template>
              </el-table-column>
              <el-table-column prop="work_city" label="工作城市" min-width="100" />
              <el-table-column label="状态" min-width="100">
                <template #default="{ row }">
                  <el-tag :type="row.status === 1 ? 'success' : 'info'">
                    {{ getJobStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="发布时间" min-width="180" />
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="最新投递记录" name="applications">
            <el-table :data="recentApplications" v-loading="loading" border stripe>
              <el-table-column prop="job_title" label="岗位名称" min-width="200" />
              <el-table-column prop="jobseeker_name" label="求职者" min-width="120" />
              <el-table-column prop="resume_title" label="简历名称" min-width="200" />
              <el-table-column label="投递状态" min-width="120">
                <template #default="{ row }">
                  <el-tag :type="getApplicationStatusTag(row.status)">
                    {{ getApplicationStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="match_score" label="匹配分数" min-width="100">
                <template #default="{ row }">
                  <span v-if="row.match_score !== null">{{ row.match_score }}分</span>
                  <span v-else>未测评</span>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="投递时间" min-width="180" />
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>

    <!-- 系统信息 -->
    <div class="mt-20">
      <el-card>
        <template #header>
          <span>系统信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="系统版本">v1.0.0</el-descriptions-item>
          <el-descriptions-item label="运行环境">开发环境</el-descriptions-item>
          <el-descriptions-item label="服务器时间">{{ currentTime }}</el-descriptions-item>
          <el-descriptions-item label="API地址">http://localhost:8000</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, OfficeBuilding, Position, Document, Clock } from '@element-plus/icons-vue'
import {
  getStatistics,
  getRecentUsers,
  getRecentJobs,
  getRecentApplications
} from '@/api/admin/dashboard'

const currentTime = ref('')
const loading = ref(false)
const activeTab = ref('users')
const statistics = ref({
  total_users: 0,
  jobseeker_count: 0,
  enterprise_count: 0,
  total_jobs: 0,
  total_applications: 0,
  pending_enterprise_auth: 0
})

const recentUsers = ref([])
const recentJobs = ref([])
const recentApplications = ref([])

const updateTime = () => {
  currentTime.value = new Date().toLocaleString()
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const res = await getStatistics()
    statistics.value = res
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取最近用户
const fetchRecentUsers = async () => {
  try {
    const res = await getRecentUsers(10)
    recentUsers.value = res
  } catch (error) {
    console.error('获取最近用户失败:', error)
  }
}

// 获取最近岗位
const fetchRecentJobs = async () => {
  try {
    const res = await getRecentJobs(10)
    recentJobs.value = res
  } catch (error) {
    console.error('获取最近岗位失败:', error)
  }
}

// 获取最近投递
const fetchRecentApplications = async () => {
  try {
    const res = await getRecentApplications(10)
    recentApplications.value = res
  } catch (error) {
    console.error('获取最近投递失败:', error)
  }
}

// 获取用户类型文本
const getUserTypeText = (type) => {
  const map = {
    1: '求职者',
    2: '企业',
    3: '管理员'
  }
  return map[type] || '未知'
}

// 获取用户类型标签颜色
const getUserTypeTag = (type) => {
  const map = {
    1: 'info',
    2: 'success',
    3: 'danger'
  }
  return map[type] || 'info'
}

// 获取岗位状态文本
const getJobStatusText = (status) => {
  const map = {
    0: '已关闭',
    1: '招聘中',
    2: '暂停'
  }
  return map[status] || '未知'
}

// 获取申请状态文本
const getApplicationStatusText = (status) => {
  const map = {
    1: '已投递',
    2: '已查看',
    3: '面试中',
    4: '已录用',
    5: '不合适'
  }
  return map[status] || '未知'
}

// 获取申请状态标签颜色
const getApplicationStatusTag = (status) => {
  const map = {
    1: 'info',
    2: 'primary',
    3: 'warning',
    4: 'success',
    5: 'danger'
  }
  return map[status] || 'info'
}

onMounted(async () => {
  updateTime()
  setInterval(updateTime, 1000)
  loading.value = true
  await Promise.all([
    fetchStatistics(),
    fetchRecentUsers(),
    fetchRecentJobs(),
    fetchRecentApplications()
  ])
  loading.value = false
})

</script>

<style scoped>
.stat-card {
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  margin-right: 20px;
}

.stat-icon.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.green {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-icon.orange {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-icon.purple {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
}

.stat-icon.cyan {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.red {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
}

.salary-text {
  color: #f56c6c;
  font-weight: 500;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}
</style>
