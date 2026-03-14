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

      <!-- 任务信息 -->
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
            <option v-for="member in members" :key="member.user_id" :value="member.user_id">
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
      <div v-if="task" class="card attachment-card">

        <h2>任务附件</h2>

        <div class="attachment-upload">

          <input type="file" @change="handleFileChange">

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
  deleteTaskAttachment

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

const attachments = ref([])
const attachmentLoading = ref(false)
const attachmentUploading = ref(false)
const selectedFile = ref(null)

const currentUsername = computed(() => {
  return localStorage.getItem('username') || ''
})

async function loadTaskDetail() {

  loading.value = true

  try {

    const res = await getTaskDetail(route.params.id)

    task.value = res.data.task

    selectedAssignee.value = task.value.assignee

    const memberRes = await getProjectMemberOptions(task.value.project)

    members.value = memberRes.data.members || []

  } catch (error) {

    errorMsg.value = error.response?.data?.message || '获取任务详情失败'

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

    alert(error.response?.data?.message || '获取评论失败')

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

    alert(error.response?.data?.message || '获取附件失败')

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

    alert(error.response?.data?.message || '上传附件失败')

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

    alert(error.response?.data?.message || '删除附件失败')

  }

}

async function handleStatusChange(status) {

  await updateTaskStatus(route.params.id, { status })

  await loadTaskDetail()

}

async function handlePriorityChange(priority) {

  await updateTaskPriority(route.params.id, { priority })

  await loadTaskDetail()

}

async function handleAssigneeChange() {

  await updateTaskAssignee(route.params.id, {
    assignee: selectedAssignee.value
      ? Number(selectedAssignee.value)
      : null
  })

  await loadTaskDetail()

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

  } finally {

    commentSubmitting.value = false

  }

}

async function handleDeleteComment(id) {

  const confirmed = window.confirm('确定删除评论吗？')

  if (!confirmed) return

  await deleteTaskComment(route.params.id, id)

  await loadComments()

}

async function handleDelete() {

  const confirmed = window.confirm('确定删除任务吗？')

  if (!confirmed) return

  const projectId = task.value.project

  await deleteTask(route.params.id)

  router.push(`/projects/${projectId}/tasks`)

}

onMounted(async () => {

  await loadTaskDetail()

  await loadComments()

  await loadAttachments()

})

</script>

<style scoped>

.attachment-card {
  margin-top: 24px;
}

.attachment-upload {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
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
}

.file-link {
  font-weight: bold;
  color: #2563eb;
  text-decoration: none;
}

.meta {
  font-size: 13px;
  color: #777;
}

</style>