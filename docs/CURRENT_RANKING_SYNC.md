# 从当前排名（Current Ranking）同步TOP500选手

## 问题背景

之前的实现通过按`current_rating__rating`排序选手列表来获取TOP500，但这不是Aligulac网站上真正的"Current Ranking"。

## 正确实现

根据Aligulac API文档，**`activerating`**端点返回的才是真正的当前排名数据。

## 实现更新

### 新增功能

1. **AligulacService.get_activeratings()**
   - 访问 `/api/v1/activerating/` 端点
   - 返回真正的当前活跃评分数据

2. **AligulacService.get_current_ranking()**
   - 基于activerating数据构建TOP N选手列表
   - 每个选手对象包含完整的当前评分信息

3. **SyncService.sync_current_ranking()**
   - 从当前排名同步TOP N选手
   - 自动保存current_rating到数据库

### 数据库更新

在Player模型中添加了`current_rating`字段：
```python
current_rating = Column(Float, nullable=True)
```

如果数据库已存在，需要运行迁移脚本：
```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python migrate_add_rating.py
```

## 使用方式

### 命令行同步（推荐）

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts

# 从当前排名同步TOP500选手
python sync_data.py players

# 同步所有数据（TOP500选手 + 战队 + 赛事）
python sync_data.py

# 仅同步比赛数据
python sync_data.py matches
```

### API调用

```python
# 后端API
POST /api/sync/top-players?limit=500

# Python代码
from services.aligulac_service import AligulacService
from services.sync_service import SyncService

aligulac = AligulacService()
sync_service = SyncService(db, aligulac)

# 从当前排名同步TOP500
sync_service.sync_current_ranking(limit=500)
```

### 前端界面

前端"选手列表"页面的同步对话框提供两种选择：
- **同步推荐选手**（使用当前排名数据）
- **同步TOP500职业选手**（明确说明，使用相同数据）

## 数据验证

同步完成后，使用验证脚本检查数据：

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python verify_sync.py
```

预期输出：
```
=== TOP500同步验证 ===

1. 数据库中选手总数: 500
2. 有评分数据的选手: 500  ← 这个必须有数值
3. 评分TOP 10 选手:
------------------------------------------------------------
排名 ID   Tag             种族  评分      国家
------------------------------------------------------------
1    123  Serral          Z     2850      FI
2    456  Reynor          Z     2800      PL
...
```

**关键点**：如果"有评分数据的选手"为0，说明：
1. API Key无效
2. 同步过程中未正确保存current_rating
3. 数据库结构未更新（需运行迁移脚本）

## 技术细节

### activerating端点返回的数据结构

```json
{
  "objects": [
    {
      "player": {
        "id": 123,
        "tag": "Serral",
        "name": "Joona Sotala",
        "race": "Z",
        "country": "FI",
        ...
      },
      "rating": 2850.50,
      "deviation": 50.20,
      "volatility": 0.06,
      ...
    }
  ]
}
```

### 如何与player端点区分

1. **activerating端点**：
   - 返回当前活跃评分
   - 对应网站上的"Current Ranking"
   - 包含最新的评分数据

2. **player端点**：
   - 返回选手基本信息
   - 包含生涯统计等数据
   - 需要额外处理才能获取评分

## 故障排除

### 问题1: 同步后current_rating为null

**症状**：
```bash
$ python verify_sync.py
...
2. 有评分数据的选手: 0
```

**可能原因：**
1. **API Key无效**（最常见）
2. 数据库未运行迁移
3. 同步服务未正确保存rating数据

**解决步骤**：
```bash
# 步骤1: 检查API Key
cd backend
grep ALIGULAC_API_KEY .env
# 确保不是 your-aligulac-api-key-here

# 步骤2: 运行迁移
cd ../scripts
python migrate_add_rating.py

# 步骤3: 重新同步
python sync_data.py players

# 步骤4: 验证
python verify_sync.py
```

### 问题2: 如何确认是从当前排名同步的

**验证方法**：
1. 访问 https://aligulac.com/ranking/ （当前排名页面）
2. 对比前10名选手
grep ALIGULAC_API_KEY .env
# 确保不是 your-aligulac-api-key-here

# 步骤2: 运行迁移
cd ../scripts
python migrate_add_rating.py

# 步骤3: 重新同步
python sync_data.py players

# 步骤4: 验证
python verify_sync.py
```

### 问题2: 如何确认是从当前排名同步的

**验证方法**：
1. 访问 https://aligulac.com/ranking/ （当前排名页面）
2. 对比数据库中top 10的选手和评分
3. 应该完全一致

## 最佳实践

1. **首次使用**：
   ```bash
   cd scripts
   python migrate_add_rating.py  # 确保数据库结构正确
   python sync_data.py players   # 从当前排名同步TOP500
   python verify_sync.py         # 验证数据
   ```

2. **定期更新**：
   - 建议每周执行一次同步
   - 每次同步都会更新current_rating

3. **数据备份**：
   ```bash
   cp ../database/sc2_stats.db ../database/sc2_stats.backup.db
   ```

## 版本信息

- **实现日期**：2026-01-19
- **版本**：v1.2.0
- **主要改动**：
  - 新增activerating端点支持
  - 添加current_ranking同步方法
  - 数据库添加current_rating字段
  - 修复TOP500同步准确性问题

## 相关文件

- `backend/services/aligulac_service.py` - API服务
- `backend/services/sync_service.py` - 同步服务
- `backend/models/__init__.py` - Player模型
- `scripts/sync_data.py` - 命令行工具
- `scripts/migrate_add_rating.py` - 数据库迁移
- `scripts/verify_sync.py` - 验证工具

## 技术参考

- Aligulac API文档：http://aligulac.com/about/api/
- 当前排名页面：https://aligulac.com/ranking/
