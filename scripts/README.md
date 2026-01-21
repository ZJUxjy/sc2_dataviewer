# SC2 Pro Stats - 维护脚本

这个目录包含项目核心维护工具脚本，用于日常数据管理和维护。

## 核心脚本说明

### 1. sync_data.py
**功能**: 主数据同步工具
**用途**: 从Aligulac API同步选手数据、比赛历史、赛事信息等

**使用方式**:
```bash
# 同步选手数据（TOP500）
python sync_data.py players

# 同步对战历史（TOP选手间比赛）
python sync_data.py history

# 同步所有数据
python sync_data.py all

# 后台运行（推荐）
nohup python sync_data.py history > /tmp/sync_history.log 2>&1 &
```

**维护频率**: 
- 选手数据：每周1次
- 对战历史：每周1-2次

---

### 2. recalculate_stats.py
**功能**: 重新计算选手统计数据
**用途**: 重新计算所有选手的胜负场数和胜率

**使用时机**:
- 发现统计数据不准确
- 同步数据后发现统计异常
- 手动修改比赛数据后

**使用方式**:
```bash
python recalculate_stats.py
```

---

### 3. update_player_earnings.py
**功能**: 更新选手奖金数据
**用途**: 从Aligulac API获取并更新选手的职业奖金总额

**使用时机**:
- 发现奖金数据缺失或为0
- 奖金数据需要定期更新（如大赛结束后）

**使用方式**:
```bash
# 直接运行
python update_player_earnings.py

# 后台运行（推荐，可能需要10-15分钟）
nohup python update_player_earnings.py > /tmp/update_earnings.log 2>&1 &
tail -f /tmp/update_earnings.log  # 查看进度
```

**注意**: 此脚本需要访问每个选手的详细信息API，耗时较长（302名选手约需5-10分钟）

---

### 4. verify_matches.py
**功能**: 验证比赛数据完整性
**用途**: 检查数据库比赛数据的完整性

**验证项目**:
- 比赛基础信息完整性
- 选手关联正确性
- 赛事关联正确性
- 日期格式正确性

**使用方式**:
```bash
python verify_matches.py
```

**输出示例**:
```
=== 数据库统计 ===
总比赛数: 1797
有效比赛: 1797 (100.0%)

=== TOP选手数据问题 ===
选手ID 1 (Serral): 第7场赛事名称为空
```

---

### 5. init_db.py
**功能**: 数据库初始化
**用途**: 初始化数据库表结构

**使用时机**:
- 首次部署项目
- 重置数据库

**使用方式**:
```bash
python init_db.py
```

---

## 维护工作流程

### 日常维护（每周）
1. **同步最新数据**
   ```bash
   cd scripts
   nohup python sync_data.py all > /tmp/weekly_sync.log 2>&1 &
   ```

2. **验证数据完整性**
   ```bash
   python verify_matches.py
   ```

3. **检查奖金数据**
   ```bash
   # 检查是否有奖金为0的TOP选手
   sqlite3 ../database/sc2_stats.db "SELECT tag, total_earnings FROM players WHERE total_earnings = 0 ORDER BY current_rating DESC LIMIT 10;"
   ```

### 问题排查
- **胜率显示异常** → 运行 `recalculate_stats.py`
- **奖金数据为0** → 运行 `update_player_earnings.py`
- **比赛数据缺失** → 运行 `sync_data.py history`

### 备份目录
`backup/` 目录包含核心脚本的备份副本，请勿删除。

## 注意事项

1. **API限制**: Aligulac API有请求频率限制，脚本已内置延迟，请勿修改
2. **运行时间**: 批量更新脚本（如 update_player_earnings）建议在后台运行
3. **日志文件**: 建议将输出重定向到日志文件，便于排查问题
4. **数据库**: 所有操作直接作用于 `../database/sc2_stats.db`

## 依赖

所有脚本依赖以下后端模块：
- `models/` - 数据库模型
- `services/` - Aligulac API服务
- `database.py` - 数据库连接

运行前请确保已在项目根目录配置 `.env` 文件（包含 ALIGULAC_API_KEY）。