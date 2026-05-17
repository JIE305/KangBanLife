<template>
  <footer class="bg-slate-900 text-slate-300 py-16 relative">
    <Transition name="toast">
      <div v-if="showToast"
        class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-emerald-500 text-white px-6 py-3 rounded-full shadow-lg shadow-emerald-200 flex items-center gap-2 z-50">
        <iconify-icon icon="solar:clock-circle-bold" width="18"></iconify-icon>
        <span class="text-sm font-medium">{{ toastMessage }}</span>
      </div>
    </Transition>
    <div class="max-w-[1440px] mx-auto px-6">
      <div class="grid md:grid-cols-4 gap-12 mb-12">
        <div class="col-span-1 md:col-span-1">
          <div class="flex items-center gap-2 mb-6">
            <div class="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-white">
              <iconify-icon icon="solar:health-bold" width="18"></iconify-icon>
            </div>
            <span class="text-xl font-bold text-white tracking-tight">优校健康</span>
          </div>
          <p class="text-sm leading-relaxed mb-6">
            "康伴生活"是一个面向在校大学生的公益性、实用型健康服务平台。我们致力于通过技术手段，帮助学生在忙碌的校园生活中建立平衡的身心状态。
          </p>
          <div class="flex gap-4">
            <p
              class="cursor-pointer w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-emerald-500 transition-colors">
              <iconify-icon icon="ri:wechat-fill"></iconify-icon>
            </p>
            <p
              class="cursor-pointer w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-emerald-500 transition-colors">
              <iconify-icon icon="ri:weibo-fill"></iconify-icon>
            </p>
            <p
              class="cursor-pointer w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-emerald-500 transition-colors">
              <iconify-icon icon="ri:github-fill"></iconify-icon>
            </p>
          </div>
        </div>
        <div>
          <h4 class="text-white font-bold mb-6">核心服务</h4>
          <ul class="space-y-4 text-sm">
            <li><router-link class="hover:text-emerald-400 transition-colors" to="/health">日常健康打卡</router-link></li>
            <li><router-link class="hover:text-emerald-400 transition-colors" to="/mental">心理情绪调控</router-link></li>
            <li><router-link class="hover:text-emerald-400 transition-colors" to="/sports">校园定制训练</router-link></li>
            <li><router-link class="hover:text-emerald-400 transition-colors" to="/resources">医疗资源地图</router-link></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-bold mb-6">关于我们</h4>
          <ul class="space-y-4 text-sm">
            <li class="cursor-pointer" v-for="item in arrList" :key="item" @click="handleClick(item)">
              <p class="hover:text-emerald-400 transition-colors">{{ item }}</p>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-bold mb-6">订阅健康周报</h4>
          <p class="text-xs mb-4">每周一早晨，获取为你量身定制的校园生活建议。</p>
          <div class="flex gap-2">
            <input v-model="subscribeEmail"
              class="bg-slate-800 border-none rounded-lg px-4 py-2 text-sm flex-1 focus:ring-1 focus:ring-emerald-500"
              placeholder="输入邮箱" type="email" />
            <button
              class="bg-emerald-500 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-emerald-600 transition-colors"
              @click="clickSubscribe">订阅</button>
          </div>
        </div>
      </div>
      <div class="pt-8 border-t border-slate-800 text-center text-xs text-slate-500">
        © 2026 优校健康 UniHealth 公益项目. 当前时间: {{ currentDate }}. 版权所有.
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentDate = ref('')
const arrList = ref(['项目愿景', '志愿者招募', '开发者 API', '隐私政策声明'])
onMounted(() => {
  const now = new Date()
  currentDate.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
})

const showToast = ref(false)
const toastMessage = ref('')
const subscribeEmail = ref('')

const handleClick = (item) => {
  toastMessage.value = `${item}敬请期待~`
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 800)
}

const clickSubscribe = () => {
  const email = subscribeEmail.value.trim()
  console.log(email)
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!emailRegex.test(email)) {
    toastMessage.value = '请输入正确的邮箱格式'
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 800)
    return
  }
  toastMessage.value = '订阅成功！'
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 800)
}

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
