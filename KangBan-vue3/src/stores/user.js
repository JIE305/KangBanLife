import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginAPI, registerAPI } from '@/api/auth'
import { getProfileAPI } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isLoggedIn = ref(false)
  const token = ref(null)
  const rememberMe = ref(false)

  const currentUser = computed(() => user.value)

  const saveAuth = (authUser, authToken) => {
    user.value = authUser
    token.value = authToken
    isLoggedIn.value = true

    sessionStorage.setItem('isLoggedIn', 'true')
    sessionStorage.setItem('user', JSON.stringify(authUser))
    localStorage.setItem('userStatus', 'loggedIn')
    localStorage.setItem('unihealth_token', authToken)
    localStorage.setItem('unihealth_user', JSON.stringify(authUser))
  }

  const login = async (credentials) => {
    const { studentId, password } = credentials
    const res = await loginAPI({ studentId, password })
    const { user: authUser, token: authToken } = res.data
    saveAuth(authUser, authToken)
    return { success: true, message: '登录成功' }
  }

  const register = async (userInfo) => {
    const { studentId, name, phone, password } = userInfo
    const res = await registerAPI({ studentId, username: name, phone, password })
    const { user: authUser, token: authToken } = res.data
    saveAuth(authUser, authToken)
    return { success: true, message: '注册成功' }
  }

  const fetchProfile = async () => {
    if (!token.value) return
    const res = await getProfileAPI()
    user.value = res.data.user
    sessionStorage.setItem('user', JSON.stringify(user.value))
    if (localStorage.getItem('unihealth_token')) {
      localStorage.setItem('unihealth_user', JSON.stringify(user.value))
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    isLoggedIn.value = false
    rememberMe.value = false

    sessionStorage.removeItem('isLoggedIn')
    sessionStorage.removeItem('user')
    localStorage.removeItem('userStatus')
    localStorage.removeItem('unihealth_token')
    localStorage.removeItem('unihealth_user')
  }

  const setRememberMe = (value) => {
    rememberMe.value = value
  }

  const checkAuth = () => {
    const savedToken = localStorage.getItem('unihealth_token')
    const savedUser = localStorage.getItem('unihealth_user')

    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
      isLoggedIn.value = true
      rememberMe.value = true

      sessionStorage.setItem('isLoggedIn', 'true')
      sessionStorage.setItem('user', savedUser)
      localStorage.setItem('userStatus', 'loggedIn')

      return true
    }
    return false
  }

  return {
    user,
    isLoggedIn,
    token,
    rememberMe,
    currentUser,
    login,
    register,
    fetchProfile,
    logout,
    setRememberMe,
    checkAuth
  }
})
