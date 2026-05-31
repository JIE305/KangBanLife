import request from '@/utils/request'

export function getMatchesAPI(params = {}) {
  return request.get('/matches', { params })
}

export function createMatchAPI(data) {
  return request.post('/matches', data)
}

export function deleteMatchAPI(id) {
  return request.delete(`/matches/${id}`)
}