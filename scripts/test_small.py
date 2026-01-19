#!/usr/bin/env python3
"""
小规模测试同步功能
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

def test_small_sync():
    """测试小批量同步"""
    print("=== 小规模测试同步 ===\n")
    
    db = SessionLocal()
    aligulac = AligulacService()
    sync = SyncService(db, aligulac)
    
    print("1. 测试TOP10选手同步...")
    players = aligulac.get_current_ranking(limit=10)
    print(f"   获取到 {len(players)} 名选手\n")
    
    for i, p in enumerate(players[:3], 1):
        tag = p.get('tag')
        rating = p.get('current_rating', {}).get('rating', 'N/A')
        print(f"   {i}. {tag} - 评分: {rating}")
    
    print("\n2. 测试对战历史获取（TOP10之间，30天）...")
    matches = aligulac.get_matches_for_top_players(players, days_back=30, limit=100)
    print(f"   获取到 {len(matches)} 场比赛\n")
    
    if matches:
        for i, m in enumerate(matches[:3], 1):
            p1 = m.get('pla', {}).get('tag', 'N/A')
            p2 = m.get('plb', {}).get('tag', 'N/A')
            score = f"{m.get('sca', '?')}-{m.get('scb', '?')}"
            print(f"   {i}. {p1} {score} {p2}")
    
    db.close()
    return True

if __name__ == "__main__":
    print("小规模测试工具")
    print("="*60)
    print()
    
    try:
        success = test_small_sync()
        if success:
            print("\n✅ 测试成功！功能正常工作")
        else:
            print("\n❌ 测试失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
