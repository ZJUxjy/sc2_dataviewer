#!/usr/bin/env python3
"""
调试当前排名数据
检查API返回的数据结构
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import os
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from services.aligulac_service import AligulacService

def debug_current_ranking():
    """调试当前排名数据"""
    print("=== 调试当前排名数据 ===\n")
    
    aligulac = AligulacService()
    
    # 获取TOP 10
    print("🔄 获取TOP 10选手...\n")
    top_players = aligulac.get_current_ranking(limit=10)
    
    print(f"获取到 {len(top_players)} 名选手\n")
    
    for i, player in enumerate(top_players, 1):
        tag = player.get('tag', 'N/A')
        race = player.get('race', 'N/A')
        
        # 检查current_rating结构
        current_rating = player.get('current_rating')
        rating_value = None
        
        if isinstance(current_rating, dict):
            rating_value = current_rating.get('rating')
        elif isinstance(current_rating, (int, float)):
            rating_value = current_rating
            
        print(f"{i}. {tag} ({race}) - current_rating: {current_rating} - rating值: {rating_value}")
    
    print("\n" + "="*60)
    print("\n第一名选手完整数据：")
    if top_players:
        import json
        print(json.dumps(top_players[0], indent=2))
    
    return True
def debug_activeratings():
    """调试activerating端点原始数据"""
    print("\n" + "="*60)
    print("=== 调试activeratings原始数据 ===\n")
    
    aligulac = AligulacService()
    
    ratings = aligulac.get_activeratings(limit=5)
    
    print(f"获取到 {len(ratings)} 个rating对象\n")
    
    import json
    
    for i, rating_obj in enumerate(ratings, 1):
        print(f"--- 第 {i} 个rating对象 ---")
        
        rating = rating_obj.get('rating')
        player_data = rating_obj.get('player', {})
        tag = player_data.get('tag', 'N/A')
        
        print(f"rating值: {rating}")
        print(f"选手: {tag}")
        print(f"完整结构:\n{json.dumps(rating_obj, indent=2)}")
        print()

if __name__ == "__main__":
    print("Current Ranking 调试工具")
    print("="*60)
    print()
    
    debug_current_ranking()
    debug_activeratings()
    
    print("调试完成")
