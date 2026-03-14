<template>
  <div class="page">
    <div class="topbar">
      <h1>数据统计面板</h1>
      <router-link to="/home" class="btn secondary">返回首页</router-link>
    </div>

    <div class="container">
      <p v-if="loading" class="loading">正在加载统计数据...</p>

      <ErrorState v-if="errorMsg" title="统计数据加载失败" :message="errorMsg">
        <button class="btn secondary" @click="loadStats">重新加载</button>
      </ErrorState>

      <EmptyState
        v-if="
          !loading &&
          !errorMsg &&
          stats &&
          stats.total_assigned_tasks === 0 &&
          stats.total_created_tasks === 0
        "
        title="你还没有任务数据"
        description="先加入团队、创建项目并开始处理任务，这里就会显示统计结果。"
      />

      <template
        v-if="
          !loading &&
          !errorMsg &&
          stats &&
          !(stats.total_assigned_tasks === 0 && stats.total_created_tasks === 0)
        "
      >
        <div class="stats-grid">
          <div class="stat-card">
            <h2>我的任务总数</h2>
            <p class="value">{{ stats.total_assigned_tasks }}</p>
          </div>

          <div class="stat-card">
            <h2>我创建的任务</h2>
            <p class="value">{{ stats.total_created_tasks }}</p>
          </div>

          <div class="stat-card">
            <h2>未完成任务</h2>
            <p class="value">{{ stats.unfinished_tasks }}</p>
          </div>

          <div class="stat-card">
            <h2>高优先级任务</h2>
            <p class="value">{{ stats.high_priority_tasks }}</p>
          </div>
        </div>

        <div class="panel-grid">
          <div class="panel-card">
            <h2>任务状态分布</h2>

            <div class="bar-item">
              <div class="bar-head">
                <span>todo</span>
                <span>{{ stats.status_counts.todo }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: getPercent(stats.status_counts.todo) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bar-item">
              <div class="bar-head">
                <span>in_progress</span>
                <span>{{ stats.status_counts.in_progress }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: getPercent(stats.status_counts.in_progress) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bar-item">
              <div class="bar-head">
                <span>done</span>
                <span>{{ stats.status_counts.done }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: getPercent(stats.status_counts.done) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bar-item">
              <div class="bar-head">
                <span>overdue</span>
                <span>{{ stats.status_counts.overdue }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: getPercent(stats.status_counts.overdue) + '%' }"
                ></div>
              </div>
            </div>
          </div>

          <div class="panel-card">
            <h2>任务优先级分布</h2>

            <div class="bar-item">
              <div class="bar-head">
                <span>low</span>
                <span>{{ stats.priority_counts.low }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill green"
                  :style="{ width: getPriorityPercent(stats.priority_counts.low) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bar-item">
              <div class="bar-head">
                <span>medium</span>
                <span>{{ stats.priority_counts.medium }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill yellow"
                  :style="{ width: getPriorityPercent(stats.priority_counts.medium) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bar-item">
              <div class="bar-head">
                <span>high</span>
                <span>{{ stats.priority_counts.high }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill orange"
                  :style="{ width: getPriorityPercent(stats.priority_counts.high) + '%' }"
                ></div>
              </div>
            </div>

            <div class="bar-item">
              <div class="bar-head">
                <span>urgent</span>
                <span>{{ stats.priority_counts.urgent }}</span>
              </div>
              <div class="bar-track">
                <div
                  class="bar-fill red"
                  :style="{ width: getPriorityPercent(stats.priority_counts.urgent) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getDashboardStats } from '../api/dashboard'
import ErrorState from '../components/ErrorState.vue'
import EmptyState from '../components/EmptyState.vue'
import { getErrorMessage } from '../utils/error'

const loading = ref(false)
const errorMsg = ref('')
const stats = ref(null)

async function loadStats() {
  try {
    loading.value = true
    errorMsg.value = ''

    const response = await getDashboardStats()
    stats.value = response.data.stats
  } catch (error) {
    errorMsg.value = getErrorMessage(error, '获取统计数据失败')
  } finally {
    loading.value = false
  }
}

function getPercent(value) {
  if (!stats.value || stats.value.total_assigned_tasks === 0) return 0
  return Math.round((value / stats.value.total_assigned_tasks) * 100)
}

function getPriorityPercent(value) {
  if (!stats.value || stats.value.total_assigned_tasks === 0) return 0
  return Math.round((value / stats.value.total_assigned_tasks) * 100)
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 32px;
}

.topbar {
  max-width: 1100px;
  margin: 0 auto 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
}

.loading {
  color: #374151;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 28px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 14px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.stat-card h2 {
  font-size: 18px;
  color: #374151;
  margin-bottom: 10px;
}

.value {
  font-size: 34px;
  font-weight: bold;
  color: #2563eb;
}

.panel-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.panel-card {
  background: white;
  padding: 24px;
  border-radius: 14px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.panel-card h2 {
  margin-bottom: 20px;
  color: #111827;
}

.bar-item {
  margin-bottom: 18px;
}

.bar-head {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #374151;
  font-size: 14px;
}

.bar-track {
  width: 100%;
  height: 10px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #2563eb;
  border-radius: 999px;
}

.bar-fill.green {
  background: #10b981;
}

.bar-fill.yellow {
  background: #f59e0b;
}

.bar-fill.orange {
  background: #f97316;
}

.bar-fill.red {
  background: #ef4444;
}

.btn {
  padding: 10px 14px;
  border-radius: 8px;
  text-decoration: none;
  display: inline-block;
  border: none;
  cursor: pointer;
}

.secondary {
  background: #e5e7eb;
  color: #111827;
}

@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .panel-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page {
    padding: 20px;
  }

  .topbar {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>