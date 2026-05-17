<template>
  <div class="min-h-screen bg-slate-50">
    <Navbar />
    
    <main class="max-w-3xl mx-auto px-6 py-12">
      <!-- 文章头部 -->
      <article class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
        <!-- 文章封面图 -->
        <img :src="article.img" :alt="article.alt" class="w-full h-64 object-cover" />
        
        <div class="p-8">
          <!-- 标签和日期 -->
          <div class="flex items-center gap-4 mb-4">
            <span class="px-3 py-1 text-sm font-bold rounded-full" :class="article.tagClass">{{ article.tag }}</span>
            <span class="text-slate-400 text-sm">{{ article.date }}</span>
            <span class="text-slate-400 text-sm">阅读 {{ article.views }}</span>
          </div>
          
          <!-- 文章标题 -->
          <h1 class="text-3xl font-bold text-slate-800 mb-6">{{ article.title }}</h1>
          
          <!-- 文章内容区域 -->
          <div class="prose prose-emerald max-w-none">
            <!-- ============ 文章正文内容（请在此处输入文章内容）============ -->
            <p class="text-slate-600 leading-relaxed mb-6">
              <!-- 在这里输入文章内容 -->
            </p>
            
            <h2 class="text-2xl font-bold text-slate-800 mt-8 mb-4">二级标题</h2>
            <p class="text-slate-600 leading-relaxed mb-6">
              <!-- 在这里输入文章内容 -->
            </p>
            
            <h3 class="text-xl font-bold text-slate-800 mt-6 mb-3">三级标题</h3>
            <p class="text-slate-600 leading-relaxed mb-6">
              <!-- 在这里输入文章内容 -->
            </p>
            
            <ul class="list-disc list-inside text-slate-600 mb-6 space-y-2">
              <!-- 列表项示例 -->
              <li>列表项一</li>
              <li>列表项二</li>
              <li>列表项三</li>
            </ul>
            
            <blockquote class="border-l-4 border-emerald-500 pl-4 italic text-slate-500 my-6">
              <!-- 引用内容 -->
            </blockquote>
            
            <p class="text-slate-600 leading-relaxed mb-6">
              <!-- 在这里输入文章内容 -->
            </p>
            <!-- ============ 文章正文内容结束 ============= -->
          </div>
        </div>
      </article>
      
      <!-- 加载失败提示 -->
      <div v-if="articleError && !article.id" class="text-center py-12 text-slate-400">
        <p class="text-lg">数据加载失败 :(</p>
      </div>

      <!-- 返回首页按钮 -->
      <div class="mt-8 flex justify-center">
        <router-link to="/" 
          class="inline-flex items-center gap-2 px-6 py-3 bg-emerald-500 text-white rounded-full font-medium shadow-lg shadow-emerald-200 hover:bg-emerald-400 transition-all">
          <iconify-icon icon="solar:arrow-left-linear" width="20"></iconify-icon>
          返回首页
        </router-link>
      </div>
    </main>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { getArticleDetailAPI } from '@/api/articles'

const article = ref({
  id: 0,
  alt: '',
  img: '',
  tag: '',
  tagClass: '',
  date: '',
  title: '',
  views: 0
})
const articleError = ref(false)

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search)
  const articleId = parseInt(urlParams.get('id')) || 1

  try {
    const res = await getArticleDetailAPI(articleId)
    const data = res.data.article
    if (data) {
      article.value = {
        id: data.id,
        alt: data.alt || '',
        img: data.img || '',
        tag: data.tag || '',
        tagClass: data.tagClass || '',
        date: data.date || '',
        title: data.title || '',
        views: data.views || 0
      }
    }
  } catch {
    articleError.value = true
  }
})
</script>