#!/usr/bin/env python3
"""
生成数据库可视化 HTML 报告
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'sc2_stats.db')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SC2 Pro Stats - 数据库报告</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f5f7fa; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 40px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #3498db; }}
        .stat-value {{ font-size: 36px; font-weight: bold; color: #2c3e50; margin: 10px 0; }}
        .stat-label {{ color: #7f8c8d; font-size: 14px; text-transform: uppercase; }}
        table {{ width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0; }}
        th {{ background: #3498db; color: white; padding: 15px; text-align: left; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        .race-P {{ color: #9b59b6; font-weight: bold; }}
        .race-T {{ color: #3498db; font-weight: bold; }}
        .race-Z {{ color: #27ae60; font-weight: bold; }}
        .earnings {{ color: #f39c12; font-weight: bold; }}
        .winrate {{ color: #2ecc71; font-weight: bold; }}
        .footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #bdc3c7; color: #95a5a6; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>📊 SC2 Pro Stats 数据库报告</h1>
    <p>生成时间: {timestamp}</p>
    
    <h2>📈 数据概览</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">职业选手</div>
            <div class="stat-value">{player_count}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">比赛记录</div>
            <div class="stat-value">{match_count}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">赛事数量</div>
            <div class="stat-value">{event_count}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">总奖金池</div>
            <div class="stat-value earnings">${total_earnings:,.0f}</div>
        </div>
    </div>

    <h2>🏆 TOP 20 选手排行</h2>
    <table>
        <thead>
            <tr>
                <th>排名</th>
                <th>选手</th>
                <th>种族</th>
                <th>国籍</th>
                <th>评分</th>
                <th>奖金</th>
                <th>胜负记录</th>
                <th>胜率</th>
            </tr>
        </thead>
        <tbody>
            {top_players}
        </tbody>
    </table>

    <h2>💰 奖金排行榜 TOP 15</h2>
    <table>
        <thead>
            <tr>
                <th>排名</th>
                <th>选手</th>
                <th>总奖金</th>
                <th>主要种族</th>
            </tr>
        </thead>
        <tbody>
            {top_earnings}
        </tbody>
    </table>

    <h2>⚔️ 最多比赛场次 TOP 15</h2>
    <table>
        <thead>
            <tr>
                <th>排名</th>
                <th>选手</th>
                <th>总场次</th>
                <th>胜负记录</th>
                <th>胜率</th>
            </tr>
        </thead>
        <tbody>
            {most_matches}
        </tbody>
    </table>

    <div class="footer">
        数据库路径: {db_path}<br>
        可通过浏览器查看此报告
    </div>
</body>
</html>
"""

def generate_report():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 基础统计
    cursor.execute("SELECT COUNT(*) as count FROM players")
    player_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM matches")
    match_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM events")
    event_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT SUM(total_earnings) as total FROM players")
    total_earnings = cursor.fetchone()['total'] or 0
    
    # TOP 20 选手（按评分）
    cursor.execute("""
        SELECT tag, race, country, current_rating, total_earnings, total_wins, total_losses
        FROM players 
        ORDER BY current_rating DESC 
        LIMIT 20
    """)
    top_players = cursor.fetchall()
    
    top_players_html = ""
    for i, p in enumerate(top_players, 1):
        win_rate = (p['total_wins'] / (p['total_wins'] + p['total_losses']) * 100) if (p['total_wins'] + p['total_losses']) > 0 else 0
        top_players_html += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{p['tag']}</strong></td>
                <td class="race-{p['race']}">{p['race']}</td>
                <td>{p['country']}</td>
                <td>{p['current_rating']:.2f}</td>
                <td class="earnings">${p['total_earnings']:,.0f}</td>
                <td>{p['total_wins']}-{p['total_losses']}</td>
                <td class="winrate">{win_rate:.1f}%</td>
            </tr>
        """
    
    # 奖金排行榜 TOP 15
    cursor.execute("""
        SELECT tag, total_earnings, race
        FROM players 
        WHERE total_earnings > 0
        ORDER BY total_earnings DESC 
        LIMIT 15
    """)
    top_earnings = cursor.fetchall()
    
    top_earnings_html = ""
    for i, p in enumerate(top_earnings, 1):
        top_earnings_html += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{p['tag']}</strong></td>
                <td class="earnings">${p['total_earnings']:,.0f}</td>
                <td class="race-{p['race']}">{p['race']}</td>
            </tr>
        """
    
    # 最多比赛场次 TOP 15
    cursor.execute("""
        SELECT tag, (total_wins + total_losses) as total_games, total_wins, total_losses
        FROM players 
        WHERE (total_wins + total_losses) > 0
        ORDER BY total_games DESC 
        LIMIT 15
    """)
    most_matches = cursor.fetchall()
    
    most_matches_html = ""
    for i, p in enumerate(most_matches, 1):
        win_rate = (p['total_wins'] / p['total_games'] * 100) if p['total_games'] > 0 else 0
        most_matches_html += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{p['tag']}</strong></td>
                <td>{p['total_games']}</td>
                <td>{p['total_wins']}-{p['total_losses']}</td>
                <td class="winrate">{win_rate:.1f}%</td>
            </tr>
        """
    
    conn.close()
    
    # 生成HTML
    html = HTML_TEMPLATE.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        db_path=DB_PATH,
        player_count=player_count,
        match_count=match_count,
        event_count=event_count,
        total_earnings=total_earnings,
        top_players=top_players_html,
        top_earnings=top_earnings_html,
        most_matches=most_matches_html
    )
    
    # 保存到文件
    output_path = os.path.join(os.path.dirname(__file__), '..', 'database_report.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 报告已生成: {output_path}")
    print(f"📊 数据概览: {player_count}名选手, {match_count}场比赛, ${total_earnings:,.0f}总奖金")
    print(f"🌐 用浏览器打开查看")

if __name__ == "__main__":
    generate_report()
