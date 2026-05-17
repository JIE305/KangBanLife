import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useHealthStore = defineStore('health', () => {
  const waterAmount = ref(850)
  const dailyGoal = ref(1500)
  
  const checklist = ref([
    { id: 1, text: '8:00 前起床', icon: 'solar:sun-bold', iconColor: 'text-orange-400', checked: true },
    { id: 2, text: '1500ml 饮水完成', icon: 'solar:tea-cup-bold', iconColor: 'text-emerald-500', checked: false },
    { id: 3, text: '摄入新鲜蔬果', icon: 'solar:leaf-bold', iconColor: 'text-green-500', checked: true },
    { id: 4, text: '23:30 前入睡', icon: 'solar:moon-bold', iconColor: 'text-blue-500', checked: false }
  ])

  const healthStats = ref([
    { label: '运动步数', data: [5000, 7200, 4800, 8100, 6500, 9200, 4300], unit: '步' },
    { label: '运动时间', data: [120, 240, 180, 200, 310, 280, 150], unit: 'min' }
  ])

  const trendData = ref([
    { day: '周一', fitness: 75, energy: 60 },
    { day: '周二', fitness: 78, energy: 65 },
    { day: '周三', fitness: 82, energy: 55 },
    { day: '周四', fitness: 80, energy: 70 },
    { day: '周五', fitness: 85, energy: 75 },
    { day: '周六', fitness: 88, energy: 90 },
    { day: '今日', fitness: 86, energy: 82 }
  ])

  const waterProgress = computed(() => {
    return Math.min(100, (waterAmount.value / dailyGoal.value) * 100)
  })

  const completedChecklist = computed(() => {
    return checklist.value.filter(item => item.checked).length
  })

  const addWater = (amount) => {
    waterAmount.value = Math.min(waterAmount.value + amount, dailyGoal.value * 2)
    updateChecklistCompletion()
  }

  const toggleChecklistItem = (itemId) => {
    const item = checklist.value.find(item => item.id === itemId)
    if (item) {
      item.checked = !item.checked
    }
  }

  const updateChecklistCompletion = () => {
    const waterItem = checklist.value.find(item => item.id === 2)
    if (waterItem) {
      waterItem.checked = waterAmount.value >= dailyGoal.value
    }
  }

  const calculateBMI = (height, weight) => {
    if (!height || !weight) return { result: null, status: '' }
    
    const h = height / 100
    const result = (weight / (h * h)).toFixed(1)
    let status = ''
    
    if (result < 18.5) {
      status = '偏瘦，建议增加营养'
    } else if (result < 24) {
      status = '非常标准'
    } else if (result < 28) {
      status = '偏重，建议适当运动'
    } else {
      status = '肥胖，建议咨询医生'
    }
    
    return { result, status }
  }

  const resetDailyData = () => {
    waterAmount.value = 0
    checklist.value.forEach(item => {
      item.checked = false
    })
  }

  return {
    waterAmount,
    dailyGoal,
    checklist,
    healthStats,
    trendData,
    waterProgress,
    completedChecklist,
    addWater,
    toggleChecklistItem,
    updateChecklistCompletion,
    calculateBMI,
    resetDailyData
  }
})