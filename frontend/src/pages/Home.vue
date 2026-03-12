<template>
    <div class="home">
      <h1>TaskFlow 协作任务管理平台</h1>
      <p>前端项目已成功启动。</p>
  
      <button @click="checkBackend" class="btn">测试后端连接</button>
  
      <div v-if="result" class="result">
        <p><strong>后端返回：</strong></p>
        <pre>{{ result }}</pre>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import http from '../api/http'
  
  const result = ref('')
  
  async function checkBackend() {
    try {
      const response = await http.get('/health/')
      result.value = JSON.stringify(response.data, null, 2)
    } catch (error) {
      result.value = '请求失败：' + (error.message || 'unknown error')
    }
  }
  </script>
  
  <style scoped>
  .home {
    padding: 40px;
  }
  
  h1 {
    margin-bottom: 16px;
    font-size: 32px;
  }
  
  p {
    margin-bottom: 10px;
    font-size: 16px;
    color: #555;
  }
  
  .btn {
    margin-top: 16px;
    padding: 10px 18px;
    border: none;
    background: #2563eb;
    color: white;
    border-radius: 6px;
    cursor: pointer;
  }
  
  .btn:hover {
    background: #1d4ed8;
  }
  
  .result {
    margin-top: 20px;
    padding: 16px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
  
  pre {
    white-space: pre-wrap;
    word-break: break-word;
  }
  </style>