import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import User from '../views/User.vue'
import Nav from '../views/Nav.vue' // 新增导航页面导入

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Nav',
    component: Nav // 根路径指向导航页面
  },
  {
    path: '/count',
    name: 'Count',
    component: Home // 原Home页面改为/count路径
  },
  {
    path: '/user',
    name: 'User',
    component: User // 保留用户管理路径
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router