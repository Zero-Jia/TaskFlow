<template>
    <div class="page">
      <div class="card">
        <div class="code">404</div>
        <h1>页面不存在</h1>
        <p>你访问的页面可能已经被删除，或者链接地址输入有误。</p>
  
        <div class="actions">
          <router-link to="/home" class="btn primary">返回首页</router-link>
          <router-link to="/teams" class="btn secondary">我的团队</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  .page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f5f7fb;
    padding: 24px;
  }
  
  .card {
    width: 100%;
    max-width: 500px;
    background: white;
    padding: 40px 32px;
    border-radius: 14px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
    text-align: center;
  }
  
  .code {
    font-size: 64px;
    font-weight: bold;
    color: #2563eb;
    margin-bottom: 12px;
  }
  
  h1 {
    font-size: 28px;
    margin-bottom: 12px;
    color: #111827;
  }
  
  p {
    font-size: 15px;
    color: #6b7280;
    margin-bottom: 24px;
    line-height: 1.7;
  }
  
  .actions {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
  }
  
  .btn {
    padding: 10px 16px;
    border-radius: 8px;
    text-decoration: none;
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
  </style>