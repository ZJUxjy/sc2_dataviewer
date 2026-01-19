#!/usr/bin/env python3
"""
直接模拟真实的同步流程
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from models import SessionLocal
from services.aligulac_service import AligulacService
from services.sync_service import SyncService

def direct_test():
    """直接模拟实际的同步调用"""
    print("=== 直接模拟 sync_data.py history ===\n")
    
    db = SessionLocal()
    aligulac = AligulacService()
    sync = SyncService(db, aligulac)
    
    # 完全复制 sync_data.py 中的调用
    print("1. 调用 aligulac.get_current_ranking(limit=500)...")
    top_players = aligulac.get_current_ranking(limit=500)
    print(f"   返回: {len(top_players)} 名选手\n")
    
    print("2. 调用 aligulac.get_matches_for_top_players(top_players, days_back=365, limit=20000)...")
    matches = aligulac.get_matches_for_top_players(top_players, days_back=365, limit=20000)
    print(f"   返回: {len(matches)} 场比赛\n")
    
    db.close()
    
    print("✅ 测试完成！")
    print(f"最终结果: 从 {len(top_players)} 名TOP选手中找到了 {len(matches)} 场比赛")

if __name__ == "__main__":
    print("直接调用测试")
    print("="*60)
    print()
    
    try:
        direct_test()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
