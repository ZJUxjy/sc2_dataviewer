# SC2 Pro Stats 完整使用指南

## 项目概述

这是一个完整的星际争霸2职业选手生涯数据查看工具，包含后台数据同步服务和前端Web界面。

## 功能特点

✅ **已完成功能**:
- 选手列表浏览和搜索
- 选手详情页面（生涯统计、对战历史）
- 排行榜功能
- 赛事展示
- 对战记录查询
- 响应式UI设计

🔄 **待完善功能**:
- 数据可视化图表（胜率趋势等）
- 性能优化
- 数据自动定时同步

## 项目结构

```
sc2-prostats/
├── backend/                # 后端代码
│   ├── main.py            # FastAPI主应用
│   ├── requirements.txt   # Python依赖
│   ├── .env.example       # 环境变量示例
│   ├── models/            # 数据库模型
│   ├── services/          # 业务逻辑
│   └── schemas.py         # Pydantic模型
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 公共组件
│   │   ├── services/      # API服务
│   │   ├── router/        # 路由配置
│   │   └── App.vue        # 主组件
│   ├── package.json       # 前端依赖
│   └── vite.config.js     # Vite配置
└── database/              # 数据库文件
    └── sc2_stats.db       # SQLite数据库文件
```

## 安装和运行

### 前端环境要求
- Node.js >= 16
- npm 或 yarn

### 后端环境要求
- Python >= 3.8
- pip

### 第一步：配置环境

1. 复制环境变量文件：
```bash
cd sc2-prostats/backend
cp .env.example .env
```

2. 编辑 `.env` 文件，填写您的 Aligulac API Key：
```env
ALIGULAC_API_KEY=your-api-key-here
```

**如何获取Aligulac API Key：**
- 访问 http://aligulac.com/about/api/
- 点击生成API密钥按钮
- 填写姓名和邮箱
- 复制生成的20位密钥

### 第二步：运行后端

```bash
cd sc2-prostats/backend

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

后端服务将在 `http://localhost:8000` 启动

API文档：`http://localhost:8000/docs`

### 第三步：运行前端

```bash
cd sc2-prostats/frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev
```

前端应用将在 `http://localhost:5173` 启动

### 第四步：首次数据同步

推荐首先同步TOP500职业选手数据：

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python sync_data.py players    # 同步TOP500选手（按Aligulac评分排名）⭐
```

或使用前端界面同步：
1. 启动前端服务并访问 http://localhost:5173
2. 进入"选手列表"页面
3. 点击"同步数据"按钮
4. 选择"同步TOP500职业选手"
5. 等待同步完成（约5-10分钟）

**注意**：首次同步会下载大量数据，请耐心等待

更多同步选项：
```bash
# 同步所有数据（TOP500选手、战队、赛事）
python sync_data.py

# 仅同步最近比赛（30天）
python sync_data.py matches

# 查看帮助
python sync_data.py --help
```

## 主要API端点

### 选手相关
- `GET /api/players` - 获取选手列表
- `GET /api/players/{id}` - 获取选手详情
- `GET /api/players/{id}/matches` - 获取选手比赛记录
- `GET /api/players/{id}/stats` - 获取选手统计数据

### 排行榜
- `GET /api/ranking` - 获取排行榜

### 数据同步
- `POST /api/sync/players` - 同步选手数据
- `POST /api/sync/matches` - 同步比赛数据

## 数据库结构

主要数据表：
- `players` - 选手信息
- `matches` - 比赛记录
- `teams` - 战队信息
- `events` - 赛事信息
- `player_stats` - 选手统计数据

## 性能优化建议

1. **添加索引**：
```sql
CREATE INDEX idx_players_rating ON players(total_wins + total_losses DESC);
CREATE INDEX idx_matches_date ON matches(date DESC);
```

2. **数据分页**：使用cursor-based pagination优化大数据量查询

3. **缓存机制**：使用Redis缓存热门选手数据

4. **异步处理**：数据同步使用Celery等任务队列

## 常见问题和解决方案

### 问题：API请求失败
**原因**：API Key无效或请求频率过高
**解决**：检查`.env`中的API Key，确保格式正确

### 问题：数据库锁定
**原因**：SQLite并发限制
**解决**：考虑切换到PostgreSQL

### 问题：前端无法连接后端
**原因**：跨域问题
**解决**：检查后端CORS配置

### 问题：同步数据缓慢
**原因**：Aligulac API限速
**解决**：在`syn_service.py`中调整同步批次大小

## 扩展开发

### 添加数据可视化

使用Chart.js添加胜率趋势图：

```javascript
// 在PlayerDetail.vue中添加
import { Line } from 'vue-chartjs'
```

### 添加用户认证

使用JWT实现用户注册和登录功能

### 添加实时数据

使用WebSocket实现比赛实时更新

## 技术栈详情

### 后端
- **FastAPI**: 现代、高性能的Web框架
- **SQLAlchemy**: Python SQL工具包和ORM
- **Pydantic**: 数据验证和设置管理
- **APScheduler**: 轻量级调度库

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **Element Plus**: Vue 3组件库
- **Vue Router**: 官方路由管理器
- **Pinia**: Vue状态管理
- **Axios**: 基于Promise的HTTP客户端

## 许可证

MIT License

## 贡献指南

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过GitHub Issues联系。

---

**最后更新**: 2024-01-19
