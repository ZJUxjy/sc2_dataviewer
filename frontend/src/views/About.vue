<template>
  <div class="about">
    <el-card class="about-card">
      <template #header>
        <h2>关于 SC2 Pro Stats</h2>
      </template>
      
      <div class="about-content">
        <el-row :gutter="40">
          <el-col :span="16" :xs="24">
            <h3>项目介绍</h3>
            <p>
              SC2 Pro Stats 是一个专注于收录和展示星际争霸2职业选手生涯数据的Web应用。
              通过整合Aligulac API提供的权威数据，我们为电竞爱好者提供最全面、最准确的职业选手数据分析。
            </p>
            
            <h3>功能特性</h3>
            <ul>
              <li>📊 选手生涯数据统计分析</li>
              <li>🏆 完整的对战历史记录查询</li>
              <li>📈 胜率趋势和数据可视化</li>
              <li>🎯 种族对战专项分析</li>
              <li>🔍 智能搜索和筛选功能</li>
              <li>⭐ 选手关注和收藏功能</li>
              <li>📱 响应式设计，支持移动端</li>
            </ul>
            
            <h3>数据来源</h3>
            <p>
              所有数据均来自
              <el-link
                href="http://aligulac.com"
                target="_blank"
                type="primary"
              >
                Aligulac
              </el-link>
              ，这是目前最权威的星际争霸2电竞数据统计网站，拥有超过37万场比赛记录和2万名职业选手的完整数据。
            </p>
            
            <h3>技术架构</h3>
            <el-row :gutter="20">
              <el-col :span="12">
                <h4>后端</h4>
                <ul>
                  <li>FastAPI - 高性能Web框架</li>
                  <li>SQLAlchemy - ORM框架</li>
                  <li>SQLite - 轻量级数据库</li>
                  <li>APScheduler - 定时同步</li>
                </ul>
              </el-col>
              <el-col :span="12">
                <h4>前端</h4>
                <ul>
                  <li>Vue.js 3 - 渐进式框架</li>
                  <li>Element Plus - UI组件库</li>
                  <li>Chart.js - 数据可视化</li>
                  <li>Axios - HTTP客户端</li>
                </ul>
              </el-col>
            </el-row>
          </el-col>
          
          <el-col :span="8" :xs="24">
            <div class="quick-links">
              <h3>快速链接</h3>
              <el-menu>
                <el-menu-item @click="$router.push('/players')">
                  <el-icon><user /></el-icon>
                  选手列表
                </el-menu-item>
                <el-menu-item @click="$router.push('/ranking')">
                  <el-icon><trophy /></el-icon>
                  排行榜
                </el-menu-item>
                <el-menu-item @click="$router.push('/events')">
                  <el-icon><calendar /></el-icon>
                  赛事列表
                </el-menu-item>
              </el-menu>
              
              <div class="external-links">
                <h4>相关资源</h4>
                <el-link
                  href="http://aligulac.com"
                  target="_blank"
                  class="link-item"
                >
                  Aligulac 官网
                </el-link>
                <el-link
                  href="https://starcraft2.com"
                  target="_blank"
                  class="link-item"
                >
                  星际争霸2 官网
                </el-link>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 关于页面
</script>

<style scoped>
.about {
  max-width: 1200px;
  margin: 0 auto;
}

.about-content h3 {
  margin: 24px 0 16px;
  color: #303133;
  font-size: 20px;
}

.about-content p {
  line-height: 1.8;
  color: #606266;
  margin-bottom: 16px;
}

.about-content ul {
  list-style: none;
  padding: 0;
}

.about-content li {
  padding: 8px 0;
  color: #606266;
}

.about-content li:before {
  content: "•";
  color: #409eff;
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}

.quick-links {
  margin-top: 0;
}

.link-item {
  display: block;
  margin: 12px 0;
}

.external-links {
  margin-top: 24px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.external-links h4 {
  margin-bottom: 12px;
  color: #303133;
}
</style>
