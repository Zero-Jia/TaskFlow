// 封装 Axios 请求
import axios from 'axios'
import { getAccessToken, clearTokens } from '../utils/auth'

const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
})

http.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      clearTokens()
    }
    return Promise.reject(error)
  }
)

export default http