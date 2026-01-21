#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import sys
import os
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from models import engine, Base

def init_database():
    """初始化数据库，创建所有表"""
    print("开始初始化数据库...")
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功！")
        
        # 显示创建的表
        print("\n创建的表:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
        
        print("\n数据库初始化完成！")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        sys.exit(1)

def test_connection():
    """测试数据库连接"""
    print("测试数据库连接...")
    
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ 数据库连接成功！")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== SC2 Pro Stats 数据库初始化工具 ===\n")
    
    # 测试连接
    test_connection()
    
    # 初始化数据库
    init_database()
    
    print("\n=== 完成 ===")
