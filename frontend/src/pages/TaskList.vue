<template>
    <div class="page">
      <div class="topbar">
        <h1>任务列表</h1>
        <div class="actions">
          <router-link to="/teams" class="btn secondary">返回团队列表</router-link>
          <router-link :to="`/projects/${projectId}/tasks/create`" class="btn primary">
            创建任务
          </router-link>
        </div>
      </div>
  
      <div class="container">
        <p v-if="loading">正在加载任务列表...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div v-if="!loading && tasks.length === 0" class="empty-box">
          当前项目还没有任务，先创建一个吧。
        </div>
  
        <div v-if="tasks.length > 0" class="task-grid">
          <div v-for="task in tasks" :key="task.id" class="task-card">
            <h2>{{ task.title }}</h2>
            <p>{{ task.description || '暂无描述' }}</p>
            <p><strong>状态：</strong>{{ task.status }}</p>
            <p><strong>优先级：</strong>{{ task.priority }}</p>
            <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
            <router-link :to="`/tasks/${task.id}`" class="detail-link">
              查看详情
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { getProjectTasks } from '../api/task'
  
  const route = useRoute()
  const projectId = route.params.projectId
  
  const tasks = ref([])
  const loading = ref(false)
  const errorMsg = ref('')
  
  async function loadTasks() {
    try {
      loading.value = true
      errorMsg.value = ''
      const response = await getProjectTasks(projectId)
      tasks.value = response.data.tasks || []
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取任务列表失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadTasks()
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
  
  .task-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  
  .task-card {
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