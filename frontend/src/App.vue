<template>
  <div id="app">
    <!-- 赛博朋克网格背景 -->
    <div class="cyborg-grid"></div>
    
    <!-- 扫描线效果 -->
    <div class="scanline"></div>
    
    <el-config-provider :locale="locale">
      <!-- 玻璃拟态头部 -->
      <header class="cyber-header glass-panel">
        <div class="header-content">
          <!-- Logo 区域 -->
          <div class="logo-section">
            <div class="logo-icon">
              <svg viewBox="0 0 100 100" class="trophy-icon">
                <path d="M50 15 L60 5 L40 5 Z" fill="var(--color-neon-cyan)"/>
                <rect x="30" y="10" width="40" height="30" rx="5" fill="var(--color-neon-blue)"/>
                <circle cx="50" cy="25" r="10" fill="var(--color-bg-primary)"/>
                <path d="M30 40 L20 70 L80 70 L70 40" fill="var(--color-neon-purple)"/>
              </svg>
            </div>
            <div class="logo-text">
              <h1 class="neon-text subtitle">SC2 Pro Stats</h1>
              <p class="logo-subtitle">Koprulu Sector Data Terminal</p>
            </div>
          </div>
          
          <!-- 导航菜单 -->
          <nav class="cyber-nav">
            <router-link 
              v-for="item in navItems" 
              :key="item.path"
              :to="item.path"
              class="nav-link"
              :class="{ active: route.path === item.path }"
            >
              <el-icon class="nav-icon">
                <component :is="item.icon" />
              </el-icon>
              <span>{{ item.label }}</span>
            </router-link>
          </nav>
          
          <!-- 状态指示器 -->
          <div class="status-indicators">
            <div class="status-dot active" title="数据同步正常">
              <span class="dot"></span>
              <span class="pulse"></span>
            </div>
            <div class="time-display">
              {{ currentTime }}
            </div>
          </div>
        </div>
      </header>
      
      <!-- 主内容区域 -->
      <main class="main-container">
        <router-view v-slot="{ Component }">
          <transition name="cyber-transition" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
      
      <!-- 底部信息 -->
      <footer class="cyber-footer">
        <div class="footer-content">
          <div class="footer-text">
            <p>&copy; 2025 SC2 Pro Stats | Koprulu Sector Intelligence</p>
          </div>
          <div class="footer-stats">
            <span class="stat-item">
              <el-icon><Operation /></el-icon>
              数据同步正常
            </span>
            <span class="stat-item">
              <el-icon><Clock /></el-icon>
              实时更新
            </span>
          </div>
        </div>
      </footer>
    </el-config-provider>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { 
  Trophy, 
  House, 
  User, 
  Medal, 
  Calendar,
  Operation,
  Clock
} from '@element-plus/icons-vue'

const route = useRoute()
const locale = ref(zhCn)
const currentTime = ref('')

// 导航项配置
const navItems = [
  { path: '/', icon: 'House', label: '首页' },
  { path: '/players', icon: 'User', label: '选手列表' },
  { path: '/ranking', icon: 'Medal', label: '排行榜' },
  { path: '/events', icon: 'Calendar', label: '赛事' }
]

// 时间更新
let timeInterval
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
})
</script>

<style scoped>
/* 头部样式 */
.cyber-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  border-radius: 0 0 20px 20px;
  border-top: none;
  border-left: none;
  border-right: none;
  border-bottom: 1px solid var(--color-border-primary);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo 区域 */
.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  position: relative;
}

.trophy-icon {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 8px var(--color-neon-cyan));
  animation: hologram 4s ease-in-out infinite;
}

.logo-text h1 {
  font-size: 1.5rem;
  margin: 0;
}

.logo-subtitle {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  font-family: var(--font-display);
  letter-spacing: 1px;
}

/* 导航样式 */
.cyber-nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  color: var(--color-text-secondary);
  text-decoration: none;
  border: 1px solid transparent;
  border-radius: 8px;
  transition: var(--transition-fast);
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, var(--color-neon-blue), transparent);
  transition: left 0.5s;
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link:hover {
  color: var(--color-neon-blue);
  border-color: var(--color-border-primary);
  transform: translateY(-2px);
}

.nav-link.active {
  color: var(--color-neon-cyan);
  background: rgba(0, 242, 254, 0.1);
  border-color: var(--color-neon-cyan);
  box-shadow: var(--shadow-neon);
}

.nav-icon {
  font-size: 1.25rem;
}

/* 状态指示器 */
.status-indicators {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.status-dot {
  position: relative;
  width: 24px;
  height: 24px;
}

.status-dot .dot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: var(--color-success);
  border-radius: 50%;
  z-index: 2;
}

.status-dot .pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border: 2px solid var(--color-success);
  border-radius: 50%;
  animation: pulse-glow 2s infinite;
}

.time-display {
  font-family: var(--font-display);
  font-size: 0.875rem;
  color: var(--color-neon-cyan);
  background: rgba(0, 255, 234, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid var(--color-border-primary);
}

/* 主内容区域 */
.main-container {
  margin-top: 80px;
  min-height: calc(100vh - 160px);
  padding: 2rem;
}

/* 底部样式 */
.cyber-footer {
  background: var(--color-bg-secondary);
  border-top: 1px solid var(--color-border-primary);
  padding: 1.5rem 0;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.footer-stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

/* 路由过渡动画 */
.cyber-transition-enter-active,
.cyber-transition-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cyber-transition-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.cyber-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .header-content {
    padding: 0 1rem;
  }
  
  .logo-text h1 {
    font-size: 1.25rem;
  }
  
  .nav-link {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 1rem;
    gap: 1rem;
  }
  
  .cyber-nav {
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.5rem;
  }
  
  .nav-link span {
    display: none;
  }
  
  .main-container {
    margin-top: 140px;
    padding: 1rem;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
