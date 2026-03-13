<template>
    <div class="page">
      <div class="card">
        <h1>注册 TaskFlow 账号</h1>
  
        <form @submit.prevent="handleRegister" class="form">
          <input v-model="form.username" type="text" placeholder="用户名" />
          <input v-model="form.email" type="email" placeholder="邮箱" />
          <input v-model="form.password" type="password" placeholder="密码" />
          <input v-model="form.password_confirm" type="password" placeholder="确认密码" />
          <textarea v-model="form.bio" placeholder="个人简介（可选）"></textarea>
  
          <button type="submit" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
  
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
        <p v-if="successMsg" class="success">{{ successMsg }}</p>
  
        <div class="link-box">
          已有账号？
          <router-link to="/login">去登录</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { registerUser } from '../api/user'
  
  const router = useRouter()
  
  const loading = ref(false)
  const errorMsg = ref('')
  const successMsg = ref('')
  
  const form = reactive({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    bio: '',
  })
  
  async function handleRegister() {
    errorMsg.value = ''
    successMsg.value = ''
  
    if (!form.username || !form.email || !form.password || !form.password_confirm) {
      errorMsg.value = '请填写完整注册信息'
      return
    }
  
    try {
      loading.value = true
      await registerUser(form)
      successMsg.value = '注册成功，即将跳转到登录页'
  
      setTimeout(() => {
        router.push('/login')
      }, 1000)
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || error.response?.data || {}) ||
        '注册失败'
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
  
  input,
  textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #d0d7e2;
    border-radius: 8px;
    font-size: 14px;
  }
  
  textarea {
    min-height: 90px;
    resize: vertical;
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
  
  .success {
    margin-top: 16px;
    color: #16a34a;
  }
  
  .link-box {
    margin-top: 20px;
    text-align: center;
  }
  </style>