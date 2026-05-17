<template>
  <section class="mb-10">
    <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-slate-50">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🤖</span>
          <div>
            <h3 class="text-base font-bold text-slate-800">AI 心理伙伴</h3>
            <p class="text-xs text-slate-400">随时倾听你的心事</p>
          </div>
        </div>
        <div class="flex items-center gap-3 relative" ref="historyRef">
          <button
            @click="toggleHistory"
            class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors"
            :class="isHistoryOpen ? 'bg-green-50 border-green-300 text-green-600' : 'bg-white border-slate-200 text-slate-500 hover:border-green-300 hover:text-green-600'"
          >
            <iconify-icon icon="solar:document-add-bold" width="14"></iconify-icon>
            历史
          </button>
          <span class="flex items-center gap-1.5 text-xs font-medium" :class="isLoggedIn ? 'text-green-500' : 'text-slate-400'">
            <span class="w-2 h-2 rounded-full" :class="isLoggedIn ? 'bg-green-400' : 'bg-slate-300'"></span>
            {{ isLoggedIn ? '在线' : '离线' }}
          </span>
          <ChatHistory
            v-if="isHistoryOpen"
            :sessions="historySessions"
            :loading="historyLoading"
            @select="selectSession"
            @close="isHistoryOpen = false"
          />
        </div>
      </div>

      <!-- Messages -->
      <div ref="msgContainer" class="px-6 py-4 h-[200px] overflow-y-auto space-y-3 bg-slate-50/50">
        <div v-if="messages.length === 0" class="text-center text-slate-400 py-12 text-sm">
          <p class="text-2xl mb-2">💬</p>
          <p>嗨！我是你的心理伙伴，今天想聊些什么？</p>
        </div>
        <div v-for="(msg, idx) in messages" :key="idx" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div
            class="max-w-[75%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed"
            :class="msg.role === 'user'
              ? 'bg-green-500 text-white rounded-br-md'
              : 'bg-white text-slate-700 rounded-bl-md shadow-sm border border-slate-100'"
          >{{ msg.content }}</div>
        </div>
        <div v-if="sending" class="flex justify-start">
          <div class="bg-white text-slate-400 rounded-bl-md shadow-sm border border-slate-100 px-4 py-2.5 rounded-2xl text-sm">
            <span class="inline-flex gap-1">
              <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay:0ms"></span>
              <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay:150ms"></span>
              <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay:300ms"></span>
            </span>
          </div>
        </div>
      </div>

      <!-- Login prompt (guest only) -->
      <div v-if="!isLoggedIn" class="px-6 py-2 bg-amber-50 border-t border-amber-100 flex items-center justify-between">
        <span class="text-xs text-amber-700">登录后解锁完整 AI 智能对话</span>
        <router-link to="/login" class="text-xs font-bold text-amber-700 bg-amber-100 px-3 py-1 rounded-full hover:bg-amber-200 transition-colors">去登录 →</router-link>
      </div>

      <!-- Input -->
      <div class="flex items-center gap-3 px-6 py-4 border-t border-slate-100">
        <input
          v-model="inputText"
          @keydown.enter="send"
          :disabled="sending"
          placeholder="输入你想说的话..."
          class="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent"
        />
        <button
          @click="send"
          :disabled="!inputText.trim() || sending"
          class="px-5 py-2.5 bg-green-500 text-white rounded-xl text-sm font-bold hover:bg-green-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-lg shadow-green-100"
        >{{ sending ? '思考中...' : '发送' }}</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick, computed } from 'vue'
import ChatHistory from '@/components/ChatHistory.vue'
import { sendMessageAPI, getHistoryAPI, getHistoryDetailAPI } from '@/api/chat'

const inputText = ref('')
const messages = ref([])
const sending = ref(false)
const isHistoryOpen = ref(false)
const historySessions = ref([])
const historyLoading = ref(false)
const msgContainer = ref(null)
const historyRef = ref(null)

const STORAGE_KEY = 'unihealth_chat_messages'

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('unihealth_token')
})

const loadGuestMessages = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : []
  } catch { return [] }
}

const saveGuestMessages = () => {
  if (!isLoggedIn.value) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.value))
  }
}

// Initialize: load from localStorage if guest
onMounted(() => {
  if (!isLoggedIn.value) {
    messages.value = loadGuestMessages()
  }
})

// Auto-scroll to bottom on new message or history load
watch(
  () => messages.value,
  async () => {
    await nextTick()
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight
    }
  },
  { deep: true }
)

// Close history on outside click
const handleClickOutside = (e) => {
  if (isHistoryOpen.value && historyRef.value && !historyRef.value.contains(e.target)) {
    isHistoryOpen.value = false
  }
}
onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

const send = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  sending.value = true
  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  saveGuestMessages()

  try {
    const res = await sendMessageAPI(text)
    messages.value.push({ role: 'ai', content: res.data.reply })
  } catch {
    messages.value.push({ role: 'ai', content: '抱歉，我暂时无法回应。请稍后再试。' })
  } finally {
    sending.value = false
  }
  saveGuestMessages()
}

const toggleHistory = () => {
  isHistoryOpen.value = !isHistoryOpen.value
  if (isHistoryOpen.value && isLoggedIn.value) {
    fetchHistory()
  }
}

const fetchHistory = async () => {
  historyLoading.value = true
  try {
    const res = await getHistoryAPI()
    historySessions.value = res.data.sessions || []
  } catch {
    historySessions.value = []
  } finally {
    historyLoading.value = false
  }
}

const selectSession = async (sessionId) => {
  try {
    const res = await getHistoryDetailAPI(sessionId)
    messages.value = res.data.messages.map(m => ({
      role: m.role,
      content: m.content
    }))
  } catch {
    // ignore
  }
  isHistoryOpen.value = false
}
</script>
