import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 选手相关API
export const playerAPI = {
  // 获取选手列表
  getPlayers(params = {}) {
    return api.get('/players', { params })
  },
  
  // 获取单个选手详情
  getPlayer(id) {
    return api.get(`/players/${id}`)
  },
  
  // 搜索选手
  searchPlayers(query) {
    return api.get('/players', { params: { search: query } })
  },
  
  // 获取选手比赛记录
  getPlayerMatches(playerId, params = {}) {
    return api.get(`/players/${playerId}/matches`, { params })
  },
  
  // 获取选手统计数据
  getPlayerStats(playerId) {
    return api.get(`/players/${playerId}/stats`)
  },
  
  // 获取对战历史
  getHeadToHead(playerId, opponentId) {
    return api.get(`/players/${playerId}/head-to-head/${opponentId}`)
  }
}

// 比赛相关API
export const matchAPI = {
  // 获取比赛列表
  getMatches(params = {}) {
    return api.get('/matches', { params })
  }
}

// 排行榜API
export const rankingAPI = {
  getRanking(params = {}) {
    return api.get('/ranking', { params })
  }
}

// 赛事API
export const eventAPI = {
  getEvents(params = {}) {
    return api.get('/events', { params })
  }
}

// 同步API
export const syncAPI = {
  syncPlayers() {
    return api.post('/sync/players')
  },
  
  syncMatches(days = 30) {
    return api.post('/sync/matches', null, { params: { days } })
  },
  
  syncTopPlayers(limit = 500) {
    return api.post('/sync/top-players', null, { params: { limit } })
  }
}

// 其他工具API
export const utilAPI = {
  getRaces() {
    return api.get('/races')
  }
}

export default api
