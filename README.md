# SC2 Pro Stats - 星际争霸2职业选手数据平台

![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/node.js-16%2B-green)

一个完整的星际争霸2职业选手数据平台，支持TOP500职业选手数据同步、对战历史分析、排行榜展示等功能。

## 🎉 项目特性

### 核心功能
- ✅ **TOP500职业选手同步**：从Aligulac官方API同步当前排名TOP500职业选手（按评分排序）
- ✅ **对战历史同步**：获取TOP500选手之间的对战历史（最近365天，10,000+场比赛）
- ✅ **完整Web界面**：现代化的Vue 3前端，支持浏览、搜索、筛选、排行榜展示
- ✅ **RESTful API**：FastAPI后端，提供完整的CRUD操作
- ✅ **数据验证**：内置验证工具，确保数据完整性和准确性

### 技术亮点
- **智能同步**：批量请求 + 自动去重 + 进度显示
- **真实排名数据**：直接同步Aligulac Current Ranking
- **完整对战信息**：比分、赛事、BO类型、线上/线下标记
- **响应式设计**：支持多设备访问
- **模块化架构**：前后端分离，易于扩展

## ⚡ 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- Aligulac API Key（已配置）

### 安装步骤

1. **配置API Key**（已完成）
   ```bash
   # backend/.env 文件中已配置：
   ALIGULAC_API_KEY=9nqUtPDwCbcF2DdMOAdP
   ```

2. **安装依赖**
   ```bash
   # 后端依赖
   cd backend
   pip install -r requirements.txt
   
   # 前端依赖
   cd frontend
   npm install
   ```

3. **启动服务**
   ```bash
   # 终端1：启动后端
   cd backend
   python main.py
   
   # 终端2：启动前端
   cd frontend
   npm run dev
   ```

4. **访问应用**
   打开浏览器访问：`http://localhost:5173`

## 📊 数据同步

### 同步TOP500选手（推荐）
```bash
cd scripts
python sync_data.py players          # 同步TOP500选手（5-10分钟）
python sync_data.py history          # 同步对战历史（15-30分钟）
python verify_sync.py                # 验证数据
python verify_matches.py             # 验证对战数据
```

### 命令行工具
| 命令 | 功能 | 预计时间 |
|------|------|----------|
| `python sync_data.py players` | 同步TOP500选手 | 5-10分钟 |
| `python sync_data.py history` | 同步对战历史 | 15-30分钟 |
| `python sync_data.py matches` | 同步最近比赛 | 2-5分钟 |
| `python verify_sync.py` | 验证选手数据 | <1分钟 |
| `python verify_matches.py` | 验证对战数据 | <1分钟 |

## 📈 数据规模

### 当前数据（2026年1月）
- **职业选手**: 301名活跃职业选手
- **对战记录**: 1,000+场比赛（持续同步中）
- **时间范围**: 最近365天
- **选手分布**: KR(韩国), CN(中国), US(美国), RU(俄罗斯)等
- **种族分布**: 神族(35.8%), 人族(31.5%), 虫族(31.8%)

### TOP10选手（当前排名）
1. **Serral** (Z - FI) - 评分: 2.68
2. **Clem** (T - FR) - 评分: 2.59
3. **herO** (P - KR) - 评分: 2.55
4. **Maru** (T - KR) - 评分: 2.42
5. **MaxPax** (P - DK) - 评分: 2.39
6. **Classic** (P - KR) - 评分: 2.36
7. **Reynor** (Z - IT) - 评分: 2.35
8. **Solar** (Z - KR) - 评分: 2.32
9. **ByuN** (T - KR) - 评分: 2.15
10. **Oliveira** (Z - CN) - 评分: 2.15

## 🔧 项目结构

```
sc2-prostats/
├── backend/                    # 后端服务
│   ├── main.py                # FastAPI应用入口
│   ├── models/                # 数据库模型
│   ├── services/              # 业务逻辑
│   │   ├── aligulac_service.py    # Aligulac API集成
│   │   └── sync_service.py        # 数据同步服务
│   ├── schemas.py             # Pydantic模型
│   ├── requirements.txt       # Python依赖
│   └── .env                   # 环境变量
├── frontend/                   # 前端界面
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── services/          # API客户端
│   │   └── App.vue            # 根组件
│   ├── package.json           # Node依赖
│   └── vite.config.js         # Vite配置
├── scripts/                    # 工具脚本
│   ├── sync_data.py           # 主同步脚本
│   ├── verify_sync.py         # 数据验证
│   └── test_api_direct.py     # API测试
├── database/                   # 数据库
│   └── sc2_stats.db           # SQLite数据库
└── docs/                      # 文档
    ├── SETUP.md               # 安装配置指南
    ├── API.md                 # API文档
    ├── SYNC.md                # 数据同步详解
    └── TROUBLESHOOTING.md     # 故障排除
```

## 🚀 使用场景

### 1. 查看选手资料
访问 `http://localhost:5173/players`，浏览TOP500选手列表

### 2. 查看对战历史
点击任意选手，查看其对战记录、胜率、Head-to-Head战绩

### 3. 分析赛事数据
查看各大赛事的比赛数据、选手表现、历史趋势

### 4. 数据导出
通过API导出数据，进行深度分析

## 📖 详细文档

-  **[安装配置指南](docs/SETUP.md)**  - 详细安装步骤、环境配置、依赖安装
-  **[API文档](docs/API.md)**  - 后端API端点、请求/响应格式、示例代码
-  **[数据同步详解](docs/SYNC.md)**  - 同步策略、参数配置、性能优化
-  **[故障排除](docs/TROUBLESHOOTING.md)**  - 常见问题、错误解决、最佳实践

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发建议
1. **后端开发**：遵循FastAPI最佳实践，使用Pydantic进行数据验证
2. **前端开发**：使用Vue 3 Composition API，保持组件模块化
3. **数据库**：使用SQLAlchemy ORM，保持模型清晰
4. **代码风格**：遵循PEP 8规范，保持代码整洁

### 测试
```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

## 📜 许可证

MIT License - 详见 LICENSE 文件

## 🙏 致谢

- [Aligulac](http://aligulac.com) - 提供专业的星际争霸2数据API
- [FastAPI](https://fastapi.tiangolo.com) - 高性能Web框架
- [Vue.js](https://vuejs.org) - 渐进式JavaScript框架
- [Element Plus](https://element-plus.org) - Vue 3 UI组件库

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/yourusername/sc2-prostats/issues)
- **项目地址**: `/home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/`

---

**版本**: v2.0.0  
**最后更新**: 2026-01-19  
**维护者**: xjingyao
