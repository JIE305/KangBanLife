import request from '@/utils/request'

export function loginAPI(data) {
  return request.post('/auth/login', data)
}

export function registerAPI(data) {
  return request.post('/auth/register', data)
}

export function logoutAPI() {
  return request.post('/auth/logout')
}
