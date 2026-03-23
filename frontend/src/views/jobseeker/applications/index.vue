<template>
  <div class="applications-page">
    <el-page-header content="我的投递" />

    <!-- 筛选区域 -->
    <div class="filter-section mt-20">
      <el-radio-group v-model="searchParams.status" @change="fetchApplicationList">
        <el-radio-button :label="null">全部</el-radio-button>
        <el-radio-button :label="1">待审核</el-radio-button>
        <el-radio-button :label="2">已通过</el-radio-button>
        <el-radio-button :label="3">面试中</el-radio-button>
        <el-radio-button :label="4">已录用</el-radio-button>
        <el-radio-button :label="5">已拒绝</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 投递列表 -->
    <div class="list-section mt-20">
      <el-card>
        <el-table
          v-loading="loading"
          :data="applicationList"
          stripe
          style="width: 100%"
        >
          <el-table-column prop="job_title" label="岗位名称" min-width="180">
            <template #default="scope">
              <span class="job-title">{{ scope.row.job_title }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="enterprise_name" label="企业名称" min-width="180" />
          <el-table-column prop="salary" label="薪资" min-width="120">
            <template #default="scope">
              <span class="salary-text">{{ scope.row.salary_min }}-{{ scope.row.salary_max }}K</span>
            </template>
          </el-table-column>
          <el-table-column prop="work_city" label="工作地点" min-width="120" />
          <el-table-column prop="apply_time" label="投递时间" min-width="180" />
          <el-table-column prop="status" label="状态" min-width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="150" fixed="right">
            <template #default="scope">
              <el-button
                type="primary"
                link
                @click="viewJobDetail(scope.row.job_id)"
              >
                查看岗位
              </el-button>
              <el-button
                type="info"
                link
                v-if="scope.row.status === 3"
              >
                查看面试
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-container mt-20">
          <el-pagination
            v-model:current-page="searchParams.page"
            v-model:page-size="searchParams.page_size"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="fetchApplicationList"
            @current-change="fetchApplicationList"
          />
        </div>

        <!-- 空状态 -->
        <div class="empty-container" v-if="!loading && applicationList.length === 0">
          <el-empty description="暂无投递记录，去看看心仪的岗位吧~">
            <el-button type="primary" @click="$router.push('/jobseeker/jobs')">
              去找工作
            </el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMyApplications } from '@/api/jobseeker/job'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const applicationList = ref([])
const total = ref(0)

const searchParams = ref({
  status: null,
  page: 1,
  page_size: 10
})

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    1: '待审核',
    2: '已通过',
    3: '面试中',
    4: '已录用',
    5: '已拒绝'
  }
  return statusMap[status] || '未知状态'
}

// 获取状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    1: 'warning',
    2: 'success',
    3: 'primary',
    4: 'success',
    5: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取投递列表
const fetchApplicationList = async () => {
  try {
    loading.value = true
    // 过滤空值参数
    const params = Object.fromEntries(
      Object.entries(searchParams.value).filter(([_, value]) => value !== null && value !== undefined)
    )
    const res = await getMyApplications(params)
    applicationList.value = res.list || res || []
    total.value = res.total || applicationList.value.length
  } catch (error) {
    console.error('获取投递记录失败:', error)
    ElMessage.error('获取投递记录失败')
  } finally {
    loading.value = false
  }
}

// 查看岗位详情
const viewJobDetail = (jobId) => {
  router.push(`/jobseeker/jobs/${jobId}`)
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
.applications-page {
  padding-bottom: 20px;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.job-title {
  font-weight: 500;
  color: #409eff;
  cursor: pointer;
}

.job-title:hover {
  text-decoration: underline;
}

.salary-text {
  color: #f56c6c;
  font-weight: 500;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
}

.empty-container {
  padding: 40px 0;
}
</style>
