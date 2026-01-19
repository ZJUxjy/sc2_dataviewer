<template>
  <div class="player-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>职业选手列表</h2>
          <div class="header-actions">
            <el-button type="primary" @click="showSyncDialog = true">
              同步数据
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="filters-section">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索选手名称..."
              clearable
              @input="handleSearch"
              prefix-icon="search"
            />
          </el-col>
          <el-col :span="4">
            <el-select
              v-model="selectedRace"
              placeholder="选择种族"
              clearable
              @change="handleFilter"
              style="width: 100%"
            >
              <el-option label="神族 (P)" value="P" />
              <el-option label="人族 (T)" value="T" />
              <el-option label="虫族 (Z)" value="Z" />
              <el-option label="随机 (R)" value="R" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select
              v-model="selectedCountry"
              placeholder="选择国家"
              clearable
              @change="handleFilter"
              style="width: 100%"
            >
              <el-option label="韩国 (KR)" value="KR" />
              <el-option label="中国 (CN)" value="CN" />
              <el-option label="美国 (US)" value="US" />
              <el-option label="欧洲 (EU)" value="EU" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button @click="resetFilters">重置</el-button>
          </el-col>
        </el-row>
      </div>
      
      <!-- 选手列表 -->
      <el-table
        :data="players"
        style="width: 100%"
        v-loading="loading"
        @sort-change="handleSort"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom" />
        <el-table-column prop="tag" label="选手" width="200" sortable="custom">
          <template #default="scope">
            <el-link
              type="primary"
              @click="$router.push(`/players/${scope.row.id}`)"
            >
              {{ scope.row.tag }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="姓名" width="180">
          <template #default="scope">
            {{ scope.row.name || '—' }}
          </template>
        </el-table-column>
        
        <el-table-column prop="race" label="种族" width="100" sortable="custom">
          <template #default="scope">
            <el-tag
              :type="getRaceTagType(scope.row.race)"
              size="small"
              class="race-tag"
            >
              {{ getRaceName(scope.row.race) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="country" label="国家" width="100">
          <template #default="scope">
            {{ getCountryName(scope.row.country) || '—' }}
          </template>
        </el-table-column>
        
        <el-table-column label="胜负统计" width="180">
          <template #default="scope">
            <div class="win-loss-stats">
              <span class="wins">{{ scope.row.total_wins }}胜</span>
              <span class="divider">/</span>
              <span class="losses">{{ scope.row.total_losses }}负</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="胜率" width="120" sortable="custom" prop="win_rate">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.win_rate * 100"
              :color="getWinRateColor(scope.row.win_rate)"
              :stroke-width="8"
              :text-inside="true"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="total_earnings" label="总奖金" width="150" sortable="custom">
          <template #default="scope">
            <span class="earnings">
              ${{ scope.row.total_earnings.toLocaleString() }}
            </span>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handlePageSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
    
    <!-- 同步数据对话框 -->
    <el-dialog
      v-model="showSyncDialog"
      title="同步数据"
      width="500px"
    >
      <p>从Aligulac API同步选手数据，可选择同步推荐选手或TOP500职业选手。</p>
      <el-radio-group v-model="syncType" style="margin-top: 15px;">
        <el-radio value="recommended">同步推荐选手（约200-300名）</el-radio>
        <el-radio value="top500">同步TOP500职业选手（按评分排名）</el-radio>
      </el-radio-group>
      <p style="color: #909399; font-size: 12px; margin-top: 10px;">
        提示：TOP500同步可能需要5-10分钟
      </p>
      <template #footer>
        <el-button @click="showSyncDialog = false">取消</el-button>
        <el-button type="primary" @click="syncData" :loading="syncing">
          开始同步
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { playerAPI, syncAPI } from '../services/api'

const loading = ref(false)
const players = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')
const selectedRace = ref('')
const selectedCountry = ref('')
const showSyncDialog = ref(false)
const syncing = ref(false)
const syncType = ref('recommended') // 'recommended' or 'top500'

const raceMap = {
  'P': '神族',
  'T': '人族',
  'Z': '虫族',
  'R': '随机'
}

const getRaceName = (race) => {
  return raceMap[race] || race || '未知'
}

const getRaceTagType = (race) => {
  const map = {
    'P': 'warning',
    'T': '',
    'Z': 'success',
    'R': 'info'
  }
  return map[race] || 'info'
}

const getWinRateColor = (winRate) => {
  if (winRate >= 0.7) return '#67c23a'
  if (winRate >= 0.5) return '#409eff'
  return '#f56c6c'
}

const getCountryName = (code) => {
  const map = {
    'KR': '韩国',
    'CN': '中国',
    'US': '美国',
    'EU': '欧洲'
  }
  return map[code] || code
}

const loadPlayers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (selectedRace.value) {
      params.race = selectedRace.value
    }
    if (selectedCountry.value) {
      params.country = selectedCountry.value
    }
    
    // 这里假设API返回的是直接的数据
    players.value = await playerAPI.getPlayers(params)
    total.value = players.value.length
  } catch (error) {
    console.error('加载选手失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadPlayers()
}

const handleFilter = () => {
  currentPage.value = 1
  loadPlayers()
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedRace.value = ''
  selectedCountry.value = ''
  currentPage.value = 1
  loadPlayers()
}

const handleSort = ({ prop, order }) => {
  console.log('排序:', prop, order)
  // 实现排序逻辑
}

const handlePageSizeChange = (size) => {
  pageSize.value = size
  loadPlayers()
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadPlayers()
}

const syncData = async () => {
  syncing.value = true
  try {
    if (syncType.value === 'top500') {
      // 同步TOP500选手
      await syncAPI.syncTopPlayers(500)
    } else {
      // 同步推荐选手
      await syncAPI.syncPlayers()
    }
    await syncAPI.syncMatches()
    showSyncDialog.value = false
    loadPlayers()
  } catch (error) {
    console.error('同步失败:', error)
  } finally {
    syncing.value = false
  }
}

onMounted(() => {
  loadPlayers()
})
</script>

<style scoped>
.player-list {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.filters-section {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.race-tag {
  font-weight: bold;
}

.win-loss-stats {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.wins {
  color: #67c23a;
  font-weight: bold;
}

.losses {
  color: #f56c6c;
  font-weight: bold;
}

.divider {
  margin: 0 8px;
  color: #dcdfe6;
}

.earnings {
  color: #e6a23c;
  font-weight: bold;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .filters-section {
    padding: 10px;
  }
}
</style>
