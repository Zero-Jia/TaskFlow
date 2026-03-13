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