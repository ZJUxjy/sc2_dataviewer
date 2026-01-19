#!/usr/bin/env python3
"""
测试导入服务
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# 设置环境变量
import os
os.environ['ALIGULAC_API_KEY'] = '9nqUtPDwCbcF2DdMOAdP'

from services.aligulac_service import AligulacService

# 测试创建服务
print("Creating AligulacService...")
service = AligulacService()

# 检查方法是否存在
print(f"get_current_ranking exists: {hasattr(service, 'get_current_ranking')}")
print(f"get_matches_for_top_players exists: {hasattr(service, 'get_matches_for_top_players')}")

# 测试简单方法
print("Testing get_top_players...")
top5 = service.get_top_players(limit=3)
print(f"Got {len(top5)} players")

if top5:
    for i, p in enumerate(top5, 1):
        print(f"{i}. {p.get('tag')}")
