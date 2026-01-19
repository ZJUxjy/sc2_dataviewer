#!/usr/bin/env python3
"""
测试前端需要的数据格式
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from models import SessionLocal, Match

def test_match_data():
    """测试比赛数据格式"""
    print("=== 比赛数据格式测试 ===\n")
    
    db = SessionLocal()
    
    try:
        # 获取几场比赛
        matches = db.query(Match).filter(
            Match.player1_score.isnot(None),
            Match.player2_score.isnot(None)
        ).order_by(Match.date.desc()).limit(2).all()
        
        print("数据库中的比赛数据结构：\n")
        for i, m in enumerate(matches, 1):
            print(f"比赛 {i}:")
            print(f"  match.player1_id: {m.player1_id}")
            print(f"  match.player1: {m.player1}")
            print(f"  match.player1.tag: {m.player1.tag if m.player1 else 'None'}")
            print(f"  match.player2_id: {m.player2_id}")
            print(f"  match.player2: {m.player2}")
            print(f"  match.player2.tag: {m.player2.tag if m.player2 else 'None'}")
            print(f"  match.player1_race: {m.player1_race}")
            print(f"  match.player2_race: {m.player2_race}")
            print(f"  match.best_of: {m.best_of}")
            print(f"  match.offline: {m.offline}")
            print()
        
        db.close()
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("前端数据格式测试")
    print("="*60)
    print()
    
    success = test_match_data()
    
    if success:
        print("✅ 测试完成")
    else:
        print("❌ 测试失败")
        sys.exit(1)
