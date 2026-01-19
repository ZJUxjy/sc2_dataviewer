# 同步TOP500选手功能

本文档介绍如何使用新增的TOP500选手同步功能。

## 功能概述

新增 `sync_data.py top500` 命令，用于同步Aligulac排行榜上评分最高的500名选手数据。

## 使用方法

### 基本命令

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python sync_data.py top500
```

### 命令选项

```bash
# 同步所有数据（选手、战队、赛事）
python sync_data.py

# 仅同步选手（200名）
python sync_data.py players

# 同步TOP500选手（按评分排序）⭐新增
python sync_data.py top500

# 仅同步比赛（最近30天）
python sync_data.py matches

# 显示帮助信息
python sync_data.py --help
```

## 功能特点

### 1. 按评分排序
- 自动按Aligulac当前评分系统排序
- 同步评分最高的500名职业选手
- 包含选手基本信息、战队、胜率等数据

### 2. 进度显示
- 每同步50名选手显示一次进度
- 预计耗时：5-10分钟
- 自动处理API请求频率限制

### 3. 数据完整性
- 自动同步选手所在战队信息
- 包含生涯统计数据（胜率、场次、收入等）
- 支持增量更新（已存在选手自动更新）

## 技术实现

### 后端API增强

**AligulacService.get_top_players()**
```python
# 参数说明
limit: int = 500    # 返回选手数量
race: str = None    # 按种族筛选（P/T/Z）
country: str = None # 按国家筛选

# 调用示例
top500 = aligulac_service.get_top_players(limit=500)
top100_protoss = aligulac_service.get_top_players(limit=100, race='P')
```

**SyncService.sync_top_players()**
```python
# 参数说明
limit: int = 500  # 同步的选手数量

# 调用示例
synced_count = sync_service.sync_top_players(limit=500)
```

### 数据库结构

同步的TOP500选手数据存储在以下表中：

- `players` - 选手基本信息
- `teams` - 战队信息（自动同步）
- `player_stats` - 选手统计数据（需额外计算）

## 最佳实践

### 1. 首次同步建议
```bash
# 先同步TOP500选手
python sync_data.py top500

# 再同步相关比赛数据
python sync_data.py matches
```

### 2. 定期更新
建议每周执行一次TOP500同步，保持数据新鲜度：

```bash
# 添加到crontab（每周日凌晨2点自动执行）
0 2 * * 0 cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts && python sync_data.py top500 >> /tmp/sc2_top500_sync.log 2>&1
```

### 3. API Key配置
确保已在 `backend/.env` 文件中配置有效的Aligulac API Key：

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend
cp .env.example .env
# 编辑.env文件，填入从 http://aligulac.com/about/api/ 获取的API Key
```

## 常见问题

### Q1: 同步失败怎么办？
- 检查API Key是否有效
- 检查网络连接
- 查看错误日志：`backend/logs/` 目录
- 等待几分钟后重试（API可能有频率限制）

### Q2: 同步需要多长时间？
- TOP500选手：5-10分钟
- 取决于网络速度和API响应
- 每50个选手约需30-60秒

### Q3: 如何确认同步成功？
- 查看脚本输出日志
- 检查数据库：
```sql
sqlite> SELECT COUNT(*) FROM players;
sqlite> SELECT tag, race, current_rating FROM players ORDER BY current_rating DESC LIMIT 10;
```
- 访问前端界面查看选手列表

### Q4: 可以同步更多或更少选手吗？
- 修改代码中的`limit`参数：
```python
# scripts/sync_data.py
player_count = sync_service.sync_top_players(limit=1000)  # 改为1000
```
- 注意：Aligulac API可能有单次请求数量限制

## 注意事项

1. **API限制**
   - 每个API Key有每日请求限额
   - 频繁同步可能导致API Key被临时限制
   - 建议控制同步频率

2. **数据完整性**
   - TOP500同步只包含选手基本信息
   - 比赛数据需单独同步
   - 选手统计数据需要额外计算（调用相关API）

3. **存储空间**
   - 500名选手数据约占用50-100MB
   - 建议定期清理旧数据（如需）

## 版本信息

- 实现日期：2026-01-19
- 相关文件：
  - `scripts/sync_data.py` - 同步脚本
  - `backend/services/aligulac_service.py` - API服务
  - `backend/services/sync_service.py` - 同步服务

## 技术支持

- Aligulac API文档：http://aligulac.com/about/api/
- 项目文档：`/home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/README-PROJECT.md`
- 问题反馈：检查项目GitHub Issues或联系维护者
