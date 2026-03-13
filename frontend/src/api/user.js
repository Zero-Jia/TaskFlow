// 封装用户 API
import http from './http'

export function registerUser(data) {
  return http.post('/users/register/', data)
}

export function loginUser(data) {
  return http.post('/users/login/', data)
}

export function getUserProfile() {
  return http.get('/users/profile/')
}