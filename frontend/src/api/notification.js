import http from './http'

export function getNotifications() {
  return http.get('/notifications/')
}

export function markNotificationAsRead(notificationId) {
  return http.post(`/notifications/${notificationId}/read/`)
}