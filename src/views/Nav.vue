<template>
  <div class="nav-container">
    <h1>导航页面</h1>
    <div class="nav-links">
      <router-link to="/count" class="nav-link">学生信息（原Home）</router-link>
      <router-link to="/user" class="nav-link">用户管理</router-link>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

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
</style>