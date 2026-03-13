<template>
    <div class="page">
      <div class="card">
        <h1>登录 TaskFlow</h1>
  
        <form @submit.prevent="handleLogin" class="form">
          <input v-model="form.username" type="text" placeholder="用户名" />
          <input v-model="form.password" type="password" placeholder="密码" />
  
          <button type="submit" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
  
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div class="link-box">
          还没有账号？
          <router-link to="/register">去注册</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '../store/user'
  
  const router = useRouter()
  const userStore = useUserStore()
  
  const loading = ref(false)
  const errorMsg = ref('')
  
  const form = reactive({
    username: '',
    password: '',
  })
  
  async function handleLogin() {
    errorMsg.value = ''
  
    if (!form.username || !form.password) {
      errorMsg.value = '请输入用户名和密码'
      return
    }
  
    try {
      loading.value = true
      await userStore.login(form)
      await userStore.fetchProfile()
      router.push('/home')
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || error.response?.data || {}) ||
        '登录失败'
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .card {
    width: 420px;
    background: white;
    padding: 32px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  }
  
  h1 {
    margin-bottom: 24px;
    text-align: center;
    font-size: 28px;
  }
  
  .form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  
  input {
    width: 100%;
    padding: 12px;
    border: 1px solid #d0d7e2;
    border-radius: 8px;
    font-size: 14px;
  }
  
  button {
    padding: 12px;
    border: none;
    border-radius: 8px;
    background: #2563eb;
    color: white;
    font-size: 15px;
  }
  
  button:disabled {
    background: #93c5fd;
    cursor: not-allowed;
  }
  
  .error {
    margin-top: 16px;
    color: #dc2626;
  }
  
  .link-box {
    margin-top: 20px;
    text-align: center;
  }
  </style>