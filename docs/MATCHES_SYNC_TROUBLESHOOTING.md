# 同步比赛数据故障排除

## 问题1: API请求失败 - 400 Bad Request

**错误信息**:
```
API request failed: 400 Client Error: Bad Request for url: http://aligulac.com/api/v1/match/?limit=5000&offset=0&order_by=-date&date__gte=2025-01-19+19%3A13%3A10.312154&apikey=...
```

**原因**: 日期格式问题。Aligulac API只支持日期格式（YYYY-MM-DD），不支持包含时间的格式。

**解决方案**: ✅ 已修复
```python
# 修改后的代码（services/sync_service.py:194-195）
start_date_str = start_date.strftime('%Y-%m-%d')  # 只发送日期部分
```

## 问题2: 同步比赛数据超时

**现象**: 命令运行很长时间没有输出，最终超时

**原因**: `python sync_data.py matches` 默认同步最近30天的所有比赛，数据量可能很大

**解决方案**:

**选项1**: 使用nohup在后台运行
```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
nohup python sync_data.py matches > /tmp/sync_matches.log 2>&1 &

# 查看进度
tail -f /tmp/sync_matches.log
```

**选项2**: 减少同步天数
```bash
# 修改 backend/main.py 中的 sync_matches 端点
curl -X POST "http://localhost:8000/api/sync/matches?days=7"  # 只同步7天
```

**选项3**: 仅同步TOP500选手之间的对战历史（推荐）
```bash
python sync_data.py history
# 这个命令会智能地只同步TOP500选手之间的比赛，数据量更小，更有价值
```

## 问题3: 数据重复或已存在

**现象**: 二次同步时仍然同步大量数据

**原因**: `sync_matches` 函数没有去重机制，会重复获取已存在的比赛

**解决方案**: 使用 `sync_matches_for_top_players` 代替
```python
# scripts/sync_data.py
# 这个函数有内置的去重机制
sync_service.sync_matches_for_top_players(
    top_players_limit=500,
    days_back=30,
    matches_limit=10000
)
```

## 推荐做法

### 对于日常数据更新

**只同步对战历史（TOP500之间）**:
```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python sync_data.py history
```

这个命令会：
- 自动获取当前TOP500选手
- 只同步他们之间的对战（质量更高）
- 默认同步365天（可配置）
- 内置去重，避免重复数据

### 首次完整同步

如果确实需要同步所有比赛数据：

```bash
# 后台运行，避免超时
cd scripts
nohup python sync_data.py matches > sync_all.log 2>&1 &

# 查看进度
tail -f sync_all.log

# 预计时间：30-60分钟（取决于API响应速度）
```

## 验证数据同步结果

```bash
# 验证比赛数量
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python verify_matches.py

# 应该看到类似输出:
# 数据库中比赛总数: 864
# 有比分的比赛数量: 864
```

## 查看已同步数据

```bash
# 查看TOP10选手的对战记录
cd scripts
python -c "
import sys; sys.path.insert(0, '../backend')
from models import SessionLocal, Player, Match
from sqlalchemy import or_

db = SessionLocal()

player = db.query(Player).filter(Player.tag == 'herO').first()
if player:
    matches = db.query(Match).filter(or_(Match.player1_id == player.id, Match.player2_id == player.id)).order_by(Match.date.desc()).limit(5)
    for m in matches:
        p1 = db.query(Player).filter(Player.id == m.player1_id).first()
        p2 = db.query(Player).filter(Player.id == m.player2_id).first()
        print(f'{p1.tag} {m.player1_score}-{m.player2_score} {p2.tag} - {m.date}')

db.close()
"
```

## 总结

对于您的使用场景：**推荐只使用 `python sync_data.py history` 即可**，这个命令会同步TOP500选手之间的对战历史，数据质量更高，更有分析价值。

`python sync_data.py matches` 会同步所有比赛（包括非TOP选手），数据量巨大且很多比赛质量不高。
