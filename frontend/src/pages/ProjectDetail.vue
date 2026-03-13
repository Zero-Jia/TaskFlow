<template>
    <div class="page">
      <div class="container">
        <div class="topbar">
          <router-link
            v-if="project"
            :to="`/teams/${project.team}/projects`"
            class="btn secondary"
          >
            返回项目列表
          </router-link>
        </div>
  
        <p v-if="loading">正在加载项目详情...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div v-if="project" class="card">
          <h1>{{ project.name }}</h1>
          <p><strong>所属团队：</strong>{{ project.team_name }}</p>
          <p><strong>状态：</strong>{{ project.status }}</p>
          <p><strong>创建人：</strong>{{ project.created_by_username }}</p>
          <p><strong>描述：</strong>{{ project.description || '暂无描述' }}</p>
          <p><strong>创建时间：</strong>{{ project.created_at }}</p>
          <p><strong>更新时间：</strong>{{ project.updated_at }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { getProjectDetail } from '../api/project'
  
  const route = useRoute()
  const project = ref(null)
  const loading = ref(false)
  const errorMsg = ref('')
  
  async function loadProjectDetail() {
    try {
      loading.value = true
      errorMsg.value = ''
      const response = await getProjectDetail(route.params.id)
      project.value = response.data.project
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取项目详情失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadProjectDetail()
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
  
  .error {
    color: #dc2626;
  }
  </style>