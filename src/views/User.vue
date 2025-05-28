<template>
  <div class="user-container">
    <h1>用户管理</h1>
    
    <!-- 添加/编辑用户表单 -->
    <div class="user-form">
      <h3>{{ currentUser ? '编辑用户' : '添加用户' }}</h3>
      <div class="form-group">
        <label>姓名：</label>
        <input type="text" v-model="formData.name" placeholder="请输入姓名">
      </div>
      <div class="form-group">
        <label>手机号：</label>
        <input type="text" v-model="formData.phone" placeholder="请输入手机号">
      </div>
      <div class="form-group">
        <label>年龄：</label>
        <input type="number" v-model="formData.age" placeholder="请输入年龄">
      </div>
      <div class="form-actions">
        <button @click="handleSave" class="save-btn">保存</button>
        <button v-if="currentUser" @click="cancelEdit" class="cancel-btn">取消</button>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="user-list">
      <h3>用户列表</h3>
      <button @click="showAddForm" class="add-btn">添加新用户</button>
      <table>
        <thead>
          <tr>
            <th>姓名</th>
            <th>手机号</th>
            <th>年龄</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in userList" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.phone }}</td>
            <td>{{ user.age }}</td>
            <td>
              <button @click="editUser(user)" class="edit-btn">编辑</button>
              <button @click="deleteUser(user.id)" class="delete-btn">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 定义用户类型
interface User {
  id: number
  name: string
  phone: string
  age: number
}

// 响应式状态
const userList = ref<User[]>([])
const formData = ref<Omit<User, 'id'>>({ name: '', phone: '', age: 0 })
const currentUser = ref<User | null>(null) // 当前编辑的用户
const isAdding = ref(false) // 是否显示添加表单

// API基地址
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

// 获取用户列表
const fetchUserList = async () => {
  try {
    const token = localStorage.getItem('token') // 从本地存储获取 Token
    const response = await fetch(`${apiBaseUrl}/users`, {
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '' // 关键：添加 Token 到请求头
      }
    })
    const data = await response.json()
    userList.value = data
  } catch (err) {
    console.error('获取用户列表失败:', err)
  }
}

// 添加/更新用户
const handleSave = async () => {
  if (!formData.value.name || !formData.value.phone || !formData.value.age) {
    alert('请填写完整用户信息')
    return
  }

  try {
    const token = localStorage.getItem('token') // 获取 Token
    let response
    if (currentUser.value) {
      // 更新用户（新增 Token 头）
      response = await fetch(`${apiBaseUrl}/users/${currentUser.value.id}`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '' // 新增 Token 头
        },
        body: JSON.stringify(formData.value)
      })
    } else {
      // 添加用户（新增 Token 头）
      response = await fetch(`${apiBaseUrl}/users`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '' // 新增 Token 头
        },
        body: JSON.stringify(formData.value)
      })
    }
    if (response.ok) {
      fetchUserList() // 刷新列表
      resetForm()
    }
  } catch (err) {
    console.error('保存用户失败:', err)
  }
}

// 删除用户（修改后）
const deleteUser = async (userId: number) => {
  if (!confirm('确定要删除该用户吗？')) return

  try {
    const token = localStorage.getItem('token') // 获取 Token
    const response = await fetch(`${apiBaseUrl}/users/${userId}`, { 
      method: 'DELETE',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '' // 新增 Token 头
      }
    })
    if (response.ok) {
      userList.value = userList.value.filter(user => user.id !== userId)
    }
  } catch (err) {
    console.error('删除用户失败:', err)
  }
}

// 编辑用户
const editUser = (user: User) => {
  currentUser.value = user
  formData.value = { name: user.name, phone: user.phone, age: user.age }
}

// 显示添加表单
const showAddForm = () => {
  currentUser.value = null
  resetForm()
  isAdding.value = true
}

// 取消编辑
const cancelEdit = () => {
  resetForm()
  currentUser.value = null
}

// 重置表单
const resetForm = () => {
  formData.value = { name: '', phone: '', age: 0 }
}

// 初始化加载用户列表
fetchUserList()
</script>

<style scoped>
.user-container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.user-form {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 300px;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
}

.form-actions {
  margin-top: 1rem;
}

.save-btn, .add-btn, .edit-btn, .delete-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 1rem;
}

.save-btn { background: #42b983; color: white; }
.add-btn { background: #646cff; color: white; }
.edit-btn { background: #ffc107; color: black; }
.delete-btn { background: #dc3545; color: white; }
.cancel-btn { background: #6c757d; color: white; }

.user-list table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.user-list th, .user-list td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.user-list th {
  background: #f8f9fa;
}
</style>