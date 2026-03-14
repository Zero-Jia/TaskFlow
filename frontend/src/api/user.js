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

export function updateUserProfile(data) {
  return http.put('/users/profile/update/', data)
}

export function changeUserPassword(data) {
  return http.post('/users/change-password/', data)
}

export function uploadUserAvatar(formData) {
  return http.post('/users/avatar/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}