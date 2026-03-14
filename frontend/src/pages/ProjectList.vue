<template>
  <div class="page">
    <div class="topbar">
      <h1>项目列表</h1>
      <div class="actions">
        <router-link to="/teams" class="btn secondary">返回团队列表</router-link>
        <router-link :to="`/teams/${teamId}/projects/create`" class="btn primary">
          创建项目
        </router-link>
      </div>
    </div>

    <div class="container">
      <p v-if="loading">正在加载项目列表...</p>

      <ErrorState v-if="errorMsg" title="项目列表加载失败" :message="errorMsg">
        <button class="btn secondary" @click="loadProjects">重新加载</button>
      </ErrorState>

      <EmptyState
        v-if="!loading && !errorMsg && projects.length === 0"
        title="该团队还没有项目"
        description="创建一个项目，开始组织任务协作。"
      >
        <router-link :to="`/teams/${teamId}/projects/create`" class="btn primary">
          创建项目
        </router-link>
      </EmptyState>

      <div v-if="!loading && !errorMsg && projects.length > 0" class="project-grid">
        <div v-for="project in projects" :key="project.id" class="project-card">
          <h2>{{ project.name }}</h2>
          <p>{{ project.description || '暂无描述' }}</p>
          <p><strong>状态：</strong>{{ project.status }}</p>
          <p><strong>创建人：</strong>{{ project.created_by_username }}</p>
          <router-link :to="`/projects/${project.id}`" class="detail-link">
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
import { getTeamProjects } from '../api/project'
import EmptyState from '../components/EmptyState.vue'
import ErrorState from '../components/ErrorState.vue'
import { getErrorMessage } from '../utils/error'

const route = useRoute()
const teamId = route.params.teamId

const projects = ref([])
const loading = ref(false)
const errorMsg = ref('')

async function loadProjects() {
  try {
    loading.value = true
    errorMsg.value = ''

    const response = await getTeamProjects(teamId)
    projects.value = response.data.projects || []
  } catch (error) {
    errorMsg.value = getErrorMessage(error, '获取项目列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProjects()
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

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.project-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.project-card h2 {
  margin-bottom: 12px;
}

.project-card p {
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

.detail-link {
  display: inline-block;
  margin-top: 12px;
  color: #2563eb;
  text-decoration: none;
}

.detail-link:hover {
  text-decoration: underline;
}
</style>