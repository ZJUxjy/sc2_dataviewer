#!/usr/bin/env python3
"""
模拟实际使用场景测试

这个脚本模拟运行: python sync_data.py history
"""

import sys
import os

# 添加backend到路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from services.aligulac_service import AligulacService, _synced_match_ids
from services.sync_service import SyncService
from data.db_client import DBClient
from config.settings import DATABASE_PATH

def test_actual_scenario():
    """模拟实际使用场景"""
    print("=" * 80)
    print("模拟实际场景: 同步TOP301选手的对战历史")
    print("=" * 80)
    
    # 清理缓存
    print(f"\n[DEBUG] 清理前的缓存大小: {len(_synced_match_ids)}")
    _synced_match_ids.clear()
    print(f"[DEBUG] 清理后的缓存大小: {len(_synced_match_ids)}")
    
    try:
        # 初始化服务
        print("\n[STEP 1] 初始化服务...")
        db = DBClient(DATABASE_PATH)
        aligulac = AligulacService()
        sync = SyncService(db, aligulac)
        print("✓ 服务初始化完成")
        
        # 获取TOP 301选手
        print("\n[STEP 2] 获取TOP 301选手...")
        top_players = aligulac.get_current_ranking(limit=301)
        print(f"\n✓ 成功获取 {len(top_players)} 个TOP选手")
        
        if len(top_players) < 300:
            print(f"❌ 错误: 只获取到 {len(top_players)} 个选手，期望至少301个")
            return False
        
        # 显示统计信息
        print(f"\n统计信息:")
        print(f"  - 总选手数: {len(top_players)}")
        player_ids = [p.get('id') for p in top_players if p.get('id')]
        print(f"  - 有效ID数: {len(player_ids)}")
        print(f"  - 唯一ID数: {len(set(player_ids))}")
        
        # 获取比赛（只测试前100个选手，避免请求过多）
        print("\n[STEP 3] 获取TOP选手之间的比赛（最近30天）...")
        test_players = top_players[:100]
        print(f"[DEBUG] 使用 {len(test_players)} 个选手进行测试")
        
        matches = aligulac.get_matches_for_top_players(
            top_players=test_players,
            days_back=30,
            limit=500
        )
        
        print(f"\n✓ 成功获取 {len(matches)} 场比赛")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_actual_scenario()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ 测试成功完成")
    else:
        print("❌ 测试失败")
    print("=" * 80)
