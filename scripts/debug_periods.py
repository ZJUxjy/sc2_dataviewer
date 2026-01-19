#!/usr/bin/env python3
"""
调试period端点，找到当前时间段
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

def debug_periods():
    """调试period端点"""
    print("=== 调试时间段 ===\n")
    
    aligulac = AligulacService()
    
    # 获取period列表
    periods = aligulac._make_request('period', {'limit': 5, 'order_by': '-start'})
    
    if periods and 'objects' in periods:
        print("最近5个时间段：\n")
        for i, period in enumerate(periods['objects'], 1):
            print(f"{i}. ID: {period.get('id')}")
            print(f"   开始: {period.get('start')}")
            print(f"   结束: {period.get('end')}")
            print(f"   名称: {period.get('name')}")
            print()
        
        # 获取当前period（第一个）
        current_period = periods['objects'][0]
        print(f"当前时间段: {current_period.get('id')}")
        print(f"名称: {current_period.get('name')}")
        return current_period.get('id')
    return None

def test_filter_by_period():
    """测试按当前period过滤"""
    print("="*60)
    print("=== 测试按当前period过滤activerating ===\n")
    
    aligulac = AligulacService()
    
    # 获取当前period
    periods = aligulac._make_request('period', {'limit': 1, 'order_by': '-start'})
    if not periods or 'objects' not in periods:
        print("❌ 无法获取时间段")
        return
    
    current_period = periods['objects'][0]
    period_id = current_period.get('id')
    print(f"当前时间段ID: {period_id}\n")
    
    # 按period过滤
    print("🔄 获取当前时间段的activerating...\n")
    ratings = aligulac._make_request('activerating', {
        'limit': 10,
        'order_by': '-rating',
        'period': period_id
    })
    
    if ratings and 'objects' in ratings:
        print(f"获取到 {len(ratings['objects'])} 条记录\n")
        
        # 统计选手
        player_ids = []
        for rating_obj in ratings['objects']:
            player = rating_obj.get('player', {})
            player_id = player.get('id')
            if player_id:
                player_ids.append(player_id)
        
        print("选手ID统计：")
        for pid in set(player_ids):
            count = player_ids.count(pid)
            # 获取选手信息
            player_info = aligulac._make_request(f'player/{pid}')
            if player_info:
                print(f"  ID {pid}: {player_info.get('tag')} - 出现 {count} 次")
        
        print("\n前5名选手：")
        for i, rating_obj in enumerate(ratings['objects'][:5], 1):
            player = rating_obj.get('player', {})
            rating = rating_obj.get('rating')
            tag = player.get('tag', 'N/A')
            race = player.get('race', 'N/A')
            print(f"{i}. {tag} ({race}) - 评分: {rating}")
    else:
        print("无法获取数据")

if __name__ == "__main__":
    print("Period 调试工具")
    print("="*60)
    print()
    
    period_id = debug_periods()
    if period_id:
        test_filter_by_period()
    
    print("\n调试完成")
