#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加current_rating字段
用于在现有数据库中添加current_rating列
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from models import engine, SessionLocal, Player
from sqlalchemy import text

def migrate_add_current_rating():
    """添加current_rating字段到players表"""
    print("=== 数据库迁移：添加current_rating字段 ===\n")
    
    try:
        # 检查字段是否已存在
        db = SessionLocal()
        result = db.execute(text("PRAGMA table_info(players)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'current_rating' in columns:
            print("✅ current_rating字段已存在，无需迁移")
            return True
        
        # 添加字段
        print("🔄 添加current_rating字段到players表...")
        db.execute(text("ALTER TABLE players ADD COLUMN current_rating FLOAT"))
        db.commit()
        print("✅ 字段添加成功\n")
        
        # 验证
        result = db.execute(text("PRAGMA table_info(players)"))
        columns = [row[1] for row in result.fetchall()]
        if 'current_rating' in columns:
            print("✅ 验证：current_rating字段已成功添加")
        else:
            print("❌ 验证失败：字段未找到")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_add_current_rating()
    
    if success:
        print("\n✅ 数据库迁移完成！")
        print("\n下一步操作：")
        print("1. 运行同步脚本获取评分数据：")
        print("   cd /home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/scripts")
        print("   python sync_data.py players")
        print("\n2. 验证数据：")
        print("   python verify_sync.py")
    else:
        print("\n❌ 迁移失败，请检查错误信息")
        sys.exit(1)
