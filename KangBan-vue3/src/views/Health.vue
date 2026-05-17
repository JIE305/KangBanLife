<template>
  <div class="text-slate-800">
    <Navbar 
      theme="emerald" 
      logo-icon="solar:health-bold" 
      right-content="date" 
      :show-login="false" 
      :show-notification="false" />

    <main class="max-w-[1440px] mx-auto px-6 py-10">
      <div class="grid md:grid-cols-12 gap-8">
        <!-- 左侧：每日打卡与小工具 (Col 4) -->
        <div class="md:col-span-4 space-y-8">
          <!-- 每日打卡 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-emerald-500" icon="solar:checklist-minimalistic-bold"></iconify-icon> 今日健康清单
            </h3>
            <div class="space-y-4">
              <label v-for="(item, idx) in checklist" :key="idx"
                class="flex items-center justify-between p-3 bg-slate-50 rounded-xl cursor-pointer hover:bg-emerald-50 transition-colors">
                <span class="flex items-center gap-3">
                  <iconify-icon :class="item.iconColor" :icon="item.icon" width="24"></iconify-icon>
                  <span>{{ item.text }}</span>
                </span>
                <input v-model="item.checked" class="w-5 h-5 accent-emerald-500" type="checkbox" />
              </label>
            </div>
          </div>
          <!-- BMI 计算器 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
              <iconify-icon class="text-blue-500" icon="solar:calculator-bold"></iconify-icon> BMI 快速测算
            </h3>
            <div class="space-y-4">
              <div>
                <label class="text-xs text-slate-400 mb-1 block">身高 (cm)</label>
                <input v-model.number="height"
                  class="w-full bg-slate-50 border-none rounded-xl px-4 py-2 text-sm focus:ring-1 focus:ring-emerald-500"
                  placeholder="例如 175" type="number" />
              </div>
              <div>
                <label class="text-xs text-slate-400 mb-1 block">体重 (kg)</label>
                <input v-model.number="weight"
                  class="w-full bg-slate-50 border-none rounded-xl px-4 py-2 text-sm focus:ring-1 focus:ring-emerald-500"
                  placeholder="例如 65" type="number" />
              </div>
              <button @click="calculateBMI"
                class="w-full bg-emerald-500 text-white py-2 rounded-xl text-sm font-bold shadow-lg shadow-emerald-100">开始计算</button>
              <div v-if="bmiResult" class="p-3 bg-emerald-50 rounded-xl text-center">
                <p class="text-xs text-emerald-600 mb-1">您的 BMI 为: {{ bmiResult }}</p>
                <span class="text-sm font-bold text-emerald-700">身体状况：{{ bmiStatus }}</span>
              </div>
            </div>
          </div>
        </div>
        <!-- 中间：核心记录区 (Col 8) -->
        <div class="md:col-span-8 space-y-8">
          <!-- 饮水记录 -->
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
            <div class="flex items-center justify-between mb-8">
              <div>
                <h3 class="text-xl font-bold mb-1">饮水记录</h3>
                <p class="text-slate-400 text-xs">建议每日饮水 1500ml - 2000ml</p>
              </div>
              <div class="text-emerald-500 font-bold text-2xl">{{ waterAmount }} <span
                  class="text-sm text-slate-400 font-normal">/ 1500 ml</span></div>
            </div>
            <div class="flex gap-4 mb-8">
              <button v-for="cup in cups" :key="cup.amount" @click="addWater(cup.amount)"
                class="flex-1 p-4 bg-emerald-50 hover:bg-emerald-100 rounded-2xl transition-all group flex flex-col items-center gap-2">
                <iconify-icon :class="cup.color" :icon="cup.icon" width="32"></iconify-icon>
                <span class="text-sm font-bold text-emerald-700">+ {{ cup.amount }}ml</span>
                <span class="text-[10px] text-emerald-400">{{ cup.label }}</span>
              </button>
            </div>
            <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
              <div class="bg-emerald-500 h-full transition-all"
                :style="{ width: `${Math.min(100, (waterAmount / 1500) * 100)}%` }"></div>
            </div>
          </div>
          <!-- 饮食建议 -->
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
            <div class="flex items-center justify-between mb-8">
              <h3 class="text-xl font-bold">校内食堂配餐建议</h3>
              <div class="flex bg-slate-100 p-1 rounded-lg">
                <button v-for="tab in mealTabs" :key="tab" @click="activeMeal = tab"
                  class="px-3 py-1 text-xs rounded-md transition-all"
                  :class="activeMeal === tab ? 'bg-emerald-500 text-white' : ''">
                  {{ tab }}
                </button>
              </div>
            </div>
            <div class="grid md:grid-cols-2 gap-6">
              <div v-for="meal in meals" :key="meal.id"
                class="p-5 bg-slate-50 rounded-2xl border border-slate-100 hover:border-emerald-200 transition-all">
                <div class="flex items-start justify-between mb-4">
                  <span class="w-10 h-10 bg-white rounded-lg flex items-center justify-center" :class="meal.iconColor">
                    <iconify-icon :icon="meal.icon" width="24"></iconify-icon>
                  </span>
                  <span class="px-2 py-0.5 text-[10px] font-bold rounded" :class="meal.tagClass">{{ meal.tag }}</span>
                </div>
                <h4 class="font-bold mb-2">{{ meal.title }}</h4>
                <p class="text-xs text-slate-500 leading-relaxed mb-4">{{ meal.desc }}</p>
                <div class="text-[10px] text-slate-400 flex items-center gap-4">
                  <span>🔥 约 {{ meal.calories }} kcal</span>
                  <span>💪 蛋白 {{ meal.protein }}g</span>
                </div>
              </div>
            </div>
          </div>
          <!-- 身体状态趋势 -->
          <div class="relative">
            <div class="glass-card p-6 rounded-[2.5rem] shadow-2xl relative z-10">
              <div class="flex items-center justify-between mb-6">
                <h3 class="font-bold text-lg flex items-center gap-2">
                  <iconify-icon class="text-emerald-500" icon="solar:chart-square-bold"></iconify-icon> 精神状态趋势图
                </h3>
                <span class="text-xs text-slate-400">点击图表可编辑数据</span>
              </div>
              <div ref="chartRef" class="w-full h-[300px]"></div>
            </div>
            <!-- 装饰元素 -->
            <div
              class="absolute -top-6 -right-6 w-32 h-32 bg-blue-100 rounded-full mix-blend-multiply filter blur-2xl opacity-70 animate-blob">
            </div>
            <div
              class="absolute -bottom-10 -left-10 w-48 h-48 bg-emerald-100 rounded-full mix-blend-multiply filter blur-2xl opacity-70 animate-blob animation-delay-2000">
            </div>

            <!-- Toast消息提示 -->
            <Transition name="toast">
              <div v-if="showToast"
                class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-emerald-500 text-white px-6 py-3 rounded-full shadow-lg shadow-emerald-200 flex items-center gap-2 z-50">
                <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
                <span class="text-sm font-medium">{{ toastMessage }}</span>
              </div>
            </Transition>

            <!-- 编辑模态框 -->
            <Transition name="modal">
              <div v-if="isEditing" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
                @click.self="cancelEdit">
                <div class="bg-white rounded-2xl p-6 w-96 shadow-2xl">
                  <div class="flex items-center justify-between mb-6">
                    <h3 class="text-lg font-bold text-slate-800">编辑数据</h3>
                    <button @click="cancelEdit" class="text-slate-400 hover:text-slate-600 transition-colors">
                      <iconify-icon icon="solar:cross-bold" width="20"></iconify-icon>
                    </button>
                  </div>
                  <div class="space-y-4">
                    <div>
                      <label class="block text-sm font-medium text-slate-600 mb-2">日期</label>
                      <input v-model="editingDate" disabled
                        class="w-full bg-slate-100 border border-slate-200 rounded-lg px-4 py-2 text-slate-600" />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-slate-600 mb-2">
                        {{ editingType === 'physical' ? '身体素质' : '精力水平' }}
                      </label>
                      <input v-model="editingValue" type="number" min="0" max="100"
                        class="w-full bg-white border border-slate-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                        placeholder="请输入数值（0-100）" />
                    </div>
                    <div class="flex gap-3 pt-4">
                      <button @click="cancelEdit"
                        class="flex-1 px-4 py-2 bg-slate-100 text-slate-600 rounded-lg font-medium hover:bg-slate-200 transition-colors">
                        取消
                      </button>
                      <button @click="saveEdit" :disabled="isLoading"
                        class="flex-1 px-4 py-2 bg-emerald-500 text-white rounded-lg font-medium hover:bg-emerald-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                        {{ isLoading ? '保存中...' : '保存' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import Navbar from '@/components/Navbar.vue'

const chartRef = ref(null)
let chart = null

const height = ref(null)
const weight = ref(null)
const bmiResult = ref(null)
const bmiStatus = ref('')
const waterAmount = ref(0)
const activeMeal = ref('早餐')

// 编辑相关状态
const isEditing = ref(false)
const editingIndex = ref(0)
const editingType = ref('physical') // 'physical' 表示身体素质, 'energy' 表示精力水平
const editingValue = ref('')
const editingDate = ref('')
const isLoading = ref(false)
const showToast = ref(false)
const toastMessage = ref('')

// 图表数据 - 使用响应式数据便于更新
const physicalData = ref([75, 78, 82, 80, 85, 88, 86])
const energyData = ref([60, 65, 55, 70, 75, 90, 82])

// 生成最近7天日期（MM-DD格式）
const generateLast7Days = () => {
  const dates = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(today.getDate() - i)
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    dates.push(`${month}-${day}`)
  }
  return dates
}

const xAxisDates = generateLast7Days()

const checklist = ref([
  { text: '8:00 前起床', icon: 'solar:sun-bold', iconColor: 'text-orange-400', checked: true },
  { text: '1500ml 饮水完成', icon: 'solar:tea-cup-bold', iconColor: 'text-emerald-500', checked: false },
  { text: '摄入新鲜蔬果', icon: 'solar:leaf-bold', iconColor: 'text-green-500', checked: true },
  { text: '23:30 前入睡', icon: 'solar:moon-bold', iconColor: 'text-blue-500', checked: false }
])

const cups = ref([
  { amount: 150, icon: 'solar:cup-first-bold', color: 'text-emerald-400', label: '小杯水' },
  { amount: 250, icon: 'ri:water-flash-line', color: 'text-emerald-500', label: '中杯水' },
  { amount: 500, icon: 'solar:bottle-bold', color: 'text-emerald-600', label: '大瓶水' }
])

const mealTabs = ['早餐', '午餐', '晚餐']

const allMeals = [
  {
    id: 1, mealType: '早餐',
    icon: 'mdi:food-variant', iconColor: 'text-emerald-500',
    tag: '均衡选择', tagClass: 'bg-emerald-100 text-emerald-600',
    title: '元气满分早餐',
    desc: '全麦包 + 煮鸡蛋 + 无糖豆浆/牛奶 + 一小份当季水果。',
    calories: 350, protein: 20
  },
  {
    id: 2, mealType: '早餐',
    icon: 'mdi:food-apple', iconColor: 'text-blue-500',
    tag: '低卡选择', tagClass: 'bg-blue-100 text-blue-600',
    title: '清爽粗粮早餐',
    desc: '燕麦粥/玉米/紫薯 + 凉拌海带丝/凉拌青菜 + 蛋白2个。',
    calories: 280, protein: 15
  },
  {
    id: 3, mealType: '午餐',
    icon: 'mdi:food-drumstick', iconColor: 'text-orange-500',
    tag: '高蛋白', tagClass: 'bg-orange-100 text-orange-600',
    title: '能量满满午餐',
    desc: '杂粮饭 + 清蒸鱼/鸡胸肉 + 清炒时蔬 + 一份汤。',
    calories: 550, protein: 35
  },
  {
    id: 4, mealType: '午餐',
    icon: 'mdi:food-variant', iconColor: 'text-red-400',
    tag: '均衡选择', tagClass: 'bg-emerald-100 text-emerald-600',
    title: '校园经典搭配',
    desc: '二两米饭 + 番茄炒蛋 + 蒜蓉西兰花 + 紫菜蛋花汤。',
    calories: 480, protein: 22
  },
  {
    id: 5, mealType: '晚餐',
    icon: 'mdi:food-drumstick', iconColor: 'text-indigo-500',
    tag: '轻食', tagClass: 'bg-purple-100 text-purple-600',
    title: '清淡养生晚餐',
    desc: '小米粥/杂粮粥 + 蒸蛋羹 + 凉拌黄瓜 + 少量水果。',
    calories: 320, protein: 18
  },
  {
    id: 6, mealType: '晚餐',
    icon: 'mdi:food-apple', iconColor: 'text-green-500',
    tag: '低卡选择', tagClass: 'bg-blue-100 text-blue-600',
    title: '素食轻盈晚',
    desc: '全麦面包 + 蔬菜沙拉 + 一杯酸奶 + 一小把坚果。',
    calories: 260, protein: 12
  }
]

const meals = computed(() => allMeals.filter(m => m.mealType === activeMeal.value))

const calculateBMI = () => {
  if (height.value && weight.value) {
    const h = height.value / 100
    bmiResult.value = (weight.value / (h * h)).toFixed(1)

    if (bmiResult.value < 18.5) {
      bmiStatus.value = '偏瘦，建议增加营养'
    } else if (bmiResult.value < 24) {
      bmiStatus.value = '非常标准'
    } else if (bmiResult.value < 28) {
      bmiStatus.value = '偏重，建议适当运动'
    } else {
      bmiStatus.value = '肥胖，建议咨询医生'
    }
  }
}

const addWater = (amount) => {
  waterAmount.value += amount
}

// 显示Toast提示
const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 2000)
}

// 图表点击事件处理
const handleChartClick = (params) => {
  if (params.componentType === 'series') {
    const dataIndex = params.dataIndex
    const seriesName = params.seriesName

    if (seriesName === '身体素质' || seriesName === '精力水平') {
      editingIndex.value = dataIndex
      editingType.value = seriesName === '身体素质' ? 'physical' : 'energy'
      editingValue.value = params.value.toString()
      editingDate.value = xAxisDates[dataIndex]
      isEditing.value = true
    }
  }
}

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false
  editingValue.value = ''
  editingDate.value = ''
}

// 保存编辑
const saveEdit = async () => {
  const value = parseInt(editingValue.value)

  // 验证输入
  if (isNaN(value)) {
    showToastMessage('请输入有效数字')
    return
  }

  // 验证范围（精神状态数据值必须在0-100之间）
  if (value < 0 || value > 100) {
    showToastMessage('数值范围应为 0-100')
    return
  }

  isLoading.value = true

  // 模拟保存延迟
  await new Promise(resolve => setTimeout(resolve, 500))

  // 更新数据
  if (editingType.value === 'physical') {
    physicalData.value[editingIndex.value] = value
  } else {
    energyData.value[editingIndex.value] = value
  }

  // 重新渲染图表
  updateChart()

  isLoading.value = false
  isEditing.value = false
  editingValue.value = ''
  editingDate.value = ''
  showToastMessage('数据保存成功')
}

// 更新图表数据
const updateChart = () => {
  if (!chart) return
  chart.setOption({
    xAxis: [{ data: xAxisDates }],
    series: [
      { data: physicalData.value },
      { data: energyData.value }
    ]
  })
}

const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  // 添加点击事件监听
  chart.on('click', handleChartClick)

  const option = {
    color: ['#10b981', '#fbbf24'],
    tooltip: { trigger: 'axis' },
    legend: { data: ['身体素质', '精力水平'], bottom: 0, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { left: '3%', right: '4%', top: '10%', bottom: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: xAxisDates,
      axisLine: { lineStyle: { color: '#f1f5f9' } },
      axisLabel: { color: '#94a3b8' }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: { formatter: '{value}%', color: '#94a3b8' },
      splitLine: { lineStyle: { color: '#f1f5f9' } }
    },
    series: [
      {
        name: '身体素质',
        type: 'line',
        smooth: true,
        data: physicalData.value,
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(16, 185, 129, 0.2)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0)' }
          ])
        },
        symbol: 'circle',
        symbolSize: 8,
        emphasis: {
          focus: 'series',
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(16, 185, 129, 0.5)' },
          scale: true,
          scaleSize: 12
        },
        cursor: 'pointer'
      },
      {
        name: '精力水平',
        type: 'line',
        smooth: true,
        data: energyData.value,
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(251, 191, 36, 0.2)' },
            { offset: 1, color: 'rgba(251, 191, 36, 0)' }
          ])
        },
        symbol: 'circle',
        symbolSize: 8,
        emphasis: {
          focus: 'series',
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(251, 191, 36, 0.5)' },
          scale: true,
          scaleSize: 12
        },
        cursor: 'pointer'
      }
    ]
  }
  chart.setOption(option)
}

const handleResize = () => {
  chart && chart.resize()
}

onMounted(() => {
  setTimeout(() => {
    initChart()
    window.addEventListener('resize', handleResize)
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart && chart.dispose()
})
</script>
