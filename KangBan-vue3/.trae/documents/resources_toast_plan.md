# Resources.vue Toast 提示功能实现计划

## 一、需求分析

用户要求为「急救知识宝典」和「常用药指南」两个卡片组件添加 Toast 提示功能：

* 点击急救知识卡片时显示相关提示信息

* 点击常用药指南卡片时显示相关提示信息

* Toast 样式需与应用主题保持一致

## 二、现有实现模式分析

通过分析项目中其他页面（Health.vue、Home.vue、Sports.vue 等）的 Toast 实现，总结出统一的实现模式：

### 模板结构（Toast 消息提示）

```html
<!-- Toast消息提示 -->
<Transition name="toast">
  <div v-if="showToast"
    class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-emerald-500 text-white px-6 py-3 rounded-full shadow-lg shadow-emerald-200 flex items-center gap-2 z-50">
    <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
    <span class="text-sm font-medium">{{ toastMessage }}</span>
  </div>
</Transition>
```

### 脚本实现

```javascript
const showToast = ref(false)
const toastMessage = ref('')

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2000)
}
```

## 三、修改方案

### 3.1 修改文件

**文件路径**: `d:\软件工程项目\KangBanLife\KangBan-vue3\src\views\Resources.vue`

### 3.2 修改内容

#### 1. 添加响应式变量（script 部分）

```javascript
const showToast = ref(false)
const toastMessage = ref('')
```

#### 2. 添加 Toast 显示函数（script 部分）

```javascript
const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2000)
}
```

#### 3. 添加点击事件处理函数（script 部分）

```javascript
const handleFirstAidClick = (resource) => {
  const messages = {
    'CPR 心肺复苏': 'CPR心肺复苏操作要点：检查意识→呼救→检查呼吸→胸外按压→人工呼吸',
    '海姆立克法': '海姆立克急救法：站在患者身后，双手环抱腹部，用力向上冲击',
    '烫伤处理': '烫伤处理五字诀：冲、脱、泡、盖、送',
    '中暑自救': '中暑急救：迅速转移至阴凉通风处，补充淡盐水',
    '外伤止血': '外伤止血：直接压迫止血法，抬高患肢，必要时使用止血带',
    '更多急救': '正在加载更多急救知识...'
  }
  showToastMessage(messages[resource.title] || '暂无详细信息')
}

const handleMedicineClick = (med) => {
  showToastMessage(`已为您推荐「${med.title}」相关药品，请在医生指导下使用`)
}
```

#### 4. 添加 Toast 模板（template 部分）

在 `</main>` 标签之前添加：

```html
<!-- Toast消息提示 -->
<Transition name="toast">
  <div v-if="showToast"
    class="fixed bottom-24 left-1/2 -translate-x-1/2 bg-emerald-500 text-white px-6 py-3 rounded-full shadow-lg shadow-emerald-200 flex items-center gap-2 z-50">
    <iconify-icon icon="solar:check-circle-bold" width="18"></iconify-icon>
    <span class="text-sm font-medium">{{ toastMessage }}</span>
  </div>
</Transition>
```

#### 5. 为卡片添加点击事件（template 部分）

* 急救知识卡片：添加 `@click="handleFirstAidClick(resource)"`

* 常用药指南卡片：添加 `@click="handleMedicineClick(med)"`

### 3.3 添加动画样式

在 `<style scoped>` 中添加：

```css
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}
```

## 四、注意事项

1. Toast 显示位置固定在底部居中，使用 `fixed bottom-24 left-1/2 -translate-x-1/2`
2. Toast 持续时间为 2000ms（2秒），与项目保持一致
3. 使用项目统一的绿色主题（emerald-500）
4. 确保点击事件与现有交互（hover 效果）不冲突
5. 为每个急救知识项目提供针对性的提示内容

## 五、测试要点

1. 点击每个急救知识卡片，验证 Toast 是否正确显示对应内容
2. 点击每个常用药指南卡片，验证 Toast 是否显示推荐提示
3. 验证 Toast 自动消失功能（2秒后）
4. 验证 Toast 显示动画效果
5. 验证在不同设备上的显示效果

