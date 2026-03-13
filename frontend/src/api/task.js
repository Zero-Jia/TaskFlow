import http from './http'

export function createTask(data) {
  return http.post('/tasks/create/', data)
}

export function getProjectTasks(projectId) {
  return http.get(`/projects/${projectId}/tasks/`)
}

export function getTaskDetail(taskId) {
  return http.get(`/tasks/${taskId}/`)
}