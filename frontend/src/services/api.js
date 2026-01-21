import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API 请求失败:', error)
    return Promise.reject(error)
  }
)

// 选手相关 API
export const playerAPI = {
  getPlayers: (params) => api.get('/api/players', { params }),
  getPlayer: (playerId) => api.get(`/api/players/${playerId}`),
  getPlayerMatches: (playerId, params) => api.get(`/api/players/${playerId}/matches`, { params }),
  getTopPlayers: () => api.get('/api/players/top10'),
  getPlayerStats: (playerId) => api.get(`/api/players/${playerId}/stats`),
  getHeadToHead: (playerId, opponentId) => api.get(`/api/players/${playerId}/head-to-head/${opponentId}`),
}

// 比赛相关 API
export const matchAPI = {
  getMatches: (params) => api.get('/api/matches', { params }),
  getMatch: (matchId) => api.get(`/api/matches/${matchId}`),
}

// 排行榜 API
export const rankingAPI = {
  getRanking: (params) => api.get('/api/ranking', { params }),
}

// 赛事相关 API
export const eventAPI = {
  getEvents: (params) => api.get('/api/events', { params }),
  getTopEvents: (params) => api.get('/api/events/top', { params }),
}

// 同步服务
export const syncAPI = {
  syncPlayers: () => api.post('/api/sync/players'),
  syncMatches: () => api.post('/api/sync/matches'),
  syncTopPlayers: () => api.post('/api/sync/top-players'),
}

// 统计数据 API
export const statsAPI = {
  getStatsSummary: () => api.get('/api/stats/summary'),
  getRaceStats: () => api.get('/api/stats/races'),
  getCountryStats: () => api.get('/api/stats/countries'),
}

export default api
