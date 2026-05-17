import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Health from '../views/Health.vue'
import Mental from '../views/Mental.vue'
import Sports from '../views/Sports.vue'
import Resources from '../views/Resources.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Map from '../views/Map.vue'
import ArticleDetail from '../views/ArticleDetail.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/health',
    name: 'Health',
    component: Health
  },
  {
    path: '/mental',
    name: 'Mental',
    component: Mental
  },
  {
    path: '/sports',
    name: 'Sports',
    component: Sports
  },
  {
    path: '/resources',
    name: 'Resources',
    component: Resources
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/map',
    name: 'Map',
    component: Map
  },
  {
    path: '/article',
    name: 'ArticleDetail',
    component: ArticleDetail
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, left: 0, behavior: 'auto' }
    }
  }
})

/**
 * 路由守卫 - 全局前置守卫
 * 用于保护需要登录才能访问的页面
 * 
 * 检查逻辑：
 * 1. 获取当前用户登录状态（从 sessionStorage 读取 isLoggedIn）
 * 2. 判断目标路由是否需要登录（meta.requiresAuth 标记）
 * 3. 如果需要登录但用户未登录，重定向到登录页面
 * 4. 否则允许正常访问
 */
router.beforeEach((to, from, next) => {
  // 从 sessionStorage 获取登录状态
  const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true'
  
  // 需要登录才能访问的路由列表
  const requiresAuth = ['Profile']
  
  // 检查目标路由是否需要登录
  if (requiresAuth.includes(to.name) && !isLoggedIn) {
    // 未登录用户尝试访问受保护页面，重定向到登录页
    next({ name: 'Login' })
  } else {
    // 已登录或访问公共页面，允许正常跳转
    next()
  }
})

export default router