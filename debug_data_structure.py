#!/usr/bin/env python3
"""
调试数据结构问题
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.aligulac_service import AligulacService

def debug_top_players_structure():
    """调试TOP选手的数据结构"""
    print("=" * 80)
    print("调试: get_current_ranking 返回的数据结构")
    print("=" * 80)
    
    service = AligulacService()
    
    # 只获取前10个用于调试
    print("\n调用 get_current_ranking(limit=10)...")
    top_players = service.get_current_ranking(limit=10)
    
    print(f"\n返回数量: {len(top_players)}")
    print("\n数据样本:")
    
    for i, player in enumerate(top_players[:5], 1):
        print(f"\n--- 选手 #{i} ---")
        print(f"完整对象: {player}")
        print(f"Keys: {list(player.keys())}")
        print(f"ID: {player.get('id')}")
        print(f"Tag: {player.get('tag')}")
        print(f"Type of ID: {type(player.get('id'))}")
        
    # 检查ID去重情况
    all_ids = []
    for p in top_players:
        pid = p.get('id')
        if pid:
            all_ids.append(pid)
    
    print(f"\nID列表: {all_ids}")
    print(f"唯一ID数量: {len(set(all_ids))}")
    print(f"重复ID: {len(all_ids) - len(set(all_ids))}")

def debug_activerating_structure():
    """调试activerating返回的数据结构"""
    print("\n" + "=" * 80)
    print("调试: get_activeratings 返回的数据结构")
    print("=" * 80)
    
    service = AligulacService()
    
    print("\n调用 get_activeratings(limit=5)...")
    ratings = service.get_activeratings(limit=5)
    
    print(f"\n返回数量: {len(ratings)}")
    print("\n数据样本:")
    
    for i, rating in enumerate(ratings, 1):
        print(f"\n--- Rating #{i} ---")
        print(f"完整对象: {rating}")
        print(f"Keys: {list(rating.keys())}")
        player_data = rating.get('player', {})
        print(f"Player data: {player_data}")
        print(f"Player ID: {player_data.get('id') if player_data else 'N/A'}")
        print(f"Player Tag: {player_data.get('tag') if player_data else 'N/A'}")

if __name__ == "__main__":
    debug_top_players_structure()
    debug_activerating_structure()
