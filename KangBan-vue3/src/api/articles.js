import request from '@/utils/request'

export function getArticlesAPI(params = {}) {
  return request.get('/articles', { params })
}

export function getFeaturedAPI(limit = 3) {
  return request.get('/articles/featured', { params: { limit } })
}

export function getArticleDetailAPI(id) {
  return request.get(`/articles/${id}`)
}
