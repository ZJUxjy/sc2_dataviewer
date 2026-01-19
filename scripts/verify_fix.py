#!/usr/bin/env python3
"""
验证TOP选手数量修复是否生效
"""

import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from services.aligulac_service import AligulacService

print("=== 验证TOP选手数量修复 ===\n")

aligulac = AligulacService()

print("1. 测试 get_current_ranking(limit=50)...")
top50 = aligulac.get_current_ranking(limit=50)
print(f"   ✓ 返回 {len(top50)} 名选手\n")

print("2. 测试提取ID数量...")
top50_ids = {p.get('id') for p in top50 if p.get('id')}
print(f"   ✓ 提取 {len(top50_ids)} 个ID\n")

print("3. 测试 get_matches_for_top_players(TOP50)...")
print("   （限制5场比赛，30天）")
matches = aligulac.get_matches_for_top_players(top50, days_back=30, limit=5)
print(f"   ✓ 返回 {len(matches)} 场比赛\n")

print("=== 验证结果 ===")
if len(top50) >= 45:  # 期望至少45个（50个目标，允许有一点误差）
    print(f"✅ 修复成功！能正确获取 {len(top50)} 名TOP选手")
    print(f"   并从中提取了 {len(top50_ids)} 个选手ID")
    print(f"   最终找到 {len(matches)} 场对战")
else:
    print(f"❌ 修复失败！只获取到 {len(top50)} 名TOP选手")
    sys.exit(1)
