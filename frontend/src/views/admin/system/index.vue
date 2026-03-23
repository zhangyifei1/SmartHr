<template>
  <div class="system-settings-page">
    <el-page-header content="系统设置" />

    <!-- 站点配置 -->
    <div class="config-section mt-20">
      <el-card>
        <template #header>
          <span>站点配置</span>
        </template>
        <el-form label-width="180px">
          <el-form-item label="站点名称">
            <el-input
              v-model="siteConfig.site_name"
              placeholder="请输入站点名称"
              style="width: 400px;"
            />
            <el-button
              type="primary"
              size="small"
              @click="saveSiteConfig('site_name', siteConfig.site_name)"
              style="margin-left: 20px;"
            >
              保存
            </el-button>
          </el-form-item>
          <el-form-item label="站点LOGO">
            <el-input
              v-model="siteConfig.site_logo"
              placeholder="请输入LOGO地址"
              style="width: 400px;"
            />
            <el-button
              type="primary"
              size="small"
              @click="saveSiteConfig('site_logo', siteConfig.site_logo)"
              style="margin-left: 20px;"
            >
              保存
            </el-button>
          </el-form-item>
          <el-form-item label="站点描述">
            <el-input
              v-model="siteConfig.site_description"
              type="textarea"
              :rows="3"
              placeholder="请输入站点描述"
              style="width: 400px;"
            />
            <el-button
              type="primary"
              size="small"
              @click="saveSiteConfig('site_description', siteConfig.site_description)"
              style="margin-left: 20px;"
            >
              保存
            </el-button>
          </el-form-item>
          <el-form-item label="是否开放注册">
            <el-switch
              v-model="siteConfig.allow_register"
              active-text="开启"
              inactive-text="关闭"
            />
            <el-button
              type="primary"
              size="small"
              @click="saveSiteConfig('allow_register', siteConfig.allow_register)"
              style="margin-left: 20px;"
            >
              保存
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { getSystemConfig, updateSystemConfig } from '@/api/admin/system'

const loading = ref(false)

// 站点配置
const siteConfig = reactive({
  site_name: 'SmartHr智能招聘系统',
  site_logo: '',
  site_description: '智能人力资源管理系统',
  allow_register: true
})

// 获取配置列表
const fetchConfigList = async () => {
  try {
    loading.value = true
    const res = await getSystemConfig()
    const list = res.list || []

    // 填充站点配置
    list.forEach(item => {
      if (item.config_key in siteConfig) {
        siteConfig[item.config_key] = item.config_value
      }
    })
  } catch (error) {
    console.error('获取系统配置失败:', error)
    ElMessage.error('获取系统配置失败')
  } finally {
    loading.value = false
  }
}

// 保存站点配置
const saveSiteConfig = async (key, value) => {
  try {
    await updateSystemConfig(key, value)
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存配置失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  }
}

onMounted(() => {
  fetchConfigList()
})
</script>

<style scoped>
.system-settings-page {
  padding-bottom: 40px;
}

.config-section {
  max-width: 900px;
}

.config-desc {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}
</style>
