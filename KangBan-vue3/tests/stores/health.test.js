import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useHealthStore } from '../../src/stores/health'

describe('useHealthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('initial state', () => {
    it('should have correct initial state', () => {
      const store = useHealthStore()
      
      expect(store.waterAmount).toBe(850)
      expect(store.dailyGoal).toBe(1500)
      expect(store.checklist.length).toBe(4)
      expect(store.healthStats.length).toBe(2)
      expect(store.trendData.length).toBe(7)
    })
  })

  describe('waterProgress', () => {
    it('should calculate correct water progress', () => {
      const store = useHealthStore()
      
      expect(store.waterProgress).toBeCloseTo(56.67, 2)
      
      store.waterAmount = 1500
      expect(store.waterProgress).toBe(100)
      
      store.waterAmount = 3000
      expect(store.waterProgress).toBe(100)
    })
  })

  describe('completedChecklist', () => {
    it('should count completed checklist items', () => {
      const store = useHealthStore()
      
      const completed = store.checklist.filter(item => item.checked).length
      expect(store.completedChecklist).toBe(completed)
    })
  })

  describe('addWater', () => {
    it('should add water amount', () => {
      const store = useHealthStore()
      const initial = store.waterAmount
      
      store.addWater(150)
      expect(store.waterAmount).toBe(initial + 150)
    })

    it('should not exceed double daily goal', () => {
      const store = useHealthStore()
      
      store.addWater(3000)
      expect(store.waterAmount).toBe(3000)
    })

    it('should update checklist when goal is reached', () => {
      const store = useHealthStore()
      store.waterAmount = 1499
      
      const waterItem = store.checklist.find(item => item.id === 2)
      expect(waterItem.checked).toBe(false)
      
      store.addWater(1)
      expect(waterItem.checked).toBe(true)
    })
  })

  describe('toggleChecklistItem', () => {
    it('should toggle checklist item', () => {
      const store = useHealthStore()
      const item = store.checklist[0]
      const initial = item.checked
      
      store.toggleChecklistItem(item.id)
      expect(item.checked).toBe(!initial)
    })
  })

  describe('calculateBMI', () => {
    it('should calculate BMI correctly', () => {
      const store = useHealthStore()
      
      const result = store.calculateBMI(175, 65)
      expect(result.result).toBe('21.2')
      expect(result.status).toBe('非常标准')
    })

    it('should return status for underweight', () => {
      const store = useHealthStore()
      
      const result = store.calculateBMI(175, 50)
      expect(result.status).toBe('偏瘦，建议增加营养')
    })

    it('should return status for overweight', () => {
      const store = useHealthStore()
      
      const result = store.calculateBMI(175, 85)
      expect(result.status).toBe('偏重，建议适当运动')
    })

    it('should return status for obese', () => {
      const store = useHealthStore()
      
      const result = store.calculateBMI(175, 100)
      expect(result.status).toBe('肥胖，建议咨询医生')
    })

    it('should return empty result for missing inputs', () => {
      const store = useHealthStore()
      
      const result = store.calculateBMI(null, 65)
      expect(result.result).toBe(null)
      expect(result.status).toBe('')
    })
  })

  describe('resetDailyData', () => {
    it('should reset daily data', () => {
      const store = useHealthStore()
      store.waterAmount = 1500
      store.checklist.forEach(item => { item.checked = true })
      
      store.resetDailyData()
      
      expect(store.waterAmount).toBe(0)
      store.checklist.forEach(item => {
        expect(item.checked).toBe(false)
      })
    })
  })
})