<template>
  <nav class="sticky top-0 z-50 backdrop-blur-md shadow-sm" :class="navBgClass">
    <div class="max-w-[1440px] mx-auto px-6 h-16 grid grid-cols-[1fr_auto_1fr] items-center">
      <div class="flex items-center gap-2">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white shadow-lg" :class="logoBgClass">
          <iconify-icon :icon="logoIcon" width="24"></iconify-icon>
        </div>
        <span class="text-xl font-bold tracking-tight" :class="logoTextClass">康伴生活
          <span class="text-xs font-normal text-slate-400 ml-1">LifePartner</span>
        </span>
      </div>
      <div class="hidden md:flex items-center gap-8">
        <router-link v-for="item in navItems" :key="item.path" :to="item.path" class="font-medium transition-all"
          :class="$route.path === item.path ? activeTextClass : 'text-slate-600'">
          {{ item.name }}
        </router-link>
      </div>
      <div class="flex items-center gap-4 justify-end">
        <template v-if="showLogin">
          <router-link v-show="userStatus === 'guest'" to="/login"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium shadow-lg transition-all"
            :class="[btnBgClass, 'text-white']">
            <span class="w-2 h-2 bg-white/80 rounded-full animate-pulse"></span>
            游客模式
          </router-link>
          <router-link v-show="userStatus === 'loggedIn'" to="/profile"
            class="flex items-center gap-2 px-1 py-1 rounded-full text-sm font-medium transition-all"
            title="个人中心">
            <div class="w-9 h-9 rounded-full overflow-hidden border-2 shadow-sm" :class="avatarBorderClass">
              <img v-if="userAvatar" :src="userAvatar" class="w-full h-full object-cover" alt="头像" />
              <iconify-icon v-else icon="solar:user-circle-bold" width="28" class="text-slate-400"></iconify-icon>
            </div>
          </router-link>
        </template>
        <router-link v-if="showNotification && userStatus === 'guest'" to="/profile"
          class="p-2 text-slate-500 hover:bg-slate-100 hover:text-emerald-500 rounded-full transition-colors">
          <iconify-icon icon="solar:user-circle-linear" width="24"></iconify-icon>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  theme: {
    type: String,
    default: 'emerald',
    validator: (value) => ['emerald', 'blue', 'orange', 'purple'].includes(value)
  },
  logoIcon: {
    type: String,
    default: 'solar:health-bold'
  },
  rightText: {
    type: String,
    default: ''
  },
  rightIcon: {
    type: String,
    default: ''
  },
  showLogin: {
    type: Boolean,
    default: true
  },
  showNotification: {
    type: Boolean,
    default: true
  },
  isLoggedIn: {
    type: Boolean,
    default: false
  },
  userName: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['logout'])

/**
 * 用户状态管理 - 基于 localStorage
 * 
 * 存储键说明：
 * - userStatus: 'guest' 表示游客状态，'loggedIn' 表示已登录状态
 * - unihealth_token: 用户认证令牌（用于验证登录有效性）
 * - unihealth_user: 用户信息JSON字符串
 * 
 * 状态判断优先级：
 * 1. 优先检查 localStorage 中的 userStatus
 * 2. 其次验证 token 是否存在（确保登录状态有效）
 * 3. 最后检查 sessionStorage 作为备选
 */

// 存储键名常量
const STORAGE_KEYS = {
  USER_STATUS: 'userStatus',
  TOKEN: 'unihealth_token',
  USER: 'unihealth_user',
  SESSION_LOGGED_IN: 'isLoggedIn'
}

// 状态值常量
const STATUS_VALUES = {
  GUEST: 'guest',
  LOGGED_IN: 'loggedIn'
}

// 响应式用户状态
const userStatus = ref(STATUS_VALUES.GUEST)
const userAvatar = ref('')

// 从 localStorage 读取用户头像
const loadUserAvatar = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEYS.USER)
    if (saved) {
      const u = JSON.parse(saved)
      userAvatar.value = u.avatar_url || ''
    }
  } catch {
    userAvatar.value = ''
  }
}

/**
 * 检查浏览器是否支持 localStorage
 * @returns {boolean} 是否支持
 */
const isLocalStorageSupported = () => {
  try {
    const key = '__storage_test__'
    localStorage.setItem(key, key)
    localStorage.removeItem(key)
    return true
  } catch (e) {
    console.warn('浏览器不支持 localStorage，将使用内存存储')
    return false
  }
}

/**
 * 安全地从 localStorage 获取值
 * @param {string} key - 存储键名
 * @param {any} defaultValue - 默认值
 * @returns {any} 获取的值或默认值
 */
const safeGetItem = (key, defaultValue = null) => {
  if (!isLocalStorageSupported()) {
    return defaultValue
  }

  try {
    const value = localStorage.getItem(key)
    return value !== null ? value : defaultValue
  } catch (e) {
    console.error(`从 localStorage 获取 ${key} 失败:`, e)
    return defaultValue
  }
}

/**
 * 安全地向 localStorage 设置值
 * @param {string} key - 存储键名
 * @param {any} value - 要存储的值
 * @returns {boolean} 是否成功
 */
const safeSetItem = (key, value) => {
  if (!isLocalStorageSupported()) {
    return false
  }

  try {
    localStorage.setItem(key, value)
    return true
  } catch (e) {
    console.error(`向 localStorage 设置 ${key} 失败:`, e)
    return false
  }
}

/**
 * 验证登录状态是否有效
 * 检查 token 和 user 数据是否同时存在
 * @returns {boolean} 是否有效登录
 */
const isLoginValid = () => {
  const token = safeGetItem(STORAGE_KEYS.TOKEN)
  const user = safeGetItem(STORAGE_KEYS.USER)

  if (!token || !user) {
    return false
  }

  try {
    const parsedUser = JSON.parse(user)
    return parsedUser && typeof parsedUser === 'object' && parsedUser.id
  } catch (e) {
    console.error('用户信息格式无效:', e)
    return false
  }
}

/**
 * 判断用户当前登录状态
 * 综合检查 localStorage、sessionStorage 和 token 有效性
 * @returns {string} 'guest' 或 'loggedIn'
 */
const determineUserStatus = () => {
  try {
    const storedStatus = safeGetItem(STORAGE_KEYS.USER_STATUS)

    if (storedStatus === STATUS_VALUES.LOGGED_IN) {
      if (isLoginValid()) {
        return STATUS_VALUES.LOGGED_IN
      } else {
        clearLoginState()
        return STATUS_VALUES.GUEST
      }
    }

    if (storedStatus === STATUS_VALUES.GUEST) {
      return STATUS_VALUES.GUEST
    }

    const sessionLoggedIn = safeGetItem(STORAGE_KEYS.SESSION_LOGGED_IN)
    if (sessionLoggedIn === 'true' && isLoginValid()) {
      safeSetItem(STORAGE_KEYS.USER_STATUS, STATUS_VALUES.LOGGED_IN)
      return STATUS_VALUES.LOGGED_IN
    }

    if (isLoginValid()) {
      safeSetItem(STORAGE_KEYS.USER_STATUS, STATUS_VALUES.LOGGED_IN)
      return STATUS_VALUES.LOGGED_IN
    }

    return STATUS_VALUES.GUEST

  } catch (e) {
    console.error('判断用户状态时发生错误:', e)
    return STATUS_VALUES.GUEST
  }
}

/**
 * 清除登录状态（登出时调用）
 */
const clearLoginState = () => {
  safeSetItem(STORAGE_KEYS.USER_STATUS, STATUS_VALUES.GUEST)
}

/**
 * 更新用户登录状态
 * @param {boolean} isLoggedIn - 是否登录
 */
const updateUserStatus = (isLoggedIn) => {
  const newStatus = isLoggedIn ? STATUS_VALUES.LOGGED_IN : STATUS_VALUES.GUEST

  if (newStatus !== userStatus.value) {
    userStatus.value = newStatus
    safeSetItem(STORAGE_KEYS.USER_STATUS, newStatus)
  }
}

/**
 * 初始化用户状态
 */
const initUserStatus = () => {
  const status = determineUserStatus()
  userStatus.value = status

  if (status === STATUS_VALUES.GUEST) {
    safeSetItem(STORAGE_KEYS.USER_STATUS, STATUS_VALUES.GUEST)
  }
}

// 组件挂载时初始化用户状态
onMounted(() => {
  initUserStatus()
  loadUserAvatar()

  if (typeof window !== 'undefined') {
    window.addEventListener('storage', handleStorageChange)
    window.addEventListener('user-avatar-updated', loadUserAvatar)
  }
})

// 组件卸载时移除监听
onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('storage', handleStorageChange)
    window.removeEventListener('user-avatar-updated', loadUserAvatar)
  }
})

// 监听 props.isLoggedIn 变化并同步到 localStorage
watch(() => props.isLoggedIn, (newVal) => {
  updateUserStatus(newVal)
}, { immediate: true })

// 处理跨标签页的 storage 变化
const handleStorageChange = (event) => {
  if (event.key === STORAGE_KEYS.USER_STATUS) {
    const newStatus = event.newValue || STATUS_VALUES.GUEST

    if (newStatus === STATUS_VALUES.LOGGED_IN) {
      if (isLoginValid()) {
        userStatus.value = newStatus
      } else {
        clearLoginState()
        userStatus.value = STATUS_VALUES.GUEST
      }
    } else {
      userStatus.value = newStatus
    }
  }
  if (event.key === STORAGE_KEYS.USER) {
    loadUserAvatar()
  }
}

// 监听 userStatus 变化，同步到 localStorage
watch(userStatus, (newStatus) => {
  safeSetItem(STORAGE_KEYS.USER_STATUS, newStatus)
})

const navItems = ref([
  { path: '/', name: '首页' },
  { path: '/health', name: '日常管理' },
  { path: '/mental', name: '身心调适' },
  { path: '/sports', name: '运动规划' },
  { path: '/resources', name: '资源查询' }
])

const currentDate = computed(() => {
  const date = new Date()
  return `${date.getMonth() + 1}月${date.getDate()}日`
})

const navBgClass = computed(() => {
  return props.theme === 'blue' ? 'bg-white/80' : 'bg-white'
})

const logoBgClass = computed(() => {
  const classes = {
    emerald: 'bg-emerald-500 shadow-emerald-200',
    blue: 'bg-blue-500 shadow-blue-200',
    orange: 'bg-orange-500 shadow-orange-200',
    purple: 'bg-purple-500 shadow-purple-200'
  }
  return classes[props.theme] || classes.emerald
})

const logoTextClass = computed(() => {
  const classes = {
    emerald: 'text-emerald-600',
    blue: 'text-blue-600',
    orange: 'text-orange-600',
    purple: 'text-purple-600'
  }
  return classes[props.theme] || classes.emerald
})

const activeTextClass = computed(() => {
  const classes = {
    emerald: 'text-emerald-600 hover:text-emerald-600',
    blue: 'text-blue-600 hover:text-blue-600',
    orange: 'text-orange-600 hover:text-orange-600',
    purple: 'text-purple-600 hover:text-purple-600'
  }
  return classes[props.theme] || classes.emerald
})

const themeColorClass = computed(() => {
  const classes = {
    emerald: 'text-emerald-500',
    blue: 'text-blue-500',
    orange: 'text-orange-500',
    purple: 'text-purple-500'
  }
  return classes[props.theme] || classes.emerald
})

const statusBadgeClass = computed(() => {
  const classes = {
    emerald: 'bg-emerald-100 text-emerald-700',
    blue: 'bg-blue-100 text-blue-700',
    orange: 'bg-orange-100 text-orange-700',
    purple: 'bg-purple-100 text-purple-700'
  }
  return classes[props.theme] || classes.emerald
})

const avatarBorderClass = computed(() => {
  const classes = {
    emerald: 'border-emerald-500',
    blue: 'border-blue-500',
    orange: 'border-orange-500',
    purple: 'border-purple-500'
  }
  return classes[props.theme] || 'border-emerald-500'
})

const btnBgClass = computed(() => {
  const classes = {
    emerald: 'bg-emerald-500 shadow-emerald-200 hover:bg-emerald-400',
    blue: 'bg-blue-500 shadow-blue-200 hover:bg-blue-400',
    orange: 'bg-orange-500 shadow-orange-200 hover:bg-orange-400',
    purple: 'bg-purple-500 shadow-purple-200 hover:bg-purple-400'
  }
  return classes[props.theme] || classes.emerald
})

const handleLogout = () => {
  emit('logout')
}
</script>
