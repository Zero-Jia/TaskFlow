import http from './http'

export function createTeam(data) {
  return http.post('/teams/create/', data)
}

export function getTeamList() {
  return http.get('/teams/')
}

export function getTeamDetail(teamId) {
  return http.get(`/teams/${teamId}/`)
}