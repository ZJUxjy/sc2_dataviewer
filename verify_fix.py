#!/usr/bin/env python3
"""
验证修复是否已正确应用
"""

import os
import sys

# 检查 aligulac_service.py 文件
service_file = '/home/xjingyao/code/js/sc2_dataViewer/sc2-prostats/backend/services/aligulac_service.py'

print("=" * 80)
print("验证修复: get_matches_for_top_players 方法")
print("=" * 80)

# 验证关键点
with open(service_file, 'r') as f:
    content = f.read()

# 检查1: 是否包含DEBUG日志
checks = [
    ('[DEBUG] 传入的top_players数量', '❌ 缺少DEBUG日志: 传入的top_players数量'),
    ('[DEBUG] 提取的TOP选手ID数量', '❌ 缺少DEBUG日志: 提取的TOP选手ID数量'),
    ('[WARNING] 没有有效的TOP选手ID', '❌ 缺少WARNING日志'),
    ('[INFO] 获取', '天内的比赛，TOP选手数量', '❌ 缺少INFO日志'),
    ('[INFO] 批次', '筛选后', '场TOP对战', '❌ 缺少批次处理日志'),
    ('[WARNING] 获取比赛数据失败或响应格式错误', '❌ 缺少错误处理日志'),
    ('[SUCCESS] 总共获取', '场TOP选手之间的比赛', '❌ 缺少SUCCESS日志'),
]

print("\n[检查1] 验证日志输出:")
all_passed = True
for i, check in enumerate(checks, 1):
    # 支持多段文本检查
    if isinstance(check, tuple):
        texts = check[:-1]
        error_msg = check[-1]
        passed = all(text in content for text in texts)
    else:
        passed = check in content
        error_msg = f"❌ 缺少: {check[:50]}"
    
    status = "✅" if passed else "❌"
    print(f"  {i}. {status} {texts if isinstance(texts, tuple) else (check,)}")
    if not passed:
        all_passed = False

# 检查2: 验证代码逻辑
checks = [
    # 检查是否直接使用 top_players 参数
    ('top_player_ids = {p.get(\'id\') for p in top_players if p.get(\'id\')}', '❌ 应为: top_player_ids = {p.get(\'id\')...}'),
    # 检查是否没有重新获取或过滤
    ('if not top_players:', '❌ 缺少空列表检查'),
    # 检查是否使用日期范围而不是period
    ('date__gte\': start_date.strftime(\'%Y-%m-%d\')', '❌ 应使用 date__gte 参数'),
    ('date__lte\': end_date.strftime(\'%Y-%m-%d\')', '❌ 应使用 date__lte 参数'),
]

print("\n[检查2] 验证代码逻辑:")
for i, check in enumerate(checks, 1):
    code, error = check
    passed = code in content
    status = "✅" if passed else "❌"
    print(f"  {i}. {status} {code[:60]}")
    if not passed:
        all_passed = False

# 检查3: 验证get_current_ranking修改
checks = [
    ('period_id=None', '❌ get_current_ranking 应传递 period_id=None'),
    ('[DEBUG] 开始获取当前排名', '❌ 缺少DEBUG日志'),
    ('[INFO] 批次', '获取到', '个activerating记录', '❌ 缺少批次activerating日志'),
    ('[SUCCESS] 成功获取', '个TOP选手', '❌ 缺少SUCCESS日志'),
    ('ratings = self.get_activeratings(limit=current_limit, offset=offset, period_id=None)', '❌ 调用格式错误'),
]

print("\n[检查3] 验证 get_current_ranking 修改:")
for i, check in enumerate(checks, 1):
    if isinstance(check, tuple):
        texts = check[:-1]
        error_msg = check[-1]
        passed = all(text in content for text in texts)
    else:
        passed = check in content
        error_msg = f"❌ 缺少: {check[:50]}"
    
    status = "✅" if passed else "❌"
    print(f"  {i}. {status}")
    if not passed:
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("✅ 所有检查通过！修复已正确应用")
else:
    print("❌ 部分检查失败，请重新应用修复")
print("=" * 80)
