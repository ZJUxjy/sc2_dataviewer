from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./../database/sc2_stats.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    aligulac_id = Column(Integer, unique=True, index=True)
    tag = Column(String(100), index=True)
    name = Column(String(200))
    romanized_name = Column(String(200))
    country = Column(String(10))
    race = Column(String(10))
    birth_date = Column(DateTime, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    # 当前状态
    active = Column(Boolean, default=True)
    
    # 当前评分（用于TOP500排名）
    current_rating = Column(Float, nullable=True)
    
    # 生涯数据
    total_earnings = Column(Float, default=0.0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    team = relationship("Team", back_populates="players")
    matches_as_p1 = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_p2 = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
    
    @property
    def total_games(self):
        return self.total_wins + self.total_losses
    
    @property
    def win_rate(self):
        if self.total_games == 0:
            return 0.0
        return self.total_wins / self.total_games

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    aligulac_id = Column(Integer, unique=True, index=True)
    name = Column(String(200), index=True)
    short_name = Column(String(50))
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    players = relationship("Player", back_populates="team")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    aligulac_id = Column(Integer, unique=True, index=True)
    date = Column(DateTime)
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"))
    player1_race = Column(String(10))
    player2_race = Column(String(10))
    player1_score = Column(Integer)
    player2_score = Column(Integer)
    best_of = Column(Integer)  # BO3, BO5, etc.
    event_id = Column(Integer, ForeignKey("events.id"))
    offline = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_p1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_p2")
    event = relationship("Event", back_populates="matches")
    
    @property
    def winner(self):
        if self.player1_score > self.player2_score:
            return self.player1
        elif self.player2_score > self.player1_score:
            return self.player2
        return None
    
    @property
    def loser(self):
        if self.player1_score < self.player2_score:
            return self.player1
        elif self.player2_score < self.player1_score:
            return self.player2
        return None

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    aligulac_id = Column(Integer, unique=True, index=True)
    name = Column(String(500))
    full_name = Column(String(1000))
    category = Column(String(100))  # Premier, Major, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    matches = relationship("Match", back_populates="event")

class PlayerStats(Base):
    __tablename__ = "player_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    period = Column(String(10))  # 2024-Q1, 2024-01, etc.
    
    # 总体数据
    total_games = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # 种族对战
    vs_protoss_games = Column(Integer, default=0)
    vs_protoss_wins = Column(Integer, default=0)
    
    vs_terran_games = Column(Integer, default=0)
    vs_terran_wins = Column(Integer, default=0)
    
    vs_zerg_games = Column(Integer, default=0)
    vs_zerg_wins = Column(Integer, default=0)
    
    # 时间戳
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    player = relationship("Player")
    
    @property
    def win_rate(self):
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games
    
    @property
    def vs_protoss_rate(self):
        if self.vs_protoss_games == 0:
            return 0.0
        return self.vs_protoss_wins / self.vs_protoss_games
    
    @property
    def vs_terran_rate(self):
        if self.vs_terran_games == 0:
            return 0.0
        return self.vs_terran_wins / self.vs_terran_games
    
    @property
    def vs_zerg_rate(self):
        if self.vs_zerg_games == 0:
            return 0.0
        return self.vs_zerg_wins / self.vs_zerg_games
