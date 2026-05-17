<template>
  <div class="text-slate-800">
    <Navbar />

    <!-- Hero 区域 -->
    <header class="relative py-16 overflow-hidden">
      <div
        class="absolute top-0 left-0 w-full h-full -z-10 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-emerald-50 via-white to-blue-50">
      </div>
      <div class="max-w-[1440px] mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <div class="inline-block px-4 py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-sm font-medium mb-6">
            今天是 {{ currentDate }}
          </div>
          <h1 class="text-5xl font-extrabold leading-tight mb-6">
            守护你的大学时光<br />
            让<span class="text-emerald-500">健康</span>成为最酷的学分
          </h1>
          <p class="text-lg text-slate-600 max-w-lg leading-relaxed"> 专为在校大学生打造的轻量化健康助手</p>
          <p class="text-lg text-slate-600 mb-8 max-w-lg leading-relaxed">
            无需繁琐注册，即刻开始健康打卡
          </p>
          <div class="flex gap-4">
            <router-link
              class="px-8 py-4 bg-emerald-500 text-white rounded-2xl font-bold shadow-xl shadow-emerald-200 hover:bg-emerald-400 hover:shadow-md transition-all flex items-center gap-2"
              to="/health">
              立即开启健康打卡 <iconify-icon icon="solar:arrow-right-up-linear"></iconify-icon>
            </router-link>
            <router-link
              class="px-8 py-4 bg-gray-100 text-slate-700 border border-slate-200 rounded-2xl font-bold shadow-xl shadow-gray-200 hover:bg-gray-50 hover:bg-slate-50 transition-all"
              to="/resources">
              查看校园医疗资源
            </router-link>
          </div>
        </div>
        <div class="relative">
          <div class="glass-card p-6 rounded-[2.5rem] shadow-2xl relative z-10">
            <div class="flex items-center justify-between mb-6">
              <h3 class="font-bold text-lg flex items-center gap-2">
                <iconify-icon class="text-emerald-500" icon="solar:chart-square-bold"></iconify-icon> 近期健康指标
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
                      {{ editingType === 'steps' ? '运动步数' : '专注时长(min)' }}
                    </label>
                    <input v-model="editingValue" type="number" min="0"
                      :max="editingType === 'steps' ? '100000' : '1440'"
                      class="w-full bg-white border border-slate-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                      :placeholder="editingType === 'steps' ? '请输入步数（0-100000）' : '请输入时间（0-1440分钟）'" />
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
    </header>

    <!-- 核心板块入口 -->
    <section class="py-20 bg-white">
      <div class="max-w-[1440px] mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold mb-4">专注大学生四大健康维度</h2>
          <p class="text-slate-500">科学、公益、实用，适配你的校园生活节奏</p>
        </div>
        <div class="grid md:grid-cols-4 gap-8">
          <router-link v-for="feature in features" :key="feature.path" :to="feature.path"
            class="feature-card p-8 rounded-3xl group" :class="feature.bgClass">
            <div
              class="w-14 h-14 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-6 group-hover:shadow-md transition-all"
              :class="[feature.iconClass, feature.iconHoverClass]">
              <iconify-icon :icon="feature.icon" width="32"></iconify-icon>
            </div>
            <h3 class="text-xl font-bold mb-3">{{ feature.title }}</h3>
            <p class="text-slate-600 text-sm leading-relaxed mb-6">{{ feature.desc }}</p>
            <span class="font-bold flex items-center gap-1 text-sm" :class="feature.textClass">去{{ feature.action }}
              <iconify-icon icon="solar:arrow-right-linear"></iconify-icon></span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 精选资讯 -->
    <section class="py-20 bg-slate-50">
      <div class="max-w-[1440px] mx-auto px-6">
        <div class="flex items-end justify-between mb-12">
          <div>
            <h2 class="text-3xl font-bold mb-2">校园健康动态</h2>
            <p class="text-slate-500">针对大学生群体的科普与精选内容</p>
          </div>
          <a class="text-emerald-600 font-medium hover:underline" href="#">查看全部资讯</a>
        </div>
        <div v-if="articleError && articles.length === 0" class="text-center py-12 text-slate-400">
          <p class="text-lg">数据加载失败 :(</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
          <router-link v-for="article in articles" :key="article.id" :to="`/article?id=${article.id}`"
            class="bg-white rounded-3xl overflow-hidden border border-slate-100 hover:shadow-xl transition-shadow block">
            <img :alt="article.alt" class="w-full h-48 object-cover" :src="article.img" />
            <div class="p-6">
              <div class="flex items-center gap-4 mb-3">
                <span class="px-2 py-0.5 text-xs font-bold rounded" :class="article.tagClass">{{ article.tag }}</span>
                <span class="text-slate-400 text-xs">{{ article.date }}</span>
              </div>
              <h3 class="text-lg font-bold mb-2 hover:text-emerald-600 transition-colors">{{
                article.title }}</h3>
              <p class="text-slate-500 text-sm mb-4">{{ article.excerpt }}</p>
              <div class="flex items-center justify-between pt-4 border-t border-slate-50">
                <span class="text-xs text-slate-400">阅读 {{ article.views }}</span>
                <span class="text-emerald-500 text-sm font-bold flex items-center gap-1">阅读全文 <iconify-icon
                    icon="solar:arrow-right-linear"></iconify-icon></span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 快捷数据统计区 -->
    <!-- <section class="py-16 bg-emerald-600 text-white">
      <div class="max-w-[1440px] mx-auto px-6 grid md:grid-cols-4 gap-8 text-center">
        <div v-for="stat in stats" :key="stat.label">
          <div class="text-4xl font-bold mb-2">{{ stat.value }}</div>
          <div class="text-emerald-100 text-sm">{{ stat.label }}</div>
        </div>
      </div>
    </section> -->

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { getFeaturedAPI, getArticlesAPI } from '@/api/articles'

const chartRef = ref(null)
let chart = null

const currentDate = ref('')

// 编辑相关状态
const isEditing = ref(false)
const editingIndex = ref(0)
const editingType = ref('steps') // 'steps' 表示运动步数, 'time' 表示专注时长
const editingValue = ref('')
const editingDate = ref('')
const isLoading = ref(false)
const showToast = ref(false)
const toastMessage = ref('')

// 图表数据 - 使用响应式数据便于更新
const stepsData = ref([5000, 7200, 4800, 8100, 6500, 9200, 4300])
const timeData = ref([120, 240, 180, 200, 310, 280, 150])

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

const xAxisDates = computed(() => generateLast7Days())

// 显示Toast提示
const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 2000)
}

const features = ref([
  {
    path: '/health',
    bgClass: 'bg-emerald-50',
    icon: 'solar:heart-pulse-bold',
    iconClass: 'text-emerald-500',
    iconHoverClass: 'group-hover:bg-emerald-500 group-hover:text-white',
    title: '日常健康',
    desc: '饮食追踪、睡眠管理、饮水提醒。拒绝期末周熬夜综合症。',
    action: '记录',
    textClass: 'text-emerald-600'
  },
  {
    path: '/mental',
    bgClass: 'bg-blue-50',
    icon: 'solar:ghost-bold',
    iconClass: 'text-blue-500',
    iconHoverClass: 'group-hover:bg-blue-500 group-hover:text-white',
    title: '身心调适',
    desc: '冥想白噪音。给在绩点和实习压力下的你一个出口。',
    action: '放松',
    textClass: 'text-blue-600'
  },
  {
    path: '/sports',
    bgClass: 'bg-orange-50',
    icon: 'solar:running-bold',
    iconClass: 'text-orange-500',
    iconHoverClass: 'group-hover:bg-orange-500 group-hover:text-white',
    title: '运动规划',
    desc: '宿舍5分钟健身、操场路线推荐。让体测不再是噩梦。',
    action: '运动',
    textClass: 'text-orange-600'
  },
  {
    path: '/resources',
    bgClass: 'bg-purple-50',
    icon: 'solar:medical-kit-bold',
    iconClass: 'text-purple-500',
    iconHoverClass: 'group-hover:bg-purple-500 group-hover:text-white',
    title: '资源查询',
    desc: '急救指南、校医室排班、周边药店。突发状况不再手忙脚乱。',
    action: '查询',
    textClass: 'text-purple-600'
  }
])

const articles = ref([])
const articleError = ref(false)

const stats = ref([
  { value: '12,450', label: '今日校园总步数 (km)' },
  { value: '3,280', label: '已完成心情打卡人数' },
  { value: '560', label: '在线提供咨询的心理导师' },
  { value: '98%', label: '服务好评率 (匿名反馈)' }
])

// 图表点击事件处理
const handleChartClick = (params) => {
  if (params.componentType === 'series') {
    const dataIndex = params.dataIndex
    const seriesName = params.seriesName

    if (seriesName === '运动步数' || seriesName === '专注时长(min)') {
      editingIndex.value = dataIndex
      editingType.value = seriesName === '运动步数' ? 'steps' : 'time'
      editingValue.value = params.value.toString()
      editingDate.value = xAxisDates.value[dataIndex]
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

  // 验证范围
  if (editingType.value === 'steps') {
    if (value < 0 || value > 100000) {
      showToastMessage('步数范围应为 0-100000')
      return
    }
  } else {
    if (value < 0 || value > 1440) {
      showToastMessage('时间范围应为 0-1440 分钟')
      return
    }
  }

  isLoading.value = true

  // 模拟保存延迟
  await new Promise(resolve => setTimeout(resolve, 500))

  // 更新数据
  if (editingType.value === 'steps') {
    stepsData.value[editingIndex.value] = value
  } else {
    timeData.value[editingIndex.value] = value
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
    xAxis: [{ data: xAxisDates.value }],
    series: [
      { data: stepsData.value },
      { data: timeData.value }
    ]
  })
}

const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  // 添加点击事件监听
  chart.on('click', handleChartClick)

  const option = {
    color: ['#10b981', '#3b82f6'],
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['运动步数', '专注时长(min)'],
      bottom: 0,
      textStyle: { color: '#94a3b8', fontSize: 10 }
    },
    grid: { left: '3%', right: '4%', top: '10%', bottom: '15%', containLabel: true },
    xAxis: [
      {
        type: 'category',
        data: xAxisDates.value,
        axisLine: { lineStyle: { color: '#f1f5f9' } },
        axisLabel: { color: '#94a3b8' }
      }
    ],
    yAxis: [
      {
        type: 'value',
        splitLine: { lineStyle: { color: '#f1f5f9', type: 'dashed' } },
        axisLabel: { color: '#94a3b8' }
      }
    ],
    series: [
      {
        name: '运动步数',
        type: 'bar',
        barWidth: '30%',
        barGap: '10%',
        data: stepsData.value,
        itemStyle: { borderRadius: [4, 4, 0, 0] },
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(16, 185, 129, 0.5)' }
        },
        cursor: 'pointer'
      },
      {
        name: '专注时长(min)',
        type: 'line',
        smooth: true,
        data: timeData.value,
        symbol: 'circle',
        symbolSize: 8,
        emphasis: {
          focus: 'series',
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(59, 130, 246, 0.5)' },
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

onMounted(async () => {
  const now = new Date()
  currentDate.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 · 周${['日', '一', '二', '三', '四', '五', '六'][now.getDay()]}`

  // 从后端获取文章数据
  try {
    const [featuredRes, listRes] = await Promise.all([
      getFeaturedAPI(3),
      getArticlesAPI({ page: 1, limit: 10 })
    ])
    const featured = featuredRes.data.items || []
    const list = listRes.data.items || []
    // 合并并去重
    const seen = new Set()
    articles.value = [...featured]
    featured.forEach(a => seen.add(a.id))
    list.forEach(a => {
      if (!seen.has(a.id)) articles.value.push(a)
    })
  } catch {
    articleError.value = true
  }

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
