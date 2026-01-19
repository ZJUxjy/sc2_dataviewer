#!/usr/bin/env python3
"""
检查赛事数据
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from models import SessionLocal, Match, Event, Player

def check_events():
    """检查赛事数据"""
    print("=== 赛事数据检查 ===\n")
    
    db = SessionLocal()
    
    # 统计赛事
    total_events = db.query(Event).count()
    print(f"总赛事数: {total_events}\n")
    
    # 显示一些赛事
    events = db.query(Event).limit(20).all()
    print("前20个赛事:")
    for i, e in enumerate(events, 1):
        if i == 1:
            # Python 万能解包用法说明：
            # 1. ** 用于解包字典作为函数的关键字参数（仅适用于字典）
            #    例如: func(**dict) 等同于 func(key1=value1, key2=value2)
            # 2. * 用于解包序列作为位置参数
            #    例如: func(*list) 等同于 func(item1, item2, item3)
            # 
            # 对于对象，需要先转换为字典才能解包：
            # 方法1: 使用 vars() 或 __dict__ 获取对象属性字典
            attrs = {k: v for k, v in vars(e).items() if not k.startswith('_')}
            print("e.__dict__ =", attrs)
            # 方法2: 对于 SQLAlchemy 对象，获取所有列的值
            columns_dict = {c.name: getattr(e, c.name) for c in e.__table__.columns}
            print("e columns =", columns_dict)
            # 方法3: ** 解包的实际应用示例（合并字典）
            extra_info = {"source": "database", "type": "Event"}
            combined = {**columns_dict, **extra_info}  # 合并字典
            print("combined dict =", combined)
            # 方法4: ** 解包用于函数调用（示例）
            def example_func(id=None, name=None, **kwargs):
                return f"ID={id}, Name={name}, Others={kwargs}"
            result = example_func(**columns_dict)  # 将字典解包为关键字参数
            print("example_func result =", result)
        print(f"{i:3d}. ID: {e.id:4d} | Name: '{e.name}' | Full: '{e.full_name}' | Category: '{e.category}'")
    
    print("\n" + "="*60 + "\n")
    
    # 查询一些有代表性的大赛事
    print("搜索包含'Cup'或'League'的赛事:")
    filtered = db.query(Event).filter(
        (Event.name.like('%Cup%')) | (Event.name.like('%League%'))
    ).limit(20).all()
    
    for i, e in enumerate(filtered, 1):
        print(f"{i}. {e.name}")
    
    print("\n" + "="*60 + "\n")
    
    # 检查比赛和赛事的关联
    print("检查比赛中的赛事关联:\n")
    matches = db.query(Match).order_by(Match.date.desc()).limit(10).all()
    
    for i, m in enumerate(matches, 1):
        p1 = db.query(Player).filter(Player.id == m.player1_id).first()
        p2 = db.query(Player).filter(Player.id == m.player2_id).first()
        
        p1_tag = p1.tag if p1 else 'Unknown'
        p2_tag = p2.tag if p2 else 'Unknown'
        
        event = db.query(Event).filter(Event.id == m.event_id).first() if m.event_id else None
        event_name = event.full_name if event else 'None'
        
        print(f"{i}. {p1_tag} vs {p2_tag}")
        print(f"   日期: {m.date}")
        print(f"   比分: {m.player1_score}-{m.player2_score}")
        print(f"   赛事ID: {m.event_id}")
        print(f"   赛事名: {event_name}")
        print()
    
    db.close()

if __name__ == "__main__":
    print("赛事数据检查工具")
    print("="*60)
    print()
    
    check_events()
