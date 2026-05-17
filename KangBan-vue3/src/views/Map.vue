<template>
  <div class="h-screen w-screen bg-slate-100" id="map-container">
    <!-- 顶部导航栏 -->
    <div class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm shadow-sm">
      <div class="max-w-full mx-auto px-4 h-14 flex items-center justify-between">
        <button @click="goBack" class="flex items-center gap-2 text-slate-600 hover:text-slate-800 transition-colors">
          <iconify-icon icon="solar:arrow-left-linear" width="20"></iconify-icon>
          <span class="text-sm font-medium">返回</span>
        </button>
        <h1 class="text-lg font-bold text-slate-800">医疗导航</h1>
        <div class="w-16"></div>
      </div>
    </div>

    <!-- 搜索框 -->
    <div class="fixed top-16 left-5 z-40">
      <div class="bg-white rounded-2xl shadow-lg p-3 flex items-center gap-4">
        <iconify-icon class="text-slate-400" icon="solar:magnifer-linear"></iconify-icon>
        <input v-model="searchKeyword" @keyup.enter="searchMedicalFacilities"
          class="flex-1 bg-transparent border-none outline-none text-sm" placeholder="搜索医疗设施（如：医院）" type="text" />
        <button @click="searchMedicalFacilities"
          class="px-4 py-2 bg-blue-500 text-white rounded-xl text-xs font-bold hover:bg-blue-600 transition-colors">
          搜索
        </button>
      </div>
    </div>

    <!-- 地图区域 -->
    <div ref="mapRef" class="w-full h-full pt-14"></div>

    <!-- 搜索结果列表 -->
    <Transition name="slide-up">
      <div v-if="showResults && medicalFacilities.length > 0"
        class="fixed bottom-0 left-0 right-0 z-40 bg-white rounded-t-3xl shadow-2xl max-h-[45vh] overflow-hidden">
        <div class="p-4 border-b border-slate-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h3 class="font-bold">
                {{ detectedType ? detectedType : '附近医疗设施' }}
              </h3>
              <span class="px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full text-xs font-medium">
                {{ medicalFacilities.length }}个
              </span>
            </div>
            <button @click="showResults = false" class="text-slate-400 hover:text-slate-600">
              <iconify-icon icon="carbon:close-outline" width="20"></iconify-icon>
            </button>
          </div>
          <div v-if="detectedType" class="mt-2 flex items-center gap-2">
            <span class="text-xs text-slate-500">已检测类型：</span>
            <span class="px-2 py-0.5 bg-blue-100 text-blue-600 rounded text-xs font-medium">
              {{ detectedType }}
            </span>
          </div>
        </div>
        <div class="overflow-y-auto max-h-[40vh] p-4 space-y-3">
          <div v-for="facility in medicalFacilities" :key="facility.id"
            class="p-4 bg-slate-50 rounded-xl cursor-pointer hover:bg-slate-100 transition-colors border border-transparent hover:border-blue-200"
            @click="selectFacility(facility)">
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <h4 class="font-bold text-sm">{{ facility.name }}</h4>
                  <span :class="getTypeBadgeClass(facility.type)"
                    class="px-1.5 py-0.5 rounded text-xs font-medium flex-shrink-0">
                    {{ facility.type }}
                  </span>
                </div>
                <p class="text-xs text-slate-500 mt-1 truncate">{{ facility.address }}</p>
                <div class="flex items-center gap-3 mt-2 flex-wrap">
                  <span v-if="facility.distance" class="text-xs text-blue-500 flex items-center gap-1">
                    <iconify-icon icon="solar:navigation-bold" width="14"></iconify-icon>
                    {{ facility.distance }}
                  </span>
                  <span v-if="facility.rating" class="text-xs text-orange-500 flex items-center gap-1">
                    <iconify-icon icon="solar:star-bold" width="14"></iconify-icon>
                    {{ facility.rating }}
                  </span>
                  <span v-if="facility.tel" class="text-xs text-green-500 flex items-center gap-1">
                    <iconify-icon icon="solar:phone-linear" width="14"></iconify-icon>
                    {{ facility.tel }}
                  </span>
                </div>
              </div>
              <button @click.stop="startNavigation(facility)"
                class="px-3 py-1.5 bg-blue-500 text-white rounded-lg text-xs font-bold hover:bg-blue-600 transition-colors flex items-center gap-1 flex-shrink-0 ml-3">
                导航
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 选中地点信息卡片 -->
    <Transition name="fade">
      <div v-if="selectedFacility" class="fixed inset-0 bg-black/30 flex items-center justify-center z-50"
        @click.self="selectedFacility = null">
        <div
          class="min-w-[280px] max-w-[400px] w-[90%] sm:w-[80%] md:w-[60%] lg:w-[45%] bg-white rounded-2xl shadow-xl p-5">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h4 class="font-bold text-base">{{ selectedFacility.name }}</h4>
              <p class="text-xs text-slate-500 mt-1.5 line-clamp-2">{{ selectedFacility.address }}</p>
              <div class="flex items-center gap-3 mt-2.5">
                <span v-if="selectedFacility.distance" class="text-xs text-blue-500 flex items-center gap-1">
                  <iconify-icon icon="solar:navigation-bold" width="14"></iconify-icon>
                  {{ selectedFacility.distance }}
                </span>
                <span v-if="selectedFacility.rating" class="text-xs text-orange-500 flex items-center gap-1">
                  <iconify-icon icon="solar:star-bold" width="14"></iconify-icon>
                  {{ selectedFacility.rating }}
                </span>
              </div>
            </div>
            <button @click="selectedFacility = null"
              class="text-slate-400 hover:text-slate-600 transition-colors ml-4 shrink-0">
              <iconify-icon icon="solar:cross-bold" width="20"></iconify-icon>
            </button>
          </div>
          <button @click="startNavigation(selectedFacility)"
            class="mt-4 w-full py-3 bg-blue-500 text-white rounded-xl font-bold hover:bg-blue-600 transition-colors flex items-center justify-center gap-2">
            <iconify-icon icon="solar:navigation-bold" width="18"></iconify-icon>
            开始导航
          </button>
        </div>
      </div>
    </Transition>

    <!-- 加载提示 -->
    <div v-if="isLoading" class="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-6 text-center">
        <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4">
        </div>
        <p class="text-slate-600">{{ loadingText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const mapRef = ref(null)
let map = null
let markers = []

const searchKeyword = ref('')
const medicalFacilities = ref([])
const showResults = ref(false)
const selectedFacility = ref(null)
const isLoading = ref(false)
const loadingText = ref('')
const navigationRoute = ref(null)
const detectedType = ref('')
const allMockData = ref([])

// 河南大学金明校区坐标（经纬度）
const campusLocation = {
  name: '河南大学金明校区',
  address: '河南省开封市龙亭区金明大道',
  lat: 34.8025,
  lng: 114.3458
}

const goBack = () => {
  window.history.back()
}

// 获取类型标签样式类
const getTypeBadgeClass = (type) => {
  const typeClassMap = {
    '三甲医院': 'bg-red-100 text-red-600',
    '二甲医院': 'bg-orange-100 text-orange-600',
    '医院': 'bg-red-100 text-red-600',
    '诊所': 'bg-green-100 text-green-600',
    '药店': 'bg-blue-100 text-blue-600',
    '药房': 'bg-blue-100 text-blue-600',
    '急救中心': 'bg-red-500 text-white',
    '卫生院': 'bg-teal-100 text-teal-600',
    '卫生所': 'bg-teal-100 text-teal-600',
    '体检中心': 'bg-purple-100 text-purple-600',
    '门诊': 'bg-yellow-100 text-yellow-600',
    '医务室': 'bg-cyan-100 text-cyan-600'
  }

  for (const [typeKey, className] of Object.entries(typeClassMap)) {
    if (type?.includes(typeKey)) {
      return className
    }
  }

  return 'bg-slate-100 text-slate-600'
}

// 初始化地图
const initMap = () => {
  if (!window.AMap) {
    setTimeout(initMap, 100)
    return
  }

  map = new window.AMap.Map(mapRef.value, {
    center: [campusLocation.lng, campusLocation.lat],
    zoom: 15,
    viewMode: '3D',
    pitch: 30,
    rotation: 0,
    features: ['bg', 'road', 'building', 'point']
  })

  // 添加地图控件（使用2.0版本兼容方式）
  try {
    if (window.AMap.Scale) {
      map.addControl(new window.AMap.Scale())
    }
  } catch (e) {
    console.log('Scale control not available')
  }

  try {
    if (window.AMap.Zoom) {
      map.addControl(new window.AMap.Zoom())
    }
  } catch (e) {
    console.log('Zoom control not available')
  }

  try {
    if (window.AMap.ToolBar) {
      map.addControl(new window.AMap.ToolBar({
        position: 'RB'
      }))
    }
  } catch (e) {
    console.log('ToolBar control not available')
  }

  // 添加起点标记（河南大学金明校区）
  addCampusMarker()

  // 自动搜索附近医疗设施
  searchMedicalFacilities()
}

// 添加校区标记
const addCampusMarker = () => {
  const marker = new window.AMap.Marker({
    position: [campusLocation.lng, campusLocation.lat],
    title: campusLocation.name,
    icon: new window.AMap.Icon({
      size: new window.AMap.Size(40, 40),
      image: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%2310b981"%3E%3Cpath d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/%3E%3C/svg%3E',
      imageSize: new window.AMap.Size(40, 40)
    }),
    offset: new window.AMap.Pixel(-20, -20)
  })

  map.add(marker)
  markers.push(marker)

  // 添加信息窗口
  const infoWindow = new window.AMap.InfoWindow({
    content: `<div style="padding: 10px;">
      <h4 style="margin: 0 0 5px 0; font-weight: bold;">${campusLocation.name}</h4>
      <p style="margin: 0; font-size: 12px; color: #666;">${campusLocation.address}</p>
      <p style="margin: 5px 0 0 0; font-size: 12px; color: #10b981;">📍 我的位置</p>
    </div>`,
    offset: new window.AMap.Pixel(0, -40)
  })

  marker.on('click', () => {
    infoWindow.open(map, marker.getPosition())
  })

  // 注释：不自动打开信息窗口，仅在用户点击标记时显示
  // infoWindow.open(map, marker.getPosition())
}

// 地点类型判断函数
const detectLocationType = (keyword) => {
  const lowerKeyword = keyword.toLowerCase().trim()

  const typePatterns = {
    '急救': ['急救', 'emergency', '急诊', '急救中心'],
    '体检': ['体检', 'health check', '体检中心'],
    '诊所': ['诊所', 'clinic', '医务室'],
    '门诊': ['门诊', 'outpatient', '门诊部'],
    '药店': ['药店', '药房', 'pharmacy', '药铺'],
    '卫生院': ['卫生院', 'health center', '卫生所', '卫生站'],
    '医院': ['医院', 'hospital', '医疗']
  }

  for (const [type, patterns] of Object.entries(typePatterns)) {
    for (const pattern of patterns) {
      if (lowerKeyword.includes(pattern)) {
        return type
      }
    }
  }

  return ''
}

// 根据类型过滤设施
const filterFacilitiesByType = (facilities, type) => {
  if (!type) return facilities

  const typeMap = {
    '医院': ['医院', '三甲医院', '二甲医院'],
    '诊所': ['诊所', '医务室', '门诊'],
    '药店': ['药店', '药房'],
    '体检': ['体检中心'],
    '急救': ['急救中心'],
    '卫生院': ['卫生院', '卫生所']
  }

  const targetTypes = typeMap[type] || []

  return facilities.filter(facility => {
    const facilityType = facility.type?.toLowerCase() || ''
    const facilityName = facility.name?.toLowerCase() || ''

    return targetTypes.some(target =>
      facilityType.includes(target.toLowerCase()) ||
      facilityName.includes(target.toLowerCase())
    )
  })
}

// 搜索附近医疗设施（包含类型判断）
const searchMedicalFacilities = async () => {
  isLoading.value = true
  loadingText.value = '正在搜索医疗设施...'

  try {
    // 判断搜索关键词类型
    detectedType.value = detectLocationType(searchKeyword.value)

    if (detectedType.value) {
      loadingText.value = `正在搜索${detectedType.value}...`
    }

    // 加载完整数据
    if (allMockData.value.length === 0) {
      loadMockData()
    }

    // 根据类型过滤数据
    if (detectedType.value) {
      const filtered = filterFacilitiesByType(allMockData.value, detectedType.value)
      medicalFacilities.value = filtered.length > 0 ? filtered : allMockData.value

      if (filtered.length === 0) {
        loadingText.value = `未找到${detectedType.value}，显示全部设施`
      } else {
        loadingText.value = `找到${filtered.length}个${detectedType.value}`
      }
    } else if (searchKeyword.value.trim()) {
      // 按名称模糊搜索
      const keyword = searchKeyword.value.toLowerCase()
      const filtered = allMockData.value.filter(facility =>
        facility.name.toLowerCase().includes(keyword) ||
        facility.address.toLowerCase().includes(keyword)
      )
      medicalFacilities.value = filtered.length > 0 ? filtered : allMockData.value
    } else {
      // 没有关键词，显示全部
      medicalFacilities.value = [...allMockData.value]
    }

    // 更新标记
    addMarkers()
    showResults.value = true
  } catch (error) {
    console.error('加载失败:', error)
    if (allMockData.value.length === 0) {
      loadMockData()
    }
    showResults.value = true
  } finally {
    isLoading.value = false
  }
}

// 尝试真实API搜索（可选功能）
const tryRealAPISearch = async () => {
  if (!window.Map) return

  const keywords = searchKeyword.value || '医院 诊所'

  try {
    const result = await new Promise((resolve, reject) => {
      if (window.Map.PlaceSearch) {
        executeSearch(resolve, reject, keywords)
      } else {
        window.Map.service('Map.PlaceSearch', () => {
          if (window.Map.PlaceSearch) {
            executeSearch(resolve, reject, keywords)
          } else {
            reject(new Error('PlaceSearch服务加载失败'))
          }
        })
      }
    })

    medicalFacilities.value = result.map(item => ({
      id: item.id || item.name,
      name: item.name,
      address: item.address || '地址不详',
      lat: item.location?.lat || item.lat,
      lng: item.location?.lng || item.lng,
      distance: item.distance ? `${(item.distance / 1000).toFixed(1)}km` : '未知',
      rating: item.rating || null,
      type: item.type || '医疗设施',
      tel: item.tel || null
    }))

    addMarkers()
  } catch (error) {
    console.warn('真实API搜索失败，继续使用模拟数据:', error)
  }
}

// 执行搜索
const executeSearch = (resolve, reject, keywords) => {
  try {
    const placeSearch = new window.AMap.PlaceSearch({
      pageSize: 20,
      pageIndex: 1,
      city: '开封',
      types: '医疗服务'
    })

    const timeout = setTimeout(() => {
      reject(new Error('搜索超时'))
    }, 10000)

    placeSearch.searchNearBy(keywords, new window.AMap.LngLat(campusLocation.lng, campusLocation.lat), 3000, (status, data) => {
      clearTimeout(timeout)
      if (status === 'complete') {
        if (data && data.poiList && data.poiList.pois && data.poiList.pois.length > 0) {
          resolve(data.poiList.pois)
        } else if (data && data.results && data.results.length > 0) {
          resolve(data.results)
        } else if (data && data.pois && data.pois.length > 0) {
          resolve(data.pois)
        } else {
          reject(new Error('未找到相关医疗设施'))
        }
      } else {
        reject(new Error(`搜索失败，状态码: ${status}`))
      }
    })
  } catch (e) {
    reject(e)
  }
}

// 获取标记图标颜色
const getMarkerColor = (type) => {
  const colorMap = {
    '三甲医院': '#ef4444',
    '二甲医院': '#f97316',
    '医院': '#ef4444',
    '诊所': '#22c55e',
    '药店': '#3b82f6',
    '药房': '#3b82f6',
    '急救中心': '#dc2626',
    '卫生院': '#14b8a6',
    '卫生所': '#14b8a6',
    '体检中心': '#a855f7',
    '门诊': '#eab308',
    '医务室': '#06b6d4'
  }

  for (const [typeKey, color] of Object.entries(colorMap)) {
    if (type?.includes(typeKey)) {
      return color
    }
  }

  return '#6366f1'
}

// 创建自定义标记SVG
const createCustomMarker = (color) => {
  const svg = `
    <svg width="32" height="40" viewBox="0 0 32 40">
      <path d="M16 0C7.163 0 0 7.163 0 16c0 5.938 3.75 10.986 9.25 13.375L16 40l6.75-10.625C28.25 26.986 32 21.938 32 16c0-8.837-7.163-16-16-16z" fill="${color}"/>
      <circle cx="16" cy="16" r="7" fill="white"/>
    </svg>`
  return svg
}

// 添加地图标记
const addMarkers = () => {
  // 清除之前的标记
  markers.forEach(marker => {
    map.remove(marker)
  })
  markers = []

  // 添加校区标记
  addCampusMarker()

  // 添加医疗设施标记（使用默认样式，简化处理）
  medicalFacilities.value.forEach(facility => {
    const marker = new window.AMap.Marker({
      position: [facility.lng, facility.lat],
      title: facility.name
    })

    marker.on('click', () => {
      selectFacility(facility)
    })

    map.add(marker)
    markers.push(marker)
  })
}

// 选择设施
const selectFacility = (facility) => {
  selectedFacility.value = facility

  // 移动地图到选中的设施
  map.panTo([facility.lng, facility.lat])
}

// 开始导航
const startNavigation = (facility) => {
  // 立即隐藏导航卡片，无论导航成功与否
  selectedFacility.value = null

  if (!facility || !facility.lng || !facility.lat) {
    alert('目标位置信息不完整，无法导航')
    return
  }

  isLoading.value = true
  loadingText.value = '正在规划导航路线...'

  // 验证坐标是否有效（中国坐标范围）
  const isValidCoord = (lng, lat) => {
    return lng >= 73 && lng <= 135 && lat >= 3 && lat <= 54
  }

  const startLng = campusLocation.lng
  const startLat = campusLocation.lat
  const endLng = facility.lng
  const endLat = facility.lat

  if (!isValidCoord(startLng, startLat) || !isValidCoord(endLng, endLat)) {
    console.error('坐标无效', { startLng, startLat, endLng, endLat })
    isLoading.value = false
    alert('坐标数据无效，请检查位置信息')
    return
  }

  setTimeout(() => {
    try {
      // 使用 Driving 路径规划
      window.AMap.plugin(['AMap.Driving'], () => {
        const driving = new window.AMap.Driving({
          map: map,
          panel: null,
          city: '开封',
          province: '河南',
          showCity: true,
          policy: window.AMap.DrivingPolicy.LEAST_TIME
        })

        driving.search(
          new window.AMap.LngLat(startLng, startLat),
          new window.AMap.LngLat(endLng, endLat),
          (status, result) => {
            console.log('导航状态:', status, result)
            isLoading.value = false

            if (status === 'complete' && result && result.routes && result.routes.length > 0) {
              showResults.value = false
              map.setFitView()
              alert(`导航路线已规划完成！\n从：${campusLocation.name}\n到：${facility.name}`)
            } else if (status === 'INVALID_USER_SCODE' || status === 'error') {
              showMockNavigation(facility)
            } else if (status === 'no_data' || (result && result.routes && result.routes.length === 0)) {
              showMockNavigation(facility)
            } else {
              showMockNavigation(facility)
            }
          }
        )
      })
    } catch (error) {
      console.error('导航创建失败:', error)
      isLoading.value = false
      showMockNavigation(facility)
    }
  }, 300)
}

const showMockNavigation = (facility) => {
  const startName = campusLocation.name
  const endName = facility.name
  const distance = facility.distance || '未知'

  try {
    // 清除之前的导航路径
    clearNavigationRoutes()

    // 创建新的导航路线
    const routeLine = new window.AMap.Polyline({
      path: [
        new window.AMap.LngLat(campusLocation.lng, campusLocation.lat),
        new window.AMap.LngLat(facility.lng, facility.lat)
      ],
      strokeColor: '#3b82f6',
      strokeWeight: 4,
      strokeOpacity: 0.8,
      strokeStyle: 'solid'
    })

    // 保存路线引用以便后续清除
    navigationRoute.value = routeLine
    map.add(routeLine)
    map.setFitView()
    showResults.value = false
  } catch (e) {
    console.error('添加路线失败:', e)
  }

  alert(`导航提示：\n\n起点：${startName}\n终点：${endName}\n距离：${distance}\n\n请使用手机地图APP进行导航`)
}

// 清除所有导航路径
const clearNavigationRoutes = () => {
  // 清除模拟导航路线
  if (navigationRoute.value) {
    try {
      map.remove(navigationRoute.value)
      navigationRoute.value = null
    } catch (e) {
      console.error('清除路线失败:', e)
    }
  }

  // 清除所有 Polyline 图层（兼容不同API版本）
  try {
    // 高德地图 2.x 版本
    if (typeof map.getOverlays === 'function') {
      const overlays = map.getOverlays()
      overlays.forEach(overlay => {
        if (overlay instanceof window.AMap.Polyline) {
          map.remove(overlay)
        }
      })
    } else if (typeof map.getAllOverlays === 'function') {
      // 高德地图 1.x 版本
      const overlays = map.getAllOverlays('polyline')
      overlays.forEach(overlay => {
        map.remove(overlay)
      })
    } else {
      console.log('无法获取图层列表，跳过批量清除')
    }
  } catch (e) {
    console.warn('清除图层时发生错误（非关键）:', e.message)
  }
}

// 定位到校区
const locateToCampus = () => {
  map.panTo([campusLocation.lng, campusLocation.lat])
  map.setZoom(15)
}

// 加载模拟数据（当API不可用时）
const loadMockData = () => {
  allMockData.value = [
    {
      id: '1',
      name: '开封市中心医院',
      address: '河南省开封市鼓楼区自由路西段168号',
      lat: 34.7908,
      lng: 114.3580,
      distance: '1.2km',
      rating: '4.5',
      type: '三甲医院',
      tel: '0371-12345678'
    },
    {
      id: '2',
      name: '河南大学第一附属医院',
      address: '河南省开封市龙亭区西门大街357号',
      lat: 34.8056,
      lng: 114.3280,
      distance: '1.8km',
      rating: '4.3',
      type: '三甲医院',
      tel: '0371-23456789'
    },
    {
      id: '3',
      name: '仁和诊所',
      address: '河南省开封市龙亭区金明大道与汉兴路交叉口',
      lat: 34.8000,
      lng: 114.3550,
      distance: '0.5km',
      rating: '4.0',
      type: '诊所',
      tel: '0371-34567890'
    },
    {
      id: '4',
      name: '康泰药店',
      address: '河南省开封市龙亭区黄河大街北段',
      lat: 34.8100,
      lng: 114.3350,
      distance: '1.0km',
      rating: '4.2',
      type: '药店',
      tel: '0371-45678901'
    },
    {
      id: '5',
      name: '开封市第二人民医院',
      address: '河南省开封市顺河回族区汴京大道东段',
      lat: 34.8200,
      lng: 114.3700,
      distance: '2.5km',
      rating: '4.4',
      type: '二甲医院',
      tel: '0371-56789012'
    },
    {
      id: '6',
      name: '开封市急救中心',
      address: '河南省开封市鼓楼区中山路中段',
      lat: 34.7950,
      lng: 114.3600,
      distance: '1.5km',
      rating: '4.8',
      type: '急救中心',
      tel: '120'
    },
    {
      id: '7',
      name: '社区卫生服务站',
      address: '河南省开封市龙亭区东京大道',
      lat: 34.8080,
      lng: 114.3400,
      distance: '0.8km',
      rating: '4.1',
      type: '卫生院',
      tel: '0371-67890123'
    },
    {
      id: '8',
      name: '体检中心',
      address: '河南省开封市龙亭区金明大道',
      lat: 34.8020,
      lng: 114.3480,
      distance: '0.6km',
      rating: '4.6',
      type: '体检中心',
      tel: '0371-78901234'
    }
  ]

  medicalFacilities.value = [...allMockData.value]
  addMarkers()
  showResults.value = true
}

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.destroy()
  }
})
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>