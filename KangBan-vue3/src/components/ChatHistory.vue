<template>
  <div class="absolute top-full right-0 mt-1 w-56 bg-white rounded-xl shadow-xl border border-slate-200 z-50 overflow-hidden">
    <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
      <span class="text-sm font-bold text-slate-700">历史对话</span>
      <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600">
        <iconify-icon icon="solar:close-circle-bold" width="18"></iconify-icon>
      </button>
    </div>
    <div class="max-h-56 overflow-y-auto">
      <div v-if="loading" class="px-4 py-6 text-center text-xs text-slate-400">加载中...</div>
      <div v-else-if="sessions.length === 0" class="px-4 py-6 text-center text-xs text-slate-400">暂无历史对话</div>
      <div
        v-for="s in sessions" :key="s.id"
        @click="$emit('select', s.id)"
        class="px-4 py-3 hover:bg-slate-50 cursor-pointer border-b border-slate-50 last:border-0 transition-colors"
      >
        <div class="text-xs font-medium text-slate-500">{{ formatDate(s.date) }}</div>
        <div class="text-sm text-slate-700 truncate mt-0.5">{{ s.preview }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  sessions: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})

defineEmits(['select', 'close'])

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  // SQLite datetime format: "2026-05-12 20:15:00"
  const parts = dateStr.split(' ')[0].split('-')
  if (parts.length === 3) return `${parts[1]}月${parts[2]}日`
  return dateStr
}
</script>
