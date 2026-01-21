import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PlayerList from '../views/PlayerList.vue'
import PlayerDetail from '../views/PlayerDetail.vue'
import Ranking from '../views/Ranking.vue'
import Events from '../views/Events.vue'
import About from '../views/About.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '星际争霸2数据终端 - SC2 Pro Stats'
    }
  },
  {
    path: '/players',
    name: 'PlayerList',
    component: PlayerList,
    meta: {
      title: '职业选手列表 - SC2 Pro Stats'
    }
  },
  {
    path: '/players/:id',
    name: 'PlayerDetail',
    component: PlayerDetail,
    props: true,
    meta: {
      title: '选手详情 - SC2 Pro Stats'
    }
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking,
    meta: {
      title: '全球排行榜 - SC2 Pro Stats'
    }
  },
  {
    path: '/events',
    name: 'Events',
    component: Events,
    meta: {
      title: '赛事记录 - SC2 Pro Stats'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      title: '关于我们 - SC2 Pro Stats'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫 - 更新页面标题
router.beforeEach((to, from, next) => {
  const title = to.meta.title || 'SC2 Pro Stats - 星际争霸2职业选手数据终端'
  document.title = title
  next()
})

export default router
