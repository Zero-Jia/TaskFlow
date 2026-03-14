<template>
  <div class="page">
    <div class="container">
      <div class="topbar">
        <router-link
          v-if="task"
          :to="`/projects/${task.project}/tasks`"
          class="btn secondary"
        >
          返回任务列表
        </router-link>

        <router-link v-else to="/teams" class="btn secondary">
          返回团队列表
        </router-link>
      </div>

      <p v-if="loading">正在加载任务详情...</p>

      <ErrorState v-if="errorMsg" title="任务详情加载失败" :message="errorMsg">
        <router-link to="/teams" class="btn secondary">返回团队列表</router-link>
      </ErrorState>

      <!-- 任务信息 -->
      <div v-if="!loading && !errorMsg && task" class="card">
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

      <!-- 附件区 -->
      <div v-if="!loading && !errorMsg && task" class="card attachment-card">
        <h2>任务附件</h2>

        <div class="attachment-upload">
          <input type="file" @change="handleFileChange" />

          <button
            class="btn primary"
            @click="handleUploadAttachment"
            :disabled="attachmentUploading"
          >
            {{ attachmentUploading ? '上传中...' : '上传附件' }}
          </button>
        </div>

        <p v-if="attachmentLoading">附件加载中...</p>

        <p v-else-if="attachments.length === 0" class="empty-text">
          暂无附件
        </p>

        <div v-else class="attachment-list">
          <div
            v-for="attachment in attachments"
            :key="attachment.id"
            class="attachment-item"
          >
            <div class="attachment-info">
              <a
                :href="attachment.file_url"
                target="_blank"
                class="file-link"
              >
                {{ attachment.file_name }}
              </a>

              <p class="meta">
                上传者：{{ attachment.uploaded_by_username }}
                ｜ 时间：{{ attachment.uploaded_at }}
              </p>
            </div>

            <div v-if="attachment.uploaded_by_username === currentUsername">
              <button
                class="btn danger small"
                @click="handleDeleteAttachment(attachment.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 评论区 -->
      <div v-if="!loading && !errorMsg && task" class="card comment-card">
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

        <p v-else-if="comments.length === 0" class="empty-text">
          暂无评论
        </p>

        <div v-else class="comment-list">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="comment-item"
          >
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
              <button
                class="btn danger small"
                @click="handleDeleteComment(comment.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
  getTaskAttachments,
  uploadTaskAttachment,
  deleteTaskAttachment,
} from '../api/task'
import ErrorState from '../components/ErrorState.vue'
import { getErrorMessage } from '../utils/error'

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

const attachments = ref([])
const attachmentLoading = ref(false)
const attachmentUploading = ref(false)
const selectedFile = ref(null)

const currentUsername = computed(() => {
  return localStorage.getItem('username') || ''
})

async function loadTaskDetail() {
  try {
    loading.value = true
    errorMsg.value = ''

    const res = await getTaskDetail(route.params.id)
    task.value = res.data.task
    selectedAssignee.value = task.value.assignee

    const memberRes = await getProjectMemberOptions(task.value.project)
    members.value = memberRes.data.members || []
  } catch (error) {
    errorMsg.value = getErrorMessage(error, '获取任务详情失败')
  } finally {
    loading.value = false
  }
}

async function loadComments() {
  commentLoading.value = true

  try {
    const res = await getTaskComments(route.params.id)
    comments.value = res.data.comments || []
  } catch (error) {
    alert(getErrorMessage(error, '获取评论失败'))
  } finally {
    commentLoading.value = false
  }
}

async function loadAttachments() {
  attachmentLoading.value = true

  try {
    const res = await getTaskAttachments(route.params.id)
    attachments.value = res.data.attachments || []
  } catch (error) {
    alert(getErrorMessage(error, '获取附件失败'))
  } finally {
    attachmentLoading.value = false
  }
}

function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function handleUploadAttachment() {
  if (!selectedFile.value) {
    alert('请先选择文件')
    return
  }

  try {
    attachmentUploading.value = true

    const formData = new FormData()
    formData.append('file', selectedFile.value)

    await uploadTaskAttachment(route.params.id, formData)
    selectedFile.value = null

    await loadAttachments()
  } catch (error) {
    alert(getErrorMessage(error, '上传附件失败'))
  } finally {
    attachmentUploading.value = false
  }
}

async function handleDeleteAttachment(id) {
  const confirmed = window.confirm('确定删除这个附件吗？')
  if (!confirmed) return

  try {
    await deleteTaskAttachment(route.params.id, id)
    await loadAttachments()
  } catch (error) {
    alert(getErrorMessage(error, '删除附件失败'))
  }
}

async function handleStatusChange(status) {
  try {
    await updateTaskStatus(route.params.id, { status })
    await loadTaskDetail()
  } catch (error) {
    alert(getErrorMessage(error, '更新任务状态失败'))
  }
}

async function handlePriorityChange(priority) {
  try {
    await updateTaskPriority(route.params.id, { priority })
    await loadTaskDetail()
  } catch (error) {
    alert(getErrorMessage(error, '更新任务优先级失败'))
  }
}

async function handleAssigneeChange() {
  try {
    await updateTaskAssignee(route.params.id, {
      assignee: selectedAssignee.value ? Number(selectedAssignee.value) : null,
    })

    await loadTaskDetail()
  } catch (error) {
    alert(getErrorMessage(error, '修改负责人失败'))
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
    alert(getErrorMessage(error, '发表评论失败'))
  } finally {
    commentSubmitting.value = false
  }
}

async function handleDeleteComment(id) {
  const confirmed = window.confirm('确定删除评论吗？')
  if (!confirmed) return

  try {
    await deleteTaskComment(route.params.id, id)
    await loadComments()
  } catch (error) {
    alert(getErrorMessage(error, '删除评论失败'))
  }
}

async function handleDelete() {
  const confirmed = window.confirm('确定删除任务吗？')
  if (!confirmed) return

  try {
    const projectId = task.value.project
    await deleteTask(route.params.id)
    router.push(`/projects/${projectId}/tasks`)
  } catch (error) {
    alert(getErrorMessage(error, '删除任务失败'))
  }
}

onMounted(async () => {
  await loadTaskDetail()

  if (!errorMsg.value) {
    await loadComments()
    await loadAttachments()
  }
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 32px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.topbar {
  margin-bottom: 20px;
}

.card {
  background: white;
  padding: 28px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.card + .card {
  margin-top: 24px;
}

.btn {
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  display: inline-block;
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

.warning {
  background: #f59e0b;
  color: white;
}

.danger {
  background: #ef4444;
  color: white;
}

.small {
  padding: 6px 10px;
  font-size: 13px;
}

.assignee-box {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.assignee-box select {
  min-width: 220px;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
}

.action-box {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.attachment-card {
  margin-top: 24px;
}

.attachment-upload {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.attachment-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.attachment-item {
  border: 1px solid #ebeef5;
  border-radius: 10px;
  padding: 14px;
  background: #fafafa;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.attachment-info {
  flex: 1;
}

.file-link {
  font-weight: bold;
  color: #2563eb;
  text-decoration: none;
}

.file-link:hover {
  text-decoration: underline;
}

.meta {
  font-size: 13px;
  color: #777;
  margin-top: 6px;
}

.comment-card {
  margin-top: 24px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  resize: vertical;
  box-sizing: border-box;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
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
  gap: 12px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.author {
  font-weight: 600;
  color: #111827;
}

.time {
  color: #6b7280;
  font-size: 13px;
}

.comment-content {
  color: #374151;
  line-height: 1.7;
}

.comment-actions {
  margin-top: 12px;
}

.empty-text {
  color: #6b7280;
}

@media (max-width: 768px) {
  .page {
    padding: 20px;
  }

  .attachment-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>