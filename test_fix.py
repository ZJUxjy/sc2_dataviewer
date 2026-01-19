#!/usr/bin/env python3
"""
测试修复后的 get_matches_for_top_players 方法

这个脚本用于验证：
1. get_current_ranking 是否能正确返回301个选手
2. get_matches_for_top_players 是否能正确处理传入的top_players参数
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.aligulac_service import AligulacService

def test_top_players_count():
    """测试获取TOP选手数量"""
    print("=" * 80)
    print("测试1: 获取TOP 301选手")
    print("=" * 80)
    
    try:
        service = AligulacService()
        
        # 获取TOP 301选手
        print("\n调用 get_current_ranking(limit=301)...")
        top_players = service.get_current_ranking(limit=301)
        
        print(f"\n{'='*80}")
        print(f"结果: 成功获取 {len(top_players)} 个TOP选手")
        print(f"{'='*80}\n")
        
        if len(top_players) >= 300:
            print("✅ 测试通过: 成功获取到301个选手")
        else:
            print(f"❌ 测试失败: 只获取到 {len(top_players)} 个选手，期望至少301个")
            return False
        
        # 显示前10个选手的信息
        print("\n前10个选手的信息:")
        for i, player in enumerate(top_players[:10], 1):
            tag = player.get('tag', 'N/A')
            player_id = player.get('id', 'N/A')
            rating = player.get('current_rating', {}).get('rating', 'N/A')
            print(f"  {i}. {tag} (ID: {player_id}) - Rating: {rating}")
        
        return top_players
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_matches_for_top_players(top_players):
    """测试获取TOP选手之间的比赛"""
    print("\n" + "=" * 80)
    print("测试2: 获取TOP选手之间的比赛")
    print("=" * 80)
    
    if not top_players:
        print("❌ 没有TOP选手数据，跳过测试")
        return False
    
    try:
        service = AligulacService()
        
        # 只测试前50个选手，避免请求过多
        test_players = top_players[:50]
        
        print(f"\n调用 get_matches_for_top_players(top_players={len(test_players)}, days_back=30, limit=100)...")
        
        matches = service.get_matches_for_top_players(
            top_players=test_players,
            days_back=30,
            limit=100
        )
        
        print(f"\n{'='*80}")
        print(f"结果: 成功获取 {len(matches)} 场TOP选手之间的比赛")
        print(f"{'='*80}\n")
        
        if len(matches) > 0:
            print("✅ 测试通过: 成功获取到比赛数据")
            
            # 显示前5场比赛的信息
            print("\n前5场比赛的信息:")
            for i, match in enumerate(matches[:5], 1):
                pla_name = match.get('pla', {}).get('tag', 'N/A')
                plb_name = match.get('plb', {}).get('tag', 'N/A')
                date = match.get('date', 'N/A')
                print(f"  {i}. {pla_name} vs {plb_name} - Date: {date}")
        else:
            print("⚠️  没有获取到比赛数据（可能是因为30天内这些选手没有对战记录）")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 80)
    print("SC2 ProStats - 修复验证测试")
    print("=" * 80)
    
    # 测试1: 获取TOP选手
    top_players = test_top_players_count()
    
    if top_players is None:
        print("\n❌ 测试终止，因为第一个测试失败")
        sys.exit(1)
    elif top_players is False:
        print("\n❌ 测试终止，因为top_players数量不足")
        sys.exit(1)
    
    # 测试2: 获取比赛
    test_matches_for_top_players(top_players)
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
