<template>
    <div class="home-container">
      <h1>Home Page</h1>
      <p>这是主页内容（Vue 3 + TypeScript 项目）</p>
      <!-- 调用接口按钮 -->
      <button @click="fetchStudentInfo" class="api-btn">获取学生信息</button>
      <!-- 状态显示区域 -->
      <div v-if="isLoading" class="result">加载中...</div>
      <div v-else-if="error" class="result error">{{ error }}</div>
      <div v-else-if="studentInfo" class="result">
        <p>姓名：{{ studentInfo.name }}</p>
        <p>手机号：{{ studentInfo.phone }}</p>
        <p>年龄：{{ studentInfo.age }}</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  // 定义学生信息类型
  interface StudentInfo {
    name: string
    phone: string
    age: number
  }
  
  // 响应式状态
  const studentInfo = ref<StudentInfo | null>(null)
  const isLoading = ref(false)
  const error = ref<string>('')
  
  // 动态获取API基地址（根据环境变量）
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
  
  // 接口调用函数
  const fetchStudentInfo = async () => {
    isLoading.value = true
    error.value = ''
    studentInfo.value = null
  
    try {
      // 使用环境变量拼接完整API路径
      const response = await fetch(`${apiBaseUrl}/info`)
      if (!response.ok) throw new Error(`HTTP错误：${response.status}`)
      const data = await response.json()
      // 校验数据格式
      if (!data?.name || !data?.phone || typeof data.age !== 'number') {
        throw new Error('接口返回数据格式不正确')
      }
      studentInfo.value = data as StudentInfo
    } catch (err) {
      error.value = err instanceof Error ? err.message : '接口调用失败'
    } finally {
      isLoading.value = false
    }
  }
  </script>
  
  <style scoped>
  .home-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    text-align: center;
  }
  .api-btn {
    padding: 0.5rem 1rem;
    margin: 1rem 0;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .api-btn:hover {
    opacity: 0.9;
  }
  .result {
    margin: 1rem 0;
    padding: 1rem;
    border-radius: 4px;
    background: #f5f5f5;
    text-align: left;
  }
  .error {
    background: #ffebee;
    color: #b71c1c;
  }
  </style>