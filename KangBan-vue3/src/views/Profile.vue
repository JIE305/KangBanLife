<template>
  <div class="min-h-screen bg-slate-50">
    <Navbar theme="emerald" logo-icon="solar:health-bold" :show-login="false" :show-notification="false" />

    <main class="max-w-4xl mx-auto px-6 py-10">
      <!-- 用户头像和基本信息 -->
      <div
        class="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-3xl p-8 text-white mb-8 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2"></div>
        <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2"></div>

        <!-- 退出登录按钮 -->
        <button @click="handleLogout"
          class="absolute top-4 right-4 z-20 flex items-center gap-1 px-3 py-1.5 bg-white/20 hover:bg-white/30 text-white text-sm rounded-lg transition-colors"
          title="退出登录">
          <iconify-icon icon="solar:logout-2-linear" width="16"></iconify-icon>
          退出登录
        </button>

        <div class="relative z-10 flex flex-col md:flex-row items-center gap-6">
          <div class="relative">
            <div class="w-24 h-24 rounded-full bg-white/20 flex items-center justify-center border-4 border-white/30">
              <iconify-icon v-if="!user.avatar_url" icon="solar:user-circle-bold" width="48"></iconify-icon>
              <img v-else :src="user.avatar_url" :alt="user.username" class="w-full h-full rounded-full object-cover" />
            </div>
            <input ref="avatarInput" type="file" accept="image/*" class="hidden" @change="handleAvatarUpload" />
            <button @click="triggerAvatarUpload"
              class="absolute -bottom-2 -right-2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-slate-100 transition-colors">
              <iconify-icon icon="solar:camera-bold" width="16" class="text-emerald-500"></iconify-icon>
            </button>
          </div>

          <div class="text-center md:text-left">
            <h1 class="text-2xl font-bold mb-2">{{ user.username || '未填写' }}</h1>
            <p class="text-emerald-100 text-sm">学号：{{ user.student_id || '未填写' }}</p>
            <p class="text-emerald-100 text-sm mt-1">注册时间：{{ formatDate(user.created_at) }}</p>
          </div>
        </div>
      </div>

      <!-- 用户详细信息卡片 -->
      <div class="grid md:grid-cols-2 gap-6 mb-8">
        <!-- 基本信息 -->
        <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <iconify-icon class="text-emerald-500" icon="solar:info-bold"></iconify-icon> 基本信息
            </h2>
            <button v-if="!isEditingBasic" @click="startEditBasic"
              class="text-emerald-500 text-sm font-medium hover:text-emerald-600 flex items-center gap-1">
              <iconify-icon icon="solar:pen-bold" width="16"></iconify-icon> 编辑
            </button>
          </div>

          <!-- 查看模式 -->
          <div v-if="!isEditingBasic" class="space-y-4">
            <div class="flex items-center justify-between py-3 border-b border-slate-50">
              <span class="text-slate-500 text-sm">用户名</span>
              <span class="font-medium">{{ user.username || '未填写' }}</span>
            </div>
            <div class="flex items-center justify-between py-3 border-b border-slate-50">
              <span class="text-slate-500 text-sm">学号</span>
              <span class="font-medium">{{ user.student_id || '未填写' }}</span>
            </div>
            <div class="flex items-center justify-between py-3 border-b border-slate-50">
              <span class="text-slate-500 text-sm">性别</span>
              <span class="font-medium">{{ getGenderText(user.gender) }}</span>
            </div>
            <div class="flex items-center justify-between py-3 border-b border-slate-50">
              <span class="text-slate-500 text-sm">身高</span>
              <span class="font-medium">{{ user.height || '未填写' }}</span>
            </div>
            <div class="flex items-center justify-between py-3">
              <span class="text-slate-500 text-sm">体重</span>
              <span class="font-medium">{{ user.weight || '未填写' }}</span>
            </div>
          </div>

          <!-- 编辑模式 -->
          <div v-else class="space-y-4">
            <div class="space-y-1">
              <label class="text-xs text-slate-400">用户名</label>
              <input v-model="editForm.username" type="text" placeholder="请输入用户名"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div class="space-y-1">
              <label class="text-xs text-slate-400">性别</label>
              <select v-model="editForm.gender"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-emerald-500">
                <option :value="0">未知</option>
                <option :value="1">男</option>
                <option :value="2">女</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-xs text-slate-400">身高 (cm)</label>
              <input v-model="editForm.height" type="number" placeholder="请输入身高"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div class="space-y-1">
              <label class="text-xs text-slate-400">体重 (kg)</label>
              <input v-model="editForm.weight" type="number" placeholder="请输入体重"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div class="flex gap-3 pt-4">
              <button @click="cancelEditBasic"
                class="flex-1 py-2 bg-slate-100 text-slate-600 rounded-xl text-sm font-medium hover:bg-slate-200 transition-colors">
                取消
              </button>
              <button @click="saveEditBasic"
                class="flex-1 py-2 bg-emerald-500 text-white rounded-xl text-sm font-medium hover:bg-emerald-600 transition-colors">
                保存
              </button>
            </div>
          </div>
        </div>

        <!-- 联系方式 -->
        <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <iconify-icon class="text-blue-500" icon="solar:phone-bold"></iconify-icon> 联系方式
            </h2>
            <button v-if="!isEditingContact" @click="startEditContact"
              class="text-emerald-500 text-sm font-medium hover:text-emerald-600 flex items-center gap-1">
              <iconify-icon icon="solar:pen-bold" width="16"></iconify-icon> 编辑
            </button>
          </div>

          <!-- 查看模式 -->
          <div v-if="!isEditingContact" class="space-y-4">
            <div class="flex items-center justify-between py-3 border-b border-slate-50">
              <span class="text-slate-500 text-sm">邮箱</span>
              <span class="font-medium text-emerald-600">{{ user.email || '未填写' }}</span>
            </div>
            <div class="flex items-center justify-between py-3">
              <span class="text-slate-500 text-sm">手机号</span>
              <span class="font-medium">{{ user.phone || '未填写' }}</span>
            </div>
          </div>

          <!-- 编辑模式 -->
          <div v-else class="space-y-4">
            <div class="space-y-1">
              <label class="text-xs text-slate-400">邮箱</label>
              <input v-model="editForm.email" type="email" placeholder="请输入邮箱"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div class="space-y-1">
              <label class="text-xs text-slate-400">手机号</label>
              <input v-model="editForm.phone" type="tel" placeholder="请输入手机号"
                class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div class="flex gap-3 pt-4">
              <button @click="cancelEditContact"
                class="flex-1 py-2 bg-slate-100 text-slate-600 rounded-xl text-sm font-medium hover:bg-slate-200 transition-colors">
                取消
              </button>
              <button @click="saveEditContact"
                class="flex-1 py-2 bg-emerald-500 text-white rounded-xl text-sm font-medium hover:bg-emerald-600 transition-colors">
                保存
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Toast 消息提示 -->
    <Transition name="toast">
      <div v-if="showToast"
        class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-emerald-500 text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-2 z-50">
        <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
        <span class="text-sm font-medium">{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { useUserStore } from '../stores/user'
import { getProfileAPI, updateBasicAPI, updateContactAPI, uploadAvatarAPI } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()

const user = reactive({
  id: 0,
  student_id: '',
  username: '',
  email: '',
  phone: '',
  avatar_url: '',
  gender: 0,
  height: null,
  weight: null,
  created_at: '',
  updated_at: ''
})

const editForm = reactive({
  username: '',
  gender: 0,
  height: null,
  weight: null,
  email: '',
  phone: ''
})

const isEditingBasic = ref(false)
const isEditingContact = ref(false)
const isUploading = ref(false)
const showToast = ref(false)
const toastMessage = ref('')
const avatarInput = ref(null)

const healthStats = ref({
  steps: '0',
  water: '0',
  sleep: '0',
  days: '0'
})

const getGenderText = (gender) => {
  const genderMap = {
    0: '未知',
    1: '男',
    2: '女'
  }
  return genderMap[gender] || '未填写'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未填写'
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 2000)
}

const startEditBasic = () => {
  editForm.username = user.username
  editForm.gender = user.gender
  editForm.height = user.height
  editForm.weight = user.weight
  isEditingBasic.value = true
}

const cancelEditBasic = () => {
  isEditingBasic.value = false
}

const saveEditBasic = async () => {
  try {
    const res = await updateBasicAPI({
      username: editForm.username,
      gender: editForm.gender,
      height: editForm.height,
      weight: editForm.weight
    })
    const updated = res.data.user
    if (updated) {
      Object.assign(user, updated)
    }
    isEditingBasic.value = false
    showToastMessage('基本信息已保存')
  } catch {
    // error handled by interceptor
  }
}

const startEditContact = () => {
  editForm.email = user.email
  editForm.phone = user.phone
  isEditingContact.value = true
}

const cancelEditContact = () => {
  isEditingContact.value = false
}

const saveEditContact = async () => {
  try {
    await updateContactAPI({
      email: editForm.email,
      phone: editForm.phone
    })
    user.email = editForm.email
    user.phone = editForm.phone
    isEditingContact.value = false
    showToastMessage('联系方式已保存')
  } catch {
    // error handled by interceptor
  }
}

const triggerAvatarUpload = () => {
  avatarInput.value.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    showToastMessage('请选择图片文件')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    showToastMessage('图片大小不能超过5MB')
    return
  }

  isUploading.value = true

  try {
    const res = await uploadAvatarAPI(file)
    user.avatar_url = res.data.avatar_url
    // 同步到 localStorage，Navbar 需要读取
    const saved = localStorage.getItem('unihealth_user')
    if (saved) {
      const u = JSON.parse(saved)
      u.avatar_url = res.data.avatar_url
      localStorage.setItem('unihealth_user', JSON.stringify(u))
    }
    isUploading.value = false
    showToastMessage('头像上传成功')
    window.dispatchEvent(new Event('user-avatar-updated'))
  } catch {
    isUploading.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

onMounted(async () => {
  try {
    const res = await getProfileAPI()
    const profile = res.data.user
    if (profile) {
      Object.assign(user, profile)
    }
  } catch {
    // 未登录或后端未启动
  }
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
</style>