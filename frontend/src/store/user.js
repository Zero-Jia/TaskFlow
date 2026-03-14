// 用 Pinia 管理用户状态
import { defineStore } from 'pinia'
import { loginUser, getUserProfile } from '../api/user'
import { setTokens, clearTokens, isLoggedIn } from '../utils/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
  }),

  getters: {
    isAuthenticated: () => isLoggedIn(),
  },

  actions: {
    async login(formData) {
      const response = await loginUser(formData)
      const data = response.data

      setTokens(data.access_token, data.refresh_token)
      this.userInfo = data.user || null

      if (data.user?.username) {
        localStorage.setItem('username', data.user.username)
      }

      return data
    },

    async fetchProfile() {
      const response = await getUserProfile()
      this.userInfo = response.data.user || response.data

      if (this.userInfo?.username) {
        localStorage.setItem('username', this.userInfo.username)
      }

      return this.userInfo
    },

    logout() {
      clearTokens()
      localStorage.removeItem('username')
      this.userInfo = null
    },
  },
})