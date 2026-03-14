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
      <input
        v-model="filters.search"
        type="text"
        placeholder="请输入任务标题关键词"
        class="search-input"
      />

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

      <button class="btn primary" @click="handleSearch">应用筛选</button>
      <button class="btn secondary" @click="resetFilters">重置</button>
    </div>

    <div class="container">
      <p v-if="loading">正在加载任务列表...</p>

      <ErrorState v-if="errorMsg" title="任务列表加载失败" :message="errorMsg">
        <button class="btn secondary" @click="loadTasks">重新加载</button>
      </ErrorState>

      <EmptyState
        v-if="!loading && !errorMsg && tasks.length === 0"
        title="当前条件下没有任务"
        description="你可以调整筛选条件，或者创建一个新任务。"
      >
        <router-link :to="`/projects/${projectId}/tasks/create`" class="btn primary">
          创建任务
        </router-link>
      </EmptyState>

      <div v-if="!loading && !errorMsg && tasks.length > 0" class="task-grid">
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

      <div
        v-if="!loading && !errorMsg && tasks.length > 0 && pagination.total_pages > 1"
        class="pagination"
      >
        <button
          class="btn secondary"
          @click="changePage(pagination.current_page - 1)"
          :disabled="!pagination.has_previous"
        >
          上一页
        </button>

        <span class="page-info">
          第 {{ pagination.current_page }} / {{ pagination.total_pages }} 页
          （共 {{ pagination.total_items }} 条）
        </span>

        <button
          class="btn secondary"
          @click="changePage(pagination.current_page + 1)"
          :disabled="!pagination.has_next"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getProjectTasks, getProjectMemberOptions } from '../api/task'
import EmptyState from '../components/EmptyState.vue'
import ErrorState from '../components/ErrorState.vue'
import { getErrorMessage } from '../utils/error'

const route = useRoute()
const projectId = route.params.projectId

const tasks = ref([])
const members = ref([])
const loading = ref(false)
const errorMsg = ref('')

const pagination = reactive({
  current_page: 1,
  total_pages: 1,
  total_items: 0,
  has_previous: false,
  has_next: false,
})

const filters = reactive({
  search: '',
  status: '',
  priority: '',
  assignee: '',
  ordering: '-created_at',
  page: 1,
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

    if (filters.search) {
      params.search = filters.search
    }

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

    if (filters.page) {
      params.page = filters.page
    }

    const response = await getProjectTasks(projectId, params)
    tasks.value = response.data.tasks || []

    const pageData = response.data.pagination || {}
    pagination.current_page = pageData.current_page || 1
    pagination.total_pages = pageData.total_pages || 1
    pagination.total_items = pageData.total_items || 0
    pagination.has_previous = pageData.has_previous || false
    pagination.has_next = pageData.has_next || false
  } catch (error) {
    errorMsg.value = getErrorMessage(error, '获取任务列表失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  filters.page = 1
  loadTasks()
}

function changePage(page) {
  filters.page = page
  loadTasks()
}

function resetFilters() {
  filters.search = ''
  filters.status = ''
  filters.priority = ''
  filters.assignee = ''
  filters.ordering = '-created_at'
  filters.page = 1
  loadTasks()
}

onMounted(async () => {
  try {
    await loadMembers()
    await loadTasks()
  } catch (error) {
    errorMsg.value = getErrorMessage(error, '页面初始化失败')
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

.filter-bar select,
.search-input {
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

.pagination {
  margin-top: 28px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.page-info {
  font-size: 14px;
  color: #374151;
}
</style>