# Sports.vue 交互效果增强方案

## 一、代码结构分析

### 当前页面结构
| 区域 | 行号 | 内容 |
|------|------|------|
| Navbar | L3-4 | 橙色主题导航栏，步数显示 |
| 运动概览卡片 | L8-32 | 渐变卡片 + 统计面板 + 操作按钮 |
| 宿舍场景推荐 | L37-71 | 分类 Tab + 课程卡片 grid |
| 校园运动地图 | L73-88 | 静态地图 + 路线信息浮层 |
| 运动勋章 | L92-107 | 勋章 grid（达成/未达成状态） |
| 约球广场 | L108-132 | 约球卡片列表 + 发布按钮 |

### 项目现有交互模式（对齐参考）
- **Transition 组件**：`toast`、`modal`、`slide-up`、`fade` 四种命名过渡
- **悬停效果**：`transition-shadow`、`transition-colors`、`transition-all`、`group-hover:*`
- **动画类**：`animate-pulse`、`animate-spin`、`animate-bounce`（Tailwind 内建）+ `animate-blob` + `animation-delay-2000`（自定义）
- **全局样式**：`.glass-card`（毛玻璃）、`.feature-card:hover`（上浮 8px）、`.nav-link:hover`（上浮 2px）

---

## 二、具体实施方案

### 步骤 1：扩展 Tailwind 动画配置
**文件**：`tailwind.config.js`
**操作**：在 `theme.extend` 中添加自定义动画和过渡定义

```js
theme: {
  extend: {
    animation: {
      'blob': 'blob 7s infinite',
      'float': 'float 3s ease-in-out infinite',
      'fade-in-up': 'fadeInUp 0.5s ease-out',
      'fade-in': 'fadeIn 0.5s ease-out',
      'scale-in': 'scaleIn 0.3s ease-out',
    },
    keyframes: {
      blob: {
        '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
        '25%': { transform: 'translate(20px, -15px) scale(1.1)' },
        '50%': { transform: 'translate(0, 10px) scale(0.9)' },
        '75%': { transform: 'translate(-20px, -15px) scale(1.1)' },
      },
      float: {
        '0%, 100%': { transform: 'translateY(0)' },
        '50%': { transform: 'translateY(-10px)' },
      },
      fadeInUp: {
        '0%': { opacity: '0', transform: 'translateY(20px)' },
        '100%': { opacity: '1', transform: 'translateY(0)' },
      },
      fadeIn: {
        '0%': { opacity: '0' },
        '100%': { opacity: '1' },
      },
      scaleIn: {
        '0%': { opacity: '0', transform: 'scale(0.9)' },
        '100%': { opacity: '1', transform: 'scale(1)' },
      },
    }
  }
}
```

### 步骤 2：在全局 CSS 补充过渡定义
**文件**：`src/style.css`
**操作**：追加 Vue Transition 的 CSS 类定义（`slide-up`、`fade`、`toast`、`modal`）

```css
/* Transition: slide-up */
.slide-up-enter-active { transition: all 0.3s ease-out; }
.slide-up-leave-active { transition: all 0.2s ease-in; }
.slide-up-enter-from,
.slide-up-leave-to { opacity: 0; transform: translateY(20px); }

/* Transition: fade */
.fade-enter-active { transition: opacity 0.3s ease-out; }
.fade-leave-active { transition: opacity 0.2s ease-in; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }

/* Transition: scale */
.scale-enter-active { transition: all 0.3s ease-out; }
.scale-leave-active { transition: all 0.2s ease-in; }
.scale-enter-from,
.scale-leave-to { opacity: 0; transform: scale(0.9); }
```

### 步骤 3：增强运动概览卡片交互
**文件**：`src/views/Sports.vue`，概览卡片区域（L8-32）

**修改点**：
- 给整个卡片区添加页面进入动画（`animate-fade-in-up`）
- 统计面板每个数据项添加数字跳动效果（使用 `ref` + `setInterval` 递增计数）
- 按钮增加 `hover:scale-105` 缩放效果，添加点击波纹反馈
- 渐变背景增加缓慢浮动装饰光斑

### 步骤 4：增强课程卡片交互
**文件**：`src/views/Sports.vue`，课程卡片区域（L46-71）

**修改点**：
- 课程卡片增加 `hover:shadow-lg hover:-translate-y-1` 上浮效果
- 卡片图片区域 hover 时视频播放图标增加 `scale-125` 缩放
- 课程卡片整体添加交错入场动画（`animate-fade-in-up` + `style="animation-delay: {idx * 100}ms"`）
- Tab 按钮高亮活跃状态（`activeCourseTab` ref + 条件样式）
- 增强 `.course-card` 的 CSS transition duration 到 400ms

### 步骤 5：校园运动地图交互增强
**文件**：`src/views/Sports.vue`，地图区域（L73-88）

**修改点**：
- 路线信息浮层添加 `hover:scale-105 hover:shadow-xl` 效果
- 图片容器添加 `hover:scale-[1.02]` 缓慢缩放
- 添加 `Transition name="fade"` 包裹路线信息面板，支持后续可能的路线切换
- 增加路线标签指示多个可用路线

### 步骤 6：勋章区域交互增强
**文件**：`src/views/Sports.vue`，勋章区域（L92-107）

**修改点**：
- 已达成的勋章添加 `hover:scale-110` 缩放效果
- 未达成的勋章添加灰度样式（`grayscale opacity-50`）
- 勋章添加悬停 tooltip 提示获得条件（使用 CSS-only tooltip）
- 勋章添加入场弹跳动画

### 步骤 7：约球广场交互增强
**文件**：`src/views/Sports.vue`，约球区域（L108-132）

**修改点**：
- 约球卡片添加 `hover:shadow-md hover:-translate-x-1` 侧移效果
- "加入" 按钮悬浮时高亮为完整按钮样式
- "发布约球信息" 按钮悬停时边框变实心橙色
- 添加 Toast 反馈系统（"约球信息发布成功"等提示）
- 滚动加载更多约球信息（IntersectionObserver）

### 步骤 8：数据加载与反馈系统
**文件**：`src/views/Sports.vue`，script 部分

**新增功能**：
- 骨架屏加载状态（Skeleton Loading）：页面初始加载时显示 pulsating placeholder
- Toast 消息系统：复用项目中 `toast` Transition + 橙色主题
- 操作确认：点击"加入约球"弹出简易确认 Toast
- 空状态提示：若无约球数据显示空状态插图

### 步骤 9：响应式适配验证
**检查点**：
- 确保所有 `hover:` 效果在移动端不会误触发（利用 `@media (hover: hover)`）
- 移动端卡片垂直排列时交错动画时序合理
- 触屏设备按钮点击区域 ≥ 44x44px（WCAG 标准）

---

## 三、实施顺序

| 步骤 | 文件 | 优先级 | 说明 |
|------|------|--------|------|
| 1 | `tailwind.config.js` | 高 | 所有动画依赖此配置 |
| 2 | `src/style.css` | 高 | 补充 Transition CSS 类 |
| 3 | `Sports.vue` 概览卡片 | 高 | 骨架屏 + 入场动画 |
| 4 | `Sports.vue` 课程卡片 | 高 | Tab 交互 + 卡片效果 |
| 5 | `Sports.vue` 地图区域 | 中 | 悬停缩放效果 |
| 6 | `Sports.vue` 勋章区域 | 中 | 条件交互动画 |
| 7 | `Sports.vue` 约球广场 | 中 | Toast + 加载反馈 |
| 8 | `Sports.vue` 数据反馈 | 中 | Toast/确认系统 |

---

## 四、验收标准

- [x] 页面打开时各区域有平滑的入场动画
- [ ] 课程 Tab 切换有明确的视觉反馈
- [ ] 卡片/按钮 hover 有缩放、阴影、位移等效果
- [ ] 数据加载时有骨架屏/加载指示器
- [ ] 用户操作（约球、点赞等）有 Toast 反馈
- [ ] 移动端 hover 效果不误触发
- [ ] 动画不卡顿（使用 `transform` 和 `opacity`，避免触发 layout）