#!/usr/bin/env python3
"""
验证对战历史同步结果
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from models import SessionLocal, Match
from sqlalchemy import func

def verify_matches_sync():
    """验证对战历史同步结果"""
    print("=== 对战历史同步验证 ===\n")
    
    db = SessionLocal()
    
    try:
        # 1. 检查总比赛数量
        total_matches = db.query(Match).count()
        print(f"1. 数据库中比赛总数: {total_matches}")
        
        if total_matches == 0:
            print("   ❌ 警告: 数据库中没有比赛数据，请先运行对战历史同步")
            print("   推荐命令: python sync_data.py history")
            return False
        
        # 2. 检查有比分的比赛
        matches_with_scores = db.query(Match).filter(
            Match.player1_score.isnot(None),
            Match.player2_score.isnot(None)
        ).count()
        print(f"2. 有比分的比赛数量: {matches_with_scores}")
        
        # 3. 按赛事统计
        event_match_count = db.query(
            Match.event_id, func.count(Match.id)
        ).filter(
            Match.event_id.isnot(None)
        ).group_by(Match.event_id).order_by(func.count(Match.id).desc()).limit(5).all()
        
        print("\n3. TOP 5 赛事（按比赛场次）：")
        if event_match_count:
            for event_id, count in event_match_count:
                print(f"   赛事ID {event_id}: {count} 场比赛")
        else:
            print("   （暂无赛事数据）")
        
        # 4. 按时间段统计
        yearly_stats = db.query(
            func.strftime('%Y', Match.date), func.count(Match.id)
        ).filter(Match.date.isnot(None)).group_by(func.strftime('%Y', Match.date)).order_by(func.strftime('%Y', Match.date).desc()).limit(5).all()
        
        print("\n4. 最近5年的比赛数量：")
        if yearly_stats:
            for year, count in yearly_stats:
                print(f"   {year}: {count} 场比赛")
        else:
            print("   （暂无年份数据）")
        
        # 5. 线上 vs 线下
        offline_matches = db.query(Match).filter(Match.offline == True).count()
        online_matches = db.query(Match).filter(Match.offline == False).count()
        
        print(f"\n5. 比赛类型统计：")
        print(f"   线下赛: {offline_matches} 场")
        print(f"   线上赛: {online_matches} 场")
        
        # 6. 关键统计
        print("\n6. 关键统计：")
        
        # 最早的比赛
        oldest_match = db.query(Match).filter(Match.date.isnot(None)).order_by(Match.date).first()
        if oldest_match and oldest_match.date:
            print(f"   最早比赛: {oldest_match.date.strftime('%Y-%m-%d')}")
        
        # 最近的比赛
        newest_match = db.query(Match).filter(Match.date.isnot(None)).order_by(Match.date.desc()).first()
        if newest_match and newest_match.date:
            print(f"   最近比赛: {newest_match.date.strftime('%Y-%m-%d')}")
        
        # BO类型分布
        bo_distribution = db.query(
            Match.best_of, func.count(Match.id)
        ).filter(Match.best_of.isnot(None)).group_by(Match.best_of).order_by(func.count(Match.id).desc()).all()
        
        if bo_distribution:
            print("\n   BO类型分布：")
            for bo, count in bo_distribution:
                print(f"     BO{bo}: {count} 场")
        
        # 最终验证结果
        print("\n" + "=" * 60)
        print("\n验证结果：")
        
        if total_matches >= 100:
            print(f"✅ 验证通过！数据库中有 {total_matches} 场比赛记录")
            
            if total_matches >= 1000:
                print("   ⭐ 比赛数据丰富，可以进行深度分析")
            elif total_matches >= 300:
                print("   ✨ 比赛数据充足，可以进行基本分析")
            else:
                print("   📊 比赛数据初步可用")
            
            return True
        else:
            print(f"⚠️  警告：数据库中比赛数量较少（{total_matches}场）")
            print("   建议运行: python sync_data.py history")
            print("   获取更多对战历史数据")
            return False
        
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

def show_match_samples():
    """显示比赛样例"""
    print("\n" + "="*60)
    print("\n=== 比赛样例 ===\n")
    
    db = SessionLocal()
    
    try:
        # 获取最近的几场比赛
        matches = db.query(Match).filter(
            Match.player1_score.isnot(None),
            Match.player2_score.isnot(None)
        ).order_by(Match.date.desc()).limit(5).all()
        
        if not matches:
            print("暂无比赛数据")
            return
        
        print("最近的比赛：\n")
        for i, match in enumerate(matches, 1):
            p1_tag = match.player1.tag if match.player1 else 'Unknown'
            p2_tag = match.player2.tag if match.player2 else 'Unknown'
            p1_race = match.player1_race or '?'
            p2_race = match.player2_race or '?'
            bo = match.best_of or '?'
            offline = '线下' if match.offline else '线上'
            
            date_str = match.date.strftime('%Y-%m-%d') if match.date else 'Unknown'
            
            print(f"{i}. {date_str}")
            print(f"   {p1_tag} ({p1_race}) {match.player1_score} - {match.player2_score} {p2_tag} ({p2_race})")
            print(f"   BO{bo} | {offline}")
            print()
            
    finally:
        db.close()

if __name__ == "__main__":
    print("对战历史验证工具")
    print("="*60)
    print()
    
    success = verify_matches_sync()
    show_match_samples()
    
    print("\n" + "="*60)
    print("\n操作建议：")
    
    if success:
        print("✅ 对战历史数据已同步，可以开始分析了！")
        print("\n下一步：")
        print("1. 启动后端服务: cd ../backend && python main.py")
        print("2. 启动前端服务: cd ../frontend && npm run dev")
        print("3. 访问 http://localhost:5173 查看对战数据")
        print("\n或者：")
        print("- 分析选手对战记录")
        print("- 计算胜率统计")
        print("- 生成对战图谱")
    else:
        print("同步更多对战历史数据：")
        print("cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts")
        print("python sync_data.py history")
