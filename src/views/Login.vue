<template>
  <div class="login-container">
    <h1>用户登录</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>用户名：</label>
        <input type="text" v-model="username" placeholder="请输入用户名" required>
      </div>
      <div class="form-group">
        <label>密码：</label>
        <input type="password" v-model="password" placeholder="请输入密码" required>
      </div>
      <button type="submit" class="login-btn">登录</button>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  error.value = ''
  try {
    // 调用登录接口（假设后端已提供 /api/login）
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })

    if (!response.ok) throw new Error('用户名或密码错误')
    const data = await response.json()
    if (data.token) {
      localStorage.setItem('token', data.token) // 存储token到本地
      router.push('/') // 登录成功跳转到导航页
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '登录失败'
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 5rem auto;
  padding: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
}
.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}
.login-btn:hover {
  opacity: 0.9;
}
.error-message {
  color: #b71c1c;
  margin-top: 1rem;
  text-align: center;
}
</style>