# ❗重要：首次运行前配置API Key

## 新增功能

✅ **新增TOP500选手同步功能** - 可以同步Aligulac排行榜上评分最高的500名职业选手数据

## 配置步骤

### 1. 创建环境变量文件

在 `backend` 目录下创建 `.env` 文件：

```bash
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend
cp .env.example .env
```

### 2. 获取Aligulac API Key

访问 http://aligulac.com/about/api/ 获取API Key

1. 点击 "Generate" 按钮生成API Key
2. 填写姓名和邮箱
3. 复制20位的API Key

### 3. 配置API Key

编辑 `.env` 文件：

```bash
# 使用nano编辑器
nano /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend/.env
```

将这一行：
```
ALIGULAC_API_KEY=your-aligulac-api-key-here
```

改为：
```
ALIGULAC_API_KEY=你复制的实际API Key
```

### 4. 现在可以运行脚本了！

```bash
# 入门推荐：同步TOP500职业选手（评分最高的）⭐
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts
python sync_data.py players    # 同步TOP500选手（按Aligulac评分排名）

# 同步所有数据（TOP500选手、战队、赛事）
python sync_data.py

# 仅同步比赛数据（最近30天）
python sync_data.py matches

# 查看帮助
python sync_data.py --help
```

## 快速测试

如果不配置API Key，也可以先测试前端和后端是否能正常运行：

```bash
# 启动后端（数据为空，但API可用）
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend
python main.py

# 新终端启动前端
cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/frontend
npm run dev
```

然后访问 http://localhost:5173 查看界面

## 故障排除

如果运行脚本时提示API Key错误：

```
❌ 错误: 请先在 backend/.env 文件中设置 ALIGULAC_API_KEY
```

这说明你还没有正确配置 `.env` 文件，请重新执行上面的配置步骤。

## 需要帮助？

- 查看完整文档：`/home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/README-PROJECT.md`
- 项目总结：`/home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/PROJECT_SUMMARY.md`
- API文档：http://localhost:8000/docs (需启动后端后访问)
