#!/usr/bin/env python3
"""
测试Aligulac API返回的数据结构
用于验证current_rating等字段是否存在
"""

import sys
from pathlib import Path
import json

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from services.aligulac_service import AligulacService

def test_api():
    """测试API返回的数据"""
    print("=== 测试Aligulac API ===\n")
    
    try:
        # 创建服务
        aligulac = AligulacService()
        
        print("🔄 获取TOP 5选手数据...\n")
        
        # 获取TOP 5选手
        top_players = aligulac.get_top_players(limit=5)
        
        if not top_players:
            print("❌ 无法获取选手数据")
            return False
        
        print(f"✅ 成功获取 {len(top_players)} 名选手数据\n")
        
        # 显示第一个选手的完整数据结构
        first_player = top_players[0]
        print("=== 第一名选手的完整数据结构 ===\n")
        print(json.dumps(first_player, indent=2))
        
        print("\n" + "="*60)
        print("\n关键字段检查：\n")
        
        # 检查关键字段
        fields_to_check = [
            'id', 'tag', 'name', 'race', 'country',
            'current_rating', 'total_earnings', 'wins', 'losses'
        ]
        
        for field in fields_to_check:
            value = first_player.get(field)
            if value is not None:
                if field == 'current_rating' and isinstance(value, dict):
                    print(f"✅ {field}: {json.dumps(value, indent=2)}")
                else:
                    print(f"✅ {field}: {value}")
            else:
                print(f"❌ {field}: 不存在或为null")
        
        print("\n" + "="*60)
        print("\n选手列表信息：\n")
        
        # 查看所有选手的基本信息
        for i, player in enumerate(top_players, 1):
            tag = player.get('tag', 'N/A')
            race = player.get('race', 'N/A')
            country = player.get('country', 'N/A')
            
            # 获取评分
            rating = 'N/A'
            current_rating = player.get('current_rating')
            if current_rating and isinstance(current_rating, dict):
                rating = current_rating.get('rating', 'N/A')
            elif isinstance(current_rating, (int, float)):
                rating = current_rating
            
            print(f"{i}. {tag} ({race} - {country}) - 评分: {rating}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_endpoints():
    """测试各种API端点"""
    print("\n" + "="*60)
    print("=== 测试不同的API端点 ===\n")
    
    try:
        aligulac = AligulacService()
        
        # 测试获取所有资源
        print("1. 获取API资源列表...")
        response = aligulac._make_request('')
        if response:
            resources = list(response.keys())
            print(f"   ✅ 可用资源: {', '.join(resources)}")
        
        # 检查是否有rating或ranking相关的端点
        print("\n2. 检查rating/ranking相关端点...")
        rating_endpoints = ['rating', 'ranking', 'period', 'player']
        for endpoint in rating_endpoints:
            try:
                test_response = aligulac._make_request(endpoint, {'limit': 1})
                if test_response and 'objects' in test_response:
                    print(f"   ✅ /{endpoint}/ - 可用")
                else:
                    print(f"   ⚠️  /{endpoint}/ - 响应异常")
            except:
                print(f"   ❌ /{endpoint}/ - 不可用")
        
        return True
        
    except Exception as e:
        print(f"❌ 端点测试失败: {e}")
        return False

if __name__ == "__main__":
    print("Aligulac API测试工具")
    print("="*60)
    print()
    
    success1 = test_api()
    success2 = test_all_endpoints()
    
    print("\n" + "="*60)
    print("\n总结：")
    if success1 and success2:
        print("✅ API测试完成，请查看上面的数据结构")
        print("\n下一步：")
        print("如果current_rating字段存在且包含评分数据，")
        print("则可以运行同步脚本将数据保存到数据库")
    else:
        print("❌ 测试遇到问题，请检查错误信息")
        sys.exit(1)
