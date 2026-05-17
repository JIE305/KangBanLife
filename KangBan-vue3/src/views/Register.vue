<template>
  <div
    class="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-blue-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div v-for="blob in blobs" :key="blob.id" class="absolute rounded-full" :style="{
        width: blob.currentSize + 'px',
        height: blob.currentSize + 'px',
        backgroundColor: blob.color,
        left: blob.x + 'px',
        top: blob.y + 'px',
        opacity: blob.opacity,
        transform: 'translate(-50%, -50%)',
        transition: 'none'
      }"></div>
    </div>

    <div class="max-w-md w-full space-y-8 relative z-10">
      <div class="text-center">
        <div
          class="w-16 h-16 bg-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-emerald-200">
          <iconify-icon icon="solar:user-plus-bold" width="32" class="text-white"></iconify-icon>
        </div>
        <h2 class="text-3xl font-bold text-slate-800">创建账号</h2>
        <p class="mt-2 text-slate-500">加入康伴生活，开启健康之旅</p>
      </div>

      <form class="bg-white/95 backdrop-blur-sm rounded-3xl shadow-xl p-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700">学号</label>
          <div class="relative">
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <iconify-icon icon="solar:user-linear" width="20"></iconify-icon>
            </div>
            <input v-model="form.studentId" type="text" placeholder="请输入学号"
              class="w-full pl-12 pr-4 py-4 outline-none border rounded-xl focus:ring-1 focus:ring-emerald-500 focus:border-transparent transition-all bg-slate-50 hover:bg-white" />
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700">姓名</label>
          <div class="relative">
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <iconify-icon icon="solar:user-circle-linear" width="20"></iconify-icon>
            </div>
            <input v-model="form.name" type="text" placeholder="请输入姓名"
              class="w-full pl-12 pr-4 py-4 outline-none border rounded-xl focus:ring-1 focus:ring-emerald-500 focus:border-transparent transition-all bg-slate-50 hover:bg-white" />
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700">手机号</label>
          <div class="relative">
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <iconify-icon icon="solar:phone-linear" width="20"></iconify-icon>
            </div>
            <input v-model="form.phone" type="tel" placeholder="请输入手机号"
              class="w-full pl-12 pr-4 py-4 outline-none border rounded-xl focus:ring-1 focus:ring-emerald-500 focus:border-transparent transition-all bg-slate-50 hover:bg-white" />
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700">密码</label>
          <div class="relative">
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <iconify-icon icon="solar:lock-linear" width="20"></iconify-icon>
            </div>
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码"
              class="w-full pl-12 pr-12 py-4 outline-none border rounded-xl focus:ring-1 focus:ring-emerald-500 focus:border-transparent transition-all bg-slate-50 hover:bg-white" />
            <button type="button" class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              @click="showPassword = !showPassword">
              <iconify-icon :icon="showPassword ? 'solar:eye-linear' : 'solar:eye-closed-linear'"
                width="20"></iconify-icon>
            </button>
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700">确认密码</label>
          <div class="relative">
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <iconify-icon icon="carbon:password" width="20"></iconify-icon>
            </div>
            <input v-model="form.confirmPassword" :type="showPassword ? 'text' : 'password'" placeholder="请再次输入密码"
              class="w-full pl-12 pr-4 py-4 outline-none border rounded-xl focus:ring-1 focus:ring-emerald-500 focus:border-transparent transition-all bg-slate-50 hover:bg-white" />
          </div>
        </div>

        <label class="flex items-start gap-3">
          <input type="checkbox" v-model="form.agree"
            class="w-4 h-4 mt-1 text-emerald-500 rounded border-slate-300 focus:ring-emerald-500" />
          <span class="text-sm text-slate-600">
            我已阅读并同意
            <a href="#" class="text-emerald-600 hover:text-emerald-500">《用户协议》</a>
            和
            <a href="#" class="text-emerald-600 hover:text-emerald-500">《隐私政策》</a>
          </span>
        </label>

        <button type="submit"
          class="w-full py-4 bg-emerald-500 text-white rounded-xl font-bold shadow-xl shadow-emerald-200 hover:bg-emerald-400 hover:shadow-md transition-all flex items-center justify-center gap-2"
          :disabled="isSubmitting">
          <iconify-icon v-if="isSubmitting" icon="solar:loader-circle-linear" width="20"
            class="animate-spin"></iconify-icon>
          {{ isSubmitting ? '注册中...' : '注 册' }}
        </button>
      </form>

      <p class="text-center text-sm text-slate-600">
        已有账号？
        <router-link to="/login" class="font-medium text-emerald-600 hover:text-emerald-500">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  studentId: '',
  name: '',
  phone: '',
  password: '',
  confirmPassword: '',
  agree: false
})

const showPassword = ref(false)
const isSubmitting = ref(false)

const colors = ['rgba(255, 255, 255, 0.6)', 'rgba(16, 185, 129, 0.15)', 'rgba(255, 255, 255, 0.8)', 'rgba(34, 197, 94, 0.12)', 'rgba(255, 255, 255, 0.5)']

const blobs = ref([])
let animationId = null
let containerWidth = 0
let containerHeight = 0

const initBlobs = () => {
  blobs.value = []
  for (let i = 0; i < 12; i++) {
    const baseSize = Math.random() * 120 + 60
    blobs.value.push({
      id: i,
      baseSize: baseSize,
      currentSize: baseSize,
      color: colors[Math.floor(Math.random() * colors.length)],
      x: Math.random() * containerWidth,
      y: Math.random() * containerHeight,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      opacity: Math.random() * 0.3 + 0.25,
      phase: Math.random() * Math.PI * 2,
      sizeSpeed: Math.random() * 0.02 + 0.01,
      wanderAngle: Math.random() * Math.PI * 2,
      wanderSpeed: Math.random() * 0.01 + 0.005
    })
  }
}

const updateBlobs = () => {
  blobs.value.forEach(blob => {
    blob.wanderAngle += blob.wanderSpeed

    const wanderForce = 0.03
    blob.vx += Math.sin(blob.wanderAngle) * wanderForce
    blob.vy += Math.cos(blob.wanderAngle) * wanderForce

    const maxSpeed = 1.2
    const speed = Math.sqrt(blob.vx * blob.vx + blob.vy * blob.vy)
    if (speed > maxSpeed) {
      blob.vx = (blob.vx / speed) * maxSpeed
      blob.vy = (blob.vy / speed) * maxSpeed
    }

    blob.x += blob.vx
    blob.y += blob.vy

    const margin = blob.baseSize / 2 + 20
    if (blob.x < margin) {
      blob.x = margin
      blob.vx *= -0.8
    }
    if (blob.x > containerWidth - margin) {
      blob.x = containerWidth - margin
      blob.vx *= -0.8
    }
    if (blob.y < margin) {
      blob.y = margin
      blob.vy *= -0.8
    }
    if (blob.y > containerHeight - margin) {
      blob.y = containerHeight - margin
      blob.vy *= -0.8
    }

    blob.phase += blob.sizeSpeed
    const sizeVariation = Math.sin(blob.phase) * 0.15
    blob.currentSize = blob.baseSize * (1 + sizeVariation)
  })

  animationId = requestAnimationFrame(updateBlobs)
}

const handleResize = () => {
  containerWidth = window.innerWidth
  containerHeight = window.innerHeight
  initBlobs()
}

const handleSubmit = async () => {
  if (!form.studentId || !form.name || !form.phone || !form.password || !form.confirmPassword) {
    alert('请填写完整信息')
    return
  }

  if (!form.agree) {
    alert('请先阅读并同意用户协议和隐私政策')
    return
  }

  if (form.password !== form.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  isSubmitting.value = true

  try {
    const result = await userStore.register({
      studentId: form.studentId,
      name: form.name,
      phone: form.phone,
      password: form.password
    })

    isSubmitting.value = false

    if (result.success) {
      const confirmed = window.confirm('注册成功！是否需要编辑个人信息？')
      if (confirmed) {
        router.push('/profile')
      } else {
        router.push('/')
      }
    }
  } catch {
    isSubmitting.value = false
  }
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  updateBlobs()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>