<template>
  <div class="events">
    <el-card>
      <template #header>
        <h2>赛事列表</h2>
      </template>
      
      <el-table :data="events" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="赛事名称" min-width="300" />
        <el-table-column prop="category" label="级别" width="120">
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)">
              {{ scope.row.category || '未知' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { eventAPI } from '../services/api'

const loading = ref(false)
const events = ref([])

const getCategoryType = (category) => {
  const map = {
    'Premier': 'danger',
    'Major': 'warning',
    'Minor': 'success'
  }
  return map[category] || 'info'
}

const formatDate = (dateString) => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const loadEvents = async () => {
  loading.value = true
  try {
    events.value = await eventAPI.getEvents()
  } catch (error) {
    console.error('加载赛事失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadEvents()
})
</script>

<style scoped>
.events {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
