from typing import List, Optional, Set
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Player, Team, Match, Event, PlayerStats
from services.aligulac_service import AligulacService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyncService:
    """数据同步服务"""
    
    def __init__(self, db: Session, aligulac_service: AligulacService):
        self.db = db
        self.aligulac = aligulac_service
    
    def sync_players(self, limit: int = 1000, offset: int = 0) -> int:
        """同步选手数据"""
        logger.info(f"开始同步选手数据，从偏移量 {offset} 开始")
        
        players_data = self.aligulac.get_players(limit=limit, offset=offset)
        if not players_data:
            logger.warning("未能获取选手数据")
            return 0
        
        synced_count = 0
        for player_data in players_data:
            try:
                self._save_player(player_data)
                synced_count += 1
            except Exception as e:
                logger.error(f"同步选手失败 ID {player_data.get('id')}: {e}")
        
        self.db.commit()
        logger.info(f"成功同步 {synced_count} 个选手")
        return synced_count
    
    def sync_top_players(self, limit: int = 500) -> int:
        """
        同步TOP N选手数据（按当前评分排名）
        
        Args:
            limit: 同步的选手数量（默认500）
        
        Returns:
            成功同步的选手数量
        """
        logger.info(f"开始同步TOP {limit} 选手数据")
        
        # 使用get_top_players方法（按评分排序的选手列表）
        players_data = self.aligulac.get_top_players(limit=limit)
        if not players_data:
            logger.warning("未能获取TOP选手数据")
            return 0
        
        logger.info(f"获取到 {len(players_data)} 名选手数据，开始同步...")
        
        synced_count = 0
        for i, player_data in enumerate(players_data, 1):
            try:
                self._save_player(player_data)
                synced_count += 1
                
                # 每同步50个选手打印一次进度
                if i % 50 == 0:
                    logger.info(f"已同步 {i}/{len(players_data)} 名选手...")
                    
            except Exception as e:
                logger.error(f"同步TOP选手失败 ID {player_data.get('id')}: {e}")
                continue
        
        self.db.commit()
        logger.info(f"成功同步TOP {synced_count} 个选手")
        return synced_count
    
    def sync_current_ranking(self, limit: int = 500) -> int:
        """
        从当前排名（Current Ranking）同步TOP N选手
        
        使用activerating端点获取Aligulac网站上显示的当前排名
        
        Args:
            limit: 同步的选手数量（默认500）
        
        Returns:
            成功同步的选手数量
        """
        logger.info(f"开始从当前排名同步TOP {limit} 选手数据")
        
        # 使用get_current_ranking获取真正的当前排名
        players_data = self.aligulac.get_current_ranking(limit=limit)
        if not players_data:
            logger.warning("未能获取当前排名的选手数据")
            return 0
        
        logger.info(f"从当前排名获取到 {len(players_data)} 名选手数据，开始同步...")
        
        synced_count = 0
        for i, player_data in enumerate(players_data, 1):
            try:
                self._save_player(player_data)
                synced_count += 1
                
                # 每同步50个选手打印一次进度
                if i % 50 == 0:
                    logger.info(f"已同步 {i}/{len(players_data)} 名选手...")
                    
            except Exception as e:
                logger.error(f"同步当前排名选手失败 ID {player_data.get('id')}: {e}")
                continue
        
        self.db.commit()
        logger.info(f"成功从当前排名同步 {synced_count} 个选手")
        return synced_count
    
    def _save_player(self, player_data: dict) -> Player:
        """保存选手数据"""
        aligulac_id = player_data.get('id')
        
        # 查询是否已存在
        player = self.db.query(Player).filter(Player.aligulac_id == aligulac_id).first()
        if not player:
            player = Player(aligulac_id=aligulac_id)
            self.db.add(player)
        
        # 更新字段
        player.tag = (player_data.get('tag') or '')[:100]
        player.name = (player_data.get('name') or '')[:200]
        player.romanized_name = (player_data.get('romanized_name') or '')[:200]
        player.country = (player_data.get('country') or '')[:10]
        player.race = (player_data.get('race') or '')[:10]
        
        # 战队信息
        current_teams = player_data.get('current_teams', [])
        if current_teams:
            team_id = current_teams[0].get('team', {}).get('id')
            if team_id:
                team = self._sync_team(current_teams[0].get('team', {}))
                player.team_id = team.id
        
        # 生涯统计
        player.total_earnings = player_data.get('total_earnings', 0.0)
        player.total_wins = player_data.get('wins', 0)
        player.total_losses = player_data.get('losses', 0)
        
        # 当前评分（用于TOP500排名）
        current_rating_data = player_data.get('current_rating')
        if current_rating_data and isinstance(current_rating_data, dict):
            player.current_rating = current_rating_data.get('rating')
        elif isinstance(current_rating_data, (int, float)):
            player.current_rating = current_rating_data
        
        # 出生日期
        birthday = player_data.get('birthday')
        if birthday:
            try:
                player.birth_date = datetime.strptime(birthday.split('T')[0], '%Y-%m-%d')
            except:
                pass
        
        self.db.flush()
        return player
    
    def _sync_team(self, team_data: dict) -> Team:
        """同步战队数据"""
        aligulac_id = team_data.get('id')
        
        team = self.db.query(Team).filter(Team.aligulac_id == aligulac_id).first()
        if not team:
            team = Team(aligulac_id=aligulac_id)
            self.db.add(team)
        
        team.name = (team_data.get('name') or '')[:200]
        team.short_name = (team_data.get('shortname') or '')[:50]
        
        self.db.flush()
        return team
    
    def sync_matches(self, player_id: Optional[int] = None, 
                     days_back: int = 30, limit: int = 1000) -> int:
        """同步比赛数据"""
        logger.info(f"开始同步比赛数据，选手ID: {player_id}")
        
        if player_id:
            matches_data = self.aligulac.get_player_matches(player_id, limit=limit)
        else:
            # 获取最近的比赛
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back) if days_back > 0 else None
            
            # Aligulac API只支持日期格式（YYYY-MM-DD），不支持时间
            start_date_str = None
            if start_date:
                start_date_str = start_date.strftime('%Y-%m-%d')
            
            matches_data = self.aligulac.get_matches(
                limit=limit,
                start_date=start_date_str
            )
        
        if not matches_data:
            logger.warning("未能获取比赛数据")
            return 0
        
        synced_count = 0
        for match_data in matches_data:
            try:
                self._save_match(match_data)
                synced_count += 1
            except Exception as e:
                logger.error(f"同步比赛失败 ID {match_data.get('id')}: {e}")
        
        self.db.commit()
        logger.info(f"成功同步 {synced_count} 场比赛")
        return synced_count
    
    def _save_match(self, match_data: dict) -> Match:
        """保存单场比赛数据"""
        aligulac_id = match_data.get('id')
        
        match = self.db.query(Match).filter(Match.aligulac_id == aligulac_id).first()
        if match:
            return match  # 已存在，跳过
        
        match = Match(aligulac_id=aligulac_id)
        self.db.add(match)
        
        # 日期
        date_str = match_data.get('date')
        if date_str:
            try:
                match.date = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
            except:
                pass
        
        # 选手信息
        pla = match_data.get('pla', {})
        plb = match_data.get('plb', {})
        
        if pla and plb:
            player1 = self._get_or_create_player_basic(pla)
            player2 = self._get_or_create_player_basic(plb)
            
            if player1 and player2:
                match.player1_id = player1.id
                match.player2_id = player2.id
                
                # 种族信息
                match.player1_race = (pla.get('race') or '')[:10]
                match.player2_race = (plb.get('race') or '')[:10]
        
        # 比分
        match.player1_score = match_data.get('sca', 0)
        match.player2_score = match_data.get('scb', 0)
        
        # BO几
        match.best_of = match_data.get('bo', 0)
        
        # 赛事信息
        event_data = match_data.get('eventobj', {})
        if event_data:
            event = self._sync_event(event_data)
            match.event_id = event.id
        
        # 线上线下
        match.offline = match_data.get('offline', False)
        
        self.db.flush()
        return match
    
    def _get_or_create_player_basic(self, player_data: dict) -> Optional[Player]:
        """获取或创建基础选手信息"""
        aligulac_id = player_data.get('id')
        if not aligulac_id:
            return None
        
        player = self.db.query(Player).filter(Player.aligulac_id == aligulac_id).first()
        if not player:
            player = Player(
                aligulac_id=aligulac_id,
                tag=(player_data.get('tag') or '')[:100],
                name=(player_data.get('name') or '')[:200],
                race=(player_data.get('race') or '')[:10]
            )
            self.db.add(player)
            self.db.flush()
        
        return player
    
    def _sync_event(self, event_data: dict) -> Event:
        """同步赛事数据"""
        aligulac_id = event_data.get('id')
        
        event = self.db.query(Event).filter(Event.aligulac_id == aligulac_id).first()
        if not event:
            event = Event(aligulac_id=aligulac_id)
            self.db.add(event)
        
        event.name = (event_data.get('name') or '')[:500]
        event.full_name = (event_data.get('fullname') or '')[:1000]
        event.category = (event_data.get('category') or '')[:100]
        
        self.db.flush()
        return event
    
    def calculate_player_stats(self, player_id: int, period: str = None) -> PlayerStats:
        """计算选手统计数据"""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise ValueError(f"选手不存在 ID: {player_id}")
        
        # 查询该选手的所有比赛
        matches = self.db.query(Match).filter(
            ((Match.player1_id == player_id) | (Match.player2_id == player_id)) &
            (Match.player1_score.isnot(None)) &
            (Match.player2_score.isnot(None))
        ).all()
        
        stats = PlayerStats(player_id=player_id, period=period or 'all')
        
        for match in matches:
            stats.total_games += 1
            
            # 判断胜负
            if match.player1_id == player_id:
                player_score = match.player1_score
                opponent_score = match.player2_score
                opponent_race = match.player2_race
            else:
                player_score = match.player2_score
                opponent_score = match.player1_score
                opponent_race = match.player1_race
            
            if player_score > opponent_score:
                stats.wins += 1
                
                # 种族对战统计
                if opponent_race == 'P':
                    stats.vs_protoss_games += 1
                    stats.vs_protoss_wins += 1
                elif opponent_race == 'T':
                    stats.vs_terran_games += 1
                    stats.vs_terran_wins += 1
                elif opponent_race == 'Z':
                    stats.vs_zerg_games += 1
                    stats.vs_zerg_wins += 1
            else:
                stats.losses += 1
                
                # 种族对战统计
                if opponent_race == 'P':
                    stats.vs_protoss_games += 1
                elif opponent_race == 'T':
                    stats.vs_terran_games += 1
                elif opponent_race == 'Z':
                    stats.vs_zerg_games += 1
        
        # 保存统计数据
        self.db.add(stats)
        self.db.commit()
        
        return stats
    
    def sync_all_data(self, batch_size: int = 500):
        """同步所有数据的主方法"""
        try:
            logger.info("=== 开始全量数据同步 ===")
            
            # 1. 同步顶级选手
            logger.info("同步顶级选手...")
            self.sync_players(limit=batch_size)
            
            # 2. 同步战队
            logger.info("同步战队数据...")
            self.sync_teams()
            
            # 3. 同步赛事
            logger.info("同步赛事数据...")
            self.sync_events()
            
            # 4. 同步最近的比赛
            logger.info("同步比赛数据...")
            self.sync_matches(days_back=90, limit=2000)
            
            logger.info("=== 数据同步完成 ===")
            
        except Exception as e:
            logger.error(f"数据同步失败: {e}")
            self.db.rollback()
            raise
    
    def sync_teams(self, limit: int = 500) -> int:
        """同步战队数据"""
        teams_data = self.aligulac.get_teams(limit=limit)
        if not teams_data:
            return 0
        
        synced_count = 0
        for team_data in teams_data:
            self._sync_team(team_data)
            synced_count += 1
        
        self.db.commit()
        return synced_count
    
    def sync_events(self, limit: int = 500) -> int:
        """同步赛事数据"""
        events_data = self.aligulac.get_events(limit=limit)
        if not events_data:
            return 0
        
        synced_count = 0
        for event_data in events_data:
            self._sync_event(event_data)
            synced_count += 1
        
        self.db.commit()
        return synced_count
    
    def sync_matches_for_top_players(self, top_players_limit: int = 500, 
                                    days_back: int = 365,
                                    matches_limit: int = 10000) -> int:
        """
        同步TOP选手之间的对战历史
        
        Args:
            top_players_limit: TOP选手数量（默认500）
            days_back: 回溯天数（默认365天）
            matches_limit: 最大同步比赛数量（默认10000）
        
        Returns:
            成功同步的比赛数量
        """
        logger.info(f"开始同步TOP {top_players_limit} 选手的对战历史（{days_back} 天）")
        
        # 首先获取TOP选手列表
        logger.info(f"获取TOP {top_players_limit} 选手列表...")
        top_players = self.aligulac.get_current_ranking(limit=top_players_limit)
        
        if not top_players:
            logger.warning("未能获取TOP选手列表")
            return 0
        
        logger.info(f"成功获取TOP {len(top_players)} 选手，开始同步对战历史...")
        
        # 获取TOP选手之间的比赛
        matches_data = self.aligulac.get_matches_for_top_players(
            top_players=top_players,
            days_back=days_back,
            limit=matches_limit
        )
        
        if not matches_data:
            logger.warning("未能获取比赛数据")
            return 0
        
        # 同步比赛数据
        synced_count = 0
        logger.info(f"获取到 {len(matches_data)} 场比赛，开始同步...")
        
        for i, match_data in enumerate(matches_data, 1):
            try:
                # 如果比赛已存在，跳过
                aligulac_id = match_data.get('id')
                if _is_match_synced(aligulac_id):
                    logger.debug(f"比赛 {aligulac_id} 已同步过，跳过")
                    continue
                
                self._save_match(match_data)
                synced_count += 1
                
                # 每同步100场比赛显示一次进度
                if i % 100 == 0:
                    logger.info(f"已同步 {synced_count}/{len(matches_data)} 场比赛...")
                
                # 记录已同步的比赛
                if aligulac_id:
                    _mark_match_as_synced(aligulac_id)
                    
            except Exception as e:
                logger.error(f"同步比赛失败 ID {aligulac_id}: {e}")
                continue
        
        self.db.commit()
        logger.info(f"成功同步 {synced_count} 场比赛")
        return synced_count

# 用于记录已同步的比赛ID，避免重复
def _is_match_synced(match_id: Optional[int]) -> bool:
    """检查比赛是否已同步过"""
    if not match_id:
        return False
    return match_id in _synced_match_ids

def _mark_match_as_synced(match_id: int):
    """标记比赛为已同步"""
    _synced_match_ids.add(match_id)

# 全局变量：记录已同步的比赛ID
_synced_match_ids: Set[int] = set()