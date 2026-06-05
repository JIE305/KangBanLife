<template>
  <div class="text-slate-800" style="background-color: #fffaf5;">
    <Navbar theme="orange" logo-icon="solar:running-bold" right-content="steps" right-text="今日已运动 8,421 步"
      :show-login="false" :show-notification="false" />

    <main class="max-w-[1440px] mx-auto px-6 py-10">
      <!-- 骨架屏加载 -->
      <template v-if="isLoading">
        <div class="animate-fade-in">
          <div class="bg-gradient-to-r from-orange-400 to-rose-500 rounded-[2.5rem] p-8 mb-12 animate-pulse">
            <div class="flex flex-col md:flex-row justify-between items-center gap-8">
              <div class="flex-1 space-y-4">
                <div class="h-8 bg-white/20 rounded-lg w-2/3"></div>
                <div class="h-4 bg-white/20 rounded w-3/4"></div>
                <div class="h-4 bg-white/20 rounded w-1/2"></div>
                <div class="flex gap-4 mt-8">
                  <div class="h-12 bg-white/30 rounded-2xl w-36"></div>
                  <div class="h-12 bg-white/10 rounded-2xl w-36"></div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 w-full md:w-auto">
                <div v-for="i in 4" :key="i" class="w-24 h-24 bg-white/10 rounded-3xl"></div>
              </div>
            </div>
          </div>
          <div class="grid md:grid-cols-12 gap-8">
            <div class="md:col-span-8 space-y-8">
              <div class="h-6 bg-slate-200 rounded w-36 animate-pulse"></div>
              <div class="grid md:grid-cols-2 gap-6">
                <div v-for="i in 2" :key="i" class="bg-white rounded-3xl h-72 animate-pulse"></div>
              </div>
              <div class="bg-white rounded-3xl h-96 animate-pulse"></div>
            </div>
            <div class="md:col-span-4 space-y-8">
              <div class="bg-white rounded-3xl h-44 animate-pulse"></div>
              <div class="bg-white rounded-3xl h-80 animate-pulse"></div>
            </div>
          </div>
        </div>
      </template>

      <template v-else>
        <!-- 运动概览卡片 -->
        <div class="animate-fade-in-up relative overflow-hidden" style="animation-delay: 0ms">
          <div
            class="bg-gradient-to-r from-orange-400 to-rose-500 rounded-[2.5rem] p-8 text-white mb-12 shadow-xl shadow-orange-100 hover:shadow-2xl hover:shadow-orange-200 transition-shadow duration-500 flex flex-col md:flex-row justify-between items-center gap-8">
            <div class="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-2xl animate-blob"></div>
            <div class="absolute -bottom-8 -left-8 w-32 h-32 bg-white/10 rounded-full blur-2xl animate-blob"
              style="animation-delay: 2s"></div>
            <div class="flex-1 relative z-10">
              <h2 class="text-3xl font-bold mb-4">开启今日训练计划</h2>
              <p class="text-orange-50 mb-8 opacity-90 max-w-md leading-relaxed">{{ goalDescription }}</p>
              <div class="flex gap-4">
                <button @click="startPlan"
                  class="px-6 py-3 bg-white text-orange-600 rounded-2xl font-bold shadow-lg flex items-center gap-2 hover:bg-orange-50 hover:scale-105 active:scale-95 transition-all duration-300">
                  <iconify-icon icon="solar:play-circle-bold"></iconify-icon> 开始今日计划
                </button>
                <button @click="openGoalModal"
                  class="px-6 py-3 bg-orange-600/20 border border-white/30 text-white rounded-2xl font-bold backdrop-blur-sm hover:bg-white/10 hover:scale-105 active:scale-95 transition-all duration-300">
                  修改训练目标
                </button>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 w-full md:w-auto relative z-10">
              <div v-for="(stat, idx) in overviewStats" :key="stat.label"
                class="bg-white/10 backdrop-blur-md p-5 rounded-3xl border border-white/20 text-center hover:bg-white/20 hover:scale-105 transition-all duration-300 cursor-default"
                :style="{ animationDelay: (200 + idx * 100) + 'ms' }">
                <div class="text-2xl font-bold">{{ stat.displayValue }}</div>
                <div class="text-[10px] text-orange-100 uppercase tracking-wider">{{ stat.label }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="grid md:grid-cols-12 gap-8">
          <!-- 宿舍健身课库 (Col 8) -->
          <div class="md:col-span-8 space-y-8">
            <div class="flex items-center justify-between animate-fade-in-up" style="animation-delay: 150ms">
              <h3 class="text-xl font-bold">宿舍场景推荐</h3>
              <div class="flex gap-2">
                <button v-for="tab in courseTabs" :key="tab" @click="activeCourseTab = tab"
                  class="px-3 py-1 rounded-lg text-xs font-bold transition-all duration-300"
                  :class="activeCourseTab === tab ? 'bg-orange-500 text-white shadow-md shadow-orange-200' : 'bg-white border border-slate-200 hover:bg-slate-50 hover:shadow-sm'">
                  {{ tab }}
                </button>
              </div>
            </div>
            <TransitionGroup name="scale" tag="div" class="grid md:grid-cols-2 gap-6">
              <div v-for="(course, idx) in filteredCourses" :key="course.id"
                class="bg-white rounded-3xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-[400ms] group cursor-pointer"
                :style="{ animationDelay: (250 + idx * 100) + 'ms' }" style="animation: fadeInUp 0.5s ease-out both">
                <div class="relative overflow-hidden h-40">
                  <img :alt="course.alt"
                    class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    :src="course.img" />
                  <div
                    class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-all duration-[400ms] flex items-center justify-center">
                    <iconify-icon
                      class="text-white text-5xl opacity-0 group-hover:opacity-100 group-hover:scale-125 transition-all duration-[400ms]"
                      icon="solar:play-circle-bold"></iconify-icon>
                  </div>
                  <span
                    class="absolute top-3 right-3 px-2 py-1 bg-black/50 backdrop-blur-md text-white text-[10px] rounded">{{
                      course.duration }}</span>
                </div>
                <div class="p-5">
                  <h4 class="font-bold mb-1 group-hover:text-orange-600 transition-colors duration-300">{{ course.title
                  }}</h4>
                  <p class="text-[10px] text-slate-400 mb-4">{{ course.desc }}</p>
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-1 text-[10px] font-bold" :class="course.intensityClass">
                      <iconify-icon icon="solar:fire-bold"></iconify-icon> {{ course.intensity }}
                    </div>
                    <span class="text-[10px] text-slate-400">{{ course.participants }} 人已练</span>
                  </div>
                </div>
              </div>
            </TransitionGroup>
            <!-- 操场跑道运动模拟 -->
            <div
              class="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-[400ms] animate-fade-in-up"
              style="animation-delay: 350ms">
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-xl font-bold flex items-center gap-2">
                  <iconify-icon class="text-orange-500" icon="solar:running-round-bold"></iconify-icon> 云端操场
                </h3>
                <div class="flex bg-slate-100 p-1 rounded-lg">
                  <button v-for="mode in trackModes" :key="mode.id"
                    class="px-3 py-1 text-xs font-bold rounded-md transition-all duration-300"
                    :class="activeTrackMode === mode.id ? mode.activeClass : 'text-slate-500 hover:text-slate-700'"
                    @click="switchTrackMode(mode.id)">
                    {{ mode.label }}
                  </button>
                </div>
              </div>
              <div class="flex flex-col lg:flex-row gap-6">
                <!-- SVG 跑道 -->
                <div
                  class="flex-1 flex items-center justify-center bg-slate-50 rounded-2xl p-4 relative overflow-hidden min-h-[280px]"
                  :class="trackBgClass">
                  <svg viewBox="0 0 400 240" class="w-full max-w-[400px]" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                      <radialGradient :id="'trackGrad'" cx="40%" cy="30%">
                        <stop offset="0%" :stop-color="trackGradientStart" />
                        <stop offset="100%" :stop-color="trackGradientEnd" />
                      </radialGradient>
                    </defs>
                    <ellipse cx="200" cy="120" rx="180" ry="100" fill="none" stroke="#e2e8f0" stroke-width="2"
                      stroke-dasharray="6 4" />
                    <ellipse cx="200" cy="120" rx="155" ry="85" fill="none" :stroke="trackColor" stroke-width="3"
                      opacity="0.6" />
                    <ellipse cx="200" cy="120" rx="130" ry="70" fill="none" :stroke="trackColor" stroke-width="3"
                      opacity="0.4" />
                    <ellipse cx="200" cy="120" rx="105" ry="55" fill="none" :stroke="trackColor" stroke-width="3"
                      opacity="0.25" />
                    <circle :cx="runnerX" :cy="runnerY" r="7" :fill="trackColor" class="drop-shadow-lg">
                      <animate attributeName="r" values="7;9;7" dur="0.8s" repeatCount="indefinite" />
                    </circle>
                    <circle :cx="runnerX" :cy="runnerY" r="14" fill="none" :stroke="trackColor" stroke-width="1.5"
                      opacity="0.3">
                      <animate attributeName="r" values="14;22;14" dur="0.8s" repeatCount="indefinite" />
                      <animate attributeName="opacity" values="0.3;0;0.3" dur="0.8s" repeatCount="indefinite" />
                    </circle>
                    <circle :cx="runnerX" :cy="runnerY" r="4" fill="white" />
                  </svg>
                  <Transition name="fade" mode="out-in">
                    <div v-if="!isTrackRunning && trackDistance === 0" :key="'idle'"
                      class="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <span class="text-slate-400 text-sm font-medium">按下「开始」启动运动</span>
                    </div>
                  </Transition>
                </div>
                <!-- 实时数据面板 -->
                <div class="w-full lg:w-56 flex flex-col gap-4">
                  <div class="grid grid-cols-2 gap-3">
                    <div class="bg-slate-50 rounded-xl p-3 text-center">
                      <div class="text-2xl font-bold tabular-nums"
                        :class="isTrackRunning ? 'text-orange-500' : 'text-slate-600'">
                        {{ formatTime(trackElapsed) }}
                      </div>
                      <div class="text-[10px] text-slate-400 mt-1">用时</div>
                    </div>
                    <div class="bg-slate-50 rounded-xl p-3 text-center">
                      <div class="text-2xl font-bold tabular-nums"
                        :class="isTrackRunning ? 'text-orange-500' : 'text-slate-600'">
                        {{ trackDistance.toFixed(1) }}
                      </div>
                      <div class="text-[10px] text-slate-400 mt-1">距离 (km)</div>
                    </div>
                    <div class="bg-slate-50 rounded-xl p-3 text-center">
                      <div class="text-2xl font-bold tabular-nums"
                        :class="isTrackRunning ? 'text-orange-500' : 'text-slate-600'">
                        {{ trackPace }}
                      </div>
                      <div class="text-[10px] text-slate-400 mt-1">配速 (/km)</div>
                    </div>
                    <div class="bg-slate-50 rounded-xl p-3 text-center">
                      <div class="text-2xl font-bold tabular-nums"
                        :class="isTrackRunning ? 'text-orange-500' : 'text-slate-600'">
                        {{ trackCalories }}
                      </div>
                      <div class="text-[10px] text-slate-400 mt-1">消耗 (kcal)</div>
                    </div>
                  </div>
                  <div class="flex gap-2">
                    <button v-if="!isTrackRunning && trackElapsed === 0" @click="startTrack"
                      class="flex-1 py-2.5 bg-orange-500 text-white rounded-xl text-sm font-bold hover:bg-orange-600 active:scale-95 transition-all duration-300 shadow-md shadow-orange-200 flex items-center justify-center gap-1.5">
                      <iconify-icon icon="solar:play-bold" width="16"></iconify-icon> 开始
                    </button>
                    <button v-if="!isTrackRunning && trackElapsed > 0" @click="startTrack"
                      class="flex-1 py-2.5 bg-orange-500 text-white rounded-xl text-sm font-bold hover:bg-orange-600 active:scale-95 transition-all duration-300 shadow-md shadow-orange-200 flex items-center justify-center gap-1.5">
                      <iconify-icon icon="solar:play-bold" width="16"></iconify-icon> 继续
                    </button>
                    <button v-if="isTrackRunning" @click="pauseTrack"
                      class="flex-1 py-2.5 bg-amber-500 text-white rounded-xl text-sm font-bold hover:bg-amber-600 active:scale-95 transition-all duration-300 shadow-md shadow-amber-200 flex items-center justify-center gap-1.5">
                      <iconify-icon icon="solar:pause-bold" width="16"></iconify-icon> 暂停
                    </button>
                    <button v-if="trackElapsed > 0" @click="resetTrack"
                      class="py-2.5 px-3 bg-slate-100 text-slate-500 rounded-xl text-sm font-bold hover:bg-slate-200 hover:text-slate-700 active:scale-95 transition-all duration-300 flex items-center justify-center gap-1">
                      <iconify-icon icon="solar:refresh-bold" width="16"></iconify-icon> 重置
                    </button>
                  </div>
                  <div class="bg-slate-50 rounded-xl p-3">
                    <div class="flex items-center justify-between mb-1.5">
                      <span class="text-[10px] text-slate-400">今日进度</span>
                      <span class="text-[10px] font-bold"
                        :class="trackProgressPercent >= 100 ? 'text-emerald-500' : 'text-orange-500'">
                        {{ Math.min(100, trackProgressPercent) }}%
                      </span>
                    </div>
                    <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-500"
                        :class="trackProgressPercent >= 100 ? 'bg-emerald-500' : 'bg-orange-500'"
                        :style="{ width: Math.min(100, trackProgressPercent) + '%' }">
                      </div>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-1 text-right">
                      目标 {{ trackGoal }} km
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 右侧：约球与成就 (Col 4) -->
          <div class="md:col-span-4 space-y-8 animate-fade-in-up" style="animation-delay: 200ms">
            <!-- 运动成就 -->
            <div
              class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-[400ms]">
              <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
                <iconify-icon class="text-yellow-500" icon="solar:medal-star-bold"></iconify-icon> 我的勋章
              </h3>
              <div class="grid grid-cols-3 gap-4">
                <div v-for="(medal, idx) in medals" :key="medal.label"
                  class="flex flex-col items-center gap-2 group relative"
                  :style="{ animationDelay: (400 + idx * 100) + 'ms' }" style="animation: fadeInUp 0.5s ease-out both">
                  <div class="w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300"
                    :class="medal.achieved ? 'bg-yellow-100 text-yellow-500 hover:scale-110 cursor-pointer' : 'bg-slate-100 text-slate-300 grayscale opacity-50'">
                    <iconify-icon :icon="medal.icon" width="24"></iconify-icon>
                  </div>
                  <span class="text-[10px]" :class="medal.achieved ? 'text-slate-500' : 'text-slate-400'">{{ medal.label
                  }}</span>
                  <div v-if="!medal.achieved"
                    class="absolute -top-2 left-1/2 -translate-x-1/2 -translate-y-full bg-slate-800 text-white text-[10px] px-2 py-1 rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
                    {{ medal.condition }}
                    <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-slate-800 rotate-45"></div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 约球广场 -->
            <div
              class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-[400ms]">
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-bold flex items-center gap-2">
                  <iconify-icon class="text-blue-500" icon="solar:users-group-rounded-bold"></iconify-icon> 约球广场
                </h3>
                <span v-if="matchesTotal > 0" class="text-[10px] text-slate-400">共 {{ matchesTotal }} 条</span>
              </div>

              <!-- 加载中 -->
              <div v-if="matchesLoading" class="flex items-center justify-center py-8">
                <iconify-icon icon="solar:spinner-bold-duotone"
                  class="text-orange-500 text-3xl animate-spin"></iconify-icon>
              </div>

              <!-- 空状态 -->
              <div v-else-if="matches.length === 0" class="text-center py-8">
                <iconify-icon icon="solar:sad-square-bold" class="text-5xl text-slate-200 mb-3"></iconify-icon>
                <p class="text-xs text-slate-400 mb-1">暂无约球信息</p>
                <p class="text-[10px] text-slate-300">快来发布第一条约球吧~</p>
              </div>

              <!-- 约球列表 -->
              <TransitionGroup v-else name="slide-up" tag="div" class="space-y-4">
                <div v-for="match in matches" :key="match.id"
                  class="p-3 bg-slate-50 rounded-xl hover:bg-orange-50 hover:shadow-md hover:-translate-x-1 transition-all duration-300 cursor-pointer group"
                  @click="joinMatch(match)">
                  <div class="flex items-center justify-between mb-2">
                    <span class="px-2 py-0.5 text-[10px] font-bold rounded" :class="match.tagClass">{{ match.sport
                      }}</span>
                    <span class="text-[10px] text-slate-400">{{ match.time }} {{ match.location }}</span>
                  </div>
                  <p class="text-xs font-medium mb-2 group-hover:text-orange-600 transition-colors duration-300">{{
                    match.desc }}</p>
                  <div class="flex items-center justify-between text-[10px] text-slate-400">
                    <span>发起人: {{ match.creator }}</span>
                    <span
                      class="text-orange-500 font-bold group-hover:bg-orange-500 group-hover:text-white px-2 py-0.5 rounded-full transition-all duration-300">加入
                      +</span>
                  </div>
                </div>
              </TransitionGroup>

              <!-- 加载更多 -->
              <div v-if="hasMoreMatches && !matchesLoading" class="text-center mt-4">
                <button @click="loadMoreMatches"
                  class="text-[10px] text-orange-500 font-bold hover:text-orange-600 transition-colors">
                  加载更多...
                </button>
              </div>

              <button @click="openMatchModal"
                class="w-full mt-6 py-2 border-2 border-dashed border-slate-200 text-slate-400 rounded-xl text-xs font-bold hover:border-orange-400 hover:text-orange-500 hover:bg-orange-50 active:scale-[0.98] transition-all duration-300">+
                发布约球信息</button>
            </div>
          </div>
        </div>
      </template>
    </main>

    <!-- 约球发布 Modal -->
    <Transition name="modal">
      <div v-if="showMatchModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4"
        @click.self="closeMatchModal">
        <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl animate-scale-in">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <iconify-icon class="text-blue-500" icon="solar:pen-bold" width="22"></iconify-icon> 发布约球
            </h3>
            <button @click="closeMatchModal" class="text-slate-400 hover:text-slate-600 transition-colors">
              <iconify-icon icon="solar:cross-bold" width="20"></iconify-icon>
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">运动类型 <span
                  class="text-red-400">*</span></label>
              <div class="grid grid-cols-3 gap-2">
                <button v-for="sport in matchSportOptions" :key="sport" @click="matchForm.sport = sport"
                  class="px-3 py-2 rounded-xl text-xs font-bold border transition-all duration-300"
                  :class="matchForm.sport === sport ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-slate-200 text-slate-500 hover:border-blue-300 hover:text-blue-500'">
                  {{ sport }}
                </button>
              </div>
              <p v-if="matchErrors.sport" class="text-[10px] text-red-400 mt-1">{{ matchErrors.sport }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">约球时间 <span
                  class="text-red-400">*</span></label>
              <input v-model="matchForm.time" type="text"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="如：明天 14:00 或 今晚 18:30" @input="matchErrors.time = ''" />
              <p v-if="matchErrors.time" class="text-[10px] text-red-400 mt-1">{{ matchErrors.time }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">约球地点 <span
                  class="text-red-400">*</span></label>
              <input v-model="matchForm.location" type="text"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="如：体育馆 · 西操场 · 游泳馆" @input="matchErrors.location = ''" />
              <p v-if="matchErrors.location" class="text-[10px] text-red-400 mt-1">{{ matchErrors.location }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">约球描述 <span
                  class="text-red-400">*</span></label>
              <textarea v-model="matchForm.desc" rows="3"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                placeholder="描述一下你的需求，如：三缺一来个水平中等的校友..." :maxlength="500" @input="matchErrors.desc = ''"></textarea>
              <div class="flex justify-between text-[10px] mt-1">
                <span v-if="matchErrors.desc" class="text-red-400">{{ matchErrors.desc }}</span>
                <span class="text-slate-400 ml-auto">{{ matchForm.desc.length }}/500</span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">你的昵称</label>
              <input v-model="matchForm.creator" type="text"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="匿名球友" :maxlength="20" />
            </div>
            <div class="flex gap-3 pt-2">
              <button @click="closeMatchModal"
                class="flex-1 px-4 py-2.5 bg-slate-100 text-slate-600 rounded-xl font-medium hover:bg-slate-200 active:scale-[0.98] transition-all duration-300">
                取消
              </button>
              <button @click="submitMatch" :disabled="matchSubmitting"
                class="flex-1 px-4 py-2.5 bg-blue-500 text-white rounded-xl font-bold hover:bg-blue-600 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-md shadow-blue-200 flex items-center justify-center gap-1.5">
                <iconify-icon v-if="matchSubmitting" icon="solar:spinner-bold-duotone" class="animate-spin"
                  width="16"></iconify-icon>
                <iconify-icon v-else icon="solar:plain-bold" width="16"></iconify-icon>
                {{ matchSubmitting ? '发布中...' : '立即发布' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 训练目标修改 Modal -->
    <Transition name="modal">
      <div v-if="showGoalModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4"
        @click.self="closeGoalModal">
        <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl animate-scale-in">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <iconify-icon class="text-orange-500" icon="solar:target-bold" width="22"></iconify-icon> 修改训练目标
            </h3>
            <button @click="closeGoalModal" class="text-slate-400 hover:text-slate-600 transition-colors">
              <iconify-icon icon="solar:cross-bold" width="20"></iconify-icon>
            </button>
          </div>
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">训练目标类型</label>
              <div class="grid grid-cols-2 gap-2">
                <button v-for="gt in goalTypes" :key="gt.value" @click="goalForm.type = gt.value"
                  class="px-3 py-2.5 rounded-xl text-xs font-bold border transition-all duration-300"
                  :class="goalForm.type === gt.value ? 'border-orange-500 bg-orange-50 text-orange-600' : 'border-slate-200 text-slate-500 hover:border-orange-300 hover:text-orange-500'">
                  {{ gt.label }}
                </button>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">
                每日运动时长 <span class="text-slate-400 font-normal">(分钟)</span>
              </label>
              <div class="flex items-center gap-3">
                <input v-model.number="goalForm.duration" type="range" min="10" max="120" step="5"
                  class="flex-1 h-2 bg-slate-200 rounded-full appearance-none cursor-pointer accent-orange-500" />
                <span class="w-14 text-center text-sm font-bold text-orange-500 bg-orange-50 rounded-lg py-1">{{
                  goalForm.duration }} 分钟</span>
              </div>
              <div class="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>10</span><span>120</span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">
                每周训练频率 <span class="text-slate-400 font-normal">(天)</span>
              </label>
              <div class="flex gap-1.5">
                <button v-for="d in 7" :key="d" @click="goalForm.frequency = d"
                  class="w-9 h-9 rounded-lg text-xs font-bold border transition-all duration-300"
                  :class="goalForm.frequency >= d ? 'border-orange-500 bg-orange-500 text-white' : 'border-slate-200 text-slate-400 hover:border-orange-300'">
                  {{ d }}
                </button>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">
                每日目标距离 <span class="text-slate-400 font-normal">(公里)</span>
              </label>
              <input v-model.number="goalForm.targetKm" type="number" min="1" max="50" step="0.5"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                placeholder="请输入距离 (1-50 km)" />
            </div>
            <div class="flex gap-3 pt-2">
              <button @click="closeGoalModal"
                class="flex-1 px-4 py-2.5 bg-slate-100 text-slate-600 rounded-xl font-medium hover:bg-slate-200 active:scale-[0.98] transition-all duration-300">
                取消
              </button>
              <button @click="saveGoal"
                class="flex-1 px-4 py-2.5 bg-orange-500 text-white rounded-xl font-bold hover:bg-orange-600 active:scale-[0.98] transition-all duration-300 shadow-md shadow-orange-200 flex items-center justify-center gap-1.5">
                <iconify-icon icon="solar:diskette-bold" width="16"></iconify-icon> 保存目标
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Toast 消息提示 -->
    <Transition name="toast">
      <div v-if="showToast"
        class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-orange-500 text-white px-6 py-3 rounded-full shadow-lg shadow-orange-200 flex items-center gap-2 z-50">
        <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
        <span class="text-sm font-medium">{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import Navbar from '@/components/Navbar.vue'
import { getMatchesAPI, createMatchAPI } from '@/api/matches'

const isLoading = ref(false)
const showToast = ref(false)
const toastMessage = ref('')
const activeCourseTab = ref('全部')

// ===== 训练目标状态 =====
const STORAGE_KEY = 'sport_goal_settings'
const showGoalModal = ref(false)

const goalTypes = [
  { label: '体质增强', value: 'fitness' },
  { label: '减脂塑形', value: 'fatloss' },
  { label: '耐力提升', value: 'endurance' },
  { label: '柔韧训练', value: 'flexibility' }
]

const defaultGoal = { type: 'fitness', duration: 20, frequency: 5, targetKm: 5 }
const savedGoal = loadGoalFromStorage()
const goalForm = reactive({ ...savedGoal })

function loadGoalFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      return {
        type: parsed.type || defaultGoal.type,
        duration: Math.min(120, Math.max(10, parsed.duration || defaultGoal.duration)),
        frequency: Math.min(7, Math.max(1, parsed.frequency || defaultGoal.frequency)),
        targetKm: Math.min(50, Math.max(1, parsed.targetKm || defaultGoal.targetKm))
      }
    }
  } catch { /* ignore */ }
  return { ...defaultGoal }
}

const goalLabel = computed(() => {
  const found = goalTypes.find(g => g.value === savedGoal.type)
  return found ? found.label : '体质增强'
})

const goalDescription = computed(() => {
  return `基于你的目标：体质增强。今天建议进行 ${savedGoal.duration} 分钟的中等强度有氧运动。`
    .replace('体质增强', goalLabel.value)
    .replace(/\d+/, String(savedGoal.duration))
})

const trackGoal = computed(() => savedGoal.targetKm)

function openGoalModal() {
  Object.assign(goalForm, { ...savedGoal })
  showGoalModal.value = true
}

function closeGoalModal() {
  showGoalModal.value = false
}

function saveGoal() {
  if (!goalForm.targetKm || goalForm.targetKm < 1 || goalForm.targetKm > 50) {
    showToastMessage('目标距离需在 1-50 km 之间')
    return
  }
  const data = { ...goalForm }
  Object.assign(savedGoal, data)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  showGoalModal.value = false
  resetTrack()
  showToastMessage('训练目标已保存！今日计划已同步更新')
}

// ===== 操场跑道状态 =====
const activeTrackMode = ref('jog')
const isTrackRunning = ref(false)
const trackElapsed = ref(0)
const trackDistance = ref(0)
let trackAnimFrame = null
let trackStartTime = 0
let trackAccumulatedElapsed = 0
let trackAccumulatedDistance = 0

const trackModes = [
  { id: 'jog', label: '慢跑', activeClass: 'bg-emerald-500 text-white', speed: 8, color: '#10b981' },
  { id: 'run', label: '快跑', activeClass: 'bg-orange-500 text-white', speed: 12, color: '#f97316' },
  { id: 'sprint', label: '冲刺', activeClass: 'bg-red-500 text-white', speed: 18, color: '#ef4444' }
]

const currentTrackMode = computed(() => trackModes.find(m => m.id === activeTrackMode.value) || trackModes[0])
const trackColor = computed(() => currentTrackMode.value.color)
const trackGradientStart = computed(() => currentTrackMode.value.color + '10')
const trackGradientEnd = computed(() => currentTrackMode.value.color + '05')

const trackBgClass = computed(() => {
  const map = { jog: 'bg-emerald-50/30', run: 'bg-orange-50/30', sprint: 'bg-red-50/30' }
  return map[activeTrackMode.value] || ''
})

const trackPace = computed(() => {
  if (trackDistance.value <= 0) return '--'
  const paceSec = (trackElapsed.value / trackDistance.value)
  const min = Math.floor(paceSec / 60)
  const sec = Math.floor(paceSec % 60)
  return `${min}'${String(sec).padStart(2, '0')}"`
})

const trackCalories = computed(() => Math.floor(trackDistance.value * 60))

const trackProgressPercent = computed(() => {
  if (!trackGoal.value || trackGoal.value <= 0) return 0
  return Math.round((trackDistance.value / trackGoal.value) * 100)
})

const runnerAngle = ref(0)
const runnerX = computed(() => 200 + 130 * Math.cos(runnerAngle.value))
const runnerY = computed(() => 120 + 70 * Math.sin(runnerAngle.value))

function switchTrackMode(modeId) {
  activeTrackMode.value = modeId
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function startTrack() {
  if (isTrackRunning.value) return
  isTrackRunning.value = true
  trackStartTime = performance.now()

  function tick(now) {
    if (!isTrackRunning.value) {
      trackAnimFrame = null
      return
    }
    const deltaSec = (now - trackStartTime) / 1000
    trackStartTime = now
    trackAccumulatedElapsed += deltaSec
    trackElapsed.value = Math.floor(trackAccumulatedElapsed)

    const speed = currentTrackMode.value.speed
    const deltaKm = speed * (deltaSec / 3600)
    trackAccumulatedDistance += deltaKm
    trackDistance.value = Math.round(trackAccumulatedDistance * 100) / 100

    const laps = trackAccumulatedDistance / 0.4
    runnerAngle.value = (laps * 2 * Math.PI) % (2 * Math.PI)

    if (trackAccumulatedDistance >= trackGoal.value) {
      pauseTrack()
      showToastMessage(`恭喜！已完成今日 ${trackGoal.value} km 目标！`)
    }

    trackAnimFrame = requestAnimationFrame(tick)
  }

  trackAnimFrame = requestAnimationFrame(tick)
}

function pauseTrack() {
  isTrackRunning.value = false
  if (trackAnimFrame) {
    cancelAnimationFrame(trackAnimFrame)
    trackAnimFrame = null
  }
}

function resetTrack() {
  pauseTrack()
  trackAccumulatedElapsed = 0
  trackAccumulatedDistance = 0
  trackElapsed.value = 0
  trackDistance.value = 0
  runnerAngle.value = 0
}

// ===== 概览统计数据 =====
const overviewStats = ref([
  { value: 285, label: '今日消耗 (kcal)', displayValue: '0' },
  { value: 45, label: '本周活跃 (min)', displayValue: '0' },
  { value: 3, label: '连续打卡 (day)', displayValue: '0' },
  { value: '1/4', label: '勋章点亮进度', displayValue: '1/4' }
])

// ===== 课程 Tab =====
const courseTabs = ['全部', '拉伸', '力量']

const allCourses = [
  {
    id: 1,
    category: '拉伸',
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
    category: '力量',
    alt: 'Abs workout',
    img: 'https://modao.cc/agent-py/media/generated_images/2026-03-26/613106ece87b4c1c8b21fb471f44d73a.jpg',
    duration: '12:30',
    title: '腹肌轰炸 (入门级)',
    desc: '仅需一张瑜伽垫，无需器械',
    intensity: '中高强度',
    intensityClass: 'text-red-500',
    participants: '856'
  }
]

const filteredCourses = computed(() => {
  if (activeCourseTab.value === '全部') return allCourses
  return allCourses.filter(c => c.category === activeCourseTab.value)
})

// ===== 勋章 =====
const medals = ref([
  { label: '清晨跑者', icon: 'solar:sun-bold', achieved: true, condition: '连续7天早上6点前跑步' },
  { label: '10天连胜', icon: 'solar:fire-bold', achieved: false, condition: '连续10天完成运动目标' },
  { label: '体测满分', icon: 'solar:crown-bold', achieved: false, condition: '体测成绩达到90分以上' }
])

// ===== 约球广场 =====
const matches = ref([])
const matchesLoading = ref(false)
const matchesTotal = ref(0)
const matchesPage = ref(1)
const matchesLimit = 10
const hasMoreMatches = ref(false)
const showMatchModal = ref(false)
const matchSubmitting = ref(false)

const matchSportOptions = ['羽毛球', '篮球', '足球', '乒乓球', '网球', '跑步', '骑行', '游泳', '排球', '其他']

const matchForm = reactive({
  sport: '',
  time: '',
  location: '',
  desc: '',
  creator: ''
})

const matchErrors = reactive({
  sport: '',
  time: '',
  location: '',
  desc: ''
})

function loadMatches(page = 1, append = false) {
  matchesLoading.value = true
  getMatchesAPI({ page, limit: matchesLimit })
    .then(res => {
      const data = res.data || {}
      const items = (data.items || []).map(item => ({
        id: item.id,
        sport: item.sport || item.sport_type || '',
        tagClass: item.tagClass || item.tag_class || 'bg-slate-100 text-slate-600',
        time: item.time || item.time_slot || '',
        location: item.location || '',
        desc: item.desc || item.description || '',
        creator: item.creator || item.creator_name || '匿名球友'
      }))
      if (append) {
        matches.value = [...matches.value, ...items]
      } else {
        matches.value = items
      }
      matchesTotal.value = data.total || 0
      matchesPage.value = page
      hasMoreMatches.value = matches.value.length < matchesTotal.value
    })
    .catch(() => {
      showToastMessage('加载约球信息失败')
    })
    .finally(() => {
      matchesLoading.value = false
    })
}

function loadMoreMatches() {
  if (hasMoreMatches.value && !matchesLoading.value) {
    loadMatches(matchesPage.value + 1, true)
  }
}

function openMatchModal() {
  matchForm.sport = ''
  matchForm.time = ''
  matchForm.location = ''
  matchForm.desc = ''
  matchForm.creator = ''
  Object.keys(matchErrors).forEach(k => matchErrors[k] = '')
  showMatchModal.value = true
}

function closeMatchModal() {
  showMatchModal.value = false
}

function submitMatch() {
  let valid = true
  if (!matchForm.sport) {
    matchErrors.sport = '请选择运动类型'
    valid = false
  }
  if (!matchForm.time.trim()) {
    matchErrors.time = '请填写约球时间'
    valid = false
  }
  if (!matchForm.location.trim()) {
    matchErrors.location = '请填写约球地点'
    valid = false
  }
  if (!matchForm.desc.trim()) {
    matchErrors.desc = '请填写约球描述'
    valid = false
  } else if (matchForm.desc.length > 500) {
    matchErrors.desc = '描述不能超过500字'
    valid = false
  }
  if (!valid) return

  matchSubmitting.value = true
  createMatchAPI({
    sport_type: matchForm.sport,
    time_slot: matchForm.time.trim(),
    location: matchForm.location.trim(),
    description: matchForm.desc.trim(),
    creator_name: matchForm.creator.trim() || '匿名球友'
  })
    .then(() => {
      showMatchModal.value = false
      showToastMessage('约球信息发布成功！等待球友加入~')
      loadMatches(1, false)
    })
    .catch(() => {
      showToastMessage('发布失败，请稍后再试')
    })
    .finally(() => {
      matchSubmitting.value = false
    })
}

function joinMatch(match) {
  showToastMessage(`已申请加入「${match.sport}」约球，等待发起人确认`)
}

// ===== 通用工具 =====
function showToastMessage(message) {
  toastMessage.value = message
  showToast.value = true
  clearTimeout(showToast._timer)
  showToast._timer = setTimeout(() => {
    showToast.value = false
  }, 2000)
}

function startPlan() {
  if (!isTrackRunning.value) {
    startTrack()
    showToastMessage('今日训练计划已开始！')
  }
}

function animateNumbers() {
  overviewStats.value.forEach((stat, idx) => {
    if (typeof stat.value === 'number') {
      const duration = 800
      const steps = 20
      const stepValue = stat.value / steps
      const stepDelay = duration / steps
      let current = 0
      const timer = setInterval(() => {
        current += stepValue
        if (current >= stat.value) {
          stat.displayValue = String(stat.value)
          clearInterval(timer)
        } else {
          stat.displayValue = String(Math.floor(current))
        }
      }, stepDelay + idx * 50)
    }
  })
}

onMounted(() => {
  loadMatches(1)
  setTimeout(() => {
    isLoading.value = false
    setTimeout(() => {
      animateNumbers()
    }, 100)
  }, 800)
})

onUnmounted(() => {
  pauseTrack()
})
</script>

<style scoped>
.course-card {
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@media (hover: hover) {
  .course-card:hover {
    transform: translateY(-4px);
  }
}
</style>