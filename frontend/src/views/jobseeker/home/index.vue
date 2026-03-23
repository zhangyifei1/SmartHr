<template>
  <div class="home-page">
    <el-page-header content="首页" />
    <div class="welcome-card mt-20">
      <h2>欢迎使用 SmartHr 求职者端</h2>
      <p>为您提供智能求职服务，助力找到合适的工作机会</p>
    </div>
    <div class="stat-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card clickable" @click="router.push('/jobseeker/resume')">
            <div class="stat-item">
              <div class="stat-icon blue">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">我的简历</div>
                <div class="stat-value">{{ resumeCount }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card clickable" @click="router.push('/jobseeker/jobs')">
            <div class="stat-item">
              <div class="stat-icon green">
                <el-icon><Position /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">在招岗位</div>
                <div class="stat-value">{{ jobCount }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card clickable" @click="router.push('/jobseeker/applications')">
            <div class="stat-item">
              <div class="stat-icon orange">
                <el-icon><Tickets /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">已投递</div>
                <div class="stat-value">{{ applicationCount }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card clickable" @click="router.push('/jobseeker/applications?status=3')">
            <div class="stat-item">
              <div class="stat-icon purple">
                <el-icon><ChatLineSquare /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">面试邀请</div>
                <div class="stat-value">{{ interviewCount }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div class="mt-20">
      <el-card>
        <template #header>
          <span>推荐岗位</span>
        </template>
        <el-empty description="暂无推荐岗位，去搜索看看吧" />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document, Position, Tickets, ChatLineSquare } from '@element-plus/icons-vue'
import { getResumeList } from '@/api/jobseeker/resume'
import { getStatistics } from '@/api/jobseeker/home'

const router = useRouter()

const resumeCount = ref(0)
const jobCount = ref(0)
const applicationCount = ref(0)
const interviewCount = ref(0)

const fetchStatistics = async () => {
  try {
    const res = await getStatistics()
    jobCount.value = res.job_count || 0
    applicationCount.value = res.application_count || 0
    interviewCount.value = res.interview_count || 0
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(async () => {
  try {
    // 获取简历数量
    const resumes = await getResumeList()
    resumeCount.value = resumes.length
    // 获取其他统计数据
    await fetchStatistics()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 40px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.welcome-card h2 {
  margin: 0 0 10px;
  font-size: 28px;
}

.welcome-card p {
  margin: 0;
  opacity: 0.9;
}

.stat-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.stat-card.clickable {
  cursor: pointer;
}

.stat-card.clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.orange {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.purple {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
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
