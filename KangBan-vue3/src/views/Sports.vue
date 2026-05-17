<template>
  <div class="text-slate-800" style="background-color: #fffaf5;">
    <Navbar theme="orange" logo-icon="solar:running-bold" right-content="steps" right-text="今日已运动 8,421 步"
      :show-login="false" :show-notification="false" />

    <main class="max-w-[1440px] mx-auto px-6 py-10">
      <!-- 运动概览卡片 -->
      <div
        class="bg-gradient-to-r from-orange-400 to-rose-500 rounded-[2.5rem] p-8 text-white mb-12 shadow-xl shadow-orange-100 flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex-1">
          <h2 class="text-3xl font-bold mb-4">开启今日训练计划</h2>
          <p class="text-orange-50 mb-8 opacity-90 max-w-md leading-relaxed">基于你的目标：<span
              class="font-bold underline">体质增强</span>。今天建议进行 20 分钟的中等强度有氧运动。</p>
          <div class="flex gap-4">
            <button
              class="px-6 py-3 bg-white text-orange-600 rounded-2xl font-bold shadow-lg flex items-center gap-2 hover:bg-orange-50 transition-colors">
              <iconify-icon icon="solar:play-circle-bold"></iconify-icon> 开始今日计划
            </button>
            <button
              class="px-6 py-3 bg-orange-600/20 border border-white/30 text-white rounded-2xl font-bold backdrop-blur-sm hover:bg-white/10 transition-colors">
              修改训练目标
            </button>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 w-full md:w-auto">
          <div v-for="stat in overviewStats" :key="stat.label"
            class="bg-white/10 backdrop-blur-md p-5 rounded-3xl border border-white/20 text-center">
            <div class="text-2xl font-bold">{{ stat.value }}</div>
            <div class="text-[10px] text-orange-100 uppercase tracking-wider">{{ stat.label }}</div>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-12 gap-8">
        <!-- 宿舍健身课库 (Col 8) -->
        <div class="md:col-span-8 space-y-8">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-bold">宿舍场景推荐</h3>
            <div class="flex gap-2">
              <button v-for="tab in courseTabs" :key="tab"
                class="px-3 py-1 bg-white border border-slate-200 rounded-lg text-xs font-bold hover:bg-slate-50 transition-colors">
                {{ tab }}
              </button>
            </div>
          </div>
          <div class="grid md:grid-cols-2 gap-6">
            <div v-for="course in courses" :key="course.id"
              class="course-card bg-white rounded-3xl overflow-hidden border border-slate-100 shadow-sm group cursor-pointer">
              <div class="relative overflow-hidden h-40">
                <img :alt="course.alt" class="w-full h-full object-cover" :src="course.img" />
                <div
                  class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-all flex items-center justify-center">
                  <iconify-icon class="text-white text-5xl opacity-0 group-hover:opacity-100 transition-opacity"
                    icon="solar:play-circle-bold"></iconify-icon>
                </div>
                <span
                  class="absolute top-3 right-3 px-2 py-1 bg-black/50 backdrop-blur-md text-white text-[10px] rounded">{{
                    course.duration }}</span>
              </div>
              <div class="p-5">
                <h4 class="font-bold mb-1">{{ course.title }}</h4>
                <p class="text-[10px] text-slate-400 mb-4">{{ course.desc }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-1 text-[10px] font-bold" :class="course.intensityClass">
                    <iconify-icon icon="solar:fire-bold"></iconify-icon> {{ course.intensity }}
                  </div>
                  <span class="text-[10px] text-slate-400">{{ course.participants }} 人已练</span>
                </div>
              </div>
            </div>
          </div>
          <!-- 校园运动地图 -->
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-xl font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-emerald-500" icon="solar:map-point-bold"></iconify-icon> 校园跑图推荐
            </h3>
            <div class="relative w-full h-64 bg-slate-100 rounded-2xl overflow-hidden">
              <img alt="Campus map for running" class="w-full h-full object-cover opacity-60"
                src="https://modao.cc/agent-py/media/generated_images/2026-03-26/5485824f869c4b20899e73165ca8351f.jpg" />
              <div class="absolute inset-0 p-6 flex flex-col justify-end">
                <div
                  class="bg-white/90 backdrop-blur-md p-4 rounded-xl shadow-lg inline-block self-start border border-emerald-100">
                  <div class="text-xs font-bold text-emerald-600 mb-1">推荐路线：樱花林小径</div>
                  <div class="text-[10px] text-slate-500">全程 2.5km · 坡度平缓 · 适合晨跑</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 右侧：约球与成就 (Col 4) -->
        <div class="md:col-span-4 space-y-8">
          <!-- 运动成就 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-yellow-500" icon="solar:medal-star-bold"></iconify-icon> 我的勋章
            </h3>
            <div class="grid grid-cols-3 gap-4">
              <div v-for="medal in medals" :key="medal.label" class="flex flex-col items-center gap-2">
                <div class="w-12 h-12 rounded-full flex items-center justify-center"
                  :class="medal.achieved ? 'bg-yellow-100 text-yellow-500' : 'bg-slate-100 text-slate-300'">
                  <iconify-icon :icon="medal.icon" width="24"></iconify-icon>
                </div>
                <span class="text-[10px]" :class="medal.achieved ? 'text-slate-500' : 'text-slate-400'">{{ medal.label
                }}</span>
              </div>
            </div>
          </div>
          <!-- 约球广场 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-blue-500" icon="solar:users-group-rounded-bold"></iconify-icon> 约球广场
            </h3>
            <div class="space-y-4">
              <div v-for="match in matches" :key="match.id"
                class="p-3 bg-slate-50 rounded-xl hover:bg-orange-50 transition-colors cursor-pointer group">
                <div class="flex items-center justify-between mb-2">
                  <span class="px-2 py-0.5 text-[10px] font-bold rounded" :class="match.tagClass">{{ match.sport
                  }}</span>
                  <span class="text-[10px] text-slate-400">{{ match.time }} {{ match.location }}</span>
                </div>
                <p class="text-xs font-medium mb-2 group-hover:text-orange-600">{{ match.desc }}</p>
                <div class="flex items-center justify-between text-[10px] text-slate-400">
                  <span>发起人: {{ match.creator }}</span>
                  <span class="text-orange-500 font-bold">加入 +</span>
                </div>
              </div>
            </div>
            <button
              class="w-full mt-6 py-2 border-2 border-dashed border-slate-200 text-slate-400 rounded-xl text-xs font-bold hover:border-orange-300 hover:text-orange-500 transition-all">+
              发布约球信息</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '@/components/Navbar.vue'

const overviewStats = ref([
  { value: '285', label: '今日消耗 (kcal)' },
  { value: '45', label: '本周活跃 (min)' },
  { value: '3', label: '连续打卡 (day)' },
  { value: '1/4', label: '勋章点亮进度' }
])

const courseTabs = ['全部', '拉伸', '力量']

const courses = ref([
  {
    id: 1,
    alt: 'Dorm stretching',
    img: 'https://modao.cc/agent-py/media/generated_images/2026-03-26/959ef2c7ddcb4e7096955de21f15ed3e.jpg',
    duration: '08:15',
    title: '睡前久坐拉伸',
    desc: '适合期末周，缓解颈椎压力',
    intensity: '低强度',
    intensityClass: 'text-orange-500',
    participants: '1.2k'
  },
  {
    id: 2,
    alt: 'Abs workout',
    img: 'https://modao.cc/agent-py/media/generated_images/2026-03-26/613106ece87b4c1c8b21fb471f44d73a.jpg',
    duration: '12:30',
    title: '腹肌轰炸 (入门级)',
    desc: '仅需一张瑜伽垫，无需器械',
    intensity: '中高强度',
    intensityClass: 'text-red-500',
    participants: '856'
  }
])

const medals = ref([
  { label: '清晨跑者', icon: 'solar:sun-bold', achieved: true },
  { label: '10天连胜', icon: 'solar:fire-bold', achieved: false },
  { label: '体测满分', icon: 'solar:crown-bold', achieved: false }
])

const matches = ref([
  {
    id: 1,
    sport: '羽毛球',
    tagClass: 'bg-orange-100 text-orange-600',
    time: '14:00',
    location: '体育馆',
    desc: '三缺一，来个水平中等的校友！',
    creator: '匿名用户A'
  },
  {
    id: 2,
    sport: '篮球',
    tagClass: 'bg-blue-100 text-blue-600',
    time: '18:30',
    location: '西操场',
    desc: '打半场，随便来，出出汗就行。',
    creator: '匿名用户B'
  }
])
</script>
