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

export function getTeamMembers(teamId) {
  return http.get(`/teams/${teamId}/members/`)
}

export function inviteTeamMember(teamId, data) {
  return http.post(`/teams/${teamId}/invite/`, data)
}

export function updateTeamMemberRole(teamId, memberId, data) {
  return http.patch(`/teams/${teamId}/members/${memberId}/role/`, data)
}

export function removeTeamMember(teamId, memberId) {
  return http.delete(`/teams/${teamId}/members/${memberId}/remove/`)
}