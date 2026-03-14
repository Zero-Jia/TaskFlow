<template>
    <div class="page">
      <div class="topbar">
        <h1>个人中心</h1>
        <router-link to="/home" class="btn secondary">返回首页</router-link>
      </div>
  
      <div class="container">
        <p v-if="loading">正在加载个人信息...</p>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
        <p v-if="successMsg" class="success">{{ successMsg }}</p>
  
        <div v-if="user" class="profile-grid">
          <div class="card profile-card">
            <h2>我的资料</h2>
  
            <div class="avatar-box">
              <img
                v-if="user.avatar"
                :src="user.avatar"
                alt="avatar"
                class="avatar"
              />
              <div v-else class="avatar-placeholder">暂无头像</div>
            </div>
  
            <div class="info-list">
              <p><strong>用户名：</strong>{{ user.username }}</p>
              <p><strong>邮箱：</strong>{{ user.email || '暂无邮箱' }}</p>
              <p><strong>简介：</strong>{{ user.bio || '暂无简介' }}</p>
              <p><strong>注册时间：</strong>{{ formatDate(user.created_at) }}</p>
            </div>
          </div>
  
          <div class="card">
            <h2>修改资料</h2>
            <form @submit.prevent="handleUpdateProfile" class="form">
              <input
                v-model="profileForm.email"
                type="email"
                placeholder="请输入邮箱"
              />
              <textarea
                v-model="profileForm.bio"
                placeholder="请输入个人简介"
              ></textarea>
              <button class="btn primary" type="submit" :disabled="profileSaving">
                {{ profileSaving ? '保存中...' : '保存资料' }}
              </button>
            </form>
          </div>
  
          <div class="card">
            <h2>上传头像</h2>
            <div class="form">
              <input
                ref="avatarInputRef"
                type="file"
                accept="image/*"
                @change="handleAvatarChange"
              />
              <p v-if="selectedAvatarName" class="file-name">
                已选择：{{ selectedAvatarName }}
              </p>
              <button
                class="btn primary"
                @click="handleUploadAvatar"
                :disabled="avatarUploading"
              >
                {{ avatarUploading ? '上传中...' : '上传头像' }}
              </button>
            </div>
          </div>
  
          <div class="card">
            <h2>修改密码</h2>
            <form @submit.prevent="handleChangePassword" class="form">
              <input
                v-model="passwordForm.old_password"
                type="password"
                placeholder="旧密码"
              />
              <input
                v-model="passwordForm.new_password"
                type="password"
                placeholder="新密码"
              />
              <input
                v-model="passwordForm.new_password_confirm"
                type="password"
                placeholder="确认新密码"
              />
              <button class="btn danger" type="submit" :disabled="passwordSaving">
                {{ passwordSaving ? '提交中...' : '修改密码' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, reactive, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '../store/user'
  import {
    getUserProfile,
    updateUserProfile,
    changeUserPassword,
    uploadUserAvatar,
  } from '../api/user'
  
  const router = useRouter()
  const userStore = useUserStore()
  
  const loading = ref(false)
  const errorMsg = ref('')
  const successMsg = ref('')
  const user = ref(null)
  
  const profileSaving = ref(false)
  const passwordSaving = ref(false)
  const avatarUploading = ref(false)
  
  const selectedAvatar = ref(null)
  const selectedAvatarName = ref('')
  const avatarInputRef = ref(null)
  
  const profileForm = reactive({
    email: '',
    bio: '',
  })
  
  const passwordForm = reactive({
    old_password: '',
    new_password: '',
    new_password_confirm: '',
  })
  
  function clearMessages() {
    errorMsg.value = ''
    successMsg.value = ''
  }
  
  function formatDate(dateString) {
    if (!dateString) return '暂无时间'
    return new Date(dateString).toLocaleString()
  }
  
  async function loadProfile() {
    try {
      loading.value = true
      clearMessages()
  
      const response = await getUserProfile()
      user.value = response.data.user
  
      profileForm.email = user.value.email || ''
      profileForm.bio = user.value.bio || ''
    } catch (error) {
      errorMsg.value = error.response?.data?.message || '获取个人信息失败'
    } finally {
      loading.value = false
    }
  }
  
  async function handleUpdateProfile() {
    try {
      profileSaving.value = true
      clearMessages()
  
      const response = await updateUserProfile({
        email: profileForm.email,
        bio: profileForm.bio,
      })
  
      user.value = response.data.user
  
      if (userStore) {
        userStore.userInfo = response.data.user
      }
  
      successMsg.value = '个人资料更新成功'
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || {}) ||
        '更新个人资料失败'
    } finally {
      profileSaving.value = false
    }
  }
  
  function handleAvatarChange(event) {
    const file = event.target.files[0] || null
    selectedAvatar.value = file
    selectedAvatarName.value = file ? file.name : ''
  }
  
  async function handleUploadAvatar() {
    if (!selectedAvatar.value) {
      errorMsg.value = '请先选择头像文件'
      successMsg.value = ''
      return
    }
  
    try {
      avatarUploading.value = true
      clearMessages()
  
      const formData = new FormData()
      formData.append('avatar', selectedAvatar.value)
  
      const response = await uploadUserAvatar(formData)
      user.value = response.data.user
  
      if (userStore) {
        userStore.userInfo = response.data.user
      }
  
      selectedAvatar.value = null
      selectedAvatarName.value = ''
  
      if (avatarInputRef.value) {
        avatarInputRef.value.value = ''
      }
  
      successMsg.value = '头像上传成功'
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || {}) ||
        '头像上传失败'
    } finally {
      avatarUploading.value = false
    }
  }
  
  async function handleChangePassword() {
    if (
      !passwordForm.old_password ||
      !passwordForm.new_password ||
      !passwordForm.new_password_confirm
    ) {
      errorMsg.value = '请填写完整密码信息'
      successMsg.value = ''
      return
    }
  
    if (passwordForm.new_password !== passwordForm.new_password_confirm) {
      errorMsg.value = '两次输入的新密码不一致'
      successMsg.value = ''
      return
    }
  
    try {
      passwordSaving.value = true
      clearMessages()
  
      await changeUserPassword({
        old_password: passwordForm.old_password,
        new_password: passwordForm.new_password,
        new_password_confirm: passwordForm.new_password_confirm,
      })
  
      passwordForm.old_password = ''
      passwordForm.new_password = ''
      passwordForm.new_password_confirm = ''
  
      successMsg.value = '密码修改成功，请重新登录'
  
      setTimeout(() => {
        userStore.logout()
        router.push('/login')
      }, 1000)
    } catch (error) {
      errorMsg.value =
        error.response?.data?.message ||
        JSON.stringify(error.response?.data?.errors || {}) ||
        '修改密码失败'
    } finally {
      passwordSaving.value = false
    }
  }
  
  onMounted(() => {
    loadProfile()
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
  }
  
  .container {
    max-width: 1100px;
    margin: 0 auto;
  }
  
  .profile-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  }
  
  .profile-card {
    grid-column: span 2;
  }
  
  .profile-card h2,
  .card h2 {
    margin-top: 0;
    margin-bottom: 16px;
    color: #111827;
  }
  
  .avatar-box {
    margin-bottom: 16px;
  }
  
  .avatar {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 50%;
    border: 1px solid #ddd;
  }
  
  .avatar-placeholder {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
  }
  
  .info-list p {
    margin: 8px 0;
    color: #374151;
  }
  
  .form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  
  input,
  textarea {
    padding: 12px;
    border: 1px solid #d0d7e2;
    border-radius: 8px;
    font-size: 14px;
    outline: none;
  }
  
  input:focus,
  textarea:focus {
    border-color: #2563eb;
  }
  
  textarea {
    min-height: 100px;
    resize: vertical;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 14px;
    border-radius: 8px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    text-align: center;
  }
  
  .primary {
    background: #2563eb;
    color: white;
  }
  
  .secondary {
    background: #e5e7eb;
    color: #111827;
  }
  
  .danger {
    background: #ef4444;
    color: white;
  }
  
  .btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  .file-name {
    margin: 0;
    color: #6b7280;
    font-size: 14px;
  }
  
  .error {
    color: #dc2626;
    margin: 0 0 16px 0;
  }
  
  .success {
    color: #16a34a;
    margin: 0 0 16px 0;
  }
  
  @media (max-width: 768px) {
    .page {
      padding: 20px;
    }
  
    .profile-grid {
      grid-template-columns: 1fr;
    }
  
    .profile-card {
      grid-column: span 1;
    }
  
    .topbar {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }
  }
  </style>