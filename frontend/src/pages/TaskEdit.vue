<template>
    <div class="page">
      <div class="card">
        <h1>编辑任务</h1>
  
        <form v-if="formLoaded" @submit.prevent="handleUpdate" class="form">
          <input v-model="form.title" type="text" placeholder="请输入任务标题" />
          <textarea v-model="form.description" placeholder="请输入任务描述"></textarea>
  
          <select v-model="form.status">
            <option value="todo">todo</option>
            <option value="in_progress">in_progress</option>
            <option value="done">done</option>
            <option value="overdue">overdue</option>
          </select>
  
          <select v-model="form.priority">
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
            <option value="urgent">urgent</option>
          </select>
  
          <select v-model="form.assignee">
            <option :value="null">未指派</option>
            <option v-for="member in members" :key="member.user_id" :value="member.user_id">
              {{ member.username }}（{{ member.role }}）
            </option>
          </select>
  
          <input v-model="form.due_date" type="datetime-local" />
  
          <button type="submit" :disabled="loading">
            {{ loading ? '保存中...' : '保存修改' }}
          </button>
        </form>
  
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div class="link-box">
          <router-link v-if="taskId" :to="`/tasks/${taskId}`">返回任务详情</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { getTaskDetail, updateTask, getProjectMemberOptions } from '../api/task'
  
  const route = useRoute()
  const router = useRouter()
  const taskId = route.params.id
  
  const loading = ref(false)
  const errorMsg = ref('')
  const formLoaded = ref(false)
  const members = ref([])
  
  const form = reactive({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium',
    assignee: null,
    due_date: '',
    project: null,
  })
  
  function toDateTimeLocal(value) {
    if (!value) return ''
    const date = new Date(value)
    const offset = date.getTimezoneOffset()
    const localDate = new Date(date.getTime() - offset * 60000)
    return localDate.toISOString().slice(0, 16)
  }
  
  async function loadTask() {
    const response = await getTaskDetail(taskId)
    const task = response.data.task
  
    form.title = task.title
    form.description = task.description
    form.status = task.status
    form.priority = task.priority
    form.assignee = task.assignee
    form.due_date = toDateTimeLocal(task.due_date)
    form.project = task.project
  
    const memberResponse = await getProjectMemberOptions(task.project)
    members.value = memberResponse.data.members || []
  
    formLoaded.value = true
  }
  
  async function handleUpdate() {
    if (!form.title.trim()) {
      errorMsg.value = '请输入任务标题'
      return
    }
  
    const payload = {
      title: form.title,
      description: form.description,
      status: form.status,
      priority: form.priority,
      assignee: form.assignee ? Number(form.assignee) : null,
      due_date: form.due_date ? new Date(form.due_date).toISOString() : null,
    }
  
    try {
      loading.value = true
      errorMsg.value = ''
      await updateTask(taskId, payload)
      router.push(`/tasks/${taskId}`)
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || {}) ||
        '更新任务失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(async () => {
    try {
      loading.value = true
      errorMsg.value = ''
      await loadTask()
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取任务详情失败'
    } finally {
      loading.value = false
    }
  })
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
    width: 560px;
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