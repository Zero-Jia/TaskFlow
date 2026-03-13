<template>
    <div class="page">
      <div class="card">
        <h1>创建项目</h1>
  
        <form @submit.prevent="handleCreate" class="form">
          <input v-model="form.name" type="text" placeholder="请输入项目名称" />
          <textarea v-model="form.description" placeholder="请输入项目描述"></textarea>
  
          <select v-model="form.status">
            <option value="active">active</option>
            <option value="completed">completed</option>
            <option value="archived">archived</option>
          </select>
  
          <button type="submit" :disabled="loading">
            {{ loading ? '创建中...' : '创建项目' }}
          </button>
        </form>
  
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div class="link-box">
          <router-link :to="`/teams/${teamId}/projects`">返回项目列表</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { createProject } from '../api/project'
  
  const route = useRoute()
  const router = useRouter()
  const teamId = Number(route.params.teamId)
  
  const loading = ref(false)
  const errorMsg = ref('')
  
  const form = reactive({
    team: teamId,
    name: '',
    description: '',
    status: 'active',
  })
  
  async function handleCreate() {
    errorMsg.value = ''
  
    if (!form.name.trim()) {
      errorMsg.value = '请输入项目名称'
      return
    }
  
    try {
      loading.value = true
      const response = await createProject(form)
      const projectId = response.data.project.id
      router.push(`/projects/${projectId}`)
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || {}) ||
        '创建项目失败'
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f5f7fb;
  }
  
  .card {
    width: 480px;
    background: white;
    padding: 32px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  }
  
  .form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  
  input,
  textarea,
  select {
    padding: 12px;
    border: 1px solid #d0d7e2;
    border-radius: 8px;
    font-size: 14px;
  }
  
  textarea {
    min-height: 120px;
    resize: vertical;
  }
  
  button {
    padding: 12px;
    border: none;
    border-radius: 8px;
    background: #2563eb;
    color: white;
  }
  
  .error {
    color: #dc2626;
    margin-top: 16px;
  }
  
  .link-box {
    margin-top: 18px;
    text-align: center;
  }
  </style>