const TOKEN_KEY = 'taskflow_access_token'
const REFRESH_TOKEN_KEY = 'taskflow_refresh_token'
const USERNAME_KEY = 'taskflow_username'


// 保存 token
export function setTokens(accessToken, refreshToken) {
  localStorage.setItem(TOKEN_KEY, accessToken)
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
}


// 获取 access token
export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY)
}


// 获取 refresh token
export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}


// 删除 token
export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}


// 判断是否登录
export function isLoggedIn() {
  return !!getAccessToken()
}


// 是否存在 token（有些地方喜欢用这个名字）
export function hasToken() {
  return !!getAccessToken()
}


// 保存用户名
export function setUsername(username) {
  localStorage.setItem(USERNAME_KEY, username)
}


// 获取用户名
export function getUsername() {
  return localStorage.getItem(USERNAME_KEY)
}


// 删除用户名
export function clearUsername() {
  localStorage.removeItem(USERNAME_KEY)
}