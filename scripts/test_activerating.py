#!/usr/bin/env python3
"""
测试Aligulac API的activerating端点
这个端点可能返回当前排名（current ranking）数据
"""

import sys
from pathlib import Path
import json

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import os
from dotenv import load_dotenv

load_dotenv()

# 临时创建简单的请求，绕过API Key检查
import requests

def test_activerating():
    """测试activerating端点 - 可能这才是真正的当前排名"""
    print("=== 测试Aligulac API - activerating端点 ===\n")
    
    api_key = os.getenv("ALIGULAC_API_KEY")
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("⚠️  警告：API Key无效，无法执行真实请求")
        print("   请先在 backend/.env 文件中设置有效的 ALIGULAC_API_KEY")
        print("   获取地址: http://aligulac.com/about/api/\n")
        
        # 提供一个示例数据结构
        print("基于Aligulac API文档，正确的数据结构应该是：\n")
        print("activerating端点返回的每个对象包含：")
        print("- player: 选手对象")
        print("- rating: 评分数值")
        print("- deviation: 不确定性")
        print("- other fields...\n")
        
        print("示例数据结构：")
        example = {
            "player": {
                "id": 123,
                "tag": "Serral",
                "name": "Joona Sotala",
                "race": "Z",
                "country": "FI"
            },
            "rating": 2850.5,
            "deviation": 50.2,
            "volatility": 0.06
        }
        print(json.dumps(example, indent=2))
        return False
    
    try:
        # 尝试访问activerating端点
        print("🔄 尝试访问 /api/v1/activerating/...\n")
        
        url = "http://aligulac.com/api/v1/activerating/"
        params = {
            'limit': 10,
            'order_by': '-rating',
            'apikey': api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ 成功获取数据！\n")
        print("=== 返回的数据结构 ===\n")
        print(json.dumps(data, indent=2))
        
        return True
        
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ API Key无效或已过期")
            print("   请访问 http://aligulac.com/about/api/ 获取新的API Key\n")
        else:
            print(f"❌ HTTP错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rating_endpoint():
    """测试rating端点"""
    print("\n" + "="*60)
    print("=== 测试Aligulac API - rating端点 ===\n")
    
    api_key = os.getenv("ALIGULAC_API_KEY")
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("⚠️  警告：API Key无效\n")
        return False
    
    try:
        url = "http://aligulac.com/api/v1/rating/"
        params = {
            'limit': 5,
            'order_by': '-rating',
            'apikey': api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ 成功获取rating数据！\n")
        
        if 'objects' in data and data['objects']:
            print("=== 前5个rating对象的结构 ===\n")
            for i, obj in enumerate(data['objects'], 1):
                print(f"--- 第 {i} 个对象 ---")
                print(json.dumps(obj, indent=2))
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ rating端点测试失败: {e}")
        return False

if __name__ == "__main__":
    print("Aligulac API - 当前排名端点测试")
    print("="*60)
    print()
    print("测试目的：找到获取'current ranking'的正确API端点")
    print("="*60)
    print()
    
    success1 = test_activerating()
    success2 = test_rating_endpoint()
    
    print("\n" + "="*60)
    print("\n测试总结：")
    
    if success1 or success2:
        print("✅ 找到正确的API端点！")
        print("   请使用上述成功的端点来获取真正的当前排名数据")
    else:
        print("⚠️  需要先配置有效的API Key才能测试")
        print("\n解决步骤：")
        print("1. 访问 http://aligulac.com/about/api/")
        print("2. 生成新的API Key")
        print("3. 编辑 backend/.env 文件")
        print("4. 将ALIGULAC_API_KEY设置为新的Key")
        print("5. 重新运行此测试脚本")
