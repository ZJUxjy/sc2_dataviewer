<template>
  <div class="ranking">
    <el-card>
      <template #header>
        <h2>选手排行榜</h2>
      </template>
      
      <!-- 筛选 -->
      <div class="filters">
        <el-radio-group v-model="selectedRace" @change="loadRanking">
          <el-radio label="">全部</el-radio>
          <el-radio label="P">神族</el-radio>
          <el-radio label="T">人族</el-radio>
          <el-radio label="Z">虫族</el-radio>
        </el-radio-group>
      </div>
      
      <!-- 排行榜表格 -->
      <el-table
        :data="ranking"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column label="排名" width="100">
          <template #default="scope">
            <div class="rank-display">
              <el-icon v-if="scope.row.rank <= 3" class="medal" :class="`medal-${scope.row.rank}`">
                <trophy />
              </el-icon>
              <span v-else class="rank-number">{{ scope.row.rank }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="选手" min-width="200">
          <template #default="scope">
            <div class="player-info">
              <el-link
                @click="$router.push(`/players/${scope.row.player_id}`)"
              >
                <strong>{{ scope.row.tag }}</strong>
              </el-link>
              <el-tag
                v-if="scope.row.country"
                size="small"
                class="country-tag"
              >
                {{ scope.row.country }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="race" label="种族" width="100">
          <template #default="scope">
            <el-tag :type="getRaceTagType(scope.row.race)" size="default" class="race-tag">
              {{ getRaceName(scope.row.race) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="total_games" label="总场次" width="120" sortable />
        
        <el-table-column prop="win_rate" label="胜率" width="150" sortable>
          <template #default="scope">
            <div class="winrate-cell">
              <span class="winrate-text">{{ scope.row.win_rate }}%</span>
              <el-progress
                :percentage="scope.row.win_rate"
                :color="getWinRateColor(scope.row.win_rate)"
                :stroke-width="6"
                :show-text="false"
                style="width: 80px"
              />
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="total_earnings" label="总奖金" width="150" sortable>
          <template #default="scope">
            <span class="earnings">
              ${{ scope.row.total_earnings.toLocaleString() }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { rankingAPI } from '../services/api'

const loading = ref(false)
const ranking = ref([])
const selectedRace = ref('')

const getRaceName = (race) => {
  const map = {
    'P': '神族',
    'T': '人族',
    'Z': '虫族',
    'R': '随机'
  }
  return map[race] || race || '未知'
}

const getRaceTagType = (race) => {
  const map = {
    'P': 'warning',
    'T': '',
    'Z': 'success',
    'R': 'info'
  }
  return map[race] || 'info'
}

const getWinRateColor = (winRate) => {
  if (winRate >= 70) return '#67c23a'
  if (winRate >= 50) return '#409eff'
  return '#f56c6c'
}

const loadRanking = async () => {
  loading.value = true
  try {
    const params = { limit: 100 }
    if (selectedRace.value) {
      params.race = selectedRace.value
    }
    ranking.value = await rankingAPI.getRanking(params)
  } catch (error) {
    console.error('加载排行榜失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRanking()
})
</script>

<style scoped>
.ranking {
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.rank-display {
  display: flex;
  justify-content: center;
  align-items: center;
}

.medal {
  font-size: 32px;
}

.medal-1 {
  color: #ffd700;
}

.medal-2 {
  color: #c0c0c0;
}

.medal-3 {
  color: #cd7f32;
}

.rank-number {
  font-size: 18px;
  font-weight: bold;
  color: #606266;
}

.player-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.country-tag {
  width: fit-content;
}

.race-tag {
  font-weight: bold;
}

.winrate-cell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.winrate-text {
  font-size: 18px;
  font-weight: bold;
}

.earnings {
  color: #e6a23c;
  font-weight: bold;
}
</style>
