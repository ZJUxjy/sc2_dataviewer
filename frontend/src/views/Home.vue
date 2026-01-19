<template>
  <div class="home">
    <!-- 欢迎区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>星际争霸2职业选手数据分析</h1>
        <p>收录全球顶尖星际争霸2职业选手的生涯数据，包括对战历史、胜率统计、赛事记录等完整信息</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/players')">
            浏览选手
          </el-button>
          <el-button size="large" @click="$router.push('/ranking')">
            查看排行
          </el-button>
        </div>
      </div>
      <div class="hero-image">
        <el-icon class="hero-icon"><medal /></el-icon>
      </div>
    </div>

    <!-- 数据概览 -->
    <el-row :gutter="20" class="stats-overview">
      <el-col :span="6" :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon"><user /></el-icon>
            <div class="stat-info">
              <h3>{{ stats.playersCount || 0 }}</h3>
              <p>职业选手</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6" :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon"><trophy /></el-icon>
            <div class="stat-info">
              <h3>{{ stats.matchesCount || 0 }}</h3>
              <p>比赛记录</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6" :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon"><opportunity /></el-icon>
            <div class="stat-info">
              <h3>{{ stats.eventsCount || 0 }}</h3>
              <p>赛事数量</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6" :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon"><money /></el-icon>
            <div class="stat-info">
              <h3>${{ stats.totalEarnings || 0 }}</h3>
              <p>总奖金</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 顶级选手 -->
    <el-card class="top-players-card">
      <template #header>
        <div class="card-header">
          <h2>顶级选手</h2>
          <el-button text @click="$router.push('/ranking')">
            查看全部 <el-icon><arrow-right /></el-icon>
          </el-button>
        </div>
      </template>
      
      <el-table :data="topPlayers" style="width: 100%" v-loading="loading">
        <el-table-column prop="rank" label="排名" width="80">
          <template #default="scope">
            <el-tag v-if="scope.row.rank <= 3" type="danger" size="small">
              {{ scope.row.rank }}
            </el-tag>
            <span v-else>{{ scope.row.rank }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="tag" label="选手">
          <template #default="scope">
            <el-link @click="$router.push(`/players/${scope.row.player_id}`)">{{ scope.row.tag }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="race" label="种族" width="80">
          <template #default="scope">
            <el-tag :type="getRaceTagType(scope.row.race)" size="small">
              {{ scope.row.race || '未知' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="country" label="国家" width="80" />
        <el-table-column prop="win_rate" label="胜率" width="100">
          <template #default="scope">
            {{ scope.row.win_rate }}%
          </template>
        </el-table-column>
        <el-table-column prop="total_games" label="总场次" width="100" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { rankingAPI } from '../services/api'

const loading = ref(false)
const topPlayers = ref([])
const stats = ref({
  playersCount: 0,
  matchesCount: 0,
  eventsCount: 0,
  totalEarnings: 0
})

const getRaceTagType = (race) => {
  const map = {
    'P': 'warning',
    'T': '',
    'Z': 'success',
    'R': 'info'
  }
  return map[race] || 'info'
}

const loadTopPlayers = async () => {
  loading.value = true
  try {
    topPlayers.value = await rankingAPI.getRanking({ limit: 10 })
    stats.value.playersCount = 1000  // 这里可以从API获取实际数据
    stats.value.matchesCount = 10000
    stats.value.eventsCount = 500
    stats.value.totalEarnings = 5000000
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTopPlayers()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 60px 40px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.hero-content h1 {
  font-size: 36px;
  margin-bottom: 16px;
  font-weight: 600;
}

.hero-content p {
  font-size: 18px;
  margin-bottom: 24px;
  opacity: 0.9;
}

.hero-actions .el-button {
  margin-right: 12px;
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-icon {
  font-size: 120px;
  color: rgba(255, 255, 255, 0.2);
}

.stats-overview {
  margin-bottom: 30px;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.stat-icon {
  font-size: 48px;
  color: #409eff;
  margin-right: 16px;
}

.stat-info h3 {
  font-size: 28px;
  margin: 0;
  color: #303133;
}

.stat-info p {
  margin: 4px 0 0;
  color: #909399;
  font-size: 14px;
}

.top-players-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 40px 20px;
  }
  
  .hero-content h1 {
    font-size: 28px;
  }
  
  .hero-image {
    margin-top: 30px;
  }
  
  .hero-icon {
    font-size: 80px;
  }
  
  .hero-actions .el-button {
    margin: 0 6px 12px;
  }
}
</style>
