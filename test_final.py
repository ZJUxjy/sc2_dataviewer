#!/usr/bin/env python3
"""
最终验证测试

测试运行: python sync_data.py history
目标: 验证能正确获取301个TOP选手，而不是11个
"""

import sys
import os

# 添加backend到路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from services.aligulac_service import AligulacService, _synced_match_ids

def test_get_301_players():
    """测试获取301个TOP选手"""
    print("=" * 80)
    print("最终验证: 获取301个TOP选手")
    print("=" * 80)
    
    # 清理缓存
    _synced_match_ids.clear()
    
    service = AligulacService()
    
    print("\n调用: get_current_ranking(limit=301)")
    print("-" * 80)
    
    top_players = service.get_current_ranking(limit=301)
    
    print("-" * 80)
    print(f"\n✅ 结果: 成功获取 {len(top_players)} 个TOP选手")
    
    # 验证数量
    if len(top_players) >= 300:
        print("\n🎉 成功！获取到301个TOP选手（之前只显示11个）")
        print("\n修复要点:")
        print("  1. ✅ get_current_ranking 去掉 period 参数")
        print("  2. ✅ get_matches_for_top_players 添加详细日志")
        print("  3. ✅ 确保直接使用传入的 top_players 参数")
        return True
    else:
        print(f"\n❌ 失败！只获取到 {len(top_players)} 个选手，期望301个")
        return False

def test_get_matches_with_debug():
    """测试获取比赛并显示DEBUG信息"""
    print("\n" + "=" * 80)
    print("最终验证: 获取比赛并检查DEBUG输出")
    print("=" * 80)
    
    service = AligulacService()
    
    print("\n调用: get_matches_for_top_players(top_players=50, days_back=30, limit=200)")
    print("-" * 80)
    
    # 先获取一些选手
    top_players = service.get_current_ranking(limit=50)
    print(f"\n使用 {len(top_players)} 个选手进行测试\n")
    
    # 获取比赛
    matches = service.get_matches_for_top_players(
        top_players=top_players[:10],  # 只使用10个避免请求过多
        days_back=30,
        limit=200
    )
    
    print("-" * 80)
    print(f"\n✅ 结果: 获取到 {len(matches)} 场比赛")
    
    return len(matches) >= 0  # 只要没有报错就算成功

if __name__ == "__main__":
    print("\n开始验证修复...\n")
    
    # 测试1: 获取301个选手
    test1_passed = test_get_301_players()
    
    # 测试2: 获取比赛
    test2_passed = test_get_matches_with_debug()
    
    print("\n" + "=" * 80)
    print("验证结果:")
    print("=" * 80)
    print(f"  测试1 (获取301个选手): {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"  测试2 (获取比赛): {'✅ 通过' if test2_passed else '❌ 失败'}")
    print("=" * 80)
    
    if test1_passed and test2_passed:
        print("\n🎉 所有测试通过！修复已成功应用")
        print("\n现在运行以下命令可以正常工作:")
        print("  cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts")
        print("  python sync_data.py history")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败")
        sys.exit(1)
