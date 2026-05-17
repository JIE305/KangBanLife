import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useUserStore } from '../../src/stores/user'

describe('useUserStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('initial state', () => {
    it('should have correct initial state', () => {
      const store = useUserStore()
      
      expect(store.user).toBe(null)
      expect(store.isLoggedIn).toBe(false)
      expect(store.token).toBe(null)
      expect(store.rememberMe).toBe(false)
      expect(store.currentUser).toBe(null)
    })
  })

  describe('login', () => {
    it('should set user and isLoggedIn after login', async () => {
      const store = useUserStore()
      
      const result = await store.login({
        studentId: '2021001',
        password: 'password123'
      })
      
      expect(result.success).toBe(true)
      expect(result.message).toBe('登录成功')
      expect(store.user).not.toBe(null)
      expect(store.user.studentId).toBe('2021001')
      expect(store.isLoggedIn).toBe(true)
      expect(store.token).not.toBe(null)
    })

    it('should store token in localStorage when rememberMe is true', async () => {
      const store = useUserStore()
      store.setRememberMe(true)
      
      await store.login({
        studentId: '2021001',
        password: 'password123'
      })
      
      expect(localStorage.getItem('unihealth_token')).not.toBe(null)
      expect(localStorage.getItem('unihealth_user')).not.toBe(null)
    })
  })

  describe('register', () => {
    it('should create user and set isLoggedIn', async () => {
      const store = useUserStore()
      
      const result = await store.register({
        studentId: '2021002',
        name: '张三',
        phone: '13800138000',
        password: 'password123'
      })
      
      expect(result.success).toBe(true)
      expect(result.message).toBe('注册成功')
      expect(store.user).not.toBe(null)
      expect(store.user.name).toBe('张三')
      expect(store.isLoggedIn).toBe(true)
    })

    it('should mask phone number', async () => {
      const store = useUserStore()
      
      await store.register({
        studentId: '2021002',
        name: '张三',
        phone: '13800138000',
        password: 'password123'
      })
      
      expect(store.user.phone).toBe('138****8000')
    })
  })

  describe('logout', () => {
    it('should clear user data on logout', async () => {
      const store = useUserStore()
      await store.login({
        studentId: '2021001',
        password: 'password123'
      })
      
      store.logout()
      
      expect(store.user).toBe(null)
      expect(store.isLoggedIn).toBe(false)
      expect(store.token).toBe(null)
      expect(localStorage.getItem('unihealth_token')).toBe(null)
    })
  })

  describe('checkAuth', () => {
    it('should restore session from localStorage', () => {
      const store = useUserStore()
      
      localStorage.setItem('unihealth_token', 'test-token')
      localStorage.setItem('unihealth_user', JSON.stringify({
        id: 1,
        studentId: '2021001',
        name: 'Test User'
      }))
      
      const result = store.checkAuth()
      
      expect(result).toBe(true)
      expect(store.isLoggedIn).toBe(true)
      expect(store.user.studentId).toBe('2021001')
    })

    it('should return false when no session exists', () => {
      const store = useUserStore()
      
      localStorage.removeItem('unihealth_token')
      localStorage.removeItem('unihealth_user')
      
      const result = store.checkAuth()
      
      expect(result).toBe(false)
      expect(store.isLoggedIn).toBe(false)
    })
  })

  describe('setRememberMe', () => {
    it('should set rememberMe flag', () => {
      const store = useUserStore()
      
      store.setRememberMe(true)
      expect(store.rememberMe).toBe(true)
      
      store.setRememberMe(false)
      expect(store.rememberMe).toBe(false)
    })
  })
})