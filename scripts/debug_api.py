#!/usr/bin/env python3
"""
调试API - 为什么对战历史栏是空的
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from models import SessionLocal, Match, Player
from sqlalchemy import or_

def debug_matches_api():
    """调试比赛API"""
    print("=== 调试API - 为什么对战历史栏是空的 ===\n")
    
    db = SessionLocal()
    
    # 查找herO
    herO = db.query(Player).filter(Player.tag == 'herO').first()
    
    if not herO:
        print("❌ 在数据库中未找到herO")
        db.close()
        return
    
    print(f"✅ 找到herO: ID={herO.id}, 名字={herO.tag}\n")
    
    # 查询数据库中herO的比赛
    db_matches = db.query(Match).filter(
        or_(Match.player1_id == herO.id, Match.player2_id == herO.id)
    ).order_by(Match.date.desc()).all()
    
    print(f"数据库中herO的比赛总数: {len(db_matches)}")
    print(f"前几场比赛:\n")
    
    for i, m in enumerate(db_matches[:5], 1):
        p1 = db.query(Player).filter(Player.id == m.player1_id).first()
        p2 = db.query(Player).filter(Player.id == m.player2_id).first()
        
        p1_tag = p1.tag if p1 else f"Unknown({m.player1_id})"
        p2_tag = p2.tag if p2 else f"Unknown({m.player2_id})"
        
        print(f"{i}. {p1_tag} {m.player1_score}-{m.player2_score} {p2_tag}")
        print(f"   player1对象: {m.player1}")
        print(f"   player2对象: {m.player2}")
        print(f"   player1.tag: {m.player1.tag if m.player1 else 'None'}")
        print(f"   player2.tag: {m.player2.tag if m.player2 else 'None'}")
        print()
    
    db.close()
    
    if len(db_matches) == 0:
        print("❌ 问题确认：数据库中没有herO的比赛数据！")
        print("   请运行: python sync_data.py history")
    else:
        print("✅ 数据库中有数据，问题可能出在后端API或前端")
        print(f"   数据库中有 {len(db_matches)} 场比赛")
        print(f"   但前端显示为空，需要检查:\n")
        print(f"   1. 后端API /api/players/{{id}}/matches 是否返回数据")
        print(f"   2. 前端是否正确调用API并渲染数据")
        print(f"   3. 浏览器控制台是否有错误")

if __name__ == "__main__":
    print("对战历史调试工具")
    print("="*60)
    print()
    
    debug_matches_api()
    
    print("\n诊断完成")
