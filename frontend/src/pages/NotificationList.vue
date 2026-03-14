<template>
    <div class="page">
      <div class="topbar">
        <h1>通知中心</h1>
        <router-link to="/home" class="btn secondary">返回首页</router-link>
      </div>
  
      <div class="container">
        <p class="summary">未读通知：{{ unreadCount }}</p>
  
        <p v-if="loading">正在加载通知...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  
        <div v-if="!loading && notifications.length === 0" class="empty-box">
          暂无通知
        </div>
  
        <div v-if="notifications.length > 0" class="notification-list">
          <div
            v-for="item in notifications"
            :key="item.id"
            class="notification-item"
            :class="{ unread: !item.is_read }"
          >
            <div class="content">
              <p class="text">{{ item.content }}</p>
              <p class="meta">
                类型：{{ formatType(item.type) }} ｜ 时间：{{ formatTime(item.created_at) }}
              </p>
            </div>
  
            <div class="actions">
              <router-link
                v-if="item.related_task_id"
                :to="`/tasks/${item.related_task_id}`"
                class="btn primary"
              >
                查看任务
              </router-link>
  
              <button
                v-if="!item.is_read"
                class="btn success"
                @click="handleMarkRead(item.id)"
              >
                标记已读
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { getNotifications, markNotificationAsRead } from '../api/notification'
  
  const loading = ref(false)
  const errorMsg = ref('')
  const notifications = ref([])
  const unreadCount = ref(0)
  
  function formatType(type) {
    if (type === 'task_assigned') return '任务指派'
    if (type === 'task_comment') return '任务评论'
    return type
  }
  
  function formatTime(timeStr) {
    if (!timeStr) return ''
    return new Date(timeStr).toLocaleString()
  }
  
  async function loadNotifications() {
    try {
      loading.value = true
      errorMsg.value = ''
  
      const response = await getNotifications()
      notifications.value = response.data.notifications || []
      unreadCount.value = response.data.unread_count || 0
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取通知失败'
    } finally {
      loading.value = false
    }
  }
  
  async function handleMarkRead(notificationId) {
    try {
      await markNotificationAsRead(notificationId)
      await loadNotifications()
    } catch (error) {
      alert(error.response?.data?.message || '标记已读失败')
    }
  }
  
  onMounted(() => {
    loadNotifications()
  })
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    background: #f5f7fb;
    padding: 32px;
  }
  
  .topbar {
    max-width: 900px;
    margin: 0 auto 24px auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .container {
    max-width: 900px;
    margin: 0 auto;
  }
  
  .summary {
    font-weight: bold;
    margin-bottom: 16px;
  }
  
  .notification-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .notification-item {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.05);
    display: flex;
    justify-content: space-between;
    gap: 20px;
    align-items: center;
  }
  
  .notification-item.unread {
    border-left: 5px solid #2563eb;
  }
  
  .content {
    flex: 1;
  }
  
  .text {
    margin: 0 0 8px 0;
    font-size: 15px;
    color: #111827;
  }
  
  .meta {
    margin: 0;
    font-size: 13px;
    color: #666;
  }
  
  .actions {
    display: flex;
    gap: 10px;
    align-items: center;
  }
  
  .btn {
    padding: 10px 14px;
    border-radius: 8px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
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
  
  .error {
    color: #dc2626;
  }
  
  .empty-box {
    background: white;
    padding: 24px;
    border-radius: 12px;
    color: #666;
  }
  </style>