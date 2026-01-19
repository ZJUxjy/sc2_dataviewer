from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv

from models import Base, SessionLocal, engine, Player, Match, Event, PlayerStats
from services.aligulac_service import AligulacService
from services.sync_service import SyncService
from schemas import PlayerResponse, PlayerDetailResponse, MatchResponse, StatsResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="SC2 Pro Stats API",
    description="星际争霸2职业选手生涯数据API",
    version="1.0.0"
)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 获取Aligulac服务
def get_aligulac_service():
    return AligulacService()

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "SC2 Pro Stats API", "version": "1.0.0"}

@app.get("/api/players", response_model=List[PlayerResponse])
async def get_players(
    skip: int = 0,
    limit: int = 100,
    race: Optional[str] = None,
    country: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取选手列表"""
    query = db.query(Player)
    
    if race:
        query = query.filter(Player.race == race)
    if country:
        query = query.filter(Player.country == country)
    if search:
        query = query.filter(Player.tag.contains(search))
    
    players = query.offset(skip).limit(limit).all()
    return players

@app.get("/api/players/{player_id}", response_model=PlayerDetailResponse)
async def get_player(player_id: int, db: Session = Depends(get_db)):
    """获取单个选手详情"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="选手未找到")
    return player

@app.get("/api/players/{player_id}/matches", response_model=List[MatchResponse])
async def get_player_matches(
    player_id: int,
    limit: int = 50,
    opponent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取选手的比赛记录"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="选手未找到")
    
    query = db.query(Match).filter(
        ((Match.player1_id == player_id) | (Match.player2_id == player_id))
    ).order_by(Match.date.desc())
    
    if opponent_id:
        query = query.filter(
            ((Match.player1_id == player_id) & (Match.player2_id == opponent_id)) |
            ((Match.player2_id == player_id) & (Match.player1_id == opponent_id))
        )
    
    matches = query.limit(limit).all()
    
    # 格式化返回数据，确保包含选手和赛事对象
    result = []
    for match in matches:
        player1 = db.query(Player).filter(Player.id == match.player1_id).first()
        player2 = db.query(Player).filter(Player.id == match.player2_id).first()
        event = db.query(Event).filter(Event.id == match.event_id).first() if match.event_id else None
        
        match_dict = {
            "id": match.id,
            "aligulac_id": match.aligulac_id,
            "date": match.date,
            "player1_id": match.player1_id,
            "player2_id": match.player2_id,
            "player1_race": match.player1_race,
            "player2_race": match.player2_race,
            "player1_score": match.player1_score,
            "player2_score": match.player2_score,
            "best_of": match.best_of,
            "event_id": match.event_id,
            "offline": match.offline,
            # 添加选手基本信息
            "player1": {
                "id": player1.id if player1 else None,
                "tag": player1.tag if player1 else None,
                "name": player1.name if player1 else None,
                "race": player1.race if player1 else None,
                "country": player1.country if player1 else None,
            } if player1 else None,
            "player2": {
                "id": player2.id if player2 else None,
                "tag": player2.tag if player2 else None,
                "name": player2.name if player2 else None,
                "race": player2.race if player2 else None,
                "country": player2.country if player2 else None,
            } if player2 else None,
            # 添加赛事信息（始终包含event字段，即使为None）
            "event": {
                "id": event.id if event else None,
                "name": event.name if event else None,
                "full_name": event.full_name if event else None,
                "category": event.category if event else None,
            },
        }
        result.append(match_dict)
    
    return result

@app.get("/api/players/{player_id}/stats", response_model=StatsResponse)
async def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    """获取选手统计数据"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="选手未找到")
    
    return {
        "player_id": player_id,
        "total_games": player.total_games,
        "wins": player.total_wins,
        "losses": player.total_losses,
        "win_rate": round(player.win_rate * 100, 2)
    }

@app.get("/api/players/{player_id}/head-to-head/{opponent_id}")
async def get_head_to_head(
    player_id: int,
    opponent_id: int,
    db: Session = Depends(get_db)
):
    """获取两名选手的对战记录"""
    player = db.query(Player).filter(Player.id == player_id).first()
    opponent = db.query(Player).filter(Player.id == opponent_id).first()
    
    if not player or not opponent:
        raise HTTPException(status_code=404, detail="选手未找到")
    
    matches = db.query(Match).filter(
        ((Match.player1_id == player_id) & (Match.player2_id == opponent_id)) |
        ((Match.player2_id == player_id) & (Match.player1_id == opponent_id))
    ).order_by(Match.date.desc()).all()
    
    # 统计对战数据
    player_wins = 0
    opponent_wins = 0
    
    for match in matches:
        winner = match.winner
        if winner and winner.id == player_id:
            player_wins += 1
        elif winner and winner.id == opponent_id:
            opponent_wins += 1
    
    total_games = len(matches)
    
    return {
        "player1": {"id": player_id, "tag": player.tag},
        "player2": {"id": opponent_id, "tag": opponent.tag},
        "total_games": total_games,
        "player1_wins": player_wins,
        "player2_wins": opponent_wins,
        "matches": matches
    }

@app.post("/api/sync/players")
async def sync_players(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    aligulac: AligulacService = Depends(get_aligulac_service)
):
    """同步选手数据（后台任务）"""
    sync_service = SyncService(db, aligulac)
    
    def sync_task():
        try:
            sync_service.sync_players()
        except Exception as e:
            logger.error(f"同步失败: {e}")
    
    background_tasks.add_task(sync_task)
    return {"message": "同步任务已启动"}

@app.post("/api/sync/matches")
async def sync_matches(
    background_tasks: BackgroundTasks,
    days: int = 30,
    db: Session = Depends(get_db),
    aligulac: AligulacService = Depends(get_aligulac_service)
):
    """同步比赛数据（后台任务）"""
    sync_service = SyncService(db, aligulac)
    
    def sync_task():
        try:
            sync_service.sync_matches(days_back=days)
        except Exception as e:
            logger.error(f"同步失败: {e}")
    
    background_tasks.add_task(sync_task)
    return {"message": "同步任务已启动"}

@app.post("/api/sync/top-players")
async def sync_top_players(
    background_tasks: BackgroundTasks,
    limit: int = 500,
    db: Session = Depends(get_db),
    aligulac: AligulacService = Depends(get_aligulac_service)
):
    """同步TOP N选手数据（后台任务）"""
    sync_service = SyncService(db, aligulac)
    
    def sync_task():
        try:
            sync_service.sync_top_players(limit=limit)
        except Exception as e:
            logger.error(f"TOP选手同步失败: {e}")
    
    background_tasks.add_task(sync_task)
    return {"message": f"TOP {limit} 选手同步任务已启动"}

@app.get("/api/events", response_model=List[dict])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取赛事列表"""
    query = db.query(Event).order_by(Event.created_at.desc())
    
    if category:
        query = query.filter(Event.category == category)
    
    events = query.offset(skip).limit(limit).all()
    
    return [{
        "id": event.id,
        "aligulac_id": event.aligulac_id,
        "name": event.name,
        "full_name": event.full_name,
        "category": event.category
    } for event in events]

@app.get("/api/races")
async def get_races():
    """获取种族列表"""
    return ["P", "T", "Z", "R"]

@app.get("/api/ranking")
async def get_ranking(
    limit: int = 50,
    race: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取排行榜"""
    query = db.query(Player).filter(Player.active == True)
    
    if race:
        query = query.filter(Player.race == race)
    
    players = query.order_by(
        (Player.total_wins + Player.total_losses).desc(),
        Player.total_wins.desc()
    ).limit(limit).all()
    
    ranking = []
    for idx, player in enumerate(players, 1):
        ranking.append({
            "rank": idx,
            "player_id": player.id,
            "tag": player.tag,
            "race": player.race,
            "country": player.country,
            "total_games": player.total_games,
            "win_rate": round(player.win_rate * 100, 2),
            "total_earnings": player.total_earnings
        })
    
    return ranking

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )