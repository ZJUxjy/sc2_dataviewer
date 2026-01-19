#!/usr/bin/env python3
"""
TOP500同步功能验证脚本
用于检查数据同步是否成功
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from models import SessionLocal, Player
from sqlalchemy import func

def verify_top500_sync():
    """验证TOP500同步结果"""
    print("=== TOP500同步验证 ===\n")
    
    db = SessionLocal()
    
    try:
        # 1. 检查总选手数量
        total_players = db.query(Player).count()
        print(f"1. 数据库中选手总数: {total_players}")
        
        if total_players == 0:
            print("   ❌ 警告: 数据库中没有选手数据，请先运行同步脚本")
            return False
        
        # 2. 检查是否有评分数据
        players_with_rating = db.query(Player).filter(Player.current_rating != None).count()
        print(f"2. 有评分数据的选手: {players_with_rating}")
        
        if players_with_rating == 0 and total_players > 0:
            print("   ⚠️  警告: 选手数据中没有current_rating信息")
            print("   可能原因:")
            print("   - API返回的数据不包含current_rating（需要检查API Key是否有效）")
            print("   - 同步时未正确保存current_rating字段")
            print("   - 数据库结构未更新（需要运行 migrate_add_rating.py）")
        
        # 3. 获取评分最高的10名选手
        print("\n3. 评分TOP 10 选手:")
        print("-" * 60)
        print(f"{'排名':<4} {'ID':<4} {'Tag':<15} {'种族':<4} {'评分':<8} {'国家'}")
        print("-" * 60)
        
        top_players = db.query(Player).filter(
            Player.current_rating != None
        ).order_by(Player.current_rating.desc()).limit(10).all()
        
        for i, player in enumerate(top_players, 1):
            country = player.country or '-'
            race = player.race or '-'
            rating = player.current_rating or 0
            print(f"{i:<4} {player.id:<4} {player.tag:<15} {race:<4} {rating:<8.0f} {country}")
        
        # 4. 种族分布
        print("\n4. 选手种族分布:")
        race_distribution = db.query(
            Player.race, func.count(Player.id)
        ).filter(
            Player.race != None,
            Player.race != ''
        ).group_by(Player.race).all()
        
        race_map = {'P': '神族(Protoss)', 'T': '人族(Terran)', 'Z': '虫族(Zerg)', 'R': '随机(Random)'}
        for race, count in race_distribution:
            race_name = race_map.get(race, race)
            percentage = (count / total_players) * 100 if total_players > 0 else 0
            print(f"   {race_name}: {count}人 ({percentage:.1f}%)")
        
        # 5. 国家分布（TOP 5）
        print("\n5. 国家分布（TOP 5）:")
        country_distribution = db.query(
            Player.country, func.count(Player.id)
        ).filter(
            Player.country != None,
            Player.country != ''
        ).group_by(Player.country).order_by(func.count(Player.id).desc()).limit(5).all()
        
        for country, count in country_distribution:
            percentage = (count / total_players) * 100 if total_players > 0 else 0
            print(f"   {country}: {count}人 ({percentage:.1f}%)")
        
        # 6. 关键统计
        print("\n6. 关键统计:")
        
        # 平均评分
        avg_rating = db.query(func.avg(Player.current_rating)).filter(
            Player.current_rating != None
        ).scalar()
        print(f"   平均评分: {avg_rating:.0f}" if avg_rating else "   平均评分: 无数据")
        
        # 最高评分
        max_rating = db.query(func.max(Player.current_rating)).filter(
            Player.current_rating != None
        ).scalar()
        print(f"   最高评分: {max_rating:.0f}" if max_rating else "   最高评分: 无数据")
        
        # 检查是否有战队信息
        players_with_team = db.query(Player).filter(Player.team_id != None).count()
        print(f"   有战队信息的选手: {players_with_team}人")
        
        # 最终验证结果
        print("\n" + "=" * 60)
        if total_players >= 400:
            print("✅ 验证通过！数据库中有足够多的选手数据")
            print(f"   这应该包含了TOP{total_players}选手的数据")
            return True
        elif total_players >= 100:
            print("⚠️  警告：数据库中选手数量较少（< 400）")
            print("   建议运行: python sync_data.py top500")
            return False
        else:
            print("❌ 错误：数据库中选手数量过少")
            print("   强烈建议运行: python sync_data.py top500")
            return False
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    success = verify_top500_sync()
    sys.exit(0 if success else 1)
