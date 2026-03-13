<template>
  <div class="home-page">
    <header class="navbar">
      <div class="logo">TaskFlow</div>
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </header>

    <main class="content">
      <div class="card">
        <h1>欢迎来到 TaskFlow</h1>
        <p>你已经成功完成前后端登录闭环。</p>

        <div v-if="user" class="user-box">
          <h2>当前用户信息</h2>
          <p><strong>用户名：</strong>{{ user.username }}</p>
          <p><strong>邮箱：</strong>{{ user.email }}</p>
          <p><strong>简介：</strong>{{ user.bio || '暂无简介' }}</p>
          <p><strong>创建时间：</strong>{{ user.created_at }}</p>

          <div v-if="user.avatar" class="avatar-box">
            <img :src="user.avatar" alt="avatar" />
          </div>
        </div>

        <p v-if="loading">正在加载用户信息...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const errorMsg = ref('')

const user = computed(() => userStore.userInfo)

async function loadProfile() {
  try {
    loading.value = true
    errorMsg.value = ''
    await userStore.fetchProfile()
  } catch (error) {
    errorMsg.value = '获取用户信息失败，请重新登录'
    userStore.logout()
    router.push('/login')
  } finally {
    loading.value = false
  }
}

function handleLogout() {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f7fb;
}

.navbar {
  height: 64px;
  background: #1f2937;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.logo {
  font-size: 22px;
  font-weight: bold;
}

.logout-btn {
  padding: 10px 16px;
  border: none;
  background: #ef4444;
  color: white;
  border-radius: 8px;
}

.content {
  padding: 32px;
  display: flex;
  justify-content: center;
}

.card {
  width: 700px;
  background: white;
  border-radius: 14px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

h1 {
  margin-bottom: 12px;
}

h2 {
  margin-top: 28px;
  margin-bottom: 14px;
}

.user-box p {
  margin: 10px 0;
}

.avatar-box {
  margin-top: 18px;
}

.avatar-box img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid #ddd;
}

.error {
  color: #dc2626;
  margin-top: 16px;
}
</style>