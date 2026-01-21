#!/usr/bin/env python3
"""
重新计算所有选手的胜负统计数据
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Player, Match, SessionLocal

# 获取数据库会话
db = SessionLocal()

def recalculate_all_player_stats():
    """重新计算所有选手的胜负统计"""
    try:
        # 获取所有选手
        players = db.query(Player).all()
        total_players = len(players)
        
        print(f"开始重新计算 {total_players} 名选手的统计数据...")
        
        for idx, player in enumerate(players, 1):
            player_id = player.id
            
            # 计算作为player1的胜场和负场
            matches_as_p1 = db.query(Match).filter(Match.player1_id == player_id).all()
            wins_as_p1 = sum(1 for m in matches_as_p1 if m.player1_score > m.player2_score)
            losses_as_p1 = sum(1 for m in matches_as_p1 if m.player1_score < m.player2_score)
            
            # 计算作为player2的胜场和负场
            matches_as_p2 = db.query(Match).filter(Match.player2_id == player_id).all()
            wins_as_p2 = sum(1 for m in matches_as_p2 if m.player2_score > m.player1_score)
            losses_as_p2 = sum(1 for m in matches_as_p2 if m.player2_score < m.player1_score)
            
            # 总胜场和负场
            total_wins = wins_as_p1 + wins_as_p2
            total_losses = losses_as_p1 + losses_as_p2
            
            # 更新选手记录
            player.total_wins = total_wins
            player.total_losses = total_losses
            
            if idx % 50 == 0:
                print(f"  进度: {idx}/{total_players} (已更新 {player.tag}: {total_wins}胜 {total_losses}负)")
        
        # 提交更改
        db.commit()
        print(f"✅ 完成！共更新 {total_players} 名选手的统计数据")
        
        # 显示更新后的统计
        print("\n=== 更新后的TOP10选手统计 ===")
        top_players = db.query(Player).order_by(Player.total_wins.desc()).limit(10).all()
        for player in top_players:
            print(f"  {player.tag}: {player.total_wins}胜 {player.total_losses}负")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    recalculate_all_player_stats()
