<template>
    <div class="error-state">
      <div class="icon">⚠️</div>
      <p class="title">{{ title }}</p>
      <p class="message">{{ message }}</p>
      <div v-if="$slots.default" class="actions">
        <slot />
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      default: '加载失败',
    },
    message: {
      type: String,
      default: '请稍后重试',
    },
  })
  </script>
  
  <style scoped>
  .error-state {
    background: white;
    padding: 32px 24px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
  }
  
  .icon {
    font-size: 32px;
    margin-bottom: 12px;
  }
  
  .title {
    font-size: 18px;
    color: #dc2626;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  .message {
    color: #6b7280;
    margin-bottom: 16px;
    line-height: 1.6;
    word-break: break-word;
  }
  
  .actions {
    display: flex;
    justify-content: center;
    gap: 12px;
  }
  </style>