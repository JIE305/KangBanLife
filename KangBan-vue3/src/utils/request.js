import axios from 'axios'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('unihealth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data.code >= 400) {
      alert(data.message || '请求失败')
      return Promise.reject(new Error(data.message))
    }
    return data
  },
  (err) => {
    const status = err.response?.status
    if (status === 401) {
      localStorage.removeItem('unihealth_token')
      localStorage.removeItem('unihealth_user')
      localStorage.removeItem('userStatus')
      sessionStorage.removeItem('isLoggedIn')
      sessionStorage.removeItem('user')
    }
    alert(err.response?.data?.message || '网络错误，请稍后再试')
    return Promise.reject(err)
  }
)

export default request
