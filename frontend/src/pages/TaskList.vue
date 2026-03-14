<template>
  <div class="page">
    <div class="topbar">
      <h1>任务列表</h1>
      <div class="actions">
        <router-link to="/teams" class="btn secondary">返回团队列表</router-link>
        <router-link :to="`/projects/${projectId}/task-board`" class="btn success">
          查看任务看板
        </router-link>
        <router-link :to="`/projects/${projectId}/tasks/create`" class="btn primary">
          创建任务
        </router-link>
      </div>
    </div>

    <div class="filter-bar">
      <select v-model="filters.status">
        <option value="">全部状态</option>
        <option value="todo">todo</option>
        <option value="in_progress">in_progress</option>
        <option value="done">done</option>
        <option value="overdue">overdue</option>
      </select>

      <select v-model="filters.priority">
        <option value="">全部优先级</option>
        <option value="low">low</option>
        <option value="medium">medium</option>
        <option value="high">high</option>
        <option value="urgent">urgent</option>
      </select>

      <select v-model="filters.assignee">
        <option value="">全部负责人</option>
        <option value="unassigned">未指派</option>
        <option
          v-for="member in members"
          :key="member.user_id"
          :value="String(member.user_id)"
        >
          {{ member.username }}
        </option>
      </select>

      <select v-model="filters.ordering">
        <option value="-created_at">创建时间倒序</option>
        <option value="created_at">创建时间正序</option>
        <option value="due_date">截止时间正序</option>
        <option value="-due_date">截止时间倒序</option>
      </select>

      <button class="btn primary" @click="loadTasks">应用筛选</button>
      <button class="btn secondary" @click="resetFilters">重置</button>
    </div>

    <div class="container">
      <p v-if="loading">正在加载任务列表...</p>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

      <div v-if="!loading && tasks.length === 0" class="empty-box">
        当前筛选条件下没有任务。
      </div>

      <div v-if="tasks.length > 0" class="task-grid">
        <div v-for="task in tasks" :key="task.id" class="task-card">
          <h2>{{ task.title }}</h2>
          <p>{{ task.description || '暂无描述' }}</p>
          <p><strong>状态：</strong>{{ task.status }}</p>
          <p><strong>优先级：</strong>{{ task.priority }}</p>
          <p><strong>负责人：</strong>{{ task.assignee_username || '未指派' }}</p>
          <p><strong>截止时间：</strong>{{ task.due_date || '未设置' }}</p>
          <router-link :to="`/tasks/${task.id}`" class="detail-link">
            查看详情
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getProjectTasks, getProjectMemberOptions } from '../api/task'

const route = useRoute()
const projectId = route.params.projectId

const tasks = ref([])
const members = ref([])
const loading = ref(false)
const errorMsg = ref('')

const filters = reactive({
  status: '',
  priority: '',
  assignee: '',
  ordering: '-created_at',
})

async function loadMembers() {
  const response = await getProjectMemberOptions(projectId)
  members.value = response.data.members || []
}

async function loadTasks() {
  try {
    loading.value = true
    errorMsg.value = ''

    const params = {}

    if (filters.status) {
      params.status = filters.status
    }

    if (filters.priority) {
      params.priority = filters.priority
    }

    if (filters.assignee) {
      params.assignee = filters.assignee
    }

    if (filters.ordering) {
      params.ordering = filters.ordering
    }

    const response = await getProjectTasks(projectId, params)
    tasks.value = response.data.tasks || []
  } catch (error) {
    errorMsg.value = error.response?.data?.message || '获取任务列表失败'
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  filters.status = ''
  filters.priority = ''
  filters.assignee = ''
  filters.ordering = '-created_at'
  loadTasks()
}

onMounted(async () => {
  try {
    await loadMembers()
    await loadTasks()
  } catch (error) {
    errorMsg.value = error.response?.data?.message || '页面初始化失败'
  }
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
  gap: 16px;
  flex-wrap: wrap;
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
}

.filter-bar select {
  padding: 10px 12px;
  border: 1px solid #d0d7e2;
  border-radius: 8px;
  min-width: 150px;
  background: white;
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

.task-card h2 {
  margin-bottom: 12px;
}

.task-card p {
  margin: 8px 0;
  color: #374151;
}

.btn {
  padding: 10px 14px;
  border-radius: 8px;
  text-decoration: none;
  display: inline-block;
  border: none;
  cursor: pointer;
}

.primary {
  background: #2563eb;
  color: white;
}

.secondary {
  background: #e5e7eb;
  color: #111827;
}

.success {
  background: #10b981;
  color: white;
}

.detail-link {
  display: inline-block;
  margin-top: 12px;
  color: #2563eb;
  text-decoration: none;
}

.detail-link:hover {
  text-decoration: underline;
}

.error {
  color: #dc2626;
  margin-bottom: 16px;
}

.empty-box {
  background: white;
  padding: 24px;
  border-radius: 12px;
  color: #6b7280;
}
</style>