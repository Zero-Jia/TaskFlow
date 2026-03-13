<template>
    <div class="page">
      <div class="container">
        <div class="topbar">
          <router-link to="/teams" class="btn secondary">返回团队列表</router-link>
        </div>
  
        <p v-if="loading">正在加载团队详情...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div v-if="team" class="card">
          <h1>{{ team.name }}</h1>
          <p><strong>描述：</strong>{{ team.description || '暂无描述' }}</p>
          <p><strong>拥有者：</strong>{{ team.owner_username }}</p>
          <p><strong>成员数：</strong>{{ team.member_count }}</p>
  
          <h2>团队成员</h2>
          <div v-if="team.members.length === 0">暂无成员</div>
  
          <div v-for="member in team.members" :key="member.id" class="member-item">
            <p><strong>用户名：</strong>{{ member.username }}</p>
            <p><strong>邮箱：</strong>{{ member.email }}</p>
            <p><strong>角色：</strong>{{ member.role }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { getTeamDetail } from '../api/team'
  
  const route = useRoute()
  const team = ref(null)
  const loading = ref(false)
  const errorMsg = ref('')
  
  async function loadTeamDetail() {
    try {
      loading.value = true
      errorMsg.value = ''
      const response = await getTeamDetail(route.params.id)
      team.value = response.data.team
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取团队详情失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadTeamDetail()
  })
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    background: #f5f7fb;
    padding: 32px;
  }
  
  .container {
    max-width: 900px;
    margin: 0 auto;
  }
  
  .card {
    background: white;
    padding: 28px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  }
  
  .topbar {
    margin-bottom: 20px;
  }
  
  .btn {
    padding: 10px 14px;
    border-radius: 8px;
    text-decoration: none;
  }
  
  .secondary {
    background: #e5e7eb;
    color: #111827;
  }
  
  .member-item {
    margin-top: 16px;
    padding: 16px;
    background: #f9fafb;
    border-radius: 10px;
  }
  
  .error {
    color: #dc2626;
  }
  </style>