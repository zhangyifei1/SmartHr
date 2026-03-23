<template>
  <div class="enterprise-auth-page">
    <el-page-header content="企业认证审核" />

    <!-- 筛选栏 -->
    <div class="filter-bar mt-20">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索企业名称、统一社会信用代码"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchParams.status" placeholder="审核状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="审核中" :value="1" />
            <el-option label="已通过" :value="2" />
            <el-option label="已拒绝" :value="3" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 认证列表 -->
    <div class="list-section mt-20">
      <el-card>
        <el-table
          :data="authList"
          v-loading="loading"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="企业ID" width="80" />
          <el-table-column prop="company_name" label="企业名称" min-width="200" />
          <el-table-column prop="unified_social_credit_code" label="统一社会信用代码" min-width="200" />
          <el-table-column prop="legal_person" label="法人姓名" min-width="120" />
          <el-table-column label="审核状态" min-width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.auth_status)">
                {{ getStatusText(row.auth_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="auth_reason" label="审核备注" min-width="200" show-overflow-tooltip />
          <el-table-column prop="created_at" label="申请时间" min-width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button
                type="success"
                size="small"
                @click="handleAudit(row, 2)"
                :disabled="row.auth_status !== 1"
              >
                通过
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleAudit(row, 3)"
                :disabled="row.auth_status !== 1"
              >
                拒绝
              </el-button>
              <el-button
                type="info"
                size="small"
                @click="viewDetail(row)"
              >
                详情
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
        <div class="empty-container" v-if="!loading && authList.length === 0">
          <el-empty description="暂无认证申请" />
        </div>
      </el-card>
    </div>

    <!-- 审核弹窗 -->
    <el-dialog v-model="auditDialogVisible" :title="`${auditAction === 2 ? '通过' : '拒绝'}认证申请`" width="500px">
      <el-form v-if="currentAuth">
        <el-form-item label="企业名称">
          <el-input :value="currentAuth.company_name" disabled />
        </el-form-item>
        <el-form-item label="统一社会信用代码">
          <el-input :value="currentAuth.unified_social_credit_code" disabled />
        </el-form-item>
        <el-form-item label="审核备注" :rules="[
          { required: auditAction === 3, message: '拒绝原因不能为空', trigger: 'blur' }
        ]">
          <el-input
            v-model="auditForm.reason"
            type="textarea"
            :rows="3"
            :placeholder="auditAction === 2 ? '请输入审核意见（可选）' : '请输入拒绝原因'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="auditDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAudit" :loading="auditing">
          确认{{ auditAction === 2 ? '通过' : '拒绝' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialogVisible" title="企业认证详情" width="700px">
      <el-descriptions :column="1" border v-if="currentAuth">
        <el-descriptions-item label="企业名称">{{ currentAuth.company_name }}</el-descriptions-item>
        <el-descriptions-item label="统一社会信用代码">{{ currentAuth.unified_social_credit_code }}</el-descriptions-item>
        <el-descriptions-item label="法人姓名">{{ currentAuth.legal_person }}</el-descriptions-item>
        <el-descriptions-item label="营业执照">
          <img :src="currentAuth.business_license" alt="营业执照" style="max-width: 100%;" />
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ currentAuth.created_at }}</el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="getStatusType(currentAuth.auth_status)">
            {{ getStatusText(currentAuth.auth_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="审核备注" v-if="currentAuth.auth_reason">
          {{ currentAuth.auth_reason }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getEnterpriseAuthList,
  auditEnterpriseAuth
} from '@/api/admin/enterpriseAuth'

const loading = ref(false)
const auditing = ref(false)
const authList = ref([])
const total = ref(0)

const searchParams = ref({
  keyword: '',
  status: '',
  page: 1,
  page_size: 10
})

const auditDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentAuth = ref(null)
const auditAction = ref(2)
const auditForm = ref({
  reason: ''
})

// 获取状态文本
const getStatusText = (status) => {
  const map = {
    1: '审核中',
    2: '已通过',
    3: '已拒绝'
  }
  return map[status] || '未知'
}

// 获取状态标签颜色
const getStatusType = (status) => {
  const map = {
    1: 'warning',
    2: 'success',
    3: 'danger'
  }
  return map[status] || 'info'
}

// 获取认证列表
const fetchAuthList = async () => {
  try {
    loading.value = true
    // 过滤空值参数
    const params = Object.fromEntries(
      Object.entries(searchParams.value).filter(([_, value]) => value !== '' && value != null)
    )
    const res = await getEnterpriseAuthList(params)
    authList.value = res.list || res || []
    total.value = res.total || authList.value.length
  } catch (error) {
    console.error('获取认证列表失败:', error)
    ElMessage.error('获取认证列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.value.page = 1
  fetchAuthList()
}

// 重置
const handleReset = () => {
  searchParams.value = {
    keyword: '',
    status: '',
    page: 1,
    page_size: 10
  }
  fetchAuthList()
}

// 审核操作
const handleAudit = (row, action) => {
  currentAuth.value = row
  auditAction.value = action
  auditForm.value.reason = ''
  auditDialogVisible.value = true
}

// 查看详情
const viewDetail = (row) => {
  currentAuth.value = row
  detailDialogVisible.value = true
}

// 确认审核
const confirmAudit = async () => {
  if (auditAction.value === 3 && !auditForm.value.reason.trim()) {
    ElMessage.warning('请输入拒绝原因')
    return
  }

  try {
    auditing.value = true
    await auditEnterpriseAuth(currentAuth.value.id, auditAction.value, auditForm.value.reason)
    ElMessage.success(`审核${auditAction.value === 2 ? '通过' : '拒绝'}成功`)
    auditDialogVisible.value = false
    fetchAuthList()
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败，请稍后重试')
  } finally {
    auditing.value = false
  }
}

onMounted(() => {
  fetchAuthList()
})
</script>

<style scoped>
.enterprise-auth-page {
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
