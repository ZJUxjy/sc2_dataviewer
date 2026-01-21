<template>
  <div class="cyber-home">
    <!-- 扫描线效果 -->
    <div class="scanline"></div>
    
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="floating-particles">
          <div v-for="i in 20" :key="i" class="particle"></div>
        </div>
      </div>
      
      <div class="hero-content glass-card">
        <div class="hero-text">
          <h1 class="neon-text title">星际争霸2</h1>
          <h2 class="neon-text subtitle">职业选手数据终端</h2>
          <p class="hero-description">
            收录全球顶尖星际争霸2职业选手的生涯数据，包括对战历史、胜率统计、赛事记录等完整信息。
            实时同步Aligulac官方数据，提供最专业的电竞数据分析。
          </p>
          <div class="hero-actions">
            <button class="neon-button" @click="$router.push('/players')">
              <el-icon class="button-icon"><User /></el-icon>
              浏览选手
            </button>
            <button class="neon-button purple" @click="$router.push('/ranking')">
              <el-icon class="button-icon"><Trophy /></el-icon>
              查看排行
            </button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="hologram-display">
            <div class="display-frame">
              <div class="display-content">
                <svg viewBox="0 0 200 200" class="hero-logo">
                  <!-- Protoss 标志 -->
                  <polygon 
                    points="100,20 130,80 170,80 140,120 160,180 100,150 40,180 60,120 30,80 70,80"
                    fill="none"
                    stroke="var(--color-neon-blue)"
                    stroke-width="2"
                  />
                  <!-- 霓虹线条装饰 -->
                  <circle cx="100" cy="100" r="90" fill="none" stroke="var(--color-neon-purple)" stroke-width="1" opacity="0.5"/>
                  <circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-neon-cyan)" stroke-width="1" opacity="0.5"/>
                </svg>
              </div>
            </div>
            <div class="display-stats">
              <div class="stat-row">
                <span class="stat-label">ACTIVE PLAYERS</span>
                <span class="stat-value">301</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">MATCH RECORDS</span>
                <span class="stat-value">10K+</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">RANKING ACCURACY</span>
                <span class="stat-value">99.8%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 数据概览 -->
    <section class="stats-overview-section">
      <h2 class="section-title text-gradient">数据概览</h2>
      <p class="section-subtitle">实时更新的职业选手核心数据</p>
      
      <div class="stats-grid">
        <div class="stat-card glass-card" v-for="(stat, index) in statsCards" :key="index">
          <div class="stat-icon">
            <el-icon :size="48" :style="{ color: stat.color }">
              <component :is="stat.icon" />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">
              <span class="number">{{ stat.number }}</span>
              <span class="label">{{ stat.label }}</span>
            </div>
            <div class="stat-desc">
              {{ stat.description }}
            </div>
          </div>
          <div class="card-glow" :style="{ background: stat.glow }"></div>
        </div>
      </div>
    </section>
    
    <!-- 种族分布 -->
    <section class="race-distribution-section">
      <div class="section-header">
        <h2 class="section-title text-gradient">种族分布</h2>
        <p class="section-subtitle">TOP500 选手种族比例统计</p>
      </div>
      
      <div class="race-chart-container glass-card">
        <div class="chart-visual">
          <div class="race-item" v-for="race in raceData" :key="race.name">
            <div class="race-icon">
              <el-icon :size="32" :style="{ color: race.color }">
                <component :is="race.icon" />
              </el-icon>
            </div>
            <div class="race-info">
              <span class="race-name">{{ race.name }}</span>
              <span class="race-percentage">{{ race.percentage }}</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: race.percentage, background: race.gradient }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- TOP 选手展示 -->
    <section class="top-players-section">
      <div class="section-header">
        <h2 class="section-title text-gradient">TOP 10 选手</h2>
        <p class="section-subtitle">当前全球排名前十的星际争霸2职业选手</p>
      </div>
      
      <div class="players-grid">
        <div 
          class="player-card glass-card" 
          v-for="(player, index) in topPlayers" 
          :key="player.id"
          @click="goToPlayer(player.id)"
        >
          <div class="rank-badge">
            <span class="rank-number">#{{ index + 1 }}</span>
          </div>
          <div class="player-info">
            <h3 class="player-name">{{ player.name }}</h3>
            <p class="player-details">
              {{ player.race }} | {{ player.country }} | Rating: {{ player.rating }}
            </p>
          </div>
          <div class="player-glow" :style="{ background: player.glow }"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, 
  Trophy, 
  Operation, 
  Opportunity, 
  Histogram,
  Grid,
  Clock
} from '@element-plus/icons-vue'

const router = useRouter()

// 数据概览卡片
const statsCards = ref([])

// 种族数据
const raceData = [
  {
    name: '神族',
    percentage: '35.8%',
    icon: 'Grid',
    color: '#00f2fe',
    gradient: 'linear-gradient(90deg, #00f2fe, #00ffea)'
  },
  {
    name: '人族',
    percentage: '31.5%',
    icon: 'Operation',
    color: '#8b00ff',
    gradient: 'linear-gradient(90deg, #8b00ff, #ff00c8)'
  },
  {
    name: '虫族',
    percentage: '31.8%',
    icon: 'Opportunity',
    color: '#00ffea',
    gradient: 'linear-gradient(90deg, #00ffea, #00ff9d)'
  }
]

// TOP 10 选手
const topPlayers = ref([])

// 跳转到选手详情
const goToPlayer = (playerId) => {
  router.push(`/players/${playerId}`)
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/stats/summary')
    const data = await response.json()
    
    statsCards.value = [
      {
        icon: 'User',
        number: data.players_count || 301,
        label: '职业选手',
        description: '来自全球的顶级选手',
        color: '#00f2fe',
        glow: 'radial-gradient(circle at center, rgba(0, 242, 254, 0.3), transparent)'
      },
      {
        icon: 'Trophy',
        number: data.matches_count || '10K+',
        label: '比赛记录',
        description: '完整的对战历史',
        color: '#8b00ff',
        glow: 'radial-gradient(circle at center, rgba(139, 0, 255, 0.3), transparent)'
      },
      {
        icon: 'Histogram',
        number: data.races?.length || 3,
        label: '游戏种族',
        description: '神族/人族/虫族',
        color: '#00ffea',
        glow: 'radial-gradient(circle at center, rgba(0, 255, 234, 0.3), transparent)'
      },
      {
        icon: 'Grid',
        number: data.countries?.length || 15,
        label: '国家地区',
        description: '覆盖全球主要赛区',
        color: '#ff00c8',
        glow: 'radial-gradient(circle at center, rgba(255, 0, 200, 0.3), transparent)'
      }
    ]
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取TOP选手
const fetchTopPlayers = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/players/top10')
    const data = await response.json()
    
    topPlayers.value = data.map((player, index) => {
      const colors = [
        { bg: 'rgba(0, 242, 254, 0.3)', border: '#00f2fe' },
        { bg: 'rgba(139, 0, 255, 0.3)', border: '#8b00ff' },
        { bg: 'rgba(0, 255, 234, 0.3)', border: '#00ffea' },
        { bg: 'rgba(255, 0, 200, 0.3)', border: '#ff00c8' }
      ]
      const color = colors[index % colors.length]
      
      return {
        ...player,
        glow: `linear-gradient(135deg, ${color.bg}, transparent)`
      }
    })
  } catch (error) {
    console.error('获取TOP选手失败:', error)
  }
}

onMounted(() => {
  fetchStats()
  fetchTopPlayers()
  
  // 定时更新数据
  setInterval(() => {
    fetchStats()
  }, 30000)
})
</script>

<style scoped>
/* ===========================================
   英雄区域样式
   =========================================== */

.hero-section {
  position: relative;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.floating-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: var(--color-neon-blue);
  border-radius: 50%;
  opacity: 0.5;
  animation: float 6s ease-in-out infinite;
}

.particle:nth-child(odd) {
  background: var(--color-neon-purple);
  animation-delay: -3s;
}

.particle:nth-child(3n) {
  background: var(--color-neon-cyan);
  animation-delay: -2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
  50% { transform: translateY(-100px) translateX(20px); opacity: 1; }
}

.hero-content {
  max-width: 1400px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-text h1 {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.hero-text h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.hero-description {
  font-size: 1.125rem;
  line-height: 1.8;
  color: var(--color-text-secondary);
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.button-icon {
  margin-right: 0.5rem;
}

/* 视觉展示区域 */
.hero-visual {
  display: flex;
  justify-content: center;
}

.hologram-display {
  position: relative;
  width: 400px;
  height: 400px;
}

.display-frame {
  width: 100%;
  height: 100%;
  border: 2px solid var(--color-neon-blue);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 242, 254, 0.1), transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: hologram 4s ease-in-out infinite;
}

.display-content {
  width: 80%;
  height: 80%;
  border: 1px solid var(--color-neon-blue);
  border-radius: 50%;
  padding: 2rem;
}

.hero-logo {
  width: 100%;
  height: 100%;
}

.display-stats {
  position: absolute;
  bottom: -60px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 2rem;
  background: var(--color-bg-glass);
  padding: 1rem 2rem;
  border-radius: 8px;
  border: 1px solid var(--color-border-primary);
}

.stat-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  font-family: var(--font-display);
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-neon-cyan);
}

/* ===========================================
   数据概览样式
   =========================================== */

.stats-overview-section {
  padding: 4rem 2rem;
  text-align: center;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

.stat-icon {
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 8px currentColor);
}

.stat-number {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.stat-number .number {
  font-size: 3rem;
  font-weight: 900;
  font-family: var(--font-display);
  color: var(--color-neon-cyan);
  margin-bottom: 0.5rem;
}

.stat-number .label {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.stat-desc {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  opacity: 0.3;
  z-index: -1;
  pointer-events: none;
}

/* ===========================================
   种族分布样式
   =========================================== */

.race-distribution-section {
  padding: 4rem 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.race-chart-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem;
}

.chart-visual {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.race-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;
}

.race-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
}

.race-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 120px;
}

.race-name {
  font-weight: 600;
  font-size: 1rem;
}

.race-percentage {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--color-neon-cyan);
  font-size: 1.125rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width var(--transition-slow);
  box-shadow: 0 0 10px currentColor;
}

/* ===========================================
   TOP 选手样式
   =========================================== */

.top-players-section {
  padding: 4rem 2rem;
  background: linear-gradient(180deg, transparent, rgba(139, 0, 255, 0.05));
}

.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.player-card {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: var(--transition-fast);
}

.player-card:hover {
  transform: translateY(-4px);
}

.rank-badge {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-neon-blue);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 242, 254, 0.1), transparent);
}

.rank-number {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 900;
  color: var(--color-neon-cyan);
}

.player-info h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.player-details {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  font-family: var(--font-display);
  letter-spacing: 0.5px;
}

.player-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  opacity: 0.2;
  z-index: -1;
  pointer-events: none;
}

/* ===========================================
   响应式设计
   =========================================== */

@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }
  
  .hero-text h1 {
    font-size: 3rem;
  }
  
  .hero-text h2 {
    font-size: 1.5rem;
  }
  
  .hologram-display {
    width: 300px;
    height: 300px;
  }
  
  .display-stats {
    flex-direction: column;
    gap: 1rem;
    bottom: -120px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: auto;
    padding: 2rem 1rem;
  }
  
  .hero-text h1 {
    font-size: 2.5rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .stats-overview-section,
  .race-distribution-section,
  .top-players-section {
    padding: 2rem 1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .players-grid {
    grid-template-columns: 1fr;
  }
  
  .race-item {
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    gap: 0.5rem;
  }
  
  .progress-bar {
    grid-column: 1 / -1;
  }
}
</style>
