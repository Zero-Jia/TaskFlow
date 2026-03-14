<template>
    <div class="page">
      <div class="topbar">
        <h1>任务看板</h1>
        <div class="actions">
          <router-link :to="`/projects/${projectId}/tasks`" class="btn secondary">
            返回任务列表
          </router-link>
        </div>
      </div>
  
      <p v-if="loading">正在加载任务看板...</p>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
      <div v-if="board" class="board-grid">
        <div class="board-column">
          <h2>Todo</h2>
          <div v-if="board.todo.length === 0" class="empty">暂无任务</div>
          <div v-for="task in board.todo" :key="task.id" class="task-card">
            <h3 @click="goToTaskDetail(task.id)">{{ task.title }}</h3>
            <p><strong>优先级：</strong>{{ task.priority }}</p>
            <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
            <p><strong>截止时间：</strong>{{ task.due_date || '未设置' }}</p>
            <div class="actions-row">
              <button @click="changeStatus(task.id, 'in_progress')">移到进行中</button>
              <button @click="changeStatus(task.id, 'done')">移到已完成</button>
            </div>
          </div>
        </div>
  
        <div class="board-column">
          <h2>In Progress</h2>
          <div v-if="board.in_progress.length === 0" class="empty">暂无任务</div>
          <div v-for="task in board.in_progress" :key="task.id" class="task-card">
            <h3 @click="goToTaskDetail(task.id)">{{ task.title }}</h3>
            <p><strong>优先级：</strong>{{ task.priority }}</p>
            <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
            <p><strong>截止时间：</strong>{{ task.due_date || '未设置' }}</p>
            <div class="actions-row">
              <button @click="changeStatus(task.id, 'todo')">移到待处理</button>
              <button @click="changeStatus(task.id, 'done')">移到已完成</button>
              <button @click="changeStatus(task.id, 'overdue')">移到已逾期</button>
            </div>
          </div>
        </div>
  
        <div class="board-column">
          <h2>Done</h2>
          <div v-if="board.done.length === 0" class="empty">暂无任务</div>
          <div v-for="task in board.done" :key="task.id" class="task-card">
            <h3 @click="goToTaskDetail(task.id)">{{ task.title }}</h3>
            <p><strong>优先级：</strong>{{ task.priority }}</p>
            <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
            <p><strong>截止时间：</strong>{{ task.due_date || '未设置' }}</p>
            <div class="actions-row">
              <button @click="changeStatus(task.id, 'todo')">移到待处理</button>
              <button @click="changeStatus(task.id, 'in_progress')">移到进行中</button>
            </div>
          </div>
        </div>
  
        <div class="board-column">
          <h2>Overdue</h2>
          <div v-if="board.overdue.length === 0" class="empty">暂无任务</div>
          <div v-for="task in board.overdue" :key="task.id" class="task-card">
            <h3 @click="goToTaskDetail(task.id)">{{ task.title }}</h3>
            <p><strong>优先级：</strong>{{ task.priority }}</p>
            <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
            <p><strong>截止时间：</strong>{{ task.due_date || '未设置' }}</p>
            <div class="actions-row">
              <button @click="changeStatus(task.id, 'todo')">移到待处理</button>
              <button @click="changeStatus(task.id, 'in_progress')">移到进行中</button>
              <button @click="changeStatus(task.id, 'done')">移到已完成</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { getProjectTaskBoard, updateTaskStatus } from '../api/task'
  
  const route = useRoute()
  const router = useRouter()
  const projectId = route.params.projectId
  
  const loading = ref(false)
  const errorMsg = ref('')
  const board = ref(null)
  
  async function loadBoard() {
    try {
      loading.value = true
      errorMsg.value = ''
      const response = await getProjectTaskBoard(projectId)
      board.value = response.data.board
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取任务看板失败'
    } finally {
      loading.value = false
    }
  }
  
  async function changeStatus(taskId, status) {
    try {
      await updateTaskStatus(taskId, { status })
      await loadBoard()
    } catch (error) {
      alert(error.response?.data?.message || '更新任务状态失败')
    }
  }
  
  function goToTaskDetail(taskId) {
    router.push(`/tasks/${taskId}`)
  }
  
  onMounted(() => {
    loadBoard()
  })
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    background: #f5f7fb;
    padding: 24px;
  }
  
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .actions {
    display: flex;
    gap: 12px;
  }
  
  .board-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .board-column {
    background: #eef2f7;
    border-radius: 12px;
    padding: 16px;
    min-height: 500px;
  }
  
  .board-column h2 {
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 18px;
  }
  
  .task-card {
    background: white;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }
  
  .task-card h3 {
    margin-top: 0;
    cursor: pointer;
    color: #2563eb;
  }
  
  .task-card p {
    margin: 6px 0;
  }
  
  .actions-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }
  
  .actions-row button {
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    background: #2563eb;
    color: white;
    cursor: pointer;
    font-size: 12px;
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
  
  .empty {
    color: #888;
    font-size: 14px;
  }
  </style>