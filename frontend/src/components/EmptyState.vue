<template>
    <div class="empty-state">
      <div class="icon">📭</div>
      <p class="title">{{ title }}</p>
      <p v-if="description" class="description">{{ description }}</p>
      <div v-if="$slots.default" class="actions">
        <slot />
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      default: '暂无数据',
    },
    description: {
      type: String,
      default: '',
    },
  })
  </script>
  
  <style scoped>
  .empty-state {
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
    color: #1f2937;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  .description {
    color: #6b7280;
    margin-bottom: 16px;
    line-height: 1.6;
  }
  
  .actions {
    display: flex;
    justify-content: center;
    gap: 12px;
  }
  </style>