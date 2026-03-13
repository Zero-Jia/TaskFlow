<template>
  <div class="page">
    <div class="container">
      <div class="topbar">
        <router-link to="/teams" class="btn secondary">返回团队列表</router-link>
      </div>

      <p v-if="loading">正在加载团队详情...</p>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

      <div v-if="team" class="card">
        <h1>{{ team.name }}</h1>
        <p><strong>描述：</strong>{{ team.description || '暂无描述' }}</p>
        <p><strong>拥有者：</strong>{{ team.owner_username }}</p>
        <p><strong>成员数：</strong>{{ team.member_count }}</p>

        <div class="invite-box">
          <h2>邀请成员</h2>
          <div class="invite-form">
            <input
              v-model="inviteUsername"
              type="text"
              placeholder="输入要邀请的用户名"
            />
            <button @click="handleInvite" :disabled="inviteLoading">
              {{ inviteLoading ? '邀请中...' : '邀请' }}
            </button>
          </div>
          <p v-if="inviteMsg" class="success">{{ inviteMsg }}</p>
          <p v-if="inviteError" class="error">{{ inviteError }}</p>
        </div>

        <h2>团队成员</h2>
        <div v-if="team.members.length === 0">暂无成员</div>

        <div v-for="member in team.members" :key="member.id" class="member-item">
          <p><strong>用户名：</strong>{{ member.username }}</p>
          <p><strong>邮箱：</strong>{{ member.email }}</p>
          <p><strong>角色：</strong>{{ member.role }}</p>

          <div class="member-actions" v-if="member.role !== 'owner'">
            <button class="btn admin" @click="changeRole(member.id, 'admin')">设为管理员</button>
            <button class="btn member" @click="changeRole(member.id, 'member')">设为普通成员</button>
            <button class="btn danger" @click="handleRemove(member.id)">移除成员</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  getTeamDetail,
  inviteTeamMember,
  updateTeamMemberRole,
  removeTeamMember,
} from '../api/team'

const route = useRoute()
const team = ref(null)
const loading = ref(false)
const errorMsg = ref('')

const inviteUsername = ref('')
const inviteLoading = ref(false)
const inviteMsg = ref('')
const inviteError = ref('')

async function loadTeamDetail() {
  try {
    loading.value = true
    errorMsg.value = ''
    const response = await getTeamDetail(route.params.id)
    team.value = response.data.team
  } catch (error) {
    errorMsg.value = error.response?.data?.message || '获取团队详情失败'
  } finally {
    loading.value = false
  }
}

async function handleInvite() {
  inviteMsg.value = ''
  inviteError.value = ''

  if (!inviteUsername.value.trim()) {
    inviteError.value = '请输入用户名'
    return
  }

  try {
    inviteLoading.value = true
    await inviteTeamMember(route.params.id, {
      username: inviteUsername.value,
    })
    inviteMsg.value = '邀请成功'
    inviteUsername.value = ''
    await loadTeamDetail()
  } catch (error) {
    inviteError.value = error.response?.data?.message || '邀请失败'
  } finally {
    inviteLoading.value = false
  }
}

async function changeRole(memberId, role) {
  try {
    await updateTeamMemberRole(route.params.id, memberId, { role })
    await loadTeamDetail()
  } catch (error) {
    alert(error.response?.data?.message || '修改角色失败')
  }
}

async function handleRemove(memberId) {
  const confirmed = window.confirm('确定要移除这个成员吗？')
  if (!confirmed) return

  try {
    await removeTeamMember(route.params.id, memberId)
    await loadTeamDetail()
  } catch (error) {
    alert(error.response?.data?.message || '移除成员失败')
  }
}

onMounted(() => {
  loadTeamDetail()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 32px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.card {
  background: white;
  padding: 28px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
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
}

.secondary {
  background: #e5e7eb;
  color: #111827;
}

.invite-box {
  margin-top: 24px;
  margin-bottom: 28px;
  padding: 20px;
  background: #f9fafb;
  border-radius: 10px;
}

.invite-form {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.invite-form input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
}

.invite-form button {
  background: #2563eb;
  color: white;
}

.member-item {
  margin-top: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 10px;
}

.member-actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.admin {
  background: #2563eb;
  color: white;
}

.member {
  background: #10b981;
  color: white;
}

.danger {
  background: #ef4444;
  color: white;
}

.error {
  color: #dc2626;
}

.success {
  color: #16a34a;
}
</style>