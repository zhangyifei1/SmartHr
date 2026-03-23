<template>
  <div class="user-management-page">
    <el-page-header content="用户管理" />

    <!-- 筛选栏 -->
    <div class="filter-bar mt-20">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索用户名、手机号、邮箱"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.user_type" placeholder="用户类型" clearable>
            <el-option label="全部" value="" />
            <el-option label="求职者" :value="1" />
            <el-option label="企业" :value="2" />
            <el-option label="管理员" :value="3" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.status" placeholder="状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="正常" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 用户列表 -->
    <div class="list-section mt-20">
      <el-card>
        <el-table
          :data="userList"
          v-loading="loading"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="用户ID" width="80" />
          <el-table-column prop="username" label="用户名" min-width="150" />
          <el-table-column prop="phone" label="手机号" min-width="130" />
          <el-table-column prop="email" label="邮箱" min-width="180" />
          <el-table-column label="用户类型" min-width="100">
            <template #default="{ row }">
              <el-tag :type="getUserTypeTag(row.user_type)">
                {{ getUserTypeText(row.user_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" min-width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                {{ row.status === 1 ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="注册时间" min-width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button
                :type="row.status === 1 ? 'danger' : 'success'"
                size="small"
                @click="handleToggleStatus(row)"
                :disabled="row.user_type === 3"
              >
                {{ row.status === 1 ? '禁用' : '启用' }}
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
            @size-change="handleSearch"
            @current-change="handleSearch"
          />
        </div>

        <!-- 空状态 -->
        <div class="empty-container" v-if="!loading && userList.length === 0">
          <el-empty description="暂无用户数据" />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, updateUserStatus } from '@/api/admin/user'

const loading = ref(false)
const userList = ref([])
const total = ref(0)

const searchParams = ref({
  keyword: '',
  user_type: '',
  status: '',
  page: 1,
  page_size: 10
})

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

// 获取用户列表
const fetchUserList = async () => {
  try {
    loading.value = true
    // 过滤空值参数
    const params = Object.fromEntries(
      Object.entries(searchParams.value).filter(([_, value]) => value !== '' && value != null)
    )
    const res = await getUserList(params)
    userList.value = res.list || res || []
    total.value = res.total || userList.value.length
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.value.page = 1
  fetchUserList()
}

// 重置
const handleReset = () => {
  searchParams.value = {
    keyword: '',
    user_type: '',
    status: '',
    page: 1,
    page_size: 10
  }
  fetchUserList()
}

// 切换用户状态
const handleToggleStatus = async (row) => {
  const actionText = row.status === 1 ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(
      `确定要${actionText}该用户吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const newStatus = row.status === 1 ? 0 : 1
    await updateUserStatus(row.id, newStatus)
    ElMessage.success(`${actionText}成功`)
    fetchUserList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
    }
  }
}

onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
.user-management-page {
  padding-bottom: 20px;
}

.filter-bar {
  padding: 15px;
  background: #fff;
  border-radius: 4px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
}

.empty-container {
  padding: 40px 0;
}
</style>
