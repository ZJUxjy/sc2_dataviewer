# TOP500选手同步功能 - 修正完成 ✅

## 问题说明

**原实现的问题**：
- 通过按`current_rating__rating`排序选手列表来获取TOP500
- 这不是Aligulac网站上真正的"Current Ranking"
- 可能无法获取到最新的评分数据

**修正后的实现**：
- 使用`activerating`端点，这正是Aligulac用于当前排名的数据
- 直接同步网站上的Current Ranking数据
- 确保评分数据是最新的、准确的

## 修正内容汇总

### 1. 后端服务 (`backend/services/`)

#### AligulacService
- ✅ **新增get_activeratings()** - 访问`/api/v1/activerating/`端点
- ✅ **新增get_current_ranking()** - 构建真正的当前排名TOP N
- ⏸️ get_top_players() - 保留，但不再是主要方法

#### SyncService
- ✅ **新增sync_current_ranking()** - 从当前排名同步TOP N选手
- 🔄 sync_top_players() - 保留备用
- ✅ **_save_player()更新** - 正确保存current_rating数据

### 2. 数据模型 (`backend/models/`)

#### Player模型
- ✅ **新增current_rating字段** - 存储当前评分（Float, nullable）
- 需要运行迁移脚本更新现有数据库

### 3. 命令行工具 (`scripts/`)

#### sync_data.py
- ✅ **sync_all_data()** - 使用sync_current_ranking()
- ✅ **sync_players_only()** - 使用sync_current_ranking()
- ✅ **帮助信息更新** - 明确说明从当前排名同步

#### 新增工具
- ✅ **test_activerating.py** - 测试activerating端点
- ✅ **verify_sync.py** - 验证同步结果
- ✅ **migrate_add_rating.py** - 数据库迁移

### 4. 文档 (`docs/`)

- ✅ **CURRENT_RANKING_SYNC.md** - 完整的实现说明
- ✅ **IMPLEMENTATION_SUMMARY.md** - 快速参考
- ✅ **SYNC_TOP500.md** - 功能详细文档
- ✅ **TOP500_FEATURE.md** - 使用指南

## 正确使用方式

### 步骤1：配置API Key（必须）

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend
nano .env

# 必须是有效的API Key，不是占位符
ALIGULAC_API_KEY=AbCdEf1234567890AbCd  ← 替换为真实Key
```

**获取Key**：http://aligulac.com/about/api/

### 步骤2：更新数据库结构

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python migrate_add_rating.py
```

如果数据库是新的，直接运行同步会自动创建表。

### 步骤3：同步TOP500选手

```bash
# 从当前排名（Current Ranking）同步TOP500
python sync_data.py players

# 或者同步所有数据（包含TOP500选手、战队、赛事）
python sync_data.py
```

### 步骤4：验证结果

```bash
python verify_sync.py
```

**关键指标**：
```
2. 有评分数据的选手: 500  ← 必须是500或其他数值，不能是0
```

如果显示为0，说明：
1. API Key无效
2. 同步失败
3. 数据库存储问题

## 工作原理

### 数据流

```
Aligulac API (activerating端点)
    ↓
返回当前活跃评分列表
每个对象包含：
  - player: 选手基本信息
  - rating: 当前评分数值
  - deviation: 不确定性
  - volatility: 波动性
    ↓
AligulacService.get_current_ranking()
    ↓
提取并合并数据到player对象
    ↓
SyncService.sync_current_ranking()
    ↓
保存到数据库（包含current_rating字段）
    ↓
验证脚本检查current_rating是否保存成功
```

### API请求示例

```python
# 请求URL
GET http://aligulac.com/api/v1/activerating/
  ?limit=10
  &order_by=-rating
  &apikey=YOUR-API-KEY

# 响应数据结构
{
  "meta": {
    "limit": 10,
    "next": "/api/v1/activerating/?limit=10&offset=10",
    "offset": 0,
    "previous": null,
    "total_count": 10000
  },
  "objects": [
    {
      "player": {
        "id": 123,
        "tag": "Serral",
        "race": "Z",
        "country": "FI",
        ...
      },
      "rating": 2850.50,
      "deviation": 50.20,
      "volatility": 0.06,
      ...
    },
    ...
  ]
}
```

## 验证正确性

### 方法一：对比Aligulac网站

1. 访问 https://aligulac.com/ranking/
2. 查看前10名选手
3. 对比数据库中的数据：
   ```bash
   cd scripts
   python verify_sync.py
   ```
4. 确认选手名称、评分、种族、国家都匹配

### 方法二：直接查看数据库

```bash
# 连接到SQLite数据库
sqlite3 ../database/sc2_stats.db

# 查看TOP10选手
SELECT tag, current_rating, race, country  
FROM players 
WHERE current_rating IS NOT NULL 
ORDER BY current_rating DESC 
LIMIT 10;
```

### 方法三：使用测试脚本

```bash
cd scripts
python test_activerating.py  # 需要有效API Key
```

## 常见问题 (FAQ)

### Q1: 同步后current_rating都是null

**原因**：API Key无效或请求被限制

**解决**：
1. 检查backend/.env文件中的API Key
2. 确保不是占位符（your-aligulac-api-key-here）
3. 重新生成API Key：http://aligulac.com/about/api/

### Q2: 如何确认数据是从当前排名同步的

**验证**：
1. 访问aligulac.com/ranking/查看前5名
2. 对比数据库中的数据
3. 如果一致，说明是正确的

### Q3: 可以同步更多或更少的选手吗

**可以**：
```python
# 同步TOP100
sync_service.sync_current_ranking(limit=100)

# 同步TOP1000
sync_service.sync_current_ranking(limit=1000)
```

### Q4: API有请求限制吗

**有**：
- 未认证请求：严格限制
- 认证请求（带API Key）：较宽松
- 建议同步间隔：至少1小时

### Q5: 是否需要每次都运行迁移脚本

**不需要**：
- 新数据库：自动创建表结构
- 旧数据库：运行一次即可

## 快速参考

### 命令速查

```bash
# 必需步骤
cd backend && nano .env  # 配置有效的API Key

# 推荐步骤
cd ../scripts
python migrate_add_rating.py  # 如果是旧数据库

# 同步数据
python sync_data.py players  # 从当前排名同步TOP500

# 验证
python verify_sync.py
```

### API调用参考

```python
# 获取当前排名TOP10
from backend.services.aligulac_service import AligulacService

aligulac = AligulacService()
top10 = aligulac.get_current_ranking(limit=10)

for player in top10:
    print(f"{player['tag']}: {player['current_rating']['rating']}")
```

## 技术支持

- API文档: http://aligulac.com/about/api/
- 问题反馈: 查看项目Issues或联系维护者
- 验证工具: scripts/verify_sync.py

## 版本信息

- **版本**: v1.2.0 (修正版)
- **实现日期**: 2026-01-19
- **修复内容**: 使用activerating端点获取真正的当前排名
- **影响范围**: 所有同步选手的功能

## 总结

这次修正确保您同步的是Aligulac网站上真正的"Current Ranking"，而不是简单排序的选手列表。

**关键点**: 必须先配置有效的API Key，否则所有同步功能都无法正常工作！
