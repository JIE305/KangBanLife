# 康伴生活 (UniHealth) — 项目总览

面向大学生的校园健康服务平台（Kanban 风格），覆盖日常健康管理、身心调适、运动规划、医疗资源查询、AI 心理陪伴等功能。

## 技术栈

| 层 | 技术 | 说明 |
|----|------|------|
| 前端 | Vue 3 (Composition API) + Vite 5 | SPA，10 个路由页面 |
| UI | Tailwind CSS 3 | 玻璃卡片风格，4 套主题色 |
| 状态 | Pinia 3 | 3 个 store（user/app/health） |
| 图表 | ECharts 5 | 健康趋势、运动数据可视化 |
| 地图 | 高德地图 JS API v1.4 | 医疗设施搜索与导航 |
| 后端 | Flask 3.x | 蓝图架构，RESTful API |
| 数据库 | SQLite（计划迁移 MySQL） | 原始 SQL，无 ORM |
| 认证 | JWT (flask-jwt-extended) | 2 小时过期，无刷新令牌 |
| AI | 火山引擎 ARK (豆包) | 心理陪伴对话，规则引擎回退 |
| HTTP | Axios（前端）/ requests（后端） | Vite 代理到 127.0.0.1:5000 |

## 功能模块

| 模块 | 前端页面 | 后端蓝图 | 状态 |
|------|---------|---------|------|
| 首页/文章 | Home.vue / ArticleDetail.vue | `/api/v1/articles` | 已对接 |
| 用户认证 | Login.vue / Register.vue / Profile.vue | `/api/v1/auth` + `/api/v1/user` | 已对接 |
| 匿名树洞 | Mental.vue（帖子部分） | `/api/v1/posts` | 已对接 |
| AI 心理陪伴 | Mental.vue（ChatPanel） | `/api/v1/chat` | 已对接 |
| 资源查询 | Resources.vue | `/api/v1/resources` | 已对接 |
| 日常管理 | Health.vue | — | 纯前端 Mock |
| 运动规划 | Sports.vue | — | 纯前端 Mock |
| 医疗导航 | Map.vue | — | 纯前端 + 高德 API |

> **已对接** = 前端通过 Axios 调用后端 API，数据来自数据库  
> **纯前端 Mock** = 数据硬编码在 Vue 组件内，无后端交互

## 项目结构

```
KB/
├── KangBan-backend/    # Flask 后端（端口 5000）
├── KangBan-vue3/        # Vue 3 前端（端口 3000）
└── plan/                # 项目文档（你在这里）
    ├── overview/        # ← 快速入门文档
    ├── API接口文档*.md
    ├── 数据库设计文档*.md
    ├── 后端开发指南*.md
    ├── 前端对接指南*.md
    └── ...
```

## 文档导航

### 我想快速了解项目全貌
→ [架构总览.md](架构总览.md) → [文件结构.md](文件结构.md) → [当前实现状态.md](当前实现状态.md)

### 我要把项目跑起来
→ [快速启动.md](快速启动.md)

### 我要开发新功能
→ [../API接口文档.md](../API接口文档.md) → [../后端开发指南.md](../后端开发指南.md) 或 [../前端对接指南.md](../前端对接指南.md)

### 我要了解数据库
→ [../数据库设计文档.md](../数据库设计文档.md) → [../数据库迁移计划.md](../数据库迁移计划.md)

### 我要部署上线
→ [../部署指南.md](../部署指南.md)

### 我要写测试
→ [../测试指南.md](../测试指南.md)

### 我接手了第二阶段开发
→ [../第二阶段实施计划.md](../第二阶段实施计划.md) → [../CHANGELOG.md](../CHANGELOG.md)
