# API Key配置与测试指南

本指南帮助您配置有效的Aligulac API Key并验证系统是否正常工作。

## 第一步：生成API Key

### 操作步骤

1. **访问API页面**
   ```
   http://aligulac.com/about/api/
   ```

2. **填写表单**
   - Name: 输入您的姓名或昵称
   - Email: 输入有效的邮箱地址

3. **点击"Generate"按钮**

4. **复制生成的API Key**
   - 格式：20位随机字符串
   - 示例：`9nqUtPDwCbcF2DdMOAdP`（这只是格式示例）

## 第二步：配置API Key

### 编辑环境变量文件

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend

# 备份原文件（可选）
cp .env .env.backup

# 编辑文件
nano .env
```

### 修改配置

找到这一行：
```
ALIGULAC_API_KEY=your-aligulac-api-key-here
```

替换为真实的Key：
```
ALIGULAC_API_KEY=你复制的20位API Key
```

**正确示例**：
```
ALIGULAC_API_KEY=AbCdEfGh1234567890Ab
```

**错误示例**：
```
ALIGULAC_API_KEY=your-aligulac-api-key-here  ← 这是占位符，无效！
```

### 保存并退出

- nano编辑器：按 `Ctrl + X`，然后按 `Y`，最后按 `Enter`

## 第三步：验证API Key

### 方法1：使用测试脚本

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts

# 测试activerating端点（推荐）
python test_activerating.py

# 测试通用API
python test_aligulac_api.py
```

**成功输出示例**：
```
=== 测试Aligulac API ===

🔄 获取TOP 5选手数据...

✅ 成功获取 5 名选手数据

=== 第一名选手的完整数据结构 ===

{
  "id": 309,
  "tag": "Stats",
  "name": "Stats",
  "race": "P",
  "country": "KR",
  "current_rating": {
    "rating": 1834.0,
    "deviation": 53.0,
    ...
  },
  ...
}
```

**失败输出示例**：
```
🔄 获取TOP 5选手数据...

API request failed: 401 Client Error: Unauthorized for url: ...
❌ 无法获取选手数据
```

如果看到`401 Unauthorized`，说明API Key无效。

### 方法2：手动curl测试

```bash
# 替换 YOUR_API_KEY 为你的真实Key
curl "http://aligulac.com/api/v1/player/?limit=2&apikey=YOUR_API_KEY"
```

**成功响应**：
```json
{"meta": {...}, "objects": [{"id": 1, "tag": "Leenock", ...}]}
```

**失败响应**：
```json
{"error": "Unauthorized"}
```

## 第四步：同步数据测试

### 测试小规模同步

在确认API Key有效后，先测试同步少量数据：

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts

# 测试同步TOP5选手（快速测试）
python -c "
import sys
sys.path.insert(0, '../backend')
from services.aligulac_service import AligulacService
from services.sync_service import SyncService
from models import SessionLocal

aligulac = AligulacService()
db = SessionLocal()
sync = SyncService(db, aligulac)

print('测试同步TOP5...')
count = sync.sync_current_ranking(limit=5)
print(f'同步完成: {count} 名选手')
db.close()
"
```

**成功标志**：
- 没有错误信息
- 显示同步进度
- 最终显示成功消息

### 查看数据库

```bash
# 连接到数据库
sqlite3 ../database/sc2_stats.db

# 查看同步的选手
SELECT id, tag, current_rating, race, country 
FROM players 
WHERE current_rating IS NOT NULL 
ORDER BY current_rating DESC 
LIMIT 5;

# 退出SQLite
.quit
```

**预期输出**：
```
id  tag      current_rating  race  country
--  -------  --------------  ----  -------
123 Serral   2850.0          Z     FI
456 Reynor   2800.0          Z     PL
...
```

如果`current_rating`列有数值，说明一切正常！

## 常见问题

### Q1: 运行测试脚本时显示"ALIGULAC_API_KEY not found"

**原因**：环境变量未加载

**解决**：
```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('ALIGULAC_API_KEY'))"
```

如果输出的是你的真实Key，说明配置正确；如果输出None或占位符，需要重新配置。

### Q2: API Key在哪里获取？

**答案**：
- 网址：http://aligulac.com/about/api/
- 需要填写：姓名 + 邮箱
- 点击"Generate"生成

### Q3: API Key可以重复使用吗？

**答案**：
- 可以，API Key永久有效
- 一个Key可以在多个项目使用
- 建议每个项目使用独立的Key

### Q4: 如何验证Key是否有效？

**方法**：
```python
import requests
response = requests.get(
    "http://aligulac.com/api/v1/player/?limit=1",
    params={"apikey": "YOUR_KEY"}
)
print(response.status_code)  # 200=有效, 401=无效
```

### Q5: Key泄露了怎么办？

**建议**：
1. 立即生成新的Key
2. 在Aligulac网站上删除旧的Key（如果支持）
3. 更新所有使用旧Key的项目

## 第五步：完整同步测试

在确认小规模测试成功后，可以进行完整同步：

```bash
# 从当前排名同步TOP500（需要5-10分钟）
python sync_data.py players

# 或者同步所有数据
python sync_data.py
```

### 监控进度

同步过程中会显示：
```
=== 同步TOP500选手数据 ===

🔄 开始同步TOP500选手数据（多种方式）...
📊 这可能需要5-10分钟，请耐心等待...

使用方式：从当前排名（Current Ranking）同步
已同步 50/500 名选手...
已同步 100/500 名选手...
...
已同步 500/500 名选手...

✅ 成功同步TOP 500 名选手
```

## 验证清单

配置完成后，请检查以下项目：

- [ ] backend/.env文件中配置了有效API Key（不是占位符）
- [ ] 运行test_activerating.py显示成功获取数据
- [ ] 运行verify_sync.py显示"有评分数据的选手" > 0
- [ ] 数据库中players表有current_rating字段
- [ ] 可以查询到TOP10选手及其评分

如果所有项目都勾选，说明配置成功！

## 技术支持

如果配置后仍然无法工作：

1. **检查网络**：确保能访问aligulac.com
2. **检查Key**：重新生成并配置API Key
3. **查看日志**：运行同步时查看错误信息
4. **测试连接**：使用curl或python直接测试API
5. **查看文档**：docs/CURRENT_RANKING_SYNC.md

## 最后提醒

**最重要的事情说三遍：**

🔴 **必须配置有效的API Key！**  
🔴 **必须配置有效的API Key！**  
🔴 **必须配置有效的API Key！**  

占位符`your-aligulac-api-key-here`是无效的，必须替换为从官网生成的真实Key。

**官网地址**：http://aligulac.com/about/api/

配置好API Key后，所有功能才能正常工作！
