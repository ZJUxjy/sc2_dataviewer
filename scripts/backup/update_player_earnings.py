#!/usr/bin/env python3
"""
更新所有选手的奖金数据
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Player, SessionLocal
from services.aligulac_service import AligulacService
import time

def update_player_earnings():
    """更新所有选手的奖金数据"""
    db = SessionLocal()
    service = AligulacService()
    
    try:
        # 获取所有选手
        players = db.query(Player).all()
        total_players = len(players)
        
        print(f"开始更新 {total_players} 名选手的奖金数据...")
        
        updated = 0
        skipped = 0
        
        for idx, player in enumerate(players, 1):
            aligulac_id = player.aligulac_id
            
            if not aligulac_id:
                print(f"  [{idx}/{total_players}] 跳过 {player.tag}: 无aligulac_id")
                skipped += 1
                continue
            
            try:
                # 获取完整选手数据
                player_detail = service.get_player_by_id(aligulac_id)
                
                if player_detail and 'total_earnings' in player_detail:
                    earnings = player_detail['total_earnings']
                    
                    # 更新奖金数据
                    if earnings != player.total_earnings:
                        player.total_earnings = earnings
                        print(f"  [{idx}/{total_players}] 更新 {player.tag}: ${earnings:,.0f}")
                        updated += 1
                    else:
                        print(f"  [{idx}/{total_players}] {player.tag}: 无需更新 (${earnings:,.0f})")
                else:
                    print(f"  [{idx}/{total_players}]  {player.tag}: 无法获取数据")
                    skipped += 1
                
                # 避免请求过快
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  [{idx}/{total_players}]  {player.tag}: 错误 - {e}")
                skipped += 1
        
        # 提交更改
        db.commit()
        
        print(f"\n✅ 完成！")
        print(f"  更新: {updated} 名选手")
        print(f"  跳过: {skipped} 名选手")
        
        # 显示更新后的TOP10奖金排行榜
        print("\n=== TOP10 奖金排行榜 ===")
        top_earners = db.query(Player).order_by(Player.total_earnings.desc()).limit(10).all()
        for i, player in enumerate(top_earners, 1):
            print(f"  {i}. {player.tag}: ${player.total_earnings:,.0f}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_player_earnings()