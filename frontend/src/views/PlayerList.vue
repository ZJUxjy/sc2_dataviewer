<template>
  <div class="cyber-player-list">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="neon-text subtitle">职业选手列表</h1>
          <p class="page-description">探索全球顶级星际争霸2职业选手的详细档案</p>
        </div>
        <div class="actions-section">
          <button class="neon-button" @click="showSyncDialog = true">
            <el-icon class="button-icon"><Refresh /></el-icon>
            同步数据
          </button>
        </div>
      </div>
    </div>
    
    <!-- 搜索和筛选面板 -->
    <div class="filters-panel glass-card">
      <div class="filter-row">
        <!-- 搜索框 -->
        <div class="search-group">
          <el-icon class="search-icon"><Search /></el-icon>
          <el-input
            v-model="searchQuery"
            placeholder="搜索选手名称..."
            clearable
            @input="handleSearch"
            class="search-input"
          />
        </div>
        
        <!-- 种族筛选 -->
        <div class="filter-group">
          <span class="filter-label">种族</span>
          <el-select
            v-model="selectedRace"
            placeholder="全部"
            clearable
            @change="handleFilter"
            class="filter-select"
          >
            <el-option label="神族" value="P"><span class="race-option protoss">神族 (P)</span></el-option>
            <el-option label="人族" value="T"><span class="race-option terran">人族 (T)</span></el-option>
            <el-option label="虫族" value="Z"><span class="race-option zerg">虫族 (Z)</span></el-option>
            <el-option label="随机" value="R"><span class="race-option random">随机 (R)</span></el-option>
          </el-select>
        </div>
        
        <!-- 国家筛选 -->
        <div class="filter-group">
          <span class="filter-label">地区</span>
          <el-select
            v-model="selectedCountry"
            placeholder="全部"
            clearable
            @change="handleFilter"
            class="filter-select"
          >
            <el-option label="韩国" value="KR"><span class="region-flag">🇰🇷</span> 韩国</el-option>
            <el-option label="中国" value="CN"><span class="region-flag">🇨🇳</span> 中国</el-option>
            <el-option label="美国" value="US"><span class="region-flag">🇺🇸</span> 美国</el-option>
            <el-option label="欧洲" value="EU"><span class="region-flag">🇪🇺</span> 欧洲</el-option>
          </el-select>
        </div>
        
        <!-- 排序方式 -->
        <div class="filter-group">
          <span class="filter-label">排序</span>
          <el-select
            v-model="sortBy"
            @change="handleFilter"
            class="filter-select"
          >
            <el-option label="评分排序" value="rating"></el-option>
            <el-option label="名称排序" value="tag"></el-option>
          </el-select>
        </div>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner">
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
      </div>
      <p class="loading-text">正在加载选手数据...</p>
    </div>
    
    <!-- 选手网格 -->
    <div v-else class="players-grid">
      <div 
        v-for="player in players" 
        :key="player.id"
        class="player-card glass-card"
        @click="goToPlayer(player.id)"
      >
        <!-- 排名徽章 -->
        <div 
          class="rank-badge"
          :class="getRankClass(player.current_rating_rank)"
        >
          <span class="rank-number">#{{ player.current_rating_rank || '-' }}</span>
        </div>
        
        <!-- 选手头像 -->
        <div class="player-avatar">
          <div class="avatar-bg" :class="`race-${player.race}`">
            <span class="race-symbol">{{ getRaceSymbol(player.race) }}</span>
          </div>
        </div>
        
        <!-- 选手信息 -->
        <div class="player-info">
          <h3 class="player-name">{{ player.tag }}</h3>
          <p class="player-alias">{{ player.name || 'Unknown' }}</p>
          <div class="player-meta">
            <span class="meta-item">
              <el-icon><Location /></el-icon>
              {{ player.country || 'Unknown' }}
            </span>
            <span class="meta-item race-tag" :class="`race-${player.race}`">
              {{ getRaceName(player.race) }}
            </span>
          </div>
        </div>
        
        <!-- 评分和胜率 -->
        <div class="player-stats">
          <div class="stat-item">
            <span class="stat-label">评分</span>
            <span class="stat-value rating">{{ player.current_rating?.toFixed(2) || 'N/A' }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">胜率</span>
            <span class="stat-value winrate">{{ calculateWinRate(player) }}%</span>
          </div>
        </div>
        
        <!-- 装饰光效 -->
        <div class="card-glow"></div>
      </div>
    </div>
    
    <!-- 分页控制 -->
    <div class="pagination-panel" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 40, 60, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
        class="cyber-pagination"
      />
    </div>
    
    <!-- 同步数据对话框 -->
    <el-dialog 
      v-model="showSyncDialog" 
      title="同步数据" 
      width="500px"
      class="cyber-dialog"
    >
      <div class="sync-content">
        <p>即将从 Aligulac API 同步最新数据</p>
        <div class="sync-warning">
          <el-icon><Warning /></el-icon>
          此操作可能需要几分钟时间，请耐心等待
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <button class="neon-button" @click="showSyncDialog = false">
            取消
          </button>
          <button class="neon-button purple" @click="syncData">
            开始同步
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Search, 
  Refresh, 
  Location,
  Warning,
  User,
  Operation,
  Opportunity,
  Grid
} from '@element-plus/icons-vue'

const router = useRouter()

// 状态
const loading = ref(false)
const players = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')
const selectedRace = ref('')
const selectedCountry = ref('')
const sortBy = ref('rating')
const showSyncDialog = ref(false)

// 获取选手数据
const fetchPlayers = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value || '',
      race: selectedRace.value || '',
      country: selectedCountry.value || '',
      sort: sortBy.value
    })
    
    const response = await fetch(`http://localhost:8000/api/players?${params}`)
    const data = await response.json()
    
    players.value = data.players
    total.value = data.total
  } catch (error) {
    console.error('获取选手数据失败:', error)
    ElMessage.error('加载数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchPlayers()
}

// 筛选处理
const handleFilter = () => {
  currentPage.value = 1
  fetchPlayers()
}

// 分页处理
const handlePageChange = () => {
  fetchPlayers()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 跳转到选手详情
const goToPlayer = (playerId) => {
  router.push(`/players/${playerId}`)
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

// 计算胜率
const calculateWinRate = (player) => {
  if (!player.total_win_loss_records || !player.total_win_loss_records.length) return '0'
  
  const record = player.total_win_loss_records[0]
  const wins = record.wins || 0
  const losses = record.losses || 0
  const total = wins + losses
  
  return total > 0 ? Math.round((wins / total) * 100) : 0
}

// 获取排名样式
const getRankClass = (rank) => {
  if (!rank) return ''
  if (rank <= 3) return 'top-3'
  if (rank <= 10) return 'top-10'
  if (rank <= 50) return 'top-50'
  return 'top-100'
}

// 同步数据
const syncData = async () => {
  showSyncDialog.value = false
  const loadingInstance = ElLoading.service({
    text: '正在同步数据...',
    background: 'rgba(10, 10, 15, 0.9)'
  })
  
  try {
    const response = await fetch('http://localhost:8000/api/sync/players', {
      method: 'POST'
    })
    
    if (response.ok) {
      ElMessage.success('数据同步完成')
      await fetchPlayers()
    } else {
      throw new Error('同步失败')
    }
  } catch (error) {
    console.error('同步数据失败:', error)
    ElMessage.error('数据同步失败，请稍后重试')
  } finally {
    loadingInstance.close()
  }
}

onMounted(() => {
  fetchPlayers()
})
</script>

<style scoped>
/* ===========================================
   页面头部样式
   =========================================== */

.page-header {
  padding: 2rem 0;
  text-align: center;
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
  text-align: left;
}

.title-section h1 {
  margin-bottom: 0.5rem;
}

.page-description {
  font-size: 1rem;
  color: var(--color-text-secondary);
}

/* ===========================================
   筛选面板样式
   =========================================== */

.filters-panel {
  max-width: 1400px;
  margin: 0 auto 2rem;
  padding: 1.5rem 2rem;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.search-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(0, 242, 254, 0.1);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  min-width: 300px;
}

.search-icon {
  font-size: 1.25rem;
  color: var(--color-neon-blue);
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--color-text-primary);
}

.search-input:focus {
  outline: none;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 120px;
}

.filter-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--color-border-secondary);
  border-radius: 6px;
  color: var(--color-text-primary);
  transition: var(--transition-fast);
}

.filter-select:hover {
  border-color: var(--color-neon-blue);
}

/* 种族选项样式 */
.race-option {
  font-weight: 600;
}

.race-option.protoss { color: #00f2fe; }
.race-option.terran { color: #8b00ff; }
.race-option.zerg { color: #00ffea; }
.race-option.random { color: #ff00c8; }

.region-flag {
  margin-right: 0.5rem;
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
   选手网格样式
   =========================================== */

.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}

.player-card {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr auto;
  grid-template-rows: auto 1fr;
  gap: 1rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: var(--transition-fast);
}

.player-card:hover {
  transform: translateY(-4px);
}

/* 排名徽章 */
.rank-badge {
  position: relative;
  grid-row: 1 / -1;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border-primary);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 242, 254, 0.1), transparent);
}

.rank-badge.top-3 {
  border-color: var(--color-neon-blue);
  box-shadow: 0 0 15px var(--color-neon-blue);
}

.rank-badge.top-10 {
  border-color: var(--color-neon-purple);
  box-shadow: 0 0 10px var(--color-neon-purple);
}

.rank-badge.top-50 {
  border-color: var(--color-warning);
  box-shadow: 0 0 8px var(--color-warning);
}

.rank-number {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 900;
  color: var(--color-neon-cyan);
}

/* 头像 */
.player-avatar {
  grid-column: 2;
  display: flex;
  align-items: center;
}

.avatar-bg {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 1.5rem;
  font-weight: bold;
  border: 2px solid;
  transition: var(--transition-fast);
}

.avatar-bg.race-P {
  background: rgba(0, 242, 254, 0.1);
  border-color: var(--color-neon-blue);
  color: var(--color-neon-blue);
}

.avatar-bg.race-T {
  background: rgba(139, 0, 255, 0.1);
  border-color: var(--color-neon-purple);
  color: var(--color-neon-purple);
}

.avatar-bg.race-Z {
  background: rgba(0, 255, 234, 0.1);
  border-color: var(--color-neon-cyan);
  color: var(--color-neon-cyan);
}

.avatar-bg.race-R {
  background: rgba(255, 0, 200, 0.1);
  border-color: var(--color-neon-pink);
  color: var(--color-neon-pink);
}

.player-card:hover .avatar-bg {
  transform: scale(1.1);
  box-shadow: 0 0 15px currentColor;
}

/* 信息区域 */
.player-info {
  grid-column: 2;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.player-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.player-alias {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin: 0;
}

.player-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.race-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.race-tag.race-P {
  background: rgba(0, 242, 254, 0.1);
  border: 1px solid var(--color-neon-blue);
  color: var(--color-neon-blue);
}

.race-tag.race-T {
  background: rgba(139, 0, 255, 0.1);
  border: 1px solid var(--color-neon-purple);
  color: var(--color-neon-purple);
}

.race-tag.race-Z {
  background: rgba(0, 255, 234, 0.1);
  border: 1px solid var(--color-neon-cyan);
  color: var(--color-neon-cyan);
}

.race-tag.race-R {
  background: rgba(255, 0, 200, 0.1);
  border: 1px solid var(--color-neon-pink);
  color: var(--color-neon-pink);
}

/* 统计数据 */
.player-stats {
  grid-column: 3;
  grid-row: 1 / -1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-end;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1rem;
}

.stat-value.rating {
  color: var(--color-neon-blue);
}

.stat-value.winrate {
  color: var(--color-success);
}

/* 装饰光效 */
.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at top right, rgba(0, 242, 254, 0.2), transparent);
  border-radius: 12px;
  opacity: 0;
  z-index: -1;
  pointer-events: none;
  transition: var(--transition-fast);
}

.player-card:hover .card-glow {
  opacity: 1;
}

/* ===========================================
   分页样式
   =========================================== */

.pagination-panel {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
}

.cyber-pagination {
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  padding: 0.5rem;
}

/* ===========================================
   对话框样式
   =========================================== */

.cyber-dialog {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 12px;
}

.sync-content {
  padding: 1rem;
}

.sync-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 170, 0, 0.1);
  border: 1px solid var(--color-warning);
  border-radius: 6px;
  color: var(--color-warning);
}

.dialog-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* ===========================================
   响应式设计
   =========================================== */

@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .title-section {
    text-align: center;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-group {
    min-width: auto;
  }
  
  .players-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .players-grid {
    grid-template-columns: 1fr;
    padding: 0 1rem;
  }
  
  .player-card {
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto auto;
  }
  
  .player-stats {
    grid-column: 1 / -1;
    grid-row: 3;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-border-secondary);
  }
  
  .stat-item {
    align-items: center;
  }
}
</style>
