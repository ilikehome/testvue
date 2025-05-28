import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import User from '../views/User.vue'
import Nav from '../views/Nav.vue'
import Login from '../views/Login.vue' // 新增登录组件导入

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false } // 登录页无需认证
  },
  {
    path: '/',
    name: 'Nav',
    component: Nav,
    meta: { requiresAuth: true } // 导航页需要认证
  },
  {
    path: '/count',
    name: 'Count',
    component: Home,
    meta: { requiresAuth: true } // 学生信息页需要认证
  },
  {
    path: '/user',
    name: 'User',
    component: User,
    meta: { requiresAuth: true } // 用户管理页需要认证
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 导航守卫：检查登录状态
router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    return { path: '/login' } // 未登录跳转到登录页
  }
})

export default router