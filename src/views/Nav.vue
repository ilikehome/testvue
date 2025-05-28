<template>
  <div class="nav-container">
    <h1>导航页面</h1>
    <div class="nav-links">
      <router-link to="/count" class="nav-link">学生信息（原Home）</router-link>
      <router-link to="/user" class="nav-link">用户管理</router-link>
      <!-- 新增退出按钮 -->
      <button @click="handleLogout" class="nav-link logout-btn">退出登录</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

// 引入路由实例
const router = useRouter()

// 退出登录方法
const handleLogout = () => {
  localStorage.removeItem('token') // 清除本地存储的 Token
  router.push('/login') // 跳转到登录页
}
</script>

<style scoped>
.nav-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  text-align: center;
}
.nav-links {
  margin-top: 2rem;
  display: flex;
  gap: 2rem;
  justify-content: center;
}
.nav-link {
  padding: 0.8rem 1.5rem;
  background: #646cff;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s;
}
.nav-link:hover {
  background: #535bf2;
}

/* 新增退出按钮样式（与导航链接风格一致） */
.logout-btn {
  padding: 0.8rem 1.5rem;
  background: #dc3545; /* 红色表示危险操作 */
  color: white;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s;
  border: none;
  cursor: pointer;
  font-size: 1em; /* 与导航链接字体大小一致 */
}
.logout-btn:hover {
  background: #bb2d3b; /* 悬停颜色加深 */
}
</style>