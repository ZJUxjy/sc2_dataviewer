#!/bin/bash

# SC2 Pro Stats 演示启动脚本
# 这个脚本会帮助你快速启动项目

echo "=========================================================================="
echo "              SC2 Pro Stats - 星际争霸2职业选手数据工具"
echo "=========================================================================="
echo ""

# 检查是否安装了Python
echo "检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未安装Python3"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未安装Node.js"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 检查配置文件
echo "检查配置文件..."
if [ ! -f "$PROJECT_DIR/backend/.env" ]; then
    echo "⚠️  警告: backend/.env 文件不存在"
    echo "    请复制 backend/.env.example 到 backend/.env"
    echo "    并填入您的 Aligulac API Key"
    echo "    获取API Key: http://aligulac.com/about/api/"
    echo ""
    read -p "是否继续启动？(y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 显示菜单
echo ""
echo "请选择操作:"
echo "1) 启动后端"
echo "2) 启动前端"
echo "3) 启动后端和前端"
echo "4) 初始化数据库"
echo "5) 同步示例数据"
echo "6) 退出"
echo ""
read -p "输入选项 (1-6): " choice

case $choice in
    1)
        echo "启动后端服务..."
        cd "$PROJECT_DIR/backend"
        echo "请确保已安装依赖: pip install -r requirements.txt"
        python3 main.py
        ;;
    2)
        echo "启动前端服务..."
        cd "$PROJECT_DIR/frontend"
        echo "请确保已安装依赖: npm install"
        npm run dev
        ;;
    3)
        echo "启动后端服务..."
        cd "$PROJECT_DIR/backend"
        
        if [ ! -f "venv" ]; then
            echo "创建虚拟环境..."
            python3 -m venv venv
        fi
        
        # 启动后端（后台运行）
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
            pip install -r requirements.txt
            nohup python3 main.py > backend.log 2>&1 &
            echo "✅ 后端已启动 (查看日志: tail -f backend.log)"
        else
            pip install -r requirements.txt
            nohup python3 main.py > backend.log 2>&1 &
            echo "✅ 后端已启动 (查看日志: tail -f backend.log)"
        fi
        
        sleep 3
        
        echo ""
        echo "启动前端服务..."
        cd "$PROJECT_DIR/frontend"
        npm install
        npm run dev
        ;;
    4)
        echo "初始化数据库..."
        cd "$PROJECT_DIR/scripts"
        python3 init_db.py
        echo "✅ 数据库初始化完成"
        ;;
    5)
        echo "同步示例数据..."
        cd "$PROJECT_DIR/scripts"
        python3 sync_data.py players
        echo ""
        echo "✅ 示例数据同步完成！"
        echo "现在你可以启动后端和前端查看数据了"
        ;;
    6)
        echo "退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "=========================================================================="
echo "                      启动完成！"
echo "=========================================================================="
