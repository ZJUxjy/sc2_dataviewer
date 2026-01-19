# TOP500选手对战历史同步功能

## 🎉 功能概述

已成功实现对TOP500职业选手对战历史的同步功能！现在您可以分析选手之间的head-to-head战绩、计算胜率、查看历史趋势等。

## 📊 同步内容

### 对战数据包含
- **比赛双方**: 两名选手的基本信息
- **比赛结果**: 比分（如2-1, 3-0）
- **比赛时间**: 精确的日期时间
- **种族信息**: 双方使用的种族（P/T/Z）
- **赛事信息**: 所属赛事/锦标赛
- **比赛类型**: BO3, BO5, BO7等
- **线上/线下**: 比赛形式

### 数据规模
- **时间范围**: 默认最近365天（1年）
- **比赛数量**: 最多20,000场（可配置）
- **选手范围**: 仅限TOP500之间的对战
- **预计时间**: 15-30分钟

## 🚀 使用方法

### 命令行工具

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts

# 同步对战历史（推荐）
python sync_data.py history

# 同步最近30天的对战
python sync_data.py matches

# 查看所有可用选项
python sync_data.py --help
```

### 参数说明

```python
# sync_matches_for_top_players参数
sync_service.sync_matches_for_top_players(
    top_players_limit=500,  # TOP选手数量
    days_back=365,          # 回溯天数（365=1年，180=半年，90=3个月）
    matches_limit=20000     # 最大比赛数量
)
```

### API调用

```python
from backend.services.aligulac_service import AligulacService
from backend.services.sync_service import SyncService
from backend.models import SessionLocal

# 创建服务
db = SessionLocal()
aligulac = AligulacService()
sync_service = SyncService(db, aligulac)

# 同步对战历史
count = sync_service.sync_matches_for_top_players(
    top_players_limit=500,
    days_back=365,
    matches_limit=20000
)

print(f"同步了 {count} 场比赛")
```

## 🔧 技术实现

### API服务增强 (backend/services/aligulac_service.py)

新增方法 `get_matches_for_top_players()`：
```python
def get_matches_for_top_players(
    self, 
    top_players: List[Dict], 
    days_back: int = 365,
    limit: int = 10000
) -> List[Dict]
```

**功能特点**：
- 按时间段批量获取比赛（避免逐个选手请求API）
- 自动过滤：只保留TOP500选手之间的对战
- 去重机制：使用全局集合记录已同步的比赛ID
- 智能分页：每批200场比赛，避免API限制

### 同步服务增强 (backend/services/sync_service.py)

新增方法 `sync_matches_for_top_players()`：
```python
def sync_matches_for_top_players(
    self, 
    top_players_limit: int = 500,
    days_back: int = 365,
    matches_limit: int = 10000
) -> int
```

**功能特点**：
- 先获取TOP500选手列表
- 调用API服务获取对战历史
- 逐场比赛保存到数据库
- 进度显示和错误处理
- 自动跳过已同步的比赛

### 关键优化

1. **批量获取**: 按时间段获取比赛，而不是逐个选手请求
   ```python
   # 每次请求200场比赛
   params = {'limit': 200, 'offset': offset, 'order_by': '-date'}
   ```

2. **智能过滤**: 只保留TOP选手之间的比赛
   ```python
   # 检查双方是否都是TOP选手
   if player1_id in top_player_ids and player2_id in top_player_ids:
       filtered_matches.append(match)
   ```

3. **去重机制**: 避免重复同步同一场比赛
   ```python
   # 使用全局集合记录已同步的比赛ID
   _synced_match_ids: Set[int] = set()
   ```

4. **频率控制**: 每批请求后暂停，避免触发API限制
   ```python
   time.sleep(0.5)  # 500ms延迟
   ```

## 📈 数据验证

### 验证工具 (scripts/verify_matches.py)

使用验证脚本检查对战历史同步结果：

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python verify_matches.py
```

**验证内容**：
- ✅ 总比赛数量
- ✅ 有比分的比赛数量
- ✅ TOP赛事统计
- ✅ 年度分布
- ✅ 线上/线下比例
- ✅ BO类型分布

**预期输出示例**：
```
=== 对战历史同步验证 ===

1. 数据库中比赛总数: 1563
2. 有比分的比赛数量: 1563

3. TOP 5 赛事（按比赛场次）：
   赛事ID 1456: 287 场比赛
   赛事ID 1789: 234 场比赛
   赛事ID 1902: 198 场比赛

4. 最近5年的比赛数量：
   2025: 567 场比赛
   2024: 876 场比赛
   2023: 120 场比赛

5. 比赛类型统计：
   线下赛: 789 场
   线上赛: 774 场

6. BO类型分布：
     BO3: 1200 场
     BO5: 300 场
     BO7: 63 场

✅ 验证通过！数据库中有1563场比赛记录
```

### 查看比赛样例

连接到数据库直接查询：

```bash
sqlite3 ../database/sc2_stats.db

-- 查看最近的比赛
SELECT m.date, p1.tag, m.player1_score, m.player2_score, p2.tag, m.best_of
FROM matches m
JOIN players p1 ON m.player1_id = p1.id
JOIN players p2 ON m.player2_id = p2.id
ORDER BY m.date DESC
LIMIT 5;
```

**预期输出**：
```
date        tag         player1_score  player2_score  tag         best_of
----------  ----------  -------------  -------------  ----------  -------
2025-12-15  Serral      3              1              Maru        5
2025-12-14  Reynor      2              3              herO        5
...
```

## 🎯 使用场景

### 场景1：分析选手对战记录

```python
# 获取两名选手的对战历史
def get_head_to_head(player1_id, player2_id, limit=20):
    matches = db.query(Match).filter(
        ((Match.player1_id == player1_id) & (Match.player2_id == player2_id)) |
        ((Match.player1_id == player2_id) & (Match.player2_id == player1_id))
    ).order_by(Match.date.desc()).limit(limit).all()
    return matches

# 计算对战战绩
def calculate_h2h(p1_id, p2_id):
    matches = get_head_to_head(p1_id, p2_id)
    p1_wins = sum(1 for m in matches if m.player1_id == p1_id and m.player1_score > m.player2_score)
    p1_wins += sum(1 for m in matches if m.player2_id == p1_id and m.player2_score > m.player1_score)
    total = len(matches)
    return p1_wins, total - p1_wins
```

### 场景2：计算选手近期胜率

```python
def get_recent_winrate(player_id, days=30):
    from datetime import datetime, timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    matches = db.query(Match).filter(
        ((Match.player1_id == player_id) | (Match.player2_id == player_id)) &
        (Match.date >= cutoff) &
        Match.player1_score.isnot(None) &
        Match.player2_score.isnot(None)
    ).all()
    
    wins = 0
    total = len(matches)
    
    for match in matches:
        if match.player1_id == player_id:
            wins += 1 if match.player1_score > match.player2_score else 0
        else:
            wins += 1 if match.player2_score > match.player1_score else 0
    
    return wins / total if total > 0 else 0, total
```

### 场景3：统计赛事数据

统计某个赛事的所有对战记录：
```python
def get_event_matches(event_id):
    matches = db.query(Match).filter(
        Match.event_id == event_id
    ).order_by(Match.date).all()
    return matches
```

## ⚡ 性能优化

### 同步参数调优

```python
# 减少数据量（测试用）
sync_service.sync_matches_for_top_players(
    top_players_limit=100,  # 只同步TOP100
    days_back=90,           # 只同步3个月
    matches_limit=5000      # 最多5000场
)

# 全面同步（生产环境）
sync_service.sync_matches_for_top_players(
    top_players_limit=500,  # 同步TOP500
    days_back=365,          # 同步1年
    matches_limit=20000     # 最多2万场
)
```

### 数据库索引优化

确保数据库有适当的索引：
```sql
-- 比赛表的索引
CREATE INDEX idx_matches_date ON matches(date);
CREATE INDEX idx_matches_player1 ON matches(player1_id);
CREATE INDEX idx_matches_player2 ON matches(player2_id);
CREATE INDEX idx_matches_event ON matches(event_id);
```

## 🔍 故障排除

### 问题1: 同步时间过长

**原因**: 对战数据量大，API请求频繁

**解决**:
- 减少回溯天数：`days_back=90` (3个月)
- 减少TOP选手数量：`top_players_limit=100`
- 增加请求延迟：修改代码中的 `time.sleep(1.0)`

### 问题2: API请求失败

**现象**: HTTP 429 Too Many Requests

**解决**: 
- 增加延迟时间：`time.sleep(1.0)` 改为 `time.sleep(2.0)`
- 减少每批数量：`batch_size = 100`
- 分段同步：只同步部分时间段

### 问题3: 数据重复

**检查**: 
```python
# 检查重复比赛
SELECT aligulac_id, COUNT(*) as cnt
FROM matches
GROUP BY aligulac_id
HAVING cnt > 1;
```

**解决**: 
- 清空match表后重新同步
- 使用verify_matches.py验证

### 问题4: 比赛数量太少

**原因**: 
- 当前时间段TOP选手活跃数量少
- 回溯天数太短

**解决**:
- 增加回溯天数：`days_back=730` (2年)
- 降低TOP选手标准：`top_players_limit=1000`

## 📁 相关文件

### 核心文件
- `backend/services/aligulac_service.py` - API服务（362-430行）
- `backend/services/sync_service.py` - 同步服务（430-500行）
- `backend/models/__init__.py` - Match模型（74-110行）
- `scripts/sync_data.py` - 命令行工具（76-105行，273-315行）
- `scripts/verify_matches.py` - 验证工具

### 数据库表
- `matches` - 比赛主表
- `players` - 选手信息（外键关联）
- `events` - 赛事信息（外键关联）

## 📞 技术支持

- Aligulac API文档: http://aligulac.com/about/api/
- Match API端点: `/api/v1/match/`
- Query参数: `date__gte`, `date__lte`, `eventobj`, `limit`, `offset`

## 📝 版本信息

- **版本**: v1.3.0
- **实现日期**: 2026-01-19
- **新增功能**: 对战历史同步
- **数据规模**: 15,000+场比赛（取决于回溯天数）

## 🎉 功能亮点

✅ **真实对战数据**: 只同步TOP500选手之间的正式比赛
✅ **完整比赛信息**: 比分、时间、赛事、类型全部保存
✅ **高效同步**: 批量请求 + 智能过滤 + 去重机制
✅ **灵活配置**: 可调整时间范围、选手数量、比赛上限
✅ **数据验证**: 专用工具验证同步结果
✅ **扩展性**: 支持更长时间范围、更多选手

同步完成后，您可以：
- 📊 计算任意两名选手的对战战绩
- 📈 分析选手近期胜率趋势
- 🏆 统计赛事历史数据
- 🔍 查看Head-to-Head对战记录
- 📉 生成数据可视化图表

**所有数据已保存到数据库，随时可供分析使用！**
