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

export function updateTask(taskId, data) {
  return http.put(`/tasks/${taskId}/update/`, data)
}

export function updateTaskStatus(taskId, data) {
  return http.patch(`/tasks/${taskId}/status/`, data)
}

export function updateTaskPriority(taskId, data) {
  return http.patch(`/tasks/${taskId}/priority/`, data)
}

export function updateTaskAssignee(taskId, data) {
  return http.patch(`/tasks/${taskId}/assignee/`, data)
}

export function deleteTask(taskId) {
  return http.delete(`/tasks/${taskId}/delete/`)
}

export function getProjectMemberOptions(projectId) {
  return http.get(`/projects/${projectId}/member-options/`)
}

export function getTaskComments(taskId) {
  return http.get(`/tasks/${taskId}/comments/`)
}

export function createTaskComment(taskId, data) {
  return http.post(`/tasks/${taskId}/comments/`, data)
}

export function deleteTaskComment(taskId, commentId) {
  return http.delete(`/tasks/${taskId}/comments/${commentId}/delete/`)
}

export function getProjectTaskBoard(projectId) {
  return http.get(`/projects/${projectId}/task-board/`)
}