#!/usr/bin/env python3
"""
调试对战历史同步问题
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from services.aligulac_service import AligulacService

def debug_matches_sync():
    """调试对战历史同步"""
    print("=== 调试对战历史同步 ===\n")
    
    aligulac = AligulacService()
    
    # 1. 获取TOP500选手
    print("1. 获取TOP500选手...")
    top_players = aligulac.get_current_ranking(limit=500)
    print(f"   获取到 {len(top_players)} 名选手\n")
    
    # 2. 提取选手ID
    top_player_ids = {p.get('id') for p in top_players if p.get('id')}
    print(f"   提取到 {len(top_player_ids)} 个选手ID\n")
    
    # 3. 测试获取比赛
    print("3. 测试获取比赛...")
    print("   尝试获取最近30天，限制10场比赛\n")
    
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        'limit': 10,
        'offset': 0,
        'order_by': '-date',
        'date__gte': start_date.strftime('%Y-%m-%d'),
        'date__lte': end_date.strftime('%Y-%m-%d')
    }
    
    data = aligulac._make_request('match', params)
    
    if not data or 'objects' not in data:
        print("   ❌ 未能获取比赛数据")
        return False
    
    matches = data['objects']
    print(f"   获取到 {len(matches)} 场比赛\n")
    
    # 4. 检查这些比赛中有多少是TOP选手之间的
    print("4. 检查TOP选手之间的比赛:\n")
    top_matches = []
    
    for match in matches:
        pla_id = match.get('pla', {}).get('id')
        plb_id = match.get('plb', {}).get('id')
        
        is_top1 = pla_id in top_player_ids
        is_top2 = plb_id in top_player_ids
        
        print(f"   比赛: {match.get('id')}")
        print(f"     player1: {pla_id} (TOP: {is_top1})")
        print(f"     player2: {plb_id} (TOP: {is_top2})")
        print(f"     是否都是TOP: {is_top1 and is_top2}\n")
        
        if is_top1 and is_top2:
            top_matches.append(match)
    
    print(f"5. 结果: {len(top_matches)}/{len(matches)} 是TOP选手之间的比赛\n")
    
    if len(top_matches) == 0:
        print("   ❌ 没有找到TOP选手之间的比赛")
        print("   可能原因:")
        print("   - 时间段内TOP选手没有比赛")
        print("   - 选手ID不匹配")
    else:
        print(f"   ✅ 找到 {len(top_matches)} 场TOP选手之间的比赛")
    
    return True

if __name__ == "__main__":
    print("对战历史同步调试工具")
    print("="*60)
    print()
    
    try:
        success = debug_matches_sync()
        if success:
            print("\n✓ 调试完成")
        else:
            print("\n✗ 调试失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
