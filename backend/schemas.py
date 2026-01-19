from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PlayerResponse(BaseModel):
    id: int
    aligulac_id: int
    tag: str
    name: Optional[str]
    romanized_name: Optional[str]
    country: Optional[str]
    race: Optional[str]
    team_id: Optional[int]
    total_earnings: float
    total_wins: int
    total_losses: int
    win_rate: float
    
    class Config:
        from_attributes = True

class PlayerDetailResponse(BaseModel):
    id: int
    aligulac_id: int
    tag: str
    name: Optional[str]
    romanized_name: Optional[str]
    country: Optional[str]
    race: Optional[str]
    team_id: Optional[int]
    total_earnings: float
    total_wins: int
    total_losses: int
    total_games: int
    win_rate: float
    active: bool
    
    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    id: int
    aligulac_id: int
    date: Optional[datetime]
    player1_id: int
    player2_id: int
    player1_race: Optional[str]
    player2_race: Optional[str]
    player1_score: int
    player2_score: int
    best_of: Optional[int]
    event_id: Optional[int]
    offline: bool
    # 添加选手和赛事基本信息，便于前端显示
    player1: Optional[dict]
    player2: Optional[dict]
    event: Optional[dict]
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    player_id: int
    total_games: int
    wins: int
    losses: int
    win_rate: float

class HeadToHeadResponse(BaseModel):
    player1: dict
    player2: dict
    total_games: int
    player1_wins: int
    player2_wins: int

class RankingResponse(BaseModel):
    rank: int
    player_id: int
    tag: str
    race: Optional[str]
    country: Optional[str]
    total_games: int
    win_rate: float
    total_earnings: float

class SyncResponse(BaseModel):
    message: str
    status: str = "success"
