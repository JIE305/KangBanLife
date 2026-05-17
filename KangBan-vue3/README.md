# 康伴生活 - 大学生健康服务平台

专为在校大学生打造的轻量化健康助手，提供日常健康管理、身心调适、运动规划和校园资源查询等功能。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite 5
- **样式**: Tailwind CSS 3
- **图表**: ECharts
- **图标**: Iconify Vue
- **测试**: Vitest

## 项目结构

```
src/
├── components/          # 公共组件
│   ├── Navbar.vue       # 导航栏组件
│   └── Footer.vue       # 页脚组件
├── router/              # 路由配置
│   └── index.js         # 路由定义
├── stores/              # Pinia 状态管理
│   ├── user.js          # 用户认证与状态管理
│   ├── health.js        # 健康数据与日常记录管理
│   └── app.js           # 应用配置与全局数据
├── views/               # 页面视图
│   ├── Home.vue         # 首页
│   ├── Health.vue       # 日常管理页
│   ├── Mental.vue       # 身心调适页
│   ├── Sports.vue       # 运动规划页
│   ├── Resources.vue    # 资源查询页
│   ├── Login.vue        # 登录页
│   └── Register.vue     # 注册页
├── App.vue              # 根组件
├── main.js              # 应用入口
└── style.css            # 全局样式
```

## Pinia Store 结构

### user.js - 用户认证与状态管理

**State**:
- `user`: 当前用户信息对象
- `isLoggedIn`: 是否已登录
- `token`: 用户认证令牌
- `rememberMe`: 是否记住登录状态

**Getters**:
- `currentUser`: 返回当前用户信息

**Actions**:
- `login(credentials)`: 用户登录
- `register(userInfo)`: 用户注册
- `logout()`: 用户登出
- `setRememberMe(value)`: 设置记住我状态
- `checkAuth()`: 检查登录状态

### health.js - 健康数据与日常记录管理

**State**:
- `waterAmount`: 当前饮水量 (ml)
- `dailyGoal`: 每日饮水目标 (ml)
- `checklist`: 每日健康清单
- `healthStats`: 健康统计数据
- `trendData`: 趋势数据

**Getters**:
- `waterProgress`: 饮水进度百分比
- `completedChecklist`: 已完成清单数量

**Actions**:
- `addWater(amount)`: 添加饮水量
- `toggleChecklistItem(itemId)`: 切换清单项状态
- `calculateBMI(height, weight)`: 计算BMI
- `resetDailyData()`: 重置每日数据

### app.js - 应用配置与全局数据

**State**:
- `currentDate`: 当前日期
- `navItems`: 导航菜单项
- `features`: 核心功能特性
- `articles`: 健康资讯文章
- `stats`: 统计数据
- `mealOptions`: 食堂配餐建议

**Getters**:
- `formattedDate`: 格式化的日期字符串

**Actions**:
- `setCurrentDate()`: 设置当前日期
- `getMealsByType(mealType)`: 根据类型获取配餐建议
- `addArticle(article)`: 添加新文章

## 使用方法

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

### 生产构建

```bash
npm run build
```

### 运行测试

```bash
npm test
```

## 路由配置

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | Home.vue | 首页 |
| `/health` | Health.vue | 日常管理 |
| `/mental` | Mental.vue | 身心调适 |
| `/sports` | Sports.vue | 运动规划 |
| `/resources` | Resources.vue | 资源查询 |
| `/login` | Login.vue | 登录页 |
| `/register` | Register.vue | 注册页 |

## 核心功能

1. **日常健康管理**: 饮水记录、BMI计算、每日健康清单
2. **身心调适**: 冥想白噪音、压力缓解
3. **运动规划**: 宿舍健身、操场路线推荐
4. **资源查询**: 急救指南、校医室排班、周边药店

## 设计规范

- 主题色: Emerald (翠绿色)
- 设计风格: 现代化、轻量化、卡片式设计
- 响应式布局: 支持移动端和桌面端