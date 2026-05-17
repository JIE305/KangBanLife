import request from '@/utils/request'

export function getProfileAPI() {
  return request.get('/user/profile')
}

export function updateBasicAPI(data) {
  return request.put('/user/profile/basic', data)
}

export function updateContactAPI(data) {
  return request.put('/user/profile/contact', data)
}

export function uploadAvatarAPI(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/user/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
