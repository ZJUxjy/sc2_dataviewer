<template>
  <div class="neon-terminal">
    <!-- 返回按钮 -->
    <div class="nav-bar">
      <button class="control-btn" @click="$router.back()">
        <svg viewBox="0 0 24 24" width="16" height="16">
          <path d="M19 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H19v-2z" fill="currentColor"/>
        </svg>
        TERMINAL
      </button>
      
      <div class="system-status">
        <div class="status-dot active"></div>
        <span>KOPRULU ONLINE</span>
      </div>
    </div>

    <div v-if="player" class="terminal-grid">
      <!-- 头部信息 -->
      <header class="player-header">
        <div class="header-bg">
          <div class="portrait-container">
            <div class="portrait-frame">
              <div class="portrait-image" :class="player.race.toLowerCase()">
                <span class="race-letter">{{ player.race }}</span>
              </div>
              <div class="frame-glow"></div>
            </div>
            
            <div class="player-identifiers">
              <h1 class="player-tag">{{ player.tag }}</h1>
              <p v-if="player.name !== player.tag" class="player-name">{{ player.name }}</p>
              <div class="identity-chips">
                <span class="chip race-chip" :class="player.race.toLowerCase()">
                  {{ getRaceName(player.race) }}
                </span>
                <span class="chip country-chip">
                  {{ getCountryName(player.country) }}
                </span>
              </div>
            </div>
          </div>

          <div class="rank-display">
            <div class="rank-title">GLOBAL RANK</div>
            <div class="rank-number">#{{ player.current_rating_rank || '---' }}</div>
            <div class="rank-bar">
              <div class="rank-fill"></div>
            </div>
          </div>
        </div>
      </header>

      <!-- 核心数据面板 -->
      <section class="stats-panel">
        <div class="panel-card">
          <h3 class="panel-title">CAREER STATS</h3>
          
          <div class="stat-row">
            <div class="stat-cell">
              <div class="value earnings">${{ formatEarnings(player.total_earnings) }}</div>
              <div class="label">EARNINGS</div>
            </div>
            <div class="stat-cell">
              <div class="value games">{{ player.total_games }}</div>
              <div class="label">GAMES</div>
            </div>
          </div>

          <div class="stat-row">
            <div class="stat-cell">
              <div class="value wins">{{ player.total_wins }}</div>
              <div class="label">WINS</div>
            </div>
            <div class="stat-cell">
              <div 
                class="value winrate"
                :class="{ 
                  high: player.win_rate >= 60, 
                  medium: player.win_rate >= 50 && player.win_rate < 60,
                  low: player.win_rate < 50 
                }"
              >
                {{ formatWinRate(player.win_rate) }}%
              </div>
              <div class="label">WINRATE</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 对战历史 -->
      <section class="matches-terminal">
        <div class="terminal-header">
          <h2 class="section-title">MATCH HISTORY</h2>
          <div class="terminal-controls">
            <button 
              class="control-btn" 
              :class="{ active: viewMode === 'all' }"
              @click="viewMode = 'all'; loadMatches()"
            >
              ALL
            </button>
            <button 
              class="control-btn" 
              :class="{ active: viewMode === 'recent' }"
              @click="viewMode = 'recent'; loadMatches()"
            >
              RECENT
            </button>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loadingMatches" class="loading-match-grid">
          <div class="loading-card" v-for="i in 6" :key="i">
            <div class="loading-bar"></div>
            <div class="loading-bar"></div>
            <div class="loading-bar"></div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="matches.length === 0" class="empty-terminal">
          <div class="empty-icon">⚠</div>
          <h3>NO MATCH DATA</h3>
          <p>Match records not available for this player</p>
        </div>

        <!-- 对战列表 -->
        <div v-else class="match-grid">
          <article 
            v-for="match in matches" 
            :key="match.id || match.aligulac_id"
            class="match-card"
            :class="getMatchOutcome(match)"
          >
            <div class="match-meta">
              <div class="date-time">{{ formatMatchDate(match.date) }}</div>
              <div class="event-name">{{ match.event?.full_name || match.event?.name || 'Event' }}</div>
            </div>

            <div class="vs-section">
              <div class="vs-line">
                <span class="vs-text">VS</span>
              </div>
              <div class="opponent-info">
                <div class="opponent-race" :class="getOpponentRace(match).toLowerCase()">
                  {{ getRaceSymbol(getOpponentRace(match)) }}
                </div>
                <span class="opponent-name">{{ getOpponentName(match) }}</span>
              </div>
            </div>

            <div class="score-section">
              <div class="score-display" :class="getMatchOutcome(match)">
                <span class="match-score">{{ match.player1_score }}-{{ match.player2_score }}</span>
              </div>
              <div class="outcome-badge" :class="getMatchOutcome(match)">
                {{ getMatchOutcome(match) }}
              </div>
            </div>

            <div class="match-bar">
              <div 
                class="fill-bar"
                :style="{ width: getMatchBarWidth(match) }"
              ></div>
            </div>
          </article>
        </div>

        <!-- 统计摘要 -->
        <div v-if="matches.length > 0" class="terminal-stats">
          <div class="stat-chip">
            <span class="stat-label">TOTAL</span>
            <span class="stat-number">{{ matches.length }}</span>
          </div>
          <div class="stat-chip win">
            <span class="stat-label">WINS</span>
            <span class="stat-number">{{ matches.filter(m => isPlayerWin(m)).length }}</span>
          </div>
          <div class="stat-chip loss">
            <span class="stat-label">LOSSES</span>
            <span class="stat-number">{{ matches.filter(m => !isPlayerWin(m)).length }}</span>
          </div>
        </div>
      </section>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="loading" class="loading-screen">
      <div class="loading-artifacts">
        <div class="artifact" style="--delay: 0s;"></div>
        <div class="artifact" style="--delay: 0.2s;"></div>
        <div class="artifact" style="--delay: 0.4s;"></div>
      </div>
      <div class="loading-text">INITIALIZING TERMINAL...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(true)
const loadingMatches = ref(false)
const player = ref(null)
const matches = ref([])
const viewMode = ref('all')

// 计算属性
const winRateDegree = computed(() => {
  const rate = Number(player.value?.win_rate || 0)
  return (rate / 100) * 360
})

// 获取选手详情
const loadPlayerDetail = async () => {
  try {
    const playerId = Number(route.params.id)
    const response = await fetch(`http://localhost:8000/api/players/${playerId}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    
    player.value = await response.json()
    await loadMatches()
  } catch (err) {
    console.error('Failed to load player:', err)
  } finally {
    loading.value = false
  }
}

// 获取对战历史
const loadMatches = async () => {
  if (!player.value) return
  
  loadingMatches.value = true
  try {
    const playerId = Number(route.params.id)
    const limit = viewMode.value === 'recent' ? 50 : 200
    
    const response = await fetch(`http://localhost:8000/api/players/${playerId}/matches?limit=${limit}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    
    const data = await response.json()
    matches.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Failed to load matches:', err)
    matches.value = []
  } finally {
    loadingMatches.value = false
  }
}

// 获取种族符号
const getRaceSymbol = (race) => {
  const symbols = { P: 'P', T: 'T', Z: 'Z', R: 'R' }
  return symbols[race] || '?'
}

// 获取种族名称
const getRaceName = (race) => {
  const names = { P: 'Protoss', T: 'Terran', Z: 'Zerg', R: 'Random' }
  return names[race] || 'Unknown'
}

// 获取国家名称
const getCountryName = (code) => {
  const countries = {
    KR: 'Korea', CN: 'China', US: 'USA', EU: 'EU',
    DK: 'Denmark', FR: 'France', IT: 'Italy', RU: 'Russia',
    PL: 'Poland', JP: 'Japan', CA: 'Canada', UK: 'UK',
    TW: 'Taiwan', UA: 'Ukraine', DE: 'Germany', FI: 'Finland'
  }
  return countries[code] || 'Unknown'
}

// 格式化奖金
const formatEarnings = (earnings) => {
  if (!earnings || earnings === 0) return '0'
  return earnings.toLocaleString()
}

// 格式化胜率
const formatWinRate = (rate) => {
  if (!rate) return 0
  return Number(rate).toFixed(1)
}

// 格式化日期
const formatMatchDate = (dateString) => {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: '2-digit'
    })
  } catch {
    return dateString
  }
}

// 获取对手信息
const getOpponentName = (match) => {
  const playerId = Number(route.params.id)
  return (match.player1_id === playerId ? match.player2_tag : match.player1_tag) || 'Unknown'
}

const getOpponentRace = (match) => {
  const playerId = Number(route.params.id)
  return match.player1_id === playerId ? match.player2_race : match.player1_race
}

// 判断比赛结果
const isPlayerWin = (match) => {
  const playerId = Number(route.params.id)
  const winnerId = Number(match.winner_id)
  return playerId === winnerId
}

const getMatchOutcome = (match) => {
  return isPlayerWin(match) ? 'win' : 'loss'
}

const getMatchBarWidth = (match) => {
  return isPlayerWin(match) ? '100%' : '0%'
}

// 组件挂载后加载数据
onMounted(() => {
  loadPlayerDetail()
})
</script>

<style scoped>
.neon-terminal {
  min-height: 100vh;
  background: #0a0a0f;
  color: #e0e0ff;
  font-family: 'Courier New', monospace;
  padding: 0;
  position: relative;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 2px solid #00f2fe;
  background: rgba(20, 20, 35, 0.8);
  backdrop-filter: blur(10px);
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: 2px solid #00f2fe;
  color: #00f2fe;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 1px;
}

.control-btn:hover {
  background: #00f2fe;
  color: #0a0a0f;
  box-shadow: 0 0 20px #00f2fe;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a0a0c0;
  font-size: 0.875rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff0044;
  animation: pulse 2s infinite;
}

.status-dot.active {
  background: #00ffea;
}

.terminal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.player-header {
  grid-column: 1 / -1;
}

.header-bg {
  background: linear-gradient(135deg, rgba(0, 242, 254, 0.05), rgba(139, 0, 255, 0.05));
  border: 2px solid #00f2fe;
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(5px);
}

.portrait-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  position: relative;
  z-index: 2;
}

.portrait-frame {
  position: relative;
  width: 120px;
  height: 120px;
}

.portrait-image {
  width: 100%;
  height: 100%;
  border: 3px solid;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 900;
  transition: all 0.3s ease;
}

.portrait-image.protoss {
  border-color: #00f2fe;
  color: #00f2fe;
  text-shadow: 0 0 20px #00f2fe;
  background: radial-gradient(circle, rgba(0, 242, 254, 0.1), transparent);
}

.portrait-image.terran {
  border-color: #8b00ff;
  color: #8b00ff;
  text-shadow: 0 0 20px #8b00ff;
  background: radial-gradient(circle, rgba(139, 0, 255, 0.1), transparent);
}

.portrait-image.zerg {
  border-color: #00ffea;
  color: #00ffea;
  text-shadow: 0 0 20px #00ffea;
  background: radial-gradient(circle, rgba(0, 255, 234, 0.1), transparent);
}

.player-identifiers {
  flex: 1;
}

.player-tag {
  font-size: 2.5rem;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.player-name {
  font-size: 1.25rem;
  color: #a0a0c0;
  margin: 0.5rem 0;
  font-style: italic;
}

.identity-chips {
  display: flex;
  gap: 1rem;
}

.chip {
  padding: 0.5rem 1rem;
  border: 2px solid;
  border-radius: 6px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 1px;
}

.rank-display {
  text-align: right;
  padding: 1rem;
  min-width: 200px;
}

.rank-title {
  font-size: 0.875rem;
  color: #a0a0c0;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.rank-number {
  font-size: 3rem;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  color: #00ffea;
  text-shadow: 0 0 20px #00ffea;
}

.panel-card {
  background: rgba(20, 20, 35, 0.6);
  border: 2px solid #8b00ff;
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(5px);
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #8b00ff;
  margin-bottom: 2rem;
  text-shadow: 0 0 10px #8b00ff;
}

.stat-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.stat-cell {
  text-align: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(139, 0, 255, 0.3);
  border-radius: 8px;
}

.value {
  font-size: 2rem;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  display: block;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px currentColor;
}

.matches-terminal {
  background: rgba(20, 20, 35, 0.6);
  border: 2px solid #00f2fe;
  border-radius: 12px;
  backdrop-filter: blur(5px);
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(0, 242, 254, 0.2);
}

.match-grid {
  padding: 1rem;
  max-height: 600px;
  overflow-y: auto;
}

.match-card {
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.match-card.win {
  border-color: #00ff9d;
  background: rgba(0, 255, 157, 0.05);
}

.match-card.loss {
  border-color: #ff0044;
  background: rgba(255, 0, 68, 0.05);
}

.match-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.event-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.score-display {
  font-family: 'Orbitron', monospace;
  font-weight: 900;
  font-size: 1.5rem;
  padding: 0.5rem 1rem;
  border: 2px solid;
  border-radius: 6px;
}

.score-display.win {
  border-color: #00ff9d;
  color: #00ff9d;
}

.score-display.loss {
  border-color: #ff0044;
  color: #ff0044;
}

.outcome-badge {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
}

.match-card.win .outcome-badge {
  background: rgba(0, 255, 157, 0.2);
  color: #00ff9d;
  border: 1px solid #00ff9d;
}

.match-card.loss .outcome-badge {
  background: rgba(255, 0, 68, 0.2);
  color: #ff0044;
  border: 1px solid #ff0044;
}

.terminal-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(0, 242, 254, 0.2);
  background: rgba(0, 0, 0, 0.3);
}

.stat-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 1rem;
  border: 2px solid;
  border-radius: 8px;
}

.stat-chip.win {
  border-color: #00ff9d;
}

.stat-chip.loss {
  border-color: #ff0044;
}
</style>