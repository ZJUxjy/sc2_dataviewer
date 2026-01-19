#!/usr/bin/env python3
"""
直接测试API Key是否有效
"""

import sys
from pathlib import Path
import requests
import os

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_api_key():
    """测试配置的API Key"""
    print("=== 直接测试API Key ===\n")
    
    api_key = os.getenv("ALIGULAC_API_KEY")
    print(f"环境变量中的API Key: {api_key}\n")
    
    if not api_key or api_key == "your-aligulac-api-key-here":
        print("❌ 错误：API Key无效或未被正确加载")
        print("   请确认backend/.env文件已保存并包含正确的Key")
        return False
    
    # 测试基础查询
    url = "http://aligulac.com/api/v1/player/"
    params = {
        'limit': 2,
        'apikey': api_key
    }
    
    print("🔄 正在发送API请求...")
    print(f"URL: {url}")
    print(f"参数: {params}\n")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        print(f"响应状态码: {response.status_code}\n")
        
        if response.status_code == 200:
            print("✅ API Key有效！请求成功！\n")
            data = response.json()
            print("返回的数据：")
            if 'objects' in data:
                print(f"获取到 {len(data['objects'])} 名选手\n")
                for player in data['objects']:
                    print(f"  - {player.get('tag')} ({player.get('race')}) - ID: {player.get('id')}")
            return True
        elif response.status_code == 401:
            print("❌ API Key无效或已过期 (401 Unauthorized)\n")
            print("解决步骤：")
            print("1. 访问 http://aligulac.com/about/api/")
            print("2. 生成新的API Key")
            print("3. 更新backend/.env文件")
            return False
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_activerating():
    """测试activerating端点"""
    print("\n" + "="*60)
    print("=== 测试activerating端点 ===\n")
    
    api_key = os.getenv("ALIGULAC_API_KEY")
    
    url = "http://aligulac.com/api/v1/activerating/"
    params = {
        'limit': 5,
        'order_by': '-rating',
        'apikey': api_key
    }
    
    print("🔄 测试当前排名查询...\n")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            print("✅ activerating端点访问成功！\n")
            data = response.json()
            
            if 'objects' in data:
                print(f"当前排名TOP5选手：\n")
                for i, rating_obj in enumerate(data['objects'], 1):
                    player = rating_obj.get('player', {})
                    rating = rating_obj.get('rating', 0)
                    tag = player.get('tag', 'N/A')
                    race = player.get('race', 'N/A')
                    country = player.get('country', 'N/A')
                    
                    print(f"{i}. {tag} ({race} - {country}) - 评分: {rating}")
            return True
        else:
            print(f"❌ activerating端点访问失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

if __name__ == "__main__":
    print("Aligulac API Key 测试工具")
    print("="*60)
    print()
    
    success1 = test_api_key()
    if success1:
        success2 = test_activerating()
    
    print("\n" + "="*60)
    print("\n测试结果：")
    
    if success1 and (success2 if 'success2' in locals() else True):
        print("✅ API Key有效，可以开始使用同步功能！")
        print("\n下一步操作：")
        print("cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts")
        print("python sync_data.py players  # 从当前排名同步TOP500")
    else:
        print("❌ API Key无效或测试失败")
        print("\n请检查：")
        print("1. backend/.env文件中是否正确配置了API Key")
        print("2. 文件是否已保存")
        print("3. API Key是否有效（访问 http://aligulac.com/about/api/ 生成新的）")
