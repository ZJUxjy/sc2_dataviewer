<template>
  <div class="cyber-ranking">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="neon-text subtitle">全球排行榜</h1>
          <p class="page-description">星际争霸2职业选手实时排名数据</p>
        </div>
        <div class="stats-overview">
          <div class="stat-item">
            <span class="stat-value">{{ totalPlayers }}</span>
            <span class="stat-label">职业选手</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ ranking.length }}</span>
            <span class="stat-label">当前显示</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 筛选控制面板 -->
    <div class="control-panel glass-card">
      <div class="filter-section">
        <h3 class="section-label">种族筛选</h3>
        <div class="radio-group">
          <button 
            v-for="option in raceOptions" 
            :key="option.value"
            class="radio-button"
            :class="{ active: selectedRace === option.value }"
            @click="selectRace(option.value)"
          >
            <span class="button-label">{{ option.label }}</span>
            <span class="button-value">{{ option.value || '全部' }}</span>
          </button>
        </div>
      </div>
      
      <div class="sort-section">
        <h3 class="section-label">排序选项</h3>
        <el-select v-model="sortBy" @change="loadRanking" class="sort-select">
          <el-option label="按评分排序" value="rating" />
          <el-option label="按胜率排序" value="win_rate" />
          <el-option label="按场次排序" value="total_games" />
        </el-select>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner">
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
      </div>
      <p class="loading-text">正在加载排行榜数据...</p>
    </div>
    
    <!-- 排行榜表格 -->
    <div v-else class="ranking-table-container glass-card">
      <div class="table-wrapper">
        <table class="cyber-table">
          <thead>
            <tr>
              <th class="col-rank">排名</th>
              <th class="col-player">选手</th>
              <th class="col-race">种族</th>
              <th class="col-rating">评分</th>
              <th class="col-games">场次</th>
              <th class="col-winrate">胜率</th>
              <th class="col-earnings">奖金</th>
              <th class="col-trend">趋势</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(player, index) in ranking" 
              :key="player.player_id"
              class="table-row"
              :class="{ 'row-top-3': index < 3 }"
            >
              <td class="cell-rank">
                <div class="rank-display">
                  <div 
                    class="rank-medal" 
                    v-if="index < 3"
                    :class="`medal-${index + 1}`"
                  >
                    <svg viewBox="0 0 100 100" class="medal-icon">
                      <path d="M50 10 L90 40 L70 90 L30 90 L10 40 Z" fill="currentColor"/>
                    </svg>
                    <span class="medal-rank">{{ index + 1 }}</span>
                  </div>
                  <div v-else class="rank-number">
                    <span class="rank-digit">{{ index + 1 }}</span>
                    <div class="rank-glow"></div>
                  </div>
                </div>
              </td>
              
              <td class="cell-player">
                <div class="player-info">
                  <div 
                    class="player-name" 
                    @click="goToPlayer(player.player_id)"
                  >
                    {{ player.tag }}
                  </div>
                  <div class="player-details">
                    <span v-if="player.name && player.name !== player.tag" class="player-alias">
                      {{ player.name }}
                    </span>
                    <span class="player-country">{{ player.country || 'Unknown' }}</span>
                  </div>
                </div>
              </td>
              
              <td class="cell-race">
                <div class="race-badge" :class="`race-${player.race}`">
                  {{ getRaceSymbol(player.race) }}
                </div>
              </td>
              
              <td class="cell-rating">
                <div class="rating-display">
                  <span class="rating-value">{{ player.current_rating?.toFixed(2) || 'N/A' }}</span>
                  <div class="rating-bar">
                    <div 
                      class="rating-fill"
                      :style="{ width: `${calculateRatingPercent(player.current_rating)}%` }"
                    ></div>
                  </div>
                </div>
              </td>
              
              <td class="cell-games">
                <div class="stat-text primary">{{ player.total_games || 0 }}</div>
              </td>
              
              <td class="cell-winrate">
                <div class="winrate-display">
                  <div class="winrate-text">{{ player.win_rate }}%</div>
                  <div class="winrate-bar">
                    <div 
                      class="winrate-fill"
                      :style="{ width: `${player.win_rate}%`, background: getWinRateColor(player.win_rate) }"
                    ></div>
                  </div>
                </div>
              </td>
              
              <td class="cell-earnings">
                <div class="earnings-display">
                  <span class="earnings-symbol">$</span>
                  <span class="earnings-value">{{ formatEarnings(player.total_earnings) }}</span>
                </div>
              </td>
              
              <td class="cell-trend">
                <div 
                  class="trend-indicator"
                  :class="getTrendClass(player.rating_trend)"
                >
                  <el-icon 
                    :size="16" 
                    class="trend-icon"
                  >
                    <component :is="getTrendIcon(player.rating_trend)" />
                  </el-icon>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-if="!loading && ranking.length === 0" class="empty-state">
      <div class="empty-icon">
        <el-icon :size="64" color="var(--color-text-muted)"><Trophy /></el-icon>
      </div>
      <h3 class="empty-title">暂无排行榜数据</h3>
      <p class="empty-description">
        可能是数据还未同步，请检查数据同步状态或稍后再试。
      </p>
      <div class="empty-actions">
        <button class="neon-button" @click="loadRanking">
          重新加载
        </button>
        <button class="neon-button purple" @click="goToSync">
          同步数据
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Trophy, 
  TrendCharts,
  Top,
  RefreshRight,
  Bottom,
  Warning,
  Search
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

// 状态
const loading = ref(false)
const ranking = ref([])
const selectedRace = ref('')
const sortBy = ref('rating')
const totalPlayers = ref(0)

// 种族选项
const raceOptions = [
  { value: '', label: '全部', count: 0 },
  { value: 'P', label: '神族', count: 0 },
  { value: 'T', label: '人族', count: 0 },
  { value: 'Z', label: '虫族', count: 0 }
]

// 获取排行榜数据
const loadRanking = async () => {
  loading.value = true
  try {
    const params = {
      race: selectedRace.value || undefined,
      limit: 500,
      sort: sortBy.value
    }
    
    const response = await axios.get('http://localhost:8000/api/ranking', { params })
    
    if (response.data && Array.isArray(response.data)) {
      ranking.value = response.data
    } else {
      ranking.value = []
    }
    
    // 更新总数
    totalPlayers.value = ranking.value.length
    
  } catch (error) {
    console.error('加载排行榜失败:', error)
    ranking.value = []
    
    // 显示错误信息
    if (error.response) {
      console.error('错误响应:', error.response.data)
    } else if (error.request) {
      console.error('无法连接到后端服务')
    } else {
      console.error('请求配置错误:', error.message)
    }
    
  } finally {
    loading.value = false
  }
}

// 选择种族
const selectRace = (race) => {
  selectedRace.value = race
  loadRanking()
}

// 跳转到选手详情
const goToPlayer = (playerId) => {
  if (playerId) {
    router.push(`/players/${playerId}`)
  }
}

// 获取种族符号
const getRaceSymbol = (race) => {
  const symbols = { P: 'P', T: 'T', Z: 'Z', R: 'R' }
  return symbols[race] || '?'
}

// 获取种族名称
const getRaceName = (race) => {
  const names = { P: '神族', T: '人族', Z: '虫族', R: '随机' }
  return names[race] || '未知'
}

// 格式化奖金
const formatEarnings = (earnings) => {
  if (!earnings || earnings === 0) return '0'
  return earnings.toLocaleString()
}

// 计算评分百分比（用于进度条）
const calculateRatingPercent = (rating) => {
  if (!rating) return 0
  // 假设评分范围 0-3000
  return Math.min(100, Math.max(0, (rating / 3000) * 100))
}

// 获取胜率颜色
const getWinRateColor = (winRate) => {
  if (!winRate) return '#606266'
  if (winRate >= 70) return '#00ff9d'
  if (winRate >= 50) return '#00f2fe'
  return '#ff0044'
}

// 获取趋势图标
const getTrendIcon = (trend) => {
  if (!trend) return TrendCharts
  if (trend === 'up') return Top
  if (trend === 'down') return Bottom
  return TrendCharts
}

// 获取趋势样式类
const getTrendClass = (trend) => {
  if (!trend) return ''
  if (trend === 'up') return 'trend-up'
  if (trend === 'down') return 'trend-down'
  return 'trend-stable'
}

// 跳转到同步页面
const goToSync = () => {
  router.push('/players')
}

onMounted(() => {
  loadRanking()
})
</script>

<style scoped>
/* ===========================================
   页面头部样式
   =========================================== */

.page-header {
  padding: 2rem 0;
  border-bottom: 1px solid var(--color-border-primary);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.page-description {
  font-size: 1rem;
  color: var(--color-text-secondary);
}

.stats-overview {
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-value {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--color-neon-cyan);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ===========================================
   控制面板样式
   =========================================== */

.control-panel {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 1.5rem 2rem;
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
  min-width: 80px;
}

.radio-group {
  display: flex;
  gap: 0.5rem;
}

.radio-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--color-border-secondary);
  color: var(--color-text-secondary);
  border-radius: 6px;
  cursor: pointer;
  transition: var(--transition-fast);
}

.radio-button:hover {
  border-color: var(--color-border-primary);
  color: var(--color-text-primary);
}

.radio-button.active {
  background: rgba(0, 242, 254, 0.1);
  border-color: var(--color-neon-blue);
  color: var(--color-neon-blue);
  box-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
}

.button-value {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.875rem;
}

.sort-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-select {
  min-width: 140px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--color-border-secondary);
  border-radius: 6px;
}

/* ===========================================
   加载状态样式
   =========================================== */

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
}

.loading-spinner {
  position: relative;
  width: 60px;
  height: 60px;
}

.spinner-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 3px solid transparent;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.spinner-ring:nth-child(1) {
  width: 60px;
  height: 60px;
  border-top-color: var(--color-neon-blue);
  animation-duration: 1.5s;
}

.spinner-ring:nth-child(2) {
  width: 48px;
  height: 48px;
  border-right-color: var(--color-neon-purple);
  animation-duration: 1.2s;
  animation-delay: -0.2s;
}

.spinner-ring:nth-child(3) {
  width: 36px;
  height: 36px;
  border-bottom-color: var(--color-neon-cyan);
  animation-duration: 1s;
  animation-delay: -0.4s;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

.loading-text {
  font-size: 1rem;
  color: var(--color-text-secondary);
}

/* ===========================================
   空状态样式
   =========================================== */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
}

.empty-icon {
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.empty-description {
  font-size: 1rem;
  color: var(--color-text-secondary);
  text-align: center;
  max-width: 400px;
  margin-bottom: 2rem;
}

.empty-actions {
  display: flex;
  gap: 1rem;
}

/* ===========================================
   表格样式
   =========================================== */

.ranking-table-container {
  max-width: 1400px;
  margin: 0 auto 2rem;
  padding: 1.5rem 2rem;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
}

.cyber-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--color-border-secondary);
}

.cyber-table thead {
  background: rgba(0, 0, 0, 0.3);
}

.cyber-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--color-neon-cyan);
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--color-border-primary);
}

.cyber-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border-secondary);
  transition: var(--transition-fast);
}

.cyber-table tr:hover td {
  background: rgba(0, 242, 254, 0.05);
}

.cyber-table tr.row-top-3 {
  background: rgba(0, 242, 254, 0.05);
}

.cyber-table tr.row-top-3:hover td {
  background: rgba(0, 242, 254, 0.1);
}

/* 列样式 */
.col-rank { width: 120px; }
.col-player { min-width: 250px; }
.col-race { width: 100px; }
.col-rating { width: 150px; }
.col-games { width: 120px; }
.col-winrate { width: 150px; }
.col-earnings { width: 150px; }
.col-trend { width: 100px; }

/* 排名显示 */
.rank-display {
  display: flex;
  justify-content: center;
  align-items: center;
}

.rank-medal {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 0 8px currentColor);
}

.rank-medal.medal-1 { color: #ffd700; }
.rank-medal.medal-2 { color: #c0c0c0; }
.rank-medal.medal-3 { color: #cd7f32; }

.medal-icon {
  width: 100%;
  height: 100%;
}

.medal-rank {
  position: absolute;
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 0.875rem;
  color: var(--color-bg-primary);
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
}

.rank-number {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border-primary);
  border-radius: 50%;
}

.rank-digit {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--color-text-secondary);
}

.rank-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, var(--color-neon-blue), transparent);
  border-radius: 50%;
  opacity: 0.3;
  animation: pulse 2s infinite;
}

/* 选手信息 */
.player-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.player-name:hover {
  color: var(--color-neon-blue);
  text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
}

.player-details {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin-top: 0.25rem;
}

.player-alias {
  font-style: italic;
}

.player-country {
  font-family: var(--font-display);
  letter-spacing: 0.5px;
}

/* 种族徽章 */
.race-badge {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
}

.race-badge.race-P {
  border-color: var(--color-neon-blue);
  color: var(--color-neon-blue);
  background: rgba(0, 242, 254, 0.1);
}

.race-badge.race-T {
  border-color: var(--color-neon-purple);
  color: var(--color-neon-purple);
  background: rgba(139, 0, 255, 0.1);
}

.race-badge.race-Z {
  border-color: var(--color-neon-cyan);
  color: var(--color-neon-cyan);
  background: rgba(0, 255, 234, 0.1);
}

.race-badge.race-R {
  border-color: var(--color-neon-pink);
  color: var(--color-neon-pink);
  background: rgba(255, 0, 200, 0.1);
}

/* 评分显示 */
.rating-display {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rating-value {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--color-neon-cyan);
}

.rating-bar {
  width: 100%;
  height: 4px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 2px;
  overflow: hidden;
}

.rating-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-neon-blue), var(--color-neon-cyan));
  border-radius: 2px;
  transition: width var(--transition-slow);
}

/* 统计数据 */
.stat-text {
  font-family: var(--font-display);
  font-weight: 600;
}

.stat-text.primary {
  color: var(--color-neon-blue);
}

/* 胜率显示 */
.winrate-display {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.winrate-text {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--color-success);
}

.winrate-bar {
  width: 100%;
  height: 6px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.winrate-fill {
  height: 100%;
  border-radius: 3px;
  transition: width var(--transition-slow);
  box-shadow: 0 0 8px currentColor;
}

/* 奖金显示 */
.earnings-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-family: var(--font-display);
}

.earnings-symbol {
  color: var(--color-warning);
}

.earnings-value {
  font-weight: 700;
  color: var(--color-warning);
}

/* 趋势指示器 */
.trend-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
}

.trend-icon {
  transition: var(--transition-fast);
}

.trend-up .trend-icon {
  color: var(--color-success);
  animation: bounce 1s infinite;
}

.trend-down .trend-icon {
  color: var(--color-error);
  animation: shake 1s infinite;
}

.trend-stable .trend-icon {
  color: var(--color-text-muted);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

/* ===========================================
   响应式设计
   =========================================== */

@media (max-width: 1200px) {
  .col-earnings { display: none; }
  .col-trend { display: none; }
}

@media (max-width: 1024px) {
  .col-games { display: none; }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .control-panel {
    padding: 1rem;
  }
  
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .radio-group {
    flex-wrap: wrap;
  }
  
  .table-wrapper {
    overflow-x: scroll;
  }
  
  .cyber-table {
    min-width: 600px;
  }
}
</style>
