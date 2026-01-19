<template>
  <el-config-provider :locale="locale">
    <div id="app">
      <el-container>
        <el-header class="header">
          <div class="logo">
            <el-icon class="logo-icon"><trophy /></el-icon>
            <h1>SC2 Pro Stats</h1>
          </div>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            router
            background-color="#001529"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/players">选手列表</el-menu-item>
            <el-menu-item index="/ranking">排行榜</el-menu-item>
            <el-menu-item index="/events">赛事</el-menu-item>
          </el-menu>
        </el-header>
        
        <el-main class="main-content">
          <router-view />
        </el-main>
        
        <el-footer class="footer">
          <p>&copy; 2024 SC2 Pro Stats | 星际争霸2职业选手数据</p>
        </el-footer>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const route = useRoute()
const locale = ref(zhCn)

const activeMenu = computed(() => {
  return route.path
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.header {
  background-color: #001529;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 50px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  margin-right: 50px;
}

.logo-icon {
  font-size: 32px;
  margin-right: 12px;
  color: #ffd04b;
}

.logo h1 {
  font-size: 24px;
  font-weight: 600;
  color: white;
}

.el-menu {
  flex: 1;
  border-bottom: none;
}

.main-content {
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.footer {
  background-color: #001529;
  color: #909399;
  text-align: center;
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    padding: 0 20px;
    flex-direction: column;
    height: auto !important;
    padding: 10px 20px;
  }
  
  .logo {
    margin-right: 0;
    margin-bottom: 10px;
  }
  
  .el-menu {
    width: 100%;
  }
  
  .main-content {
    padding: 10px;
  }
}
</style>
