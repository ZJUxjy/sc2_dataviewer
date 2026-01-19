import requests
import time
from typing import List, Dict, Optional, Any, Set
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# 用于缓存已同步的比赛ID，避免重复
_synced_match_ids: Set[int] = set()

class AligulacService:
    """
    Aligulac API 服务类
    文档: http://aligulac.com/about/api/
    """
    
    def __init__(self):
        self.api_key = os.getenv("ALIGULAC_API_KEY")
        if not self.api_key:
            raise ValueError("ALIGULAC_API_KEY not found in environment variables")
        
        self.base_url = os.getenv("ALIGULAC_BASE_URL", "http://aligulac.com/api/v1")
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """发送API请求"""
        if params is None:
            params = {}
        
        params['apikey'] = self.api_key
        
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def get_players(self, limit: int = 100, offset: int = 0, 
                   tag: str = None, country: str = None, race: str = None) -> List[Dict]:
        """
        获取选手列表
        
        Args:
            limit: 每页数量
            offset: 偏移量
            tag: 选手标签筛选
            country: 国家筛选
            race: 种族筛选 (P, T, Z)
        """
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-current_rating__rating'  # 按当前评分排序
        }
        
        if tag:
            params['tag__icontains'] = tag
        if country:
            params['country'] = country
        if race:
            params['race'] = race
        
        data = self._make_request('player', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_player_by_id(self, player_id: int) -> Optional[Dict]:
        """获取单个选手详情"""
        return self._make_request(f'player/{player_id}')
    
    def get_player_matches(self, player_id: int, limit: int = 100, 
                          offset: int = 0) -> List[Dict]:
        """获取选手的比赛记录"""
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-date'
        }
        
        data = self._make_request('match', params)
        if data and 'objects' in data:
            # 筛选包含该选手的比赛
            matches = []
            for match in data['objects']:
                if (match.get('pla', {}).get('id') == player_id or 
                    match.get('plb', {}).get('id') == player_id):
                    matches.append(match)
            return matches
        return []
    
    def get_matches(self, limit: int = 100, offset: int = 0, 
                   start_date: str = None, end_date: str = None,
                   event_id: int = None) -> List[Dict]:
        """获取比赛列表"""
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-date'
        }
        
        if start_date:
            params['date__gte'] = start_date
        if end_date:
            params['date__lte'] = end_date
        if event_id:
            params['eventobj'] = event_id
        
        data = self._make_request('match', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_teams(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """获取战队列表"""
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-active'
        }
        
        data = self._make_request('team', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_events(self, limit: int = 100, offset: int = 0, 
                   category: str = None) -> List[Dict]:
        """获取赛事列表"""
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-latest'
        }
        
        if category:
            params['category'] = category
        
        data = self._make_request('event', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_periods(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """获取时间段列表"""
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-start'
        }
        
        data = self._make_request('period', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_top_players(self, limit: int = 500, race: str = None, country: str = None) -> List[Dict]:
        """
        获取TOP N选手列表（按当前评分排序）
        
        Args:
            limit: 返回选手数量（默认500）
            race: 按种族筛选 (P-神族, T-人族, Z-虫族)
            country: 按国家筛选（国家代码，如KR, US, CN等）
        
        Returns:
            选手列表，按评分降序排列
        """
        return self.get_players(
            limit=limit,
            offset=0,
            race=race,
            country=country
        )
    
    def get_activeratings(self, limit: int = 100, offset: int = 0, period_id: int = None) -> List[Dict]:
        """
        获取当前活跃评分（Current Ranking）
        
        这才是真正的当前排名数据，包含最新的评分信息
        
        Args:
            limit: 返回记录数量
            offset: 偏移量
            period_id: 时间段ID（可选，用于过滤当前时间段）
        
        Returns:
            活跃评分列表，每个对象包含player和rating信息
        """
        params = {
            'limit': limit,
            'offset': offset,
            'order_by': '-rating'  # 按评分降序
        }
        
        # 如果提供了period_id，添加到参数中
        if period_id:
            params['period'] = period_id
        
        data = self._make_request('activerating', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_current_ranking(self, limit: int = 500) -> List[Dict]:
        """
        获取当前排名（Current Ranking）TOP N
        
        这才是Aligulac网站上显示的当前排名
        
        Args:
            limit: 返回前N名（默认500）
        
        Returns:
            选手列表，按当前排名排序
        """
        all_players = []
        offset = 0
        batch_size = 50  # 每批50个
        
        print(f"[DEBUG] 开始获取当前排名，目标数量: {limit}")
        
        while len(all_players) < limit:
            remaining = limit - len(all_players)
            current_limit = min(batch_size, remaining)
            
            # 获取activerating（不使用period参数，确保数据完整）
            ratings = self.get_activeratings(limit=current_limit, offset=offset, period_id=None)
            if not ratings:
                print(f"[WARNING] 无法获取更多activerating数据，当前已获取: {len(all_players)}")
                break
            
            print(f"[INFO] 批次 {offset//batch_size + 1}: 获取到 {len(ratings)} 个activerating记录")
            
            # 从activerating对象中提取player信息并附加rating
            valid_count = 0
            for rating_obj in ratings:
                player_data = rating_obj.get('player', {})
                if player_data:
                    # 将rating信息合并到player对象中
                    player_data['current_rating'] = {
                        'rating': rating_obj.get('rating'),
                        'deviation': rating_obj.get('deviation'),
                        'volatility': rating_obj.get('volatility')
                    }
                    all_players.append(player_data)
                    valid_count += 1
            
            print(f"[INFO] 批次 {offset//batch_size + 1}: 提取了 {valid_count} 个有效选手数据，累计: {len(all_players)}")
            
            offset += len(ratings)
            # 避免请求过快
            time.sleep(0.5)
            
            # 检查是否还有更多数据
            if len(ratings) < current_limit:
                print(f"[INFO] 没有更多数据，结束获取。最终数量: {len(all_players)}")
                break
        
        print(f"[SUCCESS] 成功获取 {len(all_players)} 个TOP选手")
        return all_players
    
    def search_players(self, query: str, limit: int = 20) -> List[Dict]:
        """搜索选手"""
        params = {
            'tag__icontains': query,
            'limit': limit,
            'order_by': '-current_rating__rating'
        }
        
        data = self._make_request('player', params)
        if data and 'objects' in data:
            return data['objects']
        return []
    
    def get_player_head_to_head(self, player1_id: int, player2_id: int, 
                               limit: int = 50) -> List[Dict]:
        """获取两名选手的对战历史"""
        # 获取两人的所有比赛并筛选
        p1_matches = self.get_player_matches(player1_id, limit=200)
        head_to_head = []
        
        for match in p1_matches:
            pla_id = match.get('pla', {}).get('id')
            plb_id = match.get('plb', {}).get('id')
            
            if (pla_id == player2_id or plb_id == player2_id):
                head_to_head.append(match)
        
        # 按日期排序（最新的在前）
        head_to_head.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return head_to_head[:limit]
    
    def get_matches_for_top_players(self, top_players: List[Dict], 
                                      days_back: int = 365,
                                      limit: int = 5000) -> List[Dict]:
        """
        获取TOP选手之间的对战历史
        
        Args:
            top_players: TOP选手列表（必须包含 'id' 字段）
            days_back: 回溯天数（默认365天）
            limit: 最大比赛数量
        
        Returns:
            比赛列表，只包含TOP选手之间的对战
        """
        if not top_players:
            return []
        
        # 直接从top_players参数中提取ID（关键：不使用外部获取）
        top_player_ids = {p.get('id') for p in top_players if p.get('id')}
        
        print(f"[DEBUG] 传入的top_players数量: {len(top_players)}")
        print(f"[DEBUG] 提取的TOP选手ID数量: {len(top_player_ids)}")
        
        if not top_player_ids:
            print("[WARNING] 没有有效的TOP选手ID")
            return []
        
        all_matches = []
        offset = 0
        batch_size = 200
        
        # 计算日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        print(f"[INFO] 获取 {days_back} 天内的比赛，TOP选手数量: {len(top_player_ids)}")
        
        while len(all_matches) < limit:
            remaining = limit - len(all_matches)
            current_limit = min(batch_size, remaining)
            
            params = {
                'limit': current_limit,
                'offset': offset,
                'order_by': '-date',
                'date__gte': start_date.strftime('%Y-%m-%d'),
                'date__lte': end_date.strftime('%Y-%m-%d')
            }
            
            data = self._make_request('match', params)
            if not data or 'objects' not in data:
                print(f"[WARNING] 获取比赛数据失败或响应格式错误")
                break
            
            matches = data['objects']
            if not matches:
                print(f"[INFO] 没有更多比赛数据")
                break
            
            # 筛选：只保留TOP选手之间的比赛
            filtered_count = 0
            for match in matches:
                match_id = match.get('id')
                
                # 跳过已同步的比赛
                if match_id in _synced_match_ids:
                    continue
                
                pla_id = match.get('pla', {}).get('id')
                plb_id = match.get('plb', {}).get('id')
                
                # 检查双方是否都是TOP选手
                if pla_id in top_player_ids and plb_id in top_player_ids:
                    all_matches.append(match)
                    _synced_match_ids.add(match_id)
                    filtered_count += 1
            
            print(f"[INFO] 批次 {offset//batch_size + 1}: 获取 {len(matches)} 场，筛选后 {filtered_count} 场TOP对战")
            
            offset += len(matches)
            
            # 避免请求过快
            time.sleep(0.3)
            
            # 检查是否还有更多数据
            if len(matches) < current_limit:
                break
        
        print(f"[SUCCESS] 总共获取 {len(all_matches)} 场TOP选手之间的比赛")
        return all_matches


if __name__ == "__main__":
    # 测试代码
    try:
        service = AligulacService()
        print("AligulacService 初始化成功")
        
        # 测试获取TOP选手
        top_players = service.get_current_ranking(limit=10)
        print(f"成功获取 {len(top_players)} 名TOP选手")
        
        # 测试获取比赛
        if top_players:
            matches = service.get_matches_for_top_players(top_players, days_back=30, limit=100)
            print(f"成功获取 {len(matches)} 场比赛")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
