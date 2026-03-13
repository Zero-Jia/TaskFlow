import http from './http'

export function createProject(data) {
  return http.post('/projects/create/', data)
}

export function getTeamProjects(teamId) {
  return http.get(`/teams/${teamId}/projects/`)
}

export function getProjectDetail(projectId) {
  return http.get(`/projects/${projectId}/`)
}

export function updateProject(projectId, data) {
  return http.put(`/projects/${projectId}/update/`, data)
}

export function updateProjectStatus(projectId, data) {
  return http.patch(`/projects/${projectId}/status/`, data)
}

export function deleteProject(projectId) {
  return http.delete(`/projects/${projectId}/delete/`)
}