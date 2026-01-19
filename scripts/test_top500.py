#!/usr/bin/env python3
"""
测试TOP500同步是否正常工作
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

def test_top500():
    """测试TOP500同步"""
    print("=== 测试TOP500选手同步 ===\n")
    
    aligulac = AligulacService()
    
    # 测试获取TOP500
    print("🔄 获取TOP500选手...")
    top_players = aligulac.get_current_ranking(limit=500)
    
    print(f"✅ 获取到 {len(top_players)} 名选手\n")
    
    if len(top_players) < 100:
        print(f"⚠️  警告：只获取到 {len(top_players)} 名选手，不是500名")
        print("问题可能原因：")
        print("1. API请求频率限制")
        print("2. 时间段过滤问题")
        print("3. 网络连接问题")
        return False
    
    # 显示TOP10
    print("TOP 10 选手:")
    for i, player in enumerate(top_players[:10], 1):
        tag = player.get('tag', 'N/A')
        race = player.get('race', 'N/A')
        country = player.get('country', 'N/A')
        rating = player.get('current_rating', {}).get('rating', 0)
        print(f"{i:2d}. {tag:<15} ({race}) - {country} - 评分: {rating:.2f}")
    
    print(f"\n✅ 测试成功！成功获取 {len(top_players)} 名TOP选手")
    return True

if __name__ == "__main__":
    print("TOP500同步测试工具")
    print("="*60)
    print()
    
    try:
        success = test_top500()
        if success:
            print("\n✓ 测试通过")
        else:
            print("\n✗ 测试失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
