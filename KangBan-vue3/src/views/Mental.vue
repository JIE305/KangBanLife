<template>
  <div class="text-slate-800" style="background-color: #f0f9ff;">
    <Navbar theme="blue" logo-icon="solar:ghost-bold" right-content="status" right-text="情绪守护进行中" :show-login="false"
      :show-notification="false" />

    <main class="max-w-[1440px] mx-auto px-6 py-10">
      <!-- 头部心情选择 -->
      <section class="mb-12 text-center">
        <h2 class="text-2xl font-bold mb-6">嘿，今天感觉怎么样？</h2>
        <div class="flex justify-center flex-wrap gap-6 pb-4 pt-1">
          <button v-for="mood in moods" :key="mood.emoji" @click="selectMood(mood.label)"
            class="flex flex-col items-center gap-2 p-4 rounded-2xl shadow-sm border transition-all duration-300 w-24"
            :class="selectedMood === mood.label ? 'bg-blue-50 border-blue-400 scale-105 shadow-md' : 'bg-white border-slate-100 hover:border-blue-400'">
            <span class="text-3xl transition-transform duration-300" :class="selectedMood === mood.label ? 'scale-110' : ''">{{ mood.emoji }}</span>
            <span class="text-xs" :class="selectedMood === mood.label ? 'text-blue-500 font-medium' : 'text-slate-500'">{{ mood.label }}</span>
          </button>
        </div>
      </section>

      <!-- AI 心理伴聊 -->
      <ChatPanel />

      <div class="grid md:grid-cols-12 gap-8">
        <!-- 匿名树洞 (Col 8) -->
        <div class="md:col-span-8 space-y-6">
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-blue-500" icon="solar:chat-round-line-bold"></iconify-icon> 匿名树洞
            </h3>
            <div class="mb-8">
              <textarea v-model="newPost" name="newPost" maxlength="100" show-word-limit
                placeholder="有些话不想告诉熟人？在这里匿名写下吧..."
                class="w-full bg-slate-50 border-none rounded-2xl p-4 text-sm focus:ring-1 focus:ring-blue-500 h-24 mb-4"></textarea>
              <div class="flex items-center justify-between">
                <span class="text-xs text-slate-400">{{ newPost.length }}/100</span>
                <button @click="addPost"
                  class="px-6 py-2 bg-blue-500 text-white rounded-xl text-sm font-bold shadow-lg shadow-blue-100">发布碎碎念</button>
              </div>
            </div>
            <!-- 动态列表 -->
            <div class="space-y-4">
              <div v-for="post in posts" :key="post.id" class="hole-card p-5 rounded-2xl border bg-white border-slate-100 shadow-sm relative">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider bg-slate-100 text-slate-400">
                    {{ post.author }}
                  </span>
                  <div class="flex items-center gap-3">
                    <span class="text-[10px] text-slate-400">{{ formatTime(post.time) }}</span>
                    <button @click="deletePost(post.id)" class="text-slate-300 hover:text-red-400 transition-colors" title="删除">
                      <iconify-icon icon="solar:trash-bin-2-linear" width="14"></iconify-icon>
                    </button>
                  </div>
                </div>
                <p class="text-sm leading-relaxed text-slate-700">{{ post.content }}</p>
                <div class="mt-4 flex items-center gap-4 text-xs text-slate-400">
                  <button @click="toggleLike(post.id)" class="flex items-center gap-1 hover:text-pink-500 transition-colors"><iconify-icon
                      icon="solar:heart-linear"></iconify-icon> {{ post.likes }}</button>
                  <button class="flex items-center gap-1 hover:text-blue-500 transition-colors"><iconify-icon
                      icon="solar:chat-dots-linear"></iconify-icon> {{ post.comments }}</button>
                </div>
              </div>
              <div v-if="postsError && posts.length === 0" class="text-center text-slate-400 py-8">数据加载失败 :(</div>
              <div v-else-if="posts.length === 0" class="text-center text-slate-400 py-8">暂无帖子，快来发布第一条吧~</div>
            </div>
          </div>
        </div>
        <!-- 右侧：冥想与咨询 (Col 4) -->
        <div class="md:col-span-4 space-y-8">
          <!-- 冥想专区 -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
              <iconify-icon class="text-indigo-500" icon="solar:music-note-bold"></iconify-icon> 专注与助眠
            </h3>
            <div class="space-y-3">
              <div v-for="track in meditationTracks" :key="track.title"
                class="flex items-center justify-between p-3 rounded-xl group cursor-pointer"
                :class="track.active ? 'bg-indigo-50' : 'bg-slate-50 hover:bg-slate-100'"
                @click="toggleTrack(track.title)">
                <div class="flex items-center gap-3">
                  <iconify-icon
                    :class="track.active ? 'text-indigo-500 group-hover:scale-125' : 'text-slate-400 group-hover:scale-125'"
                    :icon="track.active ? 'solar:pause-bold' : 'solar:play-bold'" width="24"
                    class="transition-transform"></iconify-icon>
                  <div>
                    <div class="text-sm font-bold" :class="track.active ? 'text-indigo-900' : 'text-slate-700'">{{
                      track.title }}</div>
                    <div class="text-[10px]" :class="track.active ? 'text-indigo-400' : 'text-slate-400'">{{ track.desc
                    }}</div>
                  </div>
                </div>
                <iconify-icon v-if="track.active" class="text-indigo-200" icon="solar:soundwave-bold"></iconify-icon>
              </div>
            </div>
          </div>
          <!-- 心理咨询热线 -->
          <div
            class="bg-gradient-to-br from-blue-500 to-indigo-600 p-6 rounded-3xl shadow-xl shadow-blue-200 text-white">
            <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
              <iconify-icon icon="solar:phone-calling-bold"></iconify-icon> 心理急救站
            </h3>
            <p class="text-xs text-blue-100 leading-relaxed mb-6">如果你感到极度痛苦或绝望，请务必向专业人士寻求帮助，世界依然爱你。</p>
            <div class="space-y-4">
              <div class="bg-white/10 p-3 rounded-xl border border-white/20">
                <div class="text-[10px] text-blue-100 mb-1">河大心理中心（金明校区）</div>
                <div class="text-lg font-bold tracking-widest">0371-23881927</div>
              </div>
              <div class="bg-white/10 p-3 rounded-xl border border-white/20">
                <div class="text-[10px] text-blue-100 mb-1">希望24热线 (全国)</div>
                <div class="text-lg font-bold tracking-widest">400-161-9995</div>
              </div>
            </div>
            <button
              class="w-full mt-6 py-2 bg-white text-blue-600 rounded-xl text-sm font-bold hover:bg-blue-50 transition-colors">在线咨询导师</button>
          </div>
        </div>
      </div>
    </main>

    <!-- Toast 消息提示 -->
    <Transition name="toast">
      <div v-if="showToast"
        class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-2 z-50">
        <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
        <span class="text-sm font-medium">{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '@/components/Navbar.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import { getPostsAPI, createPostAPI, toggleLikeAPI, deletePostAPI } from '@/api/posts'

const newPost = ref('')
const currentAudio = ref(null)
const currentTrackTitle = ref('')
const selectedMood = ref('')
const showToast = ref(false)
const toastMessage = ref('')

const moods = ref([
  { emoji: '😊', label: '很开心' },
  { emoji: '😐', label: '一般般' },
  { emoji: '😫', label: '有压力' },
  { emoji: '😔', label: '有点丧' },
  { emoji: '😴', label: '很疲惫' }
])

const posts = ref([])
const postsError = ref(false)

const meditationTracks = ref([
  { title: '夏日夜间', desc: '专注学习 · 5min', audioSrc: 'https://audio-previews.elements.envatousercontent.com/files/372706880/preview.mp3', active: false },
  { title: '深海呼吸冥想', desc: '减压舒缓 · 3min', audioSrc: 'https://audio-previews.elements.envatousercontent.com/files/312436737/preview.mp3', active: false },
  { title: '雨落书亭', desc: '助眠休息 · 4min', audioSrc: 'https://audio-previews.elements.envatousercontent.com/files/507697751/preview.mp3', active: false }
])

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2000)
}

const selectMood = (label) => {
  selectedMood.value = selectedMood.value === label ? '' : label
}

const fetchPosts = async () => {
  try {
    const res = await getPostsAPI({ page: 1, limit: 50 })
    posts.value = res.data.items || []
    postsError.value = false
  } catch {
    postsError.value = true
  }
}

const formatTime = (timeStr) => {
  if (!timeStr || timeStr === '刚刚') return '刚刚'
  const postTime = new Date(timeStr.replace(' ', 'T'))
  const now = new Date()
  const diff = Math.floor((now - postTime) / 1000)
  if (diff < 60) return '刚刚'
  if (diff < 3600) return Math.floor(diff / 60) + '分钟前'
  if (diff < 21600) return Math.floor(diff / 3600) + '小时前'
  // 超过6小时显示真实时间 YYYY-MM-DD HH:mm
  const y = postTime.getFullYear()
  const mm = String(postTime.getMonth() + 1).padStart(2, '0')
  const dd = String(postTime.getDate()).padStart(2, '0')
  const hh = String(postTime.getHours()).padStart(2, '0')
  const min = String(postTime.getMinutes()).padStart(2, '0')
  return `${y}-${mm}-${dd} ${hh}:${min}`
}

const addPost = async () => {
  if (!newPost.value.trim()) return
  const token = localStorage.getItem('unihealth_token')
  if (!token) {
    showToastMessage('请先登录后再发帖')
    return
  }
  try {
    const res = await createPostAPI(newPost.value.trim())
    const newPostData = res.data.post
    newPostData.time = '刚刚'
    posts.value.unshift(newPostData)
    newPost.value = ''
  } catch {
    // error handled by interceptor
  }
}

const toggleLike = async (postId) => {
  const token = localStorage.getItem('unihealth_token')
  if (!token) {
    showToastMessage('请先登录后再点赞')
    return
  }
  try {
    const res = await toggleLikeAPI(postId)
    const post = posts.value.find(p => p.id === postId)
    if (post) {
      post.likes = res.data.likes
    }
  } catch {
    // error handled by interceptor
  }
}

const deletePost = async (postId) => {
  if (!window.confirm('确定要删除这条帖子吗？')) return
  try {
    await deletePostAPI(postId)
    posts.value = posts.value.filter(p => p.id !== postId)
    showToastMessage('帖子已删除')
  } catch {
    // error handled by interceptor
  }
}

const toggleTrack = (title) => {
  const targetTrack = meditationTracks.value.find(track => track.title === title)

  if (!targetTrack) return

  if (currentTrackTitle.value === title && currentAudio.value) {
    if (currentAudio.value.paused) {
      currentAudio.value.play()
      targetTrack.active = true
    } else {
      currentAudio.value.pause()
      targetTrack.active = false
    }
  } else {
    if (currentAudio.value) {
      currentAudio.value.pause()
    }

    meditationTracks.value.forEach(track => {
      track.active = (track.title === title)
    })

    const audio = new Audio(targetTrack.audioSrc)
    audio.play().then(() => {
      currentAudio.value = audio
      currentTrackTitle.value = title
    }).catch(() => {
      currentTrackTitle.value = ''
      targetTrack.active = false
    })
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}

.hole-card {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
