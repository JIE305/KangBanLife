import request from '@/utils/request'

export function getPostsAPI(params = {}) {
  return request.get('/posts', { params })
}

export function createPostAPI(content) {
  return request.post('/posts', { content })
}

export function toggleLikeAPI(id) {
  return request.post(`/posts/${id}/like`)
}

export function deletePostAPI(id) {
  return request.delete(`/posts/${id}`)
}
