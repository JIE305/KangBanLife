import request from '@/utils/request'

// AI 聊天接口响应较慢（ARK API 可能耗时 30s+），单独设置更长超时
const CHAT_TIMEOUT = 45000

export function sendMessageAPI(message) {
  return request.post('/chat/message', { message }, { timeout: CHAT_TIMEOUT })
}

export function getHistoryAPI() {
  return request.get('/chat/history')
}

export function getHistoryDetailAPI(sessionId) {
  return request.get(`/chat/history/${sessionId}`)
}
