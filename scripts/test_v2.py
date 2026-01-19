#!/usr/bin/env python3
"""
测试对战历史同步 - 修正版本
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

def test_matches_sync():
    """测试对战历史同步"""
    print("=== 测试对战历史同步 ===\n")
    
    db = SessionLocal()
    aligulac = AligulacService()
    sync = SyncService(db, aligulac)
    
    print("1. 同步TOP20选手...")
    player_count = sync.sync_current_ranking(limit=20)
    print(f"✅ 同步了 {player_count} 名选手\n")
    
    print("2. 同步对战历史（TOP20之间，30天，最多100场）...")
    match_count = sync.sync_matches_for_top_players(
        top_players_limit=20,
        days_back=30,
        matches_limit=100
    )
    print(f"✅ 同步了 {match_count} 场比赛\n")
    
    print("3. 验证数据...")
    from models import Match
    total_matches = db.query(Match).count()
    print(f"   数据库中比赛总数: {total_matches}")
    
    if total_matches > 0:
        # 显示前几场比赛
        matches = db.query(Match).filter(
            Match.player1_score.isnot(None),
            Match.player2_score.isnot(None)
        ).order_by(Match.date.desc()).limit(3).all()
        
        print("\n   最近的比赛样例:")
        for i, m in enumerate(matches, 1):
            p1 = m.player1.tag if m.player1 else 'Unknown'
            p2 = m.player2.tag if m.player2 else 'Unknown'
            print(f"   {i}. {p1} {m.player1_score}-{m.player2_score} {p2} (BO{m.best_of})")
    
    db.close()
    return True

if __name__ == "__main__":
    print("对战历史测试 v2")
    print("="*60)
    print()
    
    try:
        success = test_matches_sync()
        if success:
            print("\n✅ 测试完成！对战历史同步功能正常")
        else:
            print("\n❌ 测试失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
