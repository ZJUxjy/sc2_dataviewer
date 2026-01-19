#!/usr/bin/env python3
"""
测试小规模同步，验证TOP选手数量
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path('../backend/.env'))

from models import SessionLocal
from services.aligulac_service import AligulacService

def test_small():
    """测试小规模同步"""
    print("=== 小规模测试TOP选手数量 ===\n")
    
    aligulac = AligulacService()
    
    print("1. 测试 get_current_ranking(limit=20)...")
    top20 = aligulac.get_current_ranking(limit=20)
    print(f"   返回: {len(top20)} 名选手\n")
    
    print("2. 测试 get_matches_for_top_players(TOP20, 30天, 限制10场)...")
    matches = aligulac.get_matches_for_top_players(top20, days_back=30, limit=10)
    print(f"   返回: {len(matches)} 场比赛\n")
    
    print("✅ 测试完成！")

if __name__ == "__main__":
    print("小规模TOP选手数量测试")
    print("="*60)
    print()
    
    try:
        test_small()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
