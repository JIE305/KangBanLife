import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentDate = ref('')

  const navItems = ref([
    { path: '/', name: '首页' },
    { path: '/health', name: '日常管理' },
    { path: '/mental', name: '身心调适' },
    { path: '/sports', name: '运动规划' },
    { path: '/resources', name: '资源查询' }
  ])

  const features = ref([
    {
      path: '/health',
      bgClass: 'bg-emerald-50',
      icon: 'solar:heart-pulse-bold',
      iconClass: 'text-emerald-500',
      iconHoverClass: 'group-hover:bg-emerald-500 group-hover:text-white',
      title: '日常健康',
      desc: '饮食追踪、睡眠管理、饮水提醒。拒绝期末周熬夜综合症。',
      action: '记录',
      textClass: 'text-emerald-600'
    },
    {
      path: '/mental',
      bgClass: 'bg-blue-50',
      icon: 'ph:text-h-fill',
      iconClass: 'text-blue-500',
      iconHoverClass: 'group-hover:bg-blue-500 group-hover:text-white',
      title: '身心调适',
      desc: '冥想白噪音。给在绩点和实习压力下的你一个出口。',
      action: '放松',
      textClass: 'text-blue-600'
    },
    {
      path: '/sports',
      bgClass: 'bg-orange-50',
      icon: 'solar:running-bold',
      iconClass: 'text-orange-500',
      iconHoverClass: 'group-hover:bg-orange-500 group-hover:text-white',
      title: '运动规划',
      desc: '宿舍5分钟健身、操场路线推荐。让体测不再是噩梦。',
      action: '运动',
      textClass: 'text-orange-600'
    },
    {
      path: '/resources',
      bgClass: 'bg-purple-50',
      icon: 'solar:medical-kit-bold',
      iconClass: 'text-purple-500',
      iconHoverClass: 'group-hover:bg-purple-500 group-hover:text-white',
      title: '资源查询',
      desc: '急救指南、校医室排班、周边药店。突发状况不再手忙脚乱。',
      action: '查询',
      textClass: 'text-purple-600'
    }
  ])

  const articles = ref([
    {
      id: 1,
      alt: 'College students eating healthy',
      img: 'https://modao.cc/agent-py/media/generated_images/2026-03-26/f3b0e445267d4e72a162aefd48896059.jpg',
      tag: '饮食指导',
      tagClass: 'bg-emerald-100 text-emerald-600',
      date: '2026-03-25',
      title: '食堂“减脂餐”点菜攻略：如何避开高油雷区？',
      excerpt: '校内食堂其实隐藏着很多健康组合，本期我们实地走访了第一食堂和第二食堂...',
      views: '1.2k+'
    },
    {
      id: 2,
      alt: 'Student exercising in dorm',
      img: 'https://modao.cc/agent-py/media/generated_images/2026-03-26/f2eaa8c06367411ebc4f98cae483627e.jpg',
      tag: '运动健身',
      tagClass: 'bg-orange-100 text-orange-600',
      date: '2026-03-24',
      title: '宿舍党福音：一张瑜伽垫，搞定全身塑形',
      excerpt: '不需要昂贵的私教课和复杂的健身房设备，在宿舍也能轻松锻炼出的马甲线...',
      views: '890+'
    },
    {
      id: 3,
      alt: 'Stress relief meditation',
      img: 'https://modao.cc/agent-py/media/generated_images/2026-03-26/ca1285ba30014ddd88fa56b0d7135e9e.jpg',
      tag: '心理调适',
      tagClass: 'bg-blue-100 text-blue-600',
      date: '2026-03-22',
      title: '拒绝容貌焦虑：如何在这场"美丽竞争"中找回自我？',
      excerpt: '当你开始在社交软件里因为别人的精修图而感到自卑时，你应该看看这篇专栏...',
      views: '2.5k+'
    }
  ])

  // const stats = ref([
  //   { value: '12,450', label: '今日校园总步数 (km)' },
  //   { value: '3,280', label: '已完成心情打卡人数' },
  //   { value: '560', label: '在线提供咨询的心理导师' },
  //   { value: '98%', label: '服务好评率 (匿名反馈)' }
  // ])

  const mealOptions = ref({
    '早餐': [
      {
        id: 1,
        icon: 'mdi:food-variant',
        iconColor: 'text-emerald-500',
        tag: '均衡选择',
        tagClass: 'bg-emerald-100 text-emerald-600',
        title: '元气满分早餐',
        desc: '全麦包 + 煮鸡蛋 + 无糖豆浆/牛奶 + 一小份当季水果。',
        calories: 350,
        protein: 20
      },
      {
        id: 2,
        icon: 'mdi:food-apple',
        iconColor: 'text-blue-500',
        tag: '低卡选择',
        tagClass: 'bg-blue-100 text-blue-600',
        title: '清爽粗粮早餐',
        desc: '燕麦粥/玉米/紫薯 + 凉拌海带丝/凉拌青菜 + 蛋白2个。',
        calories: 280,
        protein: 15
      }
    ],
    '午餐': [
      {
        id: 3,
        icon: 'mdi:silverware-fork-knife',
        iconColor: 'text-orange-500',
        tag: '营养推荐',
        tagClass: 'bg-orange-100 text-orange-600',
        title: '经典均衡套餐',
        desc: '杂粮饭 + 瘦肉蛋白 + 两种蔬菜 + 清淡汤品。少油少盐更健康。',
        calories: 550,
        protein: 28
      },
      {
        id: 4,
        icon: 'mdi:salad',
        iconColor: 'text-green-500',
        tag: '减脂选择',
        tagClass: 'bg-green-100 text-green-600',
        title: '轻食沙拉碗',
        desc: '混合生菜基底 + 鸡胸肉/虾仁 + 牛油果 + 坚果碎 + 油醋汁。',
        calories: 420,
        protein: 25
      }
    ],
    '晚餐': [
      {
        id: 5,
        icon: 'mdi:bowl',
        iconColor: 'text-purple-500',
        tag: '养胃推荐',
        tagClass: 'bg-purple-100 text-purple-600',
        title: '温润杂粮粥',
        desc: '小米粥/南瓜粥 + 清蒸鱼/豆腐 + 凉拌小菜。易消化不负担。',
        calories: 380,
        protein: 18
      },
      {
        id: 6,
        icon: 'mdi:soup',
        iconColor: 'text-emerald-500',
        tag: '清淡选择',
        tagClass: 'bg-emerald-100 text-emerald-600',
        title: '蔬菜豆腐汤',
        desc: '各种时令蔬菜 + 嫩豆腐 + 菌菇 + 少许瘦肉。汤清味鲜。',
        calories: 280,
        protein: 15
      }
    ]
  })

  const formattedDate = computed(() => {
    return currentDate.value
  })

  const setCurrentDate = () => {
    const now = new Date()
    const weekdays = ['日', '一', '二', '三', '四', '五', '六']
    currentDate.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 · 周${weekdays[now.getDay()]}`
  }

  const getMealsByType = (mealType) => {
    return mealOptions.value[mealType] || []
  }

  const addArticle = (article) => {
    articles.value.unshift({
      id: Date.now(),
      ...article,
      date: new Date().toISOString().split('T')[0],
      views: '0'
    })
  }

  return {
    currentDate,
    navItems,
    features,
    articles,
    stats,
    mealOptions,
    formattedDate,
    setCurrentDate,
    getMealsByType,
    addArticle
  }
})