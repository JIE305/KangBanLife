<template>
  <div class="text-slate-800" style="background-color: #f5f3ff;">
    <Navbar theme="purple" logo-icon="solar:medical-kit-bold" right-content="status" right-text="信息真实可靠"
      right-icon="solar:shield-check-bold" :show-login="false" :show-notification="false" />

    <main class="max-w-[1440px] mx-auto px-6 py-10">
      <!-- 搜索区 -->
      <section class="mb-12">
        <div class="bg-white p-10 rounded-[2.5rem] shadow-xl shadow-purple-100 text-center relative overflow-hidden">
          <div class="relative z-10">
            <h2 class="text-3xl font-bold mb-6">遇到了健康小麻烦？</h2>
            <div class="max-w-2xl mx-auto relative">
              <input v-model="searchQuery"
                class="w-full bg-slate-50 border-none rounded-2xl px-12 py-4 shadow-inner text-sm focus:outline-none"
                placeholder="输入关键词，如：感冒怎么办、校医室电话、心肺复苏..." type="text" />
              <iconify-icon class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" icon="solar:magnifer-linear"
                width="24"></iconify-icon>
              <button
                class="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-purple-500 text-white rounded-xl text-sm font-bold">搜索</button>
            </div>
          </div>
          <!-- 背景装饰 -->
          <iconify-icon class="absolute -top-10 -left-10 text-purple-50 opacity-10" icon="solar:pills-minimalistic-bold"
            width="200"></iconify-icon>
          <iconify-icon class="absolute -bottom-10 -right-10 text-purple-50 opacity-10" icon="solar:stethoscope-bold"
            width="200"></iconify-icon>
        </div>
      </section>

      <div class="grid md:grid-cols-12 gap-8">
        <!-- 左侧核心资源 (Col 8) -->
        <div class="md:col-span-8 space-y-8">
          <!-- 紧急急救手册 -->
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-xl font-bold mb-8 flex items-center gap-2">
              <iconify-icon class="text-red-500" icon="solar:danger-triangle-bold"></iconify-icon> 急救知识宝典
            </h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
              <div v-for="resource in firstAidResources" :key="resource.title"
                class="resource-card p-4 rounded-2xl border cursor-pointer group text-center"
                :class="[resource.bgClass, resource.borderClass]" @click="handleFirstAidClick(resource)">
                <div
                  class="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-3 shadow-sm group-hover: transition-all"
                  :class="[resource.iconClass, resource.iconHoverClass]">
                  <iconify-icon :icon="resource.icon" width="24"></iconify-icon>
                </div>
                <h4 class="text-sm font-bold" :class="resource.titleClass">{{ resource.title }}</h4>
                <p class="text-[10px] mt-1" :class="resource.descClass">{{ resource.desc }}</p>
              </div>
            </div>
          </div>
          <!-- 常用药指南 -->
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-xl font-bold mb-6">大学生宿舍常备药清单</h3>
            <div class="space-y-4">
              <div v-for="med in medicines" :key="med.title"
                class="flex items-start gap-4 p-4 hover:bg-slate-50 rounded-2xl transition-all cursor-pointer"
                :class="med.borderClass" @click="handleMedicineClick(med)">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center shrink-0" :class="med.iconBg">
                  <iconify-icon :icon="med.icon" width="24" :class="med.iconColor"></iconify-icon>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-center mb-1">
                    <h4 class="font-bold">{{ med.title }}</h4>
                    <span class="text-[10px] font-bold" :class="med.tagClass">建议备选</span>
                  </div>
                  <p class="text-xs text-slate-500">{{ med.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 右侧：校医室与地图 (Col 4) -->
        <div class="md:col-span-4 space-y-8">
          <!-- 校医室信息 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2 text-purple-600">
              <iconify-icon icon="solar:hospital-bold"></iconify-icon> 校医室概况
            </h3>
            <div class="space-y-4 mb-6">
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">今日值班</span>
                <span class="font-bold text-emerald-500">门诊开放中</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">在诊时间</span>
                <span class="font-medium">08:00 - 21:00</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">咨询热线</span>
                <span class="font-bold">0371-23928120</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">所在位置</span>
                <span class="font-medium">行政楼东侧1楼</span>
              </div>
            </div>
            <div class="p-4 bg-purple-50 rounded-2xl">
              <div class="text-[10px] text-purple-400 font-bold uppercase mb-2">特别通知</div>
              <p class="text-xs text-purple-900 leading-relaxed">近期为春季流感高发期，校医室已备好流感疫苗，有需要的同学请在后台预约。</p>
            </div>
          </div>
          <!-- 周边医院地图 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-blue-500" icon="solar:globus-bold"></iconify-icon> 周边医疗
            </h3>
            <div class="space-y-4">
              <div v-for="facility in medicalFacilities" :key="facility.name" class="p-3 bg-slate-50 rounded-xl">
                <h4 class="text-sm font-bold mb-1">{{ facility.name }}</h4>
                <p class="text-[10px] text-slate-500 mb-2">{{ facility.distance }} · {{ facility.walkTime }}</p>
                <span class="text-[10px] bg-white px-2 py-0.5 rounded" :class="facility.tagClass">{{ facility.tag
                }}</span>
              </div>
            </div>
            <router-link to="/map"
              class="w-full mt-6 py-3 bg-slate-800 text-white rounded-xl text-xs font-bold hover:bg-slate-700 transition-colors flex items-center justify-center gap-2">
              <iconify-icon icon="solar:navigation-bold" width="16"></iconify-icon>
              查看详细地图导航
            </router-link>
          </div>
        </div>
      </div>

      <!-- Toast消息提示 -->
      <Transition name="toast">
        <div v-if="showToast"
          class="fixed bottom-24 left-1/2 -translate-x-1/2 text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-2 z-50"
          :class="[toastBgClass, toastShadowClass]">
          <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
        </div>
      </Transition>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '@/components/Navbar.vue'

const searchQuery = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const toastBgClass = ref('bg-emerald-500')
const toastShadowClass = ref('shadow-emerald-200')

const showToastMessage = (message, bgClass = 'bg-emerald-500', shadowClass = 'shadow-emerald-200') => {
  toastMessage.value = message
  toastBgClass.value = bgClass
  toastShadowClass.value = shadowClass
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2000)
}

const getColorFromBgClass = (bgClass) => {
  const colorMap = {
    'bg-red-50': { bg: 'bg-red-500', shadow: 'shadow-red-200' },
    'bg-orange-50': { bg: 'bg-orange-500', shadow: 'shadow-orange-200' },
    'bg-blue-50': { bg: 'bg-blue-500', shadow: 'shadow-blue-200' },
    'bg-yellow-50': { bg: 'bg-yellow-500', shadow: 'shadow-yellow-200' },
    'bg-purple-50': { bg: 'bg-purple-500', shadow: 'shadow-purple-200' },
    'bg-slate-50': { bg: 'bg-slate-500', shadow: 'shadow-slate-200' },
    'bg-blue-100': { bg: 'bg-blue-500', shadow: 'shadow-blue-200' },
    'bg-emerald-100': { bg: 'bg-emerald-500', shadow: 'shadow-emerald-200' },
    'bg-orange-100': { bg: 'bg-orange-500', shadow: 'shadow-orange-200' }
  }
  return colorMap[bgClass] || { bg: 'bg-emerald-500', shadow: 'shadow-emerald-200' }
}

const handleFirstAidClick = (resource) => {
  const messages = {
    'CPR 心肺复苏': 'CPR心肺复苏操作要点：检查意识→呼救→检查呼吸→胸外按压→人工呼吸',
    '海姆立克法': '海姆立克急救法：站在患者身后，双手环抱腹部，用力向上冲击',
    '烫伤处理': '烫伤处理五字诀：冲、脱、泡、盖、送',
    '中暑自救': '中暑急救：迅速转移至阴凉通风处，补充淡盐水',
    '外伤止血': '外伤止血：直接压迫止血法，抬高患肢，必要时使用止血带',
    '更多急救': '正在加载更多急救知识...'
  }
  const colorInfo = getColorFromBgClass(resource.bgClass)
  showToastMessage(messages[resource.title] || '暂无详细信息', colorInfo.bg, colorInfo.shadow)
}

const handleMedicineClick = (med) => {
  const colorInfo = getColorFromBgClass(med.iconBg)
  showToastMessage(`已为您推荐「${med.title}」相关药品，请在医生指导下使用`, colorInfo.bg, colorInfo.shadow)
}

const firstAidResources = ref([
  {
    title: 'CPR 心肺复苏',
    desc: '关键时刻挽救生命',
    icon: 'mdi:heart-pulse',
    bgClass: 'bg-red-50',
    borderClass: 'border-red-100',
    iconClass: 'text-red-500',
    iconHoverClass: 'group-hover:bg-red-500 group-hover:text-white',
    titleClass: 'text-red-900',
    descClass: 'text-red-400'
  },
  {
    title: '海姆立克法',
    desc: '异物卡喉急救',
    icon: 'mdi:hospital',
    bgClass: 'bg-orange-50',
    borderClass: 'border-orange-100',
    iconClass: 'text-orange-500',
    iconHoverClass: 'group-hover:bg-orange-500 group-hover:text-white',
    titleClass: 'text-orange-900',
    descClass: 'text-orange-400'
  },
  {
    title: '烫伤处理',
    desc: '冲、脱、泡、盖、送',
    icon: 'mdi:fire-alert',
    bgClass: 'bg-blue-50',
    borderClass: 'border-blue-100',
    iconClass: 'text-blue-500',
    iconHoverClass: 'group-hover:bg-blue-500 group-hover:text-white',
    titleClass: 'text-blue-900',
    descClass: 'text-blue-400'
  },
  {
    title: '中暑自救',
    desc: '迅速降温与补水',
    icon: 'mdi:weather-sunny',
    bgClass: 'bg-yellow-50',
    borderClass: 'border-yellow-100',
    iconClass: 'text-yellow-500',
    iconHoverClass: 'group-hover:bg-yellow-500 group-hover:text-white',
    titleClass: 'text-yellow-900',
    descClass: 'text-yellow-400'
  },
  {
    title: '外伤止血',
    desc: '简易包扎与清理',
    icon: 'mdi:bandage',
    bgClass: 'bg-purple-50',
    borderClass: 'border-purple-100',
    iconClass: 'text-purple-500',
    iconHoverClass: 'group-hover:bg-purple-500 group-hover:text-white',
    titleClass: 'text-purple-900',
    descClass: 'text-purple-400'
  },
  {
    title: '更多急救',
    desc: '查看完整库',
    icon: 'mdi:dots-horizontal',
    bgClass: 'bg-slate-50',
    borderClass: 'border-slate-100',
    iconClass: 'text-slate-500',
    iconHoverClass: 'group-hover:bg-slate-500 group-hover:text-white',
    titleClass: 'text-slate-900',
    descClass: 'text-slate-400'
  }
])

const medicines = ref([
  {
    title: '感冒发烧类',
    desc: '对乙酰氨基酚（布洛芬）、复方氨酚烷胺片。若持续高烧请务必就医。',
    icon: 'mdi:thermometer',
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600',
    tagClass: 'text-blue-500',
    borderClass: ''
  },
  {
    title: '肠胃消化类',
    desc: '蒙脱石散、蒙脱石散、达喜。食堂吃坏肚子时的急救包。',
    icon: 'mdi:stomach',
    iconBg: 'bg-emerald-100',
    iconColor: 'text-emerald-600',
    tagClass: 'text-emerald-500',
    borderClass: 'border-t border-slate-50'
  },
  {
    title: '过敏与外用类',
    desc: '氯雷他定、碘伏棉签、创可贴、扶他林膏药。运动损伤与过敏季必备。',
    icon: 'mdi:allergy',
    iconBg: 'bg-orange-100',
    iconColor: 'text-orange-600',
    tagClass: 'text-orange-500',
    borderClass: 'border-t border-slate-50'
  }
])

const medicalFacilities = ref([
  {
    name: '市第一中心医院 (三甲)',
    distance: '距离学校 1.2km',
    walkTime: '步行15分钟',
    tag: '急诊 24h',
    tagClass: 'text-blue-500 border border-blue-100',
    position: { x: 70, y: 55 }
  },
  {
    name: '仁康大药房 (校门口店)',
    distance: '距离学校 200m',
    walkTime: '步行3分钟',
    tag: '支持医保',
    tagClass: 'text-emerald-500 border border-emerald-100',
    position: { x: 35, y: 30 }
  },
  {
    name: '康泰诊所',
    distance: '距离学校 800m',
    walkTime: '步行10分钟',
    tag: '全科门诊',
    tagClass: 'text-purple-500 border border-purple-100',
    position: { x: 55, y: 75 }
  }
])
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}
</style>
