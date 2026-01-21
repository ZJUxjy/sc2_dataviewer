# API 调试指南

## 常见问题排查

### 1. 检查 API 连接

```javascript
// 在浏览器控制台测试
fetch('http://localhost:8000/api/ranking')
  .then(res => {
    console.log('Status:', res.status)
    console.log('Content-Type:', res.headers.get('content-type'))
    return res.json()
  })
  .then(data => console.log('Data:', data))
  .catch(err => console.error('Error:', err))
```

### 2. 检查后端日志

后端日志会显示：
- 请求是否到达
- SQL 查询是否执行
- 是否有错误信息

### 3. 常见数据格式问题

#### 问题：数据为 null 或 undefined
```javascript
// 添加默认值
const value = player.current_rating?.toFixed(2) || 'N/A'
const games = player.total_games || 0
```

#### 问题：字段名不匹配
```javascript
// 检查后端返回的字段名
console.log('Sample player:', ranking.value[0])
```

#### 问题：数据类型错误
```javascript
// 确保 win_rate 是数字
const winRate = Number(player.win_rate) || 0
```

### 4. 测试 API 端点

```bash
# 测试排行榜
curl http://localhost:8000/api/ranking

# 测试带参数
curl "http://localhost:8000/api/ranking?limit=10&race=P"

# 检查返回状态码
curl -v http://localhost:8000/api/ranking
```

### 5. 前端错误捕获

```javascript
try {
  const response = await axios.get('/api/ranking')
  console.log('Success:', response)
} catch (error) {
  console.error('Error details:', {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    url: error.config?.url
  })
}
```

### 6. 数据库检查

```bash
# 检查数据库中是否有数据
sqlite3 sc2_stats.db "SELECT COUNT(*) FROM players;"
sqlite3 sc2_stats.db "SELECT tag, race, current_rating FROM players LIMIT 5;"
```

## API 调试技巧

1. **使用浏览器开发者工具**
   - Network 标签查看请求/响应
   - Console 查看 console.log 输出
   - Application 查看 LocalStorage/Cookies

2. **添加请求日志**
```javascript
api.interceptors.request.use(config => {
  console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`, config.params)
  return config
})
```

3. **添加响应日志**
```javascript
api.interceptors.response.use(response => {
  console.log(`API Response: ${response.config.url}`, response.data)
  return response
})
```

4. **检查 CORS 问题**
   - 确保后端允许前端域名
   - 检查 preflight OPTIONS 请求

5. **验证数据完整性**
```javascript
const validatePlayer = (player) => {
  const required = ['player_id', 'tag', 'race']
  const missing = required.filter(field => !player[field])
  if (missing.length > 0) {
    console.warn(`Player missing fields: ${missing.join(', ')}`, player)
  }
}
ranking.value.forEach(validatePlayer)
```
