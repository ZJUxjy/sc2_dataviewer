# SC2 Pro Stats - 安装配置指南

## 📋 目录

1. [环境要求](#环境要求)
2. [快速安装](#快速安装)
3. [详细安装步骤](#详细安装步骤)
4. [配置说明](#配置说明)
5. [验证安装](#验证安装)
6. [常见问题](#常见问题)

## 环境要求

### 系统要求
- **操作系统**：Linux (Ubuntu 20.04+ 推荐) 或 macOS
- **内存**：至少 4GB RAM
- **磁盘空间**：至少 2GB 可用空间
- **网络**：稳定的互联网连接（用于API调用）

### 软件依赖

#### Python环境
- **Python版本**：3.8, 3.9, 3.10 或 3.11
- **pip**：最新版本
- **虚拟环境**：推荐使用 virtualenv 或 conda

```bash
# 检查Python版本
python --version
# 或
python3 --version
```

#### Node.js环境
- **Node.js版本**：16.0 或更高
- **npm版本**：8.0 或更高

```bash
# 检查Node.js版本
node --version

# 检查npm版本
npm --version
```

### Aligulac API Key
- **必需**：有效的Aligulac API Key（已从 http://aligulac.com/about/api/ 获取）
- **配置位置**：`backend/.env` 文件

## 快速安装

### 1. 克隆项目（已完成）
```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats
```

### 2. 安装Python依赖
```bash
cd backend

# 建议使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

**requirements.txt 内容**：
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.13.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
apscheduler==3.10.4
pandas==2.1.3
numpy==1.24.4
python-multipart==0.0.06
jinja2==3.1.2
httpx==0.25.2
aiofiles==23.2.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### 3. 安装Node.js依赖
```bash
cd frontend
npm install
```

**package.json 关键依赖**：
```json
{
  "dependencies": {
    "vue": "^3.3.8",
    "element-plus": "^2.4.2",
    "vue-router": "^4.2.5",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-vue": "^4.5.0"
  }
}
```

### 4. 配置环境变量

创建 `backend/.env` 文件（已配置）：
```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，确保包含：
```env
# API设置
DEBUG=true
SECRET_KEY=your-secret-key-here

# 数据库设置
DATABASE_URL=sqlite:///./../database/sc2_stats.db

# Aligulac API - 已配置有效的API Key
ALIGULAC_API_KEY=9nqUtPDwCbcF2DdMOAdP
ALIGULAC_BASE_URL=http://aligulac.com/api/v1

# 服务器设置
HOST=0.0.0.0
PORT=8000

# 定时任务
SYNC_INTERVAL_HOURS=24
```

### 5. 初始化数据库（自动完成）
数据库会在首次运行时自动创建，无需手动初始化。

## 详细安装步骤

### 后端详细安装

1. **创建虚拟环境（推荐）**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

2. **升级pip**
   ```bash
   pip install --upgrade pip
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **验证安装**
   ```bash
   python -c "import fastapi, sqlalchemy, requests; print('所有依赖已正确安装')"
   ```

### 前端详细安装

1. **确保Node.js版本**
   ```bash
   node --version  # 应该显示 v16.x 或更高
   ```

2. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

3. **验证安装**
   ```bash
   npm list vue  # 应该显示 vue@3.x
   ```

### 数据库设置

项目使用SQLite数据库，文件位于 `database/sc2_stats.db`。

**首次运行时自动创建**：无需手动初始化，数据库会在首次同步数据时自动创建。

**数据库结构**：
- `players` - 选手表
- `matches` - 比赛表
- `teams` - 战队表
- `events` - 赛事表
- `player_stats` - 选手统计表

## 配置说明

### API Key配置

Aligulac API Key是必需的，用于访问Aligulac官方数据。

**获取方法**：
1. 访问 http://aligulac.com/about/api/
2. 填写表单获取API Key
3. 将Key填入 `backend/.env` 文件

**已配置的Key**：
```env
ALIGULAC_API_KEY=9nqUtPDwCbcF2DdMOAdP
```

### 数据库配置

**SQLite配置**（默认）：
```env
DATABASE_URL=sqlite:///./../database/sc2_stats.db
```

**PostgreSQL配置**（生产环境推荐）：
```env
DATABASE_URL=postgresql://user:password@localhost/sc2_prostats
```

### 服务器配置

**开发环境**：
```env
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

**生产环境**：
```env
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### 同步配置

**同步间隔**（小时）：
```env
SYNC_INTERVAL_HOURS=24
```

## 验证安装

### 1. 验证后端API
```bash
cd backend
python main.py &

# 在另一个终端测试
curl http://localhost:8000/api/players
curl http://localhost:8000/api/ranking
```

**预期输出**：JSON格式的选手数据和排行榜数据

### 2. 验证前端
```bash
cd frontend
npm run dev

# 访问浏览器
# http://localhost:5173 应该能看到选手列表
```

### 3. 验证数据同步
```bash
cd scripts
python test_api_direct.py

# 应该显示：
# ✅ API Key有效！请求成功！
```

### 4. 测试完整流程
```bash
cd scripts
python sync_data.py players
python verify_sync.py
```

**预期结果**：
- 成功同步TOP500选手
- 数据库中有300+名选手
- 比赛数据有800+场

## 常见问题

### Q1: `ModuleNotFoundError: No module named 'fastapi'`

**原因**：Python依赖未安装

**解决**：
```bash
cd backend
pip install -r requirements.txt
```

### Q2: `npm: command not found`

**原因**：Node.js未安装

**解决**：
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node
```

### Q3: API请求失败（401 Unauthorized）

**原因**：API Key无效或未配置

**解决**：
1. 检查 `backend/.env` 文件是否存在
2. 确认 `ALIGULAC_API_KEY` 已设置为有效值
3. 重新获取API Key：http://aligulac.com/about/api/

### Q4: `sqlite3.OperationalError: no such table: players`

**原因**：数据库未初始化

**解决**：
- 首次运行会自动创建数据库和表
- 或者手动创建：
  ```bash
  cd scripts
  python sync_data.py players
  ```

### Q5: 前端显示"无法连接到后端"

**原因**：后端服务未启动或端口被占用

**解决**：
1. 确保后端已启动：`python main.py`
2. 检查端口8000是否被占用：`lsof -i :8000`
3. 修改 `.env` 中的端口配置

### Q6: 同步超时

**原因**：数据量大或网络慢

**解决**：
1. 使用后台运行：`nohup python sync_data.py history &`
2. 减少同步天数：`python sync_data.py history --days=30`
3. 查看日志：`tail -f /tmp/sync_history.log`

## 🚀 生产环境部署

### 使用 Gunicorn（推荐）
```bash
cd backend
pip install gunicorn

gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 使用 PM2（进程管理）
```bash
# 后端
cd backend
pm2 start "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000" --name sc2-backend

# 前端
cd frontend
pm2 start "npm run dev" --name sc2-frontend
```

### 使用 Docker（即将支持）
```dockerfile
# Dockerfile 示例
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

## 📈 性能优化

### 数据库优化
1. **索引**：确保所有外键和常用查询字段都有索引
2. **查询优化**：使用SQLAlchemy的`joinedload`减少N+1查询
3. **连接池**：调整SQLAlchemy连接池大小

### API优化
1. **分页**：使用游标分页而不是OFFSET
2. **缓存**：对不常变化的数据添加缓存
3. **压缩**：启用Gzip压缩

### 前端优化
1. **懒加载**：组件按需加载
2. **虚拟滚动**：长列表使用虚拟滚动
3. **缓存**：API响应缓存

## 🔒 安全建议

1. **API Key**：不要将API Key提交到版本控制
2. **数据库**：定期备份数据库
3. **密码**：使用环境变量存储敏感信息
4. **CORS**：配置适当的CORS策略

## 📞 支持

- **Issues**: 提交GitHub Issue
- **文档**: 查看 `/docs` 目录
- **日志**: 检查 `/tmp/*.log` 文件

---

**版本**: v2.0.0  
**最后更新**: 2026-01-19  
**维护者**: xjingyao
