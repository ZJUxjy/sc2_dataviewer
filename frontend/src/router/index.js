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
    component: Home
  },
  {
    path: '/players',
    name: 'PlayerList',
    component: PlayerList
  },
  {
    path: '/players/:id',
    name: 'PlayerDetail',
    component: PlayerDetail,
    props: true
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/events',
    name: 'Events',
    component: Events
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
