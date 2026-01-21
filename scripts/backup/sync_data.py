#!/usr/bin/env python3
"""
数据同步脚本 - 手动同步数据
"""

import sys
import os
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import SessionLocal
from services.aligulac_service import AligulacService
from services.sync_service import SyncService

def sync_all_data():
    """同步所有数据"""
    print("=== 开始数据同步 ===\n")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查API Key
    api_key = os.getenv("ALIGULAC_API_KEY")
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("❌ 错误: 请先在 backend/.env 文件中设置 ALIGULAC_API_KEY")
        print("   获取API Key: http://aligulac.com/about/api/")
        sys.exit(1)
    
    try:
        # 创建数据库会话
        db = SessionLocal()
        
        # 创建服务
        aligulac_service = AligulacService()
        sync_service = SyncService(db, aligulac_service)
        
        print("🔄 开始同步数据...\n")
        
        # 从当前排名同步TOP500选手
        print("1. 从当前排名同步TOP500选手数据...")
        print("   📊 这可能需要5-10分钟，请耐心等待...")
        player_count = sync_service.sync_current_ranking(limit=500)
        print(f"\n   ✅ 从当前排名同步了TOP {player_count} 名选手\n")
        
        # 同步战队
        print("2. 同步战队数据...")
        team_count = sync_service.sync_teams(limit=100)
        print(f"   ✅ 同步了 {team_count} 支战队\n")
        
        # 同步赛事
        print("3. 同步赛事数据...")
        event_count = sync_service.sync_events(limit=1000)
        print(f"   ✅ 同步了 {event_count} 个赛事\n")
        
        print("=== 数据同步完成 ===")
        
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        db.close()

def sync_players_only():
    """仅同步选手数据（TOP500）"""
    print("=== 同步TOP500选手数据 ===\n")
    
    load_dotenv()
    
    # 检查API Key
    api_key = os.getenv("ALIGULAC_API_KEY")
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("❌ 错误: 请先在 backend/.env 文件中设置 ALIGULAC_API_KEY")
        print("   获取API Key: http://aligulac.com/about/api/")
        sys.exit(1)
    
    try:
        db = SessionLocal()
        aligulac_service = AligulacService()
        sync_service = SyncService(db, aligulac_service)
        
        print("🔄 同步TOP500选手数据（多种方式）...")
        print("📊 这可能需要5-10分钟，请耐心等待...")
        print()
        
        # 提供选择：使用当前排名（activerating）或按评分排序
        use_current_ranking = True  # 默认为True，使用真正的当前排名
        
        if use_current_ranking:
            print("使用方式：从当前排名（Current Ranking）同步")
            player_count = sync_service.sync_current_ranking(limit=500)
        else:
            print("使用方式：按评分排序同步")
            player_count = sync_service.sync_top_players(limit=500)
        
        print(f"\n✅ 成功同步TOP {player_count} 名选手")
        
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        db.close()

def sync_matches_only():
    """仅同步比赛数据"""
    print("=== 同步比赛数据 ===\n")
    
    load_dotenv()
    
    try:
        db = SessionLocal()
        aligulac_service = AligulacService()
        sync_service = SyncService(db, aligulac_service)
        
        print("🔄 同步比赛数据...")
        match_count = sync_service.sync_matches(days_back=365, limit=5000)
        print(f"✅ 同步了 {match_count} 场比赛")
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        sys.exit(1)
    
    finally:
        db.close()

def sync_matches_history():
    """同步TOP500选手对战历史"""
    print("=== 同步TOP500选手对战历史 ===\n")
    
    load_dotenv()
    
    # 检查API Key
    api_key = os.getenv("ALIGULAC_API_KEY")
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("❌ 错误: 请先在 backend/.env 文件中设置 ALIGULAC_API_KEY")
        print("   获取API Key: http://aligulac.com/about/api/")
        sys.exit(1)
    
    try:
        # 创建数据库会话
        db = SessionLocal()
        
        # 创建服务
        aligulac_service = AligulacService()
        sync_service = SyncService(db, aligulac_service)
        
        print("🔄 开始同步TOP500选手的对战历史...")
        print("📊 这可能需要较长时间，请耐心等待...")
        print("   预计：15-30分钟（根据网络速度和比赛数量）")
        print()
        
        # 同步对战历史（默认最近365天，最多10000场比赛）
        match_count = sync_service.sync_matches_for_top_players(
            top_players_limit=500,
            days_back=365,  # 1年的对战历史
            matches_limit=20000  # 最多2万场比赛
        )
        
        print(f"\n✅ 成功同步 {match_count} 场对战记录\n")
        
        print("=== 对战历史同步完成 ===")
        
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        db.close()

def sync_top500_players():
    """同步TOP500选手数据"""
    print("=== 同步TOP500选手数据 ===\n")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查API Key
    api_key = os.getenv("ALIGULAC_API_KEY")
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("❌ 错误: 请先在 backend/.env 文件中设置 ALIGULAC_API_KEY")
        print("   获取API Key: http://aligulac.com/about/api/")
        sys.exit(1)
    
    try:
        # 创建数据库会话
        db = SessionLocal()
        
        # 创建服务
        aligulac_service = AligulacService()
        sync_service = SyncService(db, aligulac_service)
        
        print("🔄 开始同步TOP500选手数据（按当前评分排名）...")
        print("📊 这可能需要5-10分钟，请耐心等待...")
        print()
        
        # 使用专门的sync_top_players方法来同步
        player_count = sync_service.sync_top_players(limit=500)
        
        print()
        print(f"✅ 成功同步TOP {player_count} 名选手\n")
        
        print("=== TOP500选手数据同步完成 ===")
        
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        db.close()

def show_help():
    """显示帮助信息"""
    print("""
=== SC2 Pro Stats 数据同步工具 ===

重要提示：使用前必须配置有效的Aligulac API Key
获取地址: http://aligulac.com/about/api/

使用方法:
    python sync_data.py             同步所有数据（TOP500选手、战队、赛事）⭐
    python sync_data.py players     从当前排名同步TOP500选手⭐
    python sync_data.py matches     仅同步比赛（最近30天）
    python sync_data.py ranking     从当前排名同步TOP500选手（与players相同）
    python sync_data.py --help      显示帮助

环境要求:
    - backend/.env 文件中已配置有效的ALIGULAC_API_KEY
    - Python 3.8+ 环境

注意事项:
    - 首次使用必须先配置API Key（见上述获取地址）
    - 选手数据从Aligulac当前排名（Current Ranking）同步
    - API有请求频率限制，建议间隔至少1小时
    - 同步TOP500选手需要5-10分钟

故障排除:
    如果看到"401 Unauthorized"错误，说明API Key无效
    请重新访问 http://aligulac.com/about/api/ 获取有效Key
""")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='SC2 Pro Stats 数据同步工具')
    parser.add_argument('type', nargs='?', default='all', 
                       choices=['all', 'players', 'matches', 'history'],
                       help='同步类型 (all:全部数据, players:TOP500选手, matches:最近比赛, history:对战历史)')
    
    args = parser.parse_args()
    
    if args.type == 'all':
        sync_all_data()
    elif args.type == 'players':
        sync_players_only()
    elif args.type == 'matches':
        sync_matches_only()
    elif args.type == 'history':
        sync_matches_history()
