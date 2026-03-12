<template>
  <div id="app">
    <header class="navbar">
      <div class="logo">TaskFlow</div>
      <nav class="nav-links">
        <a href="/">首页</a>
      </nav>
    </header>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f5f7fb;
  color: #222;
}

.navbar {
  height: 64px;
  background: #1f2937;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.logo {
  font-size: 22px;
  font-weight: bold;
}

.nav-links a {
  color: white;
  text-decoration: none;
  margin-left: 16px;
}

.main-content {
  padding: 24px;
}
</style>