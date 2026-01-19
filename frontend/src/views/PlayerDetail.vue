<template>
  <div class="player-detail" v-if="player">
    <!-- 选手基本信息卡片 -->
    <el-card class="player-info-card">
      <div class="player-header">
        <div class="player-basic-info">
          <h1>{{ player.tag }}</h1>
          <p v-if="player.name" class="real-name">{{ player.name }}</p>
          <div class="player-tags">
            <el-tag :type="getRaceTagType(player.race)" size="large">
              {{ getRaceName(player.race) }}
            </el-tag>
            <el-tag v-if="player.country" type="info">
              {{ getCountryName(player.country) }}
            </el-tag>
            <el-tag v-if="player.team_id" type="success">
              战队 #{{ player.team_id }}
            </el-tag>
          </div>
        </div>
        <div class="player-stats-overview">
          <div class="stat-item">
            <el-icon class="stat-icon"><trophy /></el-icon>
            <div class="stat-info">
              <span class="stat-value">${{ player.total_earnings.toLocaleString() }}</span>
              <span class="stat-label">总奖金</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 生涯统计卡片 -->
    <el-card class="career-stats-card">
      <template #header>
        <h2>生涯统计</h2>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-box">
            <el-icon class="stat-icon"><opportunity /></el-icon>
            <div class="stat-content">
              <span class="stat-number">{{ player.total_games }}</span>
              <span class="stat-label">总场次</span>
            </div>
          </div>
        </el-col>
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-box win-box">
            <el-icon class="stat-icon"><check /></el-icon>
            <div class="stat-content">
              <span class="stat-number">{{ player.total_wins }}</span>
              <span class="stat-label">胜场</span>
            </div>
          </div>
        </el-col>
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-box loss-box">
            <el-icon class="stat-icon"><close /></el-icon>
            <div class="stat-content">
              <span class="stat-number">{{ player.total_losses }}</span>
              <span class="stat-label">负场</span>
            </div>
          </div>
        </el-col>
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-box rate-box">
            <el-icon class="stat-icon"><aim /></el-icon>
            <div class="stat-content">
              <span class="stat-number">{{ (player.win_rate * 100).toFixed(1) }}%</span>
              <span class="stat-label">胜率</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 对战历史 -->
    <el-card class="matches-card">
      <template #header>
        <div class="card-header">
          <h2>对战历史</h2>
          <el-button-group>
            <el-button
              :type="viewMode === 'all' ? 'primary' : 'default'"
              @click="viewMode = 'all'"
            >
              全部
            </el-button>
            <el-button
              :type="viewMode === 'headtohead' ? 'primary' : 'default'"
              @click="openHeadToHeadDialog"
            >
              对战记录
            </el-button>
          </el-button-group>
        </div>
      </template>
      
      <el-table
        :data="matches"
        style="width: 100%"
        v-loading="loadingMatches"
        @sort-change="handleSort"
      >
        <el-table-column prop="date" label="日期" width="120" sortable="custom">
          <template #default="scope">
            {{ formatDate(scope.row.date) }}
          </template>
        </el-table-column>
        <el-table-column label="对手" min-width="150">
          <template #default="scope">
            <div class="opponent-info">
              <span>{{ getOpponentName(scope.row) }}</span>
              <el-tag size="small" :type="getRaceTagType(getOpponentRace(scope.row))">
                {{ getRaceName(getOpponentRace(scope.row)) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="比分" width="120">
          <template #default="scope">
            <div class="score" :class="{ win: isPlayerWin(scope.row) }">
              {{ getPlayerScore(scope.row) }} : {{ getOpponentScore(scope.row) }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="结果" width="100">
          <template #default="scope">
            <el-tag :type="isPlayerWin(scope.row) ? 'success' : 'danger'">
              {{ isPlayerWin(scope.row) ? '胜' : '负' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="event" label="赛事" min-width="150">
          <template #default="scope">
            <span class="event-name">{{ getEventName(scope.row) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="80">
          <template #default="scope">
            <div style="display: flex; flex-direction: column; gap: 4px;">
              <el-tag size="small" type="success">
                {{ getBestOf(scope.row) }}
              </el-tag>
              <el-tag size="small" :type="scope.row.offline ? 'warning' : 'info'">
                {{ scope.row.offline ? '线下' : '线上' }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="matchPage"
          v-model:page-size="matchPageSize"
          :total="totalMatches"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleMatchPageSizeChange"
          @current-change="handleMatchPageChange"
        />
      </div>
    </el-card>

    <!-- 对战记录对话框 -->
    <el-dialog
      v-model="showHeadToHeadDialog"
      title="选择对手查看对战记录"
      width="600px"
    >
      <el-form @submit.prevent="loadHeadToHead">
        <el-form-item label="对手账号">
          <el-input
            v-model="opponentQuery"
            placeholder="输入对手名称"
            clearable
          />
        </el-form-item>
      </el-form>
      
      <div v-if="headToHeadData" class="head-to-head-result">
        <div class="h2h-summary">
          <h3>对战总览</h3>
          <div class="h2h-stats">
            <div class="h2h-player">
              <strong>{{ player.tag }}</strong>
              <span class="h2h-wins">{{ headToHeadData.player1_wins }}</span>
            </div>
            <div class="h2h-vs">VS</div>
            <div class="h2h-player">
              <strong>{{ headToHeadData.player2.tag }}</strong>
              <span class="h2h-wins">{{ headToHeadData.player2_wins }}</span>
            </div>
          </div>
          <p class="h2h-total">共 {{ headToHeadData.total_games }} 场比赛</p>
        </div>
        
        <el-divider />
        
        <el-table :data="headToHeadData.matches" style="width: 100%" max-height="300">
          <el-table-column prop="date" label="日期" width="120">
            <template #default="scope">
              {{ formatDate(scope.row.date) }}
            </template>
          </el-table-column>
          <el-table-column label="比分" width="100">
            <template #default="scope">
              <span :class="getMatchResultClass(scope.row)">
                {{ scope.row.player1_score }}:{{ scope.row.player2_score }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="event" label="赛事" />
        </el-table>
      </div>
      
      <template #footer>
        <el-button @click="showHeadToHeadDialog = false">关闭</el-button>
        <el-button type="primary" @click="loadHeadToHead" :loading="loadingHeadToHead">
          查询
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { playerAPI } from '../services/api'

const route = useRoute()
const playerId = route.params.id

const player = ref(null)
const matches = ref([])
const loading = ref(false)
const loadingMatches = ref(false)
const loadingHeadToHead = ref(false)

const viewMode = ref('all')
const matchPage = ref(1)
const matchPageSize = ref(20)
const totalMatches = ref(0)

const showHeadToHeadDialog = ref(false)
const opponentQuery = ref('')
const headToHeadData = ref(null)

const raceMap = {
  'P': '神族',
  'T': '人族',
  'Z': '虫族',
  'R': '随机'
}

const getRaceName = (race) => {
  return raceMap[race] || race || '未知'
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

const getCountryName = (code) => {
  const map = {
    'KR': '韩国',
    'CN': '中国',
    'US': '美国',
    'EU': '欧洲'
  }
  return map[code] || code
}

const loadPlayer = async () => {
  loading.value = true
  try {
    player.value = await playerAPI.getPlayer(playerId)
    loadMatches()
  } catch (error) {
    console.error('加载选手失败:', error)
  } finally {
    loading.value = false
  }
}

const loadMatches = async () => {
  loadingMatches.value = true
  try {
    const response = await playerAPI.getPlayerMatches(playerId, {
      limit: matchPageSize.value,
      offset: (matchPage.value - 1) * matchPageSize.value
    })
    matches.value = response
    totalMatches.value = response.length
  } catch (error) {
    console.error('加载比赛失败:', error)
  } finally {
    loadingMatches.value = false
  }
}

const getOpponentName = (match) => {
  // 从player对象获取名字（如果存在），否则返回ID
  if (match.player1_id === parseInt(playerId)) {
    return match.player2?.tag || match.player2?.name || `Player ${match.player2_id}`
  }
  return match.player1?.tag || match.player1?.name || `Player ${match.player1_id}`
}

const getOpponentRace = (match) => {
  if (match.player1_id === parseInt(playerId)) {
    return match.player2_race
  }
  return match.player1_race
}

const getPlayerScore = (match) => {
  if (match.player1_id === parseInt(playerId)) {
    return match.player1_score
  }
  return match.player2_score
}

const getOpponentScore = (match) => {
  if (match.player1_id === parseInt(playerId)) {
    return match.player2_score
  }
  return match.player1_score
}

const getBestOf = (match) => {
  // 根据比分推断BO类型
  const p1_score = match.player1_score || 0
  const p2_score = match.player2_score || 0
  const max_score = Math.max(p1_score, p2_score)
  
  // 根据最大比分推断
  if (max_score === 1) return 'BO1'
  if (max_score === 2) return 'BO3'
  if (max_score === 3) return 'BO5'
  if (max_score === 4) return 'BO7'
  if (max_score >= 5) return 'BO9+'
  
  // 如果无法确定，根据常见情况推断
  // 如果双方都有分数，可能是BO3或BO5
  if (p1_score > 0 && p2_score > 0) {
    if (p1_score + p2_score <= 3) return 'BO3'
    if (p1_score + p2_score <= 5) return 'BO5'
    return 'BO7+'
  }
  
  return 'unknown'
}

const isPlayerWin = (match) => {
  return getPlayerScore(match) > getOpponentScore(match)
}

const getEventName = (match) => {
  // 优先使用event.full_name，如果没有则使用event.name，如果都没有显示'未知赛事'
  if (match.event) {
    
    return match.event.full_name || match.event.name || '未知赛事'
  }
  return '未知赛事'
}

const formatDate = (dateString) => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const openHeadToHeadDialog = () => {
  showHeadToHeadDialog.value = true
  headToHeadData.value = null
}

const loadHeadToHead = async () => {
  loadingHeadToHead.value = true
  try {
    // 这里应该搜索对手并获取对战数据
    // 暂时模拟数据
    headToHeadData.value = {
      player1_wins: 5,
      player2_wins: 3,
      total_games: 8,
      player2: { tag: opponentQuery.value || '未知对手' },
      matches: []
    }
  } catch (error) {
    console.error('加载对战数据失败:', error)
  } finally {
    loadingHeadToHead.value = false
  }
}

const getMatchResultClass = (match) => {
  return isPlayerWin(match) ? 'match-win' : 'match-loss'
}

const handleSort = ({ prop, order }) => {
  console.log('排序:', prop, order)
}

const handleMatchPageSizeChange = (size) => {
  matchPageSize.value = size
  loadMatches()
}

const handleMatchPageChange = (page) => {
  matchPage.value = page
  loadMatches()
}

onMounted(() => {
  loadPlayer()
})
</script>

<style scoped>
.player-detail {
  max-width: 1200px;
  margin: 0 auto;
}

.player-info-card {
  margin-bottom: 20px;
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.player-basic-info h1 {
  margin: 0 0 10px;
  font-size: 32px;
  color: #303133;
}

.real-name {
  margin: 0 0 15px;
  color: #909399;
  font-size: 18px;
}

.player-tags .el-tag {
  margin-right: 10px;
  font-weight: bold;
}

.player-stats-overview .stat-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.stat-icon {
  font-size: 40px;
  margin-right: 15px;
  color: rgba(255, 255, 255, 0.8);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.career-stats-card {
  margin-bottom: 20px;
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s;
}

.stat-box:hover {
  transform: translateY(-5px);
}

.stat-box .stat-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.stat-box.win-box {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
  color: white;
}

.stat-box.loss-box {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
  color: white;
}

.stat-box.rate-box {
  background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
  color: white;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  opacity: 0.9;
}

.matches-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.opponent-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.score {
  font-weight: bold;
  font-size: 16px;
}

.score.win {
  color: #67c23a;
}

.score:not(.win) {
  color: #f56c6c;
}

.event-name {
  font-size: 14px;
  color: #606266;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.head-to-head-result {
  margin-top: 20px;
}

.h2h-summary {
  text-align: center;
  padding: 20px;
}

.h2h-summary h3 {
  margin-bottom: 20px;
}

.h2h-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
  gap: 30px;
}

.h2h-player {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.h2h-wins {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-top: 10px;
}

.h2h-vs {
  font-size: 18px;
  color: #909399;
}

.h2h-total {
  color: #606266;
  font-size: 14px;
}

.match-win {
  color: #67c23a;
  font-weight: bold;
}

.match-loss {
  color: #f56c6c;
  font-weight: bold;
}

@media (max-width: 768px) {
  .player-header {
    flex-direction: column;
    text-align: center;
  }
  
  .player-stats-overview {
    margin-top: 20px;
  }
  
  .h2h-stats {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
