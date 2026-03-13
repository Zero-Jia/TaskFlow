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

        <div class="assignee-box">
          <select v-model="selectedAssignee">
            <option :value="null">未指派</option>
            <option
              v-for="member in members"
              :key="member.user_id"
              :value="member.user_id"
            >
              {{ member.username }}（{{ member.role }}）
            </option>
          </select>
          <button class="btn primary" @click="handleAssigneeChange">
            修改负责人
          </button>
        </div>

        <div class="action-box">
          <router-link :to="`/tasks/${task.id}/edit`" class="btn primary">
            编辑任务
          </router-link>

          <button class="btn success" @click="handleStatusChange('todo')">
            设为 todo
          </button>
          <button class="btn success" @click="handleStatusChange('in_progress')">
            设为 in_progress
          </button>
          <button class="btn success" @click="handleStatusChange('done')">
            设为 done
          </button>
          <button class="btn success" @click="handleStatusChange('overdue')">
            设为 overdue
          </button>

          <button class="btn warning" @click="handlePriorityChange('low')">
            优先级 low
          </button>
          <button class="btn warning" @click="handlePriorityChange('medium')">
            优先级 medium
          </button>
          <button class="btn warning" @click="handlePriorityChange('high')">
            优先级 high
          </button>
          <button class="btn warning" @click="handlePriorityChange('urgent')">
            优先级 urgent
          </button>

          <button class="btn danger" @click="handleDelete">
            删除任务
          </button>
        </div>
      </div>

      <!-- 评论区 -->
      <div v-if="task" class="card comment-card">
        <h2>任务评论</h2>

        <div class="comment-form">
          <textarea
            v-model="commentContent"
            placeholder="请输入评论内容"
            rows="4"
          ></textarea>
          <button
            class="btn primary"
            @click="handleCreateComment"
            :disabled="commentSubmitting"
          >
            {{ commentSubmitting ? '提交中...' : '发表评论' }}
          </button>
        </div>

        <p v-if="commentLoading">评论加载中...</p>
        <p v-else-if="comments.length === 0" class="empty-text">暂无评论</p>

        <div v-else class="comment-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="author">{{ comment.author_username }}</span>
              <span class="time">{{ comment.created_at }}</span>
            </div>

            <div class="comment-content">
              {{ comment.content }}
            </div>

            <div
              v-if="comment.author_username === currentUsername"
              class="comment-actions"
            >
              <button class="btn danger small" @click="handleDeleteComment(comment.id)">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- 评论区结束 -->

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getTaskDetail,
  updateTaskStatus,
  updateTaskPriority,
  updateTaskAssignee,
  deleteTask,
  getProjectMemberOptions,
  getTaskComments,
  createTaskComment,
  deleteTaskComment,
} from '../api/task'

const route = useRoute()
const router = useRouter()

const task = ref(null)
const members = ref([])
const selectedAssignee = ref(null)
const loading = ref(false)
const errorMsg = ref('')

const comments = ref([])
const commentContent = ref('')
const commentLoading = ref(false)
const commentSubmitting = ref(false)

const currentUsername = computed(() => {
  return localStorage.getItem('username') || ''
})

async function loadTaskDetail() {
  try {
    loading.value = true
    errorMsg.value = ''

    const response = await getTaskDetail(route.params.id)
    task.value = response.data.task
    selectedAssignee.value = task.value.assignee

    const memberResponse = await getProjectMemberOptions(task.value.project)
    members.value = memberResponse.data.members || []
  } catch (error) {
    errorMsg.value = error.response?.data?.message || '获取任务详情失败'
  } finally {
    loading.value = false
  }
}

async function loadComments() {
  try {
    commentLoading.value = true
    const response = await getTaskComments(route.params.id)
    comments.value = response.data.comments || []
  } catch (error) {
    alert(error.response?.data?.message || '获取评论失败')
  } finally {
    commentLoading.value = false
  }
}

async function handleStatusChange(status) {
  try {
    await updateTaskStatus(route.params.id, { status })
    await loadTaskDetail()
  } catch (error) {
    alert(error.response?.data?.message || '更新任务状态失败')
  }
}

async function handlePriorityChange(priority) {
  try {
    await updateTaskPriority(route.params.id, { priority })
    await loadTaskDetail()
  } catch (error) {
    alert(error.response?.data?.message || '更新任务优先级失败')
  }
}

async function handleAssigneeChange() {
  try {
    await updateTaskAssignee(route.params.id, {
      assignee: selectedAssignee.value ? Number(selectedAssignee.value) : null,
    })
    await loadTaskDetail()
  } catch (error) {
    alert(error.response?.data?.message || '更新任务负责人失败')
  }
}

async function handleCreateComment() {
  const content = commentContent.value.trim()
  if (!content) {
    alert('评论内容不能为空')
    return
  }

  try {
    commentSubmitting.value = true
    await createTaskComment(route.params.id, { content })
    commentContent.value = ''
    await loadComments()
  } catch (error) {
    alert(error.response?.data?.message || '发表评论失败')
  } finally {
    commentSubmitting.value = false
  }
}

async function handleDeleteComment(commentId) {
  const confirmed = window.confirm('确定要删除这条评论吗？')
  if (!confirmed) return

  try {
    await deleteTaskComment(route.params.id, commentId)
    await loadComments()
  } catch (error) {
    alert(error.response?.data?.message || '删除评论失败')
  }
}

async function handleDelete() {
  const confirmed = window.confirm('确定要删除这个任务吗？删除后无法恢复。')
  if (!confirmed) return

  try {
    const projectId = task.value.project
    await deleteTask(route.params.id)
    router.push(`/projects/${projectId}/tasks`)
  } catch (error) {
    alert(error.response?.data?.message || '删除任务失败')
  }
}

onMounted(async () => {
  await loadTaskDetail()
  await loadComments()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 32px;
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

.card {
  background: white;
  padding: 28px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.comment-card {
  margin-top: 24px;
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
  display: inline-block;
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

.warning {
  background: #f59e0b;
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

.assignee-box {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  align-items: center;
}

.assignee-box select {
  padding: 10px 12px;
  border: 1px solid #d0d7e2;
  border-radius: 8px;
  min-width: 220px;
  font-size: 14px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 18px;
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  border: 1px solid #d0d7e2;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  resize: vertical;
  box-sizing: border-box;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  border: 1px solid #ebeef5;
  border-radius: 10px;
  padding: 14px;
  background: #fafafa;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.author {
  font-weight: bold;
  color: #333;
}

.time {
  color: #999;
  font-size: 13px;
}

.comment-content {
  color: #444;
  line-height: 1.6;
  white-space: pre-wrap;
}

.comment-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

.empty-text {
  color: #999;
}

.small {
  padding: 6px 10px;
  font-size: 12px;
}

.error {
  color: #dc2626;
}
</style>