<template>
    <div class="page">
      <div class="container">
        <div class="topbar">
          <router-link v-if="task" :to="`/projects/${task.project}/tasks`" class="btn secondary">
            返回任务列表
          </router-link>
        </div>
  
        <p v-if="loading">正在加载任务详情...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div v-if="task" class="card">
          <h1>{{ task.title }}</h1>
          <p><strong>所属项目：</strong>{{ task.project_name }}</p>
          <p><strong>状态：</strong>{{ task.status }}</p>
          <p><strong>优先级：</strong>{{ task.priority }}</p>
          <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
          <p><strong>创建人：</strong>{{ task.creator_username }}</p>
          <p><strong>描述：</strong>{{ task.description || '暂无描述' }}</p>
          <p><strong>截止时间：</strong>{{ task.due_date || '未设置' }}</p>
          <p><strong>创建时间：</strong>{{ task.created_at }}</p>
          <p><strong>更新时间：</strong>{{ task.updated_at }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { getTaskDetail } from '../api/task'
  
  const route = useRoute()
  const task = ref(null)
  const loading = ref(false)
  const errorMsg = ref('')
  
  async function loadTaskDetail() {
    try {
      loading.value = true
      errorMsg.value = ''
      const response = await getTaskDetail(route.params.id)
      task.value = response.data.task
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取任务详情失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadTaskDetail()
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