# 变更日志

每次对项目的代码改动都记录在此。附带 **文档同步检查清单**，确保相关文档随代码一同更新。

---

## 文档同步检查清单

改代码后，对照下表勾选需要同步更新的文档：

| 改动范围 | 需检查的文档 |
|---------|-------------|
| 后端新增/修改 API | `API接口文档.md` / `API接口文档_lite.md` |
| 后端新增/修改蓝图 | `后端开发指南.md` / `后端开发指南_lite.md` |
| 数据库表/字段变更 | `数据库设计文档.md` / `数据库设计文档_lite.md` / `数据库迁移计划.md` |
| 前端对接新 API | `前端对接指南.md` / `前端对接指南_lite.md` / `前后端对接实施记录.md` |
| 架构/技术栈变更 | `overview/架构总览.md` |
| 文件增删 | `overview/文件结构.md` |
| 实现进度变化 | `overview/当前实现状态.md` |
| 环境配置变更 | `overview/快速启动.md` |
| 部署方式变更 | `部署指南.md` |

---

## 2026-05-13 — 文档体系建设

**类型**: 文档新增/更新

**新增文件**:
- `plan/overview/README.md` — 项目总览入口
- `plan/overview/架构总览.md` — 前后端架构与数据流
- `plan/overview/文件结构.md` — 带注释的项目文件树
- `plan/overview/当前实现状态.md` — Mock vs 真实 API 对照 + 已知问题
- `plan/overview/快速启动.md` — 5 分钟跑起来指南
- `plan/CHANGELOG.md` — 本文件
- `plan/数据库迁移计划.md` — SQLite→MySQL 迁移方案
- `plan/部署指南.md` — 生产环境部署
- `plan/测试指南.md` — 测试编写与运行
- `plan/第二阶段实施计划.md` — 未实现模块的实施路线图

**更新文件**:
- `plan/API接口文档.md` — 新增实现状态总览表
- `plan/API接口文档_lite.md` — 新增 chat 模块（3 个端点），端点从 14→17
- `plan/数据库设计文档.md` — 新增表实现状态总览
- `plan/数据库设计文档_lite.md` — 新增 chat_sessions + chat_messages 表，建表 SQL 及 API 映射
- `plan/后端开发指南.md` — 新增实现状态说明
- `plan/前端对接指南.md` — 新增实施状态说明
- `plan/前端对接指南_lite.md` — 新增实施状态说明

---

## 2026-05-12 — 前后端首批对接

**类型**: 功能实现

**后端**:
- 确认 6 个蓝图正常运行：auth, user, articles, posts, resources, chat
- 实际使用 `schema_lite.sql`（6 表），非完整版 `schema.sql`

**前端**:
- 新建 `src/utils/request.js` — Axios 实例 + 拦截器
- 新建 `src/api/auth.js` — 登录/注册/登出 API
- 新建 `src/api/user.js` — 个人资料/头像 API
- 新建 `src/api/articles.js` — 文章 API
- 新建 `src/api/posts.js` — 树洞帖子 API
- 新建 `src/api/chat.js` — AI 聊天 API
- 修改 `src/stores/user.js` — 对接真实登录/注册
- 修改 `vite.config.js` — 添加 /api 和 /uploads 代理
- 修改 `src/views/Home.vue` — 文章从 Mock 切换为 API
- 修改 `src/views/Mental.vue` — 帖子/聊天切换为 API
- 修改 `src/views/Profile.vue` — 个人资料切换为 API

**验证**: 14 个核心端点全部正常响应，前端 `npm run build` 通过（663 模块, 0 错误）

**未修改的前端页面**: Health.vue, Sports.vue, Resources.vue, Map.vue（继续使用 Mock 数据）

---

## 2026-05-11 — 项目规划与文档初建

**类型**: 文档

- 创建 `plan/` 目录及 9 份设计文档（API/数据库/后端/前端 × 完整版+精简版 + 实施记录）
- 定义 9 大功能模块、30 个 API 端点、15 张数据库表的设计
- 确定技术栈：Flask + Vue 3 + SQLite

---

## 2026-05-13（修订）— 文档与代码交叉验证修正

**类型**: 文档修正

基于实际代码与文档的交叉验证，修正了以下 12 处差异：

**架构总览.md**:
- Store 使用表：移除 Navbar 和 Mental（实际直接读 localStorage，不走 Pinia Store）
- health.js Store：更正为"未被任何组件导入"（原错误声称 Health.vue 部分使用）
- ER 图 articles 表：`summary→excerpt`, `img→img_url`, `alt→img_alt`, 移除不存在的 `bg_class`
- ER 图新增 posts 表定义（含缺失的 `author` 和 `updated_at` 字段）
- Mental.vue 路由 API 列表：补充 `DELETE /posts/:id`

**API接口文档_lite.md**:
- `GET /chat/history` 从公开接口移至需认证接口（代码中为 `@jwt_required()`）

**数据库设计文档.md**:
- 标题中"其余 9 张表"更正为"其余 11 张表"

**数据库设计文档_lite.md**:
- chat_sessions/chat_messages 表定义中的类型和约束更正为与实际 schema_lite.sql 一致：
  - `created_at` 类型 `DATETIME→TEXT`，默认值 `CURRENT_TIMESTAMP→(datetime('now','localtime'))`
  - `session_id` 约束 `NOT NULL→可空（REFERENCES）`
  - `role` 类型 `VARCHAR(10)→TEXT`
  - 移除嵌入式 SQL 中 schema_lite.sql 不存在的外键约束

**文件结构.md**:
- 后端补充 `.gitignore`
- 前端补充 `.gitignore`、`README.md`、`data_persistence_requirements.md`、`package-lock.json`

**当前实现状态.md**:
- 已知问题 #3 更正：Health.vue 完全不使用 health Store（非"部分使用"）

---

## 2026-05-13（修订 2）— 修复后端启动失败

**类型**: 修复

**问题**: `python app.py` 启动报错 `ModuleNotFoundError: No module named 'dotenv'`

**根因**: 虚拟环境中缺少 `python-dotenv` 包。`requirements.txt` 中定义了该依赖但此前未通过 `pip install -r requirements.txt` 完整安装（只单独安装了 flask/flask-cors/flask-jwt-extended/werkzeug/requests）。

**修复**: `pip install python-dotenv`（已同步执行 `pip install -r requirements.txt` 确保无遗漏）

**验证**: 后端在 `http://127.0.0.1:5000` 正常启动，Flask debug mode 就绪

---

## 2026-05-13（修订 3）— 修复两个前端 Bug

**类型**: 修复

### Bug 1: 浏览器重启后头像显示但点击跳转登录页

**根因**: 认证状态双重数据源不同步。登录时将 `isLoggedIn` 同时写入 `sessionStorage` 和 `localStorage`，浏览器重启后 `sessionStorage` 被清空但 `localStorage` 保留。路由守卫只读 `sessionStorage`（为空 → 拦截跳转登录），Navbar 读 `localStorage`（有 token → 显示头像）。

`userStore.checkAuth()` 方法专门用于从 `localStorage` 恢复 `sessionStorage`，但从未在应用启动时调用。

**修复**: `App.vue` 的 `setup()` 中调用 `userStore.checkAuth()`，每次应用初始化时从 `localStorage` 恢复认证状态到 `sessionStorage`。

### Bug 2: 导航栏非首页偏右

**根因**: Navbar 使用 `flex justify-between` 布局。当 `showLogin=false` 时（Health/Mental/Sports/Resources/Profile 页面），右侧区域为空，导航项变成 flex 容器中最后一个子元素，被 `justify-between` 推到右端。

**修复**: 将 `flex justify-between` 改为 `grid grid-cols-[1fr_auto_1fr]`，三列布局使导航项始终居中，无论左右两侧是否有内容。右侧列加 `justify-end` 保持登录按钮右对齐。

**影响文件**: `src/App.vue`, `src/components/Navbar.vue`

---

## 2026-05-13（修订 4）— 项目评审材料准备

**类型**: 文档

创建 `KB/review/` 目录，为软件工程课程需求评审准备全套材料：

| 文件 | 内容 |
|------|------|
| `review/小组分工与评审提纲.md` | 6 人分工表 + 组长 5 分钟评审介绍大纲 |
| `review/需求规格说明书.md` | 课程简化版 SRS：8 个功能模块、4 类非功能需求、外部接口 |
| `review/用例图与用例描述.md` | Mermaid 用例图（3 Actor, 19 用例）+ 6 个核心用例详细描述 |
| `review/活动图.md` | 5 个核心流程活动图：注册登录、AI 对话、树洞发帖、文章浏览、资料管理 |
| `review/类图.md` | 4 个类图：后端蓝图架构、数据库实体关系、前端组件结构、API 模块 |
| `review/状态图_时序图_协作图.md` | 3 状态图 + 4 时序图 + 2 协作图，覆盖用户认证/帖子/AI对话/头像上传 |

---

## 2026-05-13（修订 5）— 修复 AI 聊天超时 + 等待体验

**类型**: 修复

**问题**: 发送聊天消息后弹出"网络错误，请稍后再试"，AI 对话和规则对话均不可用。

**根因**: ARK API 响应耗时波动至 ~27 秒，但 Axios 全局超时仅 10 秒。后端 `chat.py` 先等 AI API（30s timeout）再回落规则引擎，Axios 10s 就断开了连接——AI 回复和规则引擎回复都来不及返回。

**修复**:
- `src/api/chat.js`: `sendMessageAPI` 超时从 10s → 45s
- `src/components/ChatPanel.vue`: 等待时显示三点跳动动画，按钮变为"思考中..."，发送中禁用输入框防止重复发送

**影响文件**: `src/api/chat.js`, `src/components/ChatPanel.vue`
