<template>
    <div class="page">
      <header class="topbar">
        <h1>我的团队</h1>
        <div class="actions">
          <router-link to="/home" class="btn secondary">返回首页</router-link>
          <router-link to="/teams/create" class="btn primary">创建团队</router-link>
        </div>
      </header>
  
      <div class="container">
        <p v-if="loading">正在加载团队列表...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div v-if="!loading && teams.length === 0" class="empty-box">
          你还没有加入任何团队，先创建一个吧。
        </div>
  
        <div v-if="teams.length > 0" class="team-grid">
          <div v-for="team in teams" :key="team.id" class="team-card">
            <h2>{{ team.name }}</h2>
            <p>{{ team.description || '暂无描述' }}</p>
            <p><strong>拥有者：</strong>{{ team.owner_username }}</p>
            <p><strong>成员数：</strong>{{ team.member_count }}</p>
            <router-link :to="`/teams/${team.id}`" class="detail-link">查看详情</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { getTeamList } from '../api/team'
  
  const teams = ref([])
  const loading = ref(false)
  const errorMsg = ref('')
  
  async function loadTeams() {
    try {
      loading.value = true
      errorMsg.value = ''
      const response = await getTeamList()
      teams.value = response.data.teams || []
    } catch (error) {
      errorMsg.value = '获取团队列表失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadTeams()
  })
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    background: #f5f7fb;
    padding: 32px;
  }
  
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .actions {
    display: flex;
    gap: 12px;
  }
  
  .container {
    max-width: 1000px;
    margin: 0 auto;
  }
  
  .team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  
  .team-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  }
  
  .btn {
    padding: 10px 14px;
    border-radius: 8px;
    text-decoration: none;
  }
  
  .primary {
    background: #2563eb;
    color: white;
  }
  
  .secondary {
    background: #e5e7eb;
    color: #111827;
  }
  
  .detail-link {
    display: inline-block;
    margin-top: 12px;
    color: #2563eb;
  }
  
  .error {
    color: #dc2626;
  }
  
  .empty-box {
    background: white;
    padding: 24px;
    border-radius: 12px;
  }
  </style>