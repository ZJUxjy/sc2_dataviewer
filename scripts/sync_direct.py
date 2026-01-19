#!/usr/bin/env python3
"""
直接同步脚本 - 使用明确的参数
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# 加载环境变量
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from models import SessionLocal
from services.aligulac_service import AligulacService
from services.sync_service import SyncService

def sync_top500_direct():
    """直接同步TOP500（绕过复杂逻辑）"""
    print("=== 直接同步TOP500选手 ===\n")
    
    try:
        db = SessionLocal()
        aligulac_service = AligulacService()
        sync_service = SyncService(db, aligulac_service)
        
        print("🔄 获取当前时间段...")
        periods = aligulac_service._make_request('period', {'limit': 1, 'order_by': '-start'})
        
        if periods and 'objects' in periods and periods['objects']:
            current_period_id = periods['objects'][0].get('id')
            print(f"✅ 当前时间段ID: {current_period_id}\n")
        else:
            print("⚠️  无法获取当前时间段，将不使用period过滤\n")
            current_period_id = None
        
        all_players = []
        offset = 0
        batch_size = 50
        limit = 500
        
        print(f"开始获取TOP{limit}选手（每批{batch_size}个）...\n")
        
        while len(all_players) < limit:
            remaining = limit - len(all_players)
            current_limit = min(batch_size, remaining)
            
            params = {
                'limit': current_limit,
                'offset': offset,
                'order_by': '-rating'
            }
            if current_period_id:
                params['period'] = current_period_id
            
            print(f"请求: offset={offset}, limit={current_limit}")
            ratings_response = aligulac_service._make_request('activerating', params)
            
            if not ratings_response or 'objects' not in ratings_response:
                print("❌ 无法获取数据或响应格式错误")
                break
            
            ratings = ratings_response['objects']
            print(f"  成功获取 {len(ratings)} 条记录")
            
            if not ratings:
                break
            
            # 处理数据
            for rating_obj in ratings:
                player_data = rating_obj.get('player', {})
                if player_data:
                    player_data['current_rating'] = {
                        'rating': rating_obj.get('rating'),
                        'deviation': rating_obj.get('deviation'),
                        'volatility': rating_obj.get('volatility')
                    }
                    all_players.append(player_data)
            
            actual_got = len(ratings)
            offset += actual_got
            
            print(f"  总计: {len(all_players)}/{limit} 名选手\n")
            
            if actual_got < current_limit:
                print(f"⚠️  数据不足，停止获取（只获得 {len(all_players)} 名）")
                break
        
        print(f"\n✅ 共获取 {len(all_players)} 名选手数据")
        print("\n开始同步到数据库...")
        
        # 同步到数据库
        synced = 0
        for i, player_data in enumerate(all_players, 1):
            try:
                sync_service._save_player(player_data)
                synced += 1
                if i % 50 == 0:
                    print(f"  已同步 {i}/{len(all_players)} 名...")
            except Exception as e:
                print(f"❌ 同步失败 ID {player_data.get('id')}: {e}")
        
        db.commit()
        print(f"\n✅ 成功同步 {synced} 名选手到数据库")
        
        # 显示前10名
        print("\n前10名选手：")
        all_players_sorted = sorted(all_players, key=lambda x: x.get('current_rating', {}).get('rating', 0), reverse=True)
        for i, p in enumerate(all_players_sorted[:10], 1):
            tag = p.get('tag')
            rating = p.get('current_rating', {}).get('rating', 0)
            print(f"{i:2d}. {tag:<15} - 评分: {rating}")
        
        return synced
        
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return 0
    
    finally:
        db.close()

if __name__ == "__main__":
    print("TOP500同步工具（直接版本）")
    print("="*60)
    print()
    
    count = sync_top500_direct()
    
    if count > 0:
        print("\n" + "="*60)
        print("\n同步完成！请运行验证脚本：")
        print("cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts")
        print("python verify_sync.py")
    else:
        print("\n同步失败")
        sys.exit(1)
