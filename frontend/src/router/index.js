import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn } from '../utils/auth'

import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import TeamList from '../pages/TeamList.vue'
import TeamCreate from '../pages/TeamCreate.vue'
import TeamDetail from '../pages/TeamDetail.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/teams', name: 'teams', component: TeamList, meta: { requiresAuth: true } },
  { path: '/teams/create', name: 'team-create', component: TeamCreate, meta: { requiresAuth: true } },
  { path: '/teams/:id', name: 'team-detail', component: TeamDetail, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const loggedIn = isLoggedIn()

  if (to.meta.requiresAuth && !loggedIn) {
    next('/login')
    return
  }

  if ((to.path === '/login' || to.path === '/register') && loggedIn) {
    next('/home')
    return
  }

  next()
})

export default router