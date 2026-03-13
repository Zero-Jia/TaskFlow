import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn } from '../utils/auth'

import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import TeamList from '../pages/TeamList.vue'
import TeamCreate from '../pages/TeamCreate.vue'
import TeamDetail from '../pages/TeamDetail.vue'
import ProjectList from '../pages/ProjectList.vue'
import ProjectCreate from '../pages/ProjectCreate.vue'
import ProjectDetail from '../pages/ProjectDetail.vue'
import ProjectEdit from '../pages/ProjectEdit.vue'
import TaskList from '../pages/TaskList.vue'
import TaskCreate from '../pages/TaskCreate.vue'
import TaskDetail from '../pages/TaskDetail.vue'
import TaskEdit from '../pages/TaskEdit.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/teams', name: 'teams', component: TeamList, meta: { requiresAuth: true } },
  { path: '/teams/create', name: 'team-create', component: TeamCreate, meta: { requiresAuth: true } },
  { path: '/teams/:id', name: 'team-detail', component: TeamDetail, meta: { requiresAuth: true } },
  { path: '/teams/:teamId/projects', name: 'project-list', component: ProjectList, meta: { requiresAuth: true } },
  { path: '/teams/:teamId/projects/create', name: 'project-create', component: ProjectCreate, meta: { requiresAuth: true } },
  { path: '/projects/:id', name: 'project-detail', component: ProjectDetail, meta: { requiresAuth: true } },
  { path: '/projects/:id/edit', name: 'project-edit', component: ProjectEdit, meta: { requiresAuth: true } },
  { path: '/projects/:projectId/tasks',name: 'task-list',component: TaskList,meta: { requiresAuth: true }},
  { path: '/projects/:projectId/tasks/create',name: 'task-create',component: TaskCreate,meta: { requiresAuth: true }},
  {path: '/tasks/:id',name: 'task-detail',component: TaskDetail,meta: { requiresAuth: true }},
  { path: '/tasks/:id/edit', name: 'task-edit', component: TaskEdit, meta: { requiresAuth: true } },
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