<template>
  <div class="page">
    <div class="container">
      <div class="topbar">
        <router-link v-if="project" :to="`/teams/${project.team}/projects`" class="btn secondary">
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

        <div class="action-box">
          <router-link :to="`/projects/${project.id}/edit`" class="btn primary">
            编辑项目
          </router-link>

          <button class="btn success" @click="handleStatusChange('active')">设为 active</button>
          <button class="btn success" @click="handleStatusChange('completed')">设为 completed</button>
          <button class="btn success" @click="handleStatusChange('archived')">设为 archived</button>

          <button class="btn danger" @click="handleDelete">删除项目</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getProjectDetail, updateProjectStatus, deleteProject } from '../api/project'

const route = useRoute()
const router = useRouter()

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

async function handleStatusChange(status) {
  try {
    await updateProjectStatus(route.params.id, { status })
    await loadProjectDetail()
  } catch (error) {
    alert(error.response?.data?.message || '更新项目状态失败')
  }
}

async function handleDelete() {
  const confirmed = window.confirm('确定要删除这个项目吗？删除后无法恢复。')
  if (!confirmed) return

  try {
    const teamId = project.value.team
    await deleteProject(route.params.id)
    router.push(`/teams/${teamId}/projects`)
  } catch (error) {
    alert(error.response?.data?.message || '删除项目失败')
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
  border: none;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
}

.secondary {
  background: #e5e7eb;
  color: #111827;
}

.primary {
  background: #2563eb;
  color: white;
}

.success {
  background: #10b981;
  color: white;
}

.danger {
  background: #ef4444;
  color: white;
}

.action-box {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.error {
  color: #dc2626;
}
</style>