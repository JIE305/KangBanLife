# 康伴生活(UniHealth) - API 接口文档

> 版本: v1.0 | 基础路径: `/api/v1` | 最后更新: 2026-05-11 | 审核: 2026-05-13

> **实现状态说明**: 本文档定义了 9 个模块共 30 个端点设计。当前实际实现 6 个模块约 21 个端点（见标注）。health/meals/sports/mood 4 个模块尚未实现，为第二阶段计划。实际运行数据库为 schema_lite.sql（6 表），非完整版的 15 表。详见 [当前实现状态](overview/当前实现状态.md)。

## 实现状态总览

| 模块 | 端点数 | 实现状态 |
|------|--------|---------|
| 认证 auth | 3 | 已实现 |
| 用户 user | 4 | 已实现 |
| 文章 articles | 3 | 已实现 |
| 匿名树洞 posts | 4 | 已实现 |
| AI 聊天 chat | 3 | **已实现**（本文档未收录，见精简版） |
| 资源 resources | 4 | 已实现 |
| 健康 health | 3 | 未实现 |
| 配餐 meals | 2 | 未实现 |
| 运动 sports | 4 | 未实现 |
| 心情 mood | 3 | 未实现 |

---

## 目录

1. [通用约定](#通用约定)
2. [认证模块 auth](#认证模块-auth)
3. [用户模块 user](#用户模块-user)
4. [文章模块 articles](#文章模块-articles)
5. [健康模块 health](#健康模块-health)
6. [配餐模块 meals](#配餐模块-meals)
7. [匿名树洞 posts](#匿名树洞模块-posts)
8. [运动模块 sports](#运动模块-sports)
9. [资源模块 resources](#资源模块-resources)
10. [心情模块 mood](#心情模块-mood)

---

## 通用约定

### 基础URL

```
开发环境: http://localhost:5000/api/v1
```

### 统一响应格式

**成功响应**:
```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

**分页响应**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "items": [ ... ],
    "total": 100,
    "page": 1,
    "limit": 10
  }
}
```

**错误响应**:
```json
{
  "code": 400,
  "message": "参数校验失败",
  "errors": {
    "studentId": "学号不能为空",
    "password": "密码长度不能少于6位"
  }
}
```

### HTTP状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未登录(token无效/过期) |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 数据冲突(重复学号等) |
| 413 | 文件大小超出限制 |
| 500 | 服务器内部错误 |

### 认证方式

需要登录的接口在请求头中携带:
```
Authorization: Bearer {token}
```

Token 通过登录/注册接口获取，有效期2小时。

### 字段命名说明

- **请求参数**: 使用驼峰命名 `studentId` (与前端一致)
- **响应字段**: 使用下划线命名 `student_id` (与数据库一致)

> 后端可根据习惯调整，但需确保前端能正确解析。建议响应字段用下划线，前端 axios 拦截器统一转换。

---

## 认证模块 auth

### POST /auth/login — 用户登录

```
POST /api/v1/auth/login
```

**请求体**:
```json
{
  "studentId": "2024001",
  "password": "mypassword"
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "student_id": "2024001",
      "username": "张三",
      "email": null,
      "phone": "138****8888",
      "avatar_url": null,
      "gender": 1,
      "height": 175.00,
      "weight": 65.00,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-05-11T10:30:00"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**失败响应** (401):
```json
{
  "code": 401,
  "message": "学号或密码错误"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| studentId | string | 是 | 学号 |
| password | string | 是 | 密码，至少6位 |

---

### POST /auth/register — 用户注册

```
POST /api/v1/auth/register
```

**请求体**:
```json
{
  "studentId": "2024002",
  "username": "张三",
  "phone": "13812345678",
  "password": "mypassword123"
}
```

**成功响应** (201):
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 2,
      "student_id": "2024002",
      "username": "张三",
      "email": null,
      "phone": "138****5678",
      "avatar_url": null,
      "gender": 0,
      "height": null,
      "weight": null,
      "created_at": "2026-05-11T12:00:00",
      "updated_at": "2026-05-11T12:00:00"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**失败响应** (409):
```json
{
  "code": 409,
  "message": "该学号已被注册"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| studentId | string | 是 | 学号，必须唯一 |
| username | string | 是 | 用户名，必须唯一 |
| phone | string | 是 | 手机号 |
| password | string | 是 | 密码，至少6位 |

---

### POST /auth/logout — 用户登出

```
POST /api/v1/auth/logout
Authorization: Bearer {token}
```

**请求体**: 无

**成功响应** (200):
```json
{
  "code": 200,
  "message": "登出成功"
}
```

---

## 用户模块 user

> 以下接口均需携带 `Authorization: Bearer {token}`

### GET /user/profile — 获取个人信息

```
GET /api/v1/user/profile
Authorization: Bearer {token}
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "user": {
      "id": 1,
      "student_id": "2024001",
      "username": "张三",
      "email": "zhangsan@example.com",
      "phone": "138****8888",
      "avatar_url": "/uploads/avatars/1.jpg",
      "gender": 1,
      "height": 175.00,
      "weight": 65.00,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-05-11T10:30:00"
    }
  }
}
```

**性别枚举**: 0=未知, 1=男, 2=女

---

### PUT /user/profile/basic — 更新基本信息

```
PUT /api/v1/user/profile/basic
Authorization: Bearer {token}
```

**请求体** (所有字段可选):
```json
{
  "username": "张三丰",
  "gender": 1,
  "height": 178.00,
  "weight": 70.00
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "基本信息已更新",
  "data": {
    "user": { ... }
  }
}
```

---

### PUT /user/profile/contact — 更新联系方式

```
PUT /api/v1/user/profile/contact
Authorization: Bearer {token}
```

**请求体** (所有字段可选):
```json
{
  "email": "newemail@example.com",
  "phone": "13900001111"
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "联系方式已更新"
}
```

---

### POST /user/avatar — 上传头像

```
POST /api/v1/user/avatar
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**请求体**: 表单文件字段名 `file`

**限制**:
- 仅允许图片格式 (jpg/png/gif/webp)
- 文件大小不超过 5MB

**成功响应** (200):
```json
{
  "code": 200,
  "message": "头像上传成功",
  "data": {
    "avatar_url": "/uploads/avatars/1_20260511.jpg"
  }
}
```

**失败响应** (413):
```json
{
  "code": 413,
  "message": "图片大小不能超过5MB"
}
```

---

## 文章模块 articles

### GET /articles — 文章列表

```
GET /api/v1/articles?tag=饮食指导&page=1&limit=10
```

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| tag | string | 否 | - | 按标签筛选 |
| page | int | 否 | 1 | 页码 |
| limit | int | 否 | 10 | 每页条数(最大50) |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "title": "食堂减脂餐点菜攻略",
        "excerpt": "校内食堂其实隐藏着很多健康组合...",
        "tag": "饮食指导",
        "tag_class": "bg-emerald-100 text-emerald-600",
        "img_url": "https://example.com/img1.jpg",
        "img_alt": "学生健康饮食",
        "date": "2026-03-25",
        "views": 1200
      }
    ],
    "total": 3,
    "page": 1,
    "limit": 10
  }
}
```

---

### GET /articles/featured — 首页推荐文章

```
GET /api/v1/articles/featured?limit=3
```

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| limit | int | 否 | 3 | 返回条数(最大10) |

**响应格式**: 同 `/articles` 的 `items` 字段

---

### GET /articles/:id — 文章详情

```
GET /api/v1/articles/1
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "article": {
      "id": 1,
      "title": "食堂减脂餐点菜攻略",
      "excerpt": "校内食堂其实隐藏着很多健康组合...",
      "content": "<p>完整的文章正文内容...</p>",
      "tag": "饮食指导",
      "tag_class": "bg-emerald-100 text-emerald-600",
      "img_url": "https://example.com/img1.jpg",
      "img_alt": "学生健康饮食",
      "date": "2026-03-25",
      "views": 1201,
      "created_at": "2026-03-25T08:00:00",
      "updated_at": "2026-03-25T08:00:00"
    }
  }
}
```

> 注意: 每次请求文章详情，`views` 字段自动 +1

**失败响应** (404):
```json
{
  "code": 404,
  "message": "文章不存在"
}
```

---

## 健康模块 health

> 以下接口均需登录，数据按日期与当前用户绑定

### GET /health/checklist — 获取每日健康清单

```
GET /api/v1/health/checklist?date=2026-05-11
Authorization: Bearer {token}
```

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| date | string | 否 | 今天 | 日期 YYYY-MM-DD |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "date": "2026-05-11",
    "checklist": [
      {
        "id": 1,
        "text": "8:00前起床",
        "icon": "solar:sun-bold",
        "iconColor": "text-orange-400",
        "checked": true
      },
      {
        "id": 2,
        "text": "1500ml饮水完成",
        "icon": "solar:tea-cup-bold",
        "iconColor": "text-emerald-500",
        "checked": false
      },
      {
        "id": 3,
        "text": "摄入新鲜蔬果",
        "icon": "solar:leaf-bold",
        "iconColor": "text-green-500",
        "checked": true
      },
      {
        "id": 4,
        "text": "23:30前入睡",
        "icon": "solar:moon-bold",
        "iconColor": "text-blue-500",
        "checked": false
      }
    ]
  }
}
```

---

### PUT /health/checklist/:itemId — 切换清单项

```
PUT /api/v1/health/checklist/2
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "checked": true
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "已更新",
  "data": {
    "id": 2,
    "checked": true
  }
}
```

---

### GET /health/water — 获取当日饮水量

```
GET /api/v1/health/water?date=2026-05-11
Authorization: Bearer {token}
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "date": "2026-05-11",
    "water_ml": 850,
    "daily_goal": 1500,
    "progress_pct": 56.7
  }
}
```

---

### POST /health/water — 增加饮水

```
POST /api/v1/health/water
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "amount_ml": 250
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "date": "2026-05-11",
    "water_ml": 1100,
    "daily_goal": 1500,
    "progress_pct": 73.3
  }
}
```

---

### GET /health/trend — 获取身心趋势

```
GET /api/v1/health/trend?days=7
Authorization: Bearer {token}
```

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| days | int | 否 | 7 | 天数(最大30) |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "trend": [
      { "day": "周一", "fitness": 75, "energy": 60 },
      { "day": "周二", "fitness": 78, "energy": 65 },
      { "day": "周三", "fitness": 82, "energy": 55 },
      { "day": "周四", "fitness": 80, "energy": 70 },
      { "day": "周五", "fitness": 85, "energy": 75 },
      { "day": "周六", "fitness": 88, "energy": 90 },
      { "day": "今日", "fitness": 86, "energy": 82 }
    ]
  }
}
```

---

### PUT /health/trend — 更新单日趋势

```
PUT /api/v1/health/trend
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "date": "2026-05-11",
  "fitness": 90,
  "energy": 85
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期 YYYY-MM-DD |
| fitness | int | 否 | 体能评分 0-100 |
| energy | int | 否 | 精力评分 0-100 |

**成功响应** (200):
```json
{
  "code": 200,
  "message": "趋势数据已更新"
}
```

---

### GET /health/chart — 获取图表数据(首页)

```
GET /api/v1/health/chart?days=7
Authorization: Bearer {token}
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "steps": [5000, 7200, 4800, 8100, 6500, 9200, 4300],
    "focus_time": [120, 240, 180, 200, 310, 280, 150],
    "dates": ["05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11"]
  }
}
```

---

### PUT /health/chart — 更新单日图表数据

```
PUT /api/v1/health/chart
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "date": "2026-05-11",
  "steps": 10000,
  "focus_time": 300
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期 YYYY-MM-DD |
| steps | int | 否 | 步数 0-100000 |
| focus_time | int | 否 | 专注时间(分钟) 0-1440 |

**成功响应** (200):
```json
{
  "code": 200,
  "message": "数据已更新"
}
```

---

## 配餐模块 meals

### GET /meals — 获取食堂配餐建议

```
GET /api/v1/meals?meal_type=breakfast
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| meal_type | string | 是 | breakfast / lunch / dinner |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "meals": [
      {
        "id": 1,
        "icon": "mdi:food-variant",
        "iconColor": "text-emerald-500",
        "tag": "均衡选择",
        "tagClass": "bg-emerald-100 text-emerald-600",
        "title": "元气满分早餐",
        "desc": "全麦包+煮鸡蛋+无糖豆浆/牛奶+一份当季水果",
        "calories": 350,
        "protein": 20
      },
      {
        "id": 2,
        "icon": "mdi:food-apple",
        "iconColor": "text-blue-500",
        "tag": "低卡选择",
        "tagClass": "bg-blue-100 text-blue-600",
        "title": "清爽粗粮早餐",
        "desc": "燕麦粥/玉米/紫薯+凉拌海带丝+蛋白2个",
        "calories": 280,
        "protein": 15
      }
    ]
  }
}
```

---

## 匿名树洞模块 posts

### GET /posts — 帖子列表

```
GET /api/v1/posts?page=1&limit=20
```

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| limit | int | 否 | 20 | 每页条数(最大50) |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "author": "校友 #12938",
        "time": "10分钟前",
        "content": "图书馆闭馆时的星光真的好美，虽然考研的路很难，但我觉得我还能坚持。大家加油呀！",
        "likes": 42,
        "comments": 5
      },
      {
        "id": 2,
        "author": "校友 #12901",
        "time": "2小时前",
        "content": "今天的午饭好咸，第一食堂那个大叔是不是手抖了...",
        "likes": 12,
        "comments": 3
      }
    ],
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```

> 说明: `time` 字段后端返回 ISO 时间格式，前端自行计算"几分钟前"显示。`author` 是创建时生成的匿名代号，不关联真实用户。

---

### POST /posts — 发布匿名帖子

```
POST /api/v1/posts
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "content": "今天心情很好，分享一下！"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 内容，1-1000字 |

**成功响应** (201):
```json
{
  "code": 201,
  "message": "发布成功",
  "data": {
    "post": {
      "id": 101,
      "author": "校友 #47291",
      "time": "2026-05-11T12:30:00",
      "content": "今天心情很好，分享一下！",
      "likes": 0,
      "comments": 0
    }
  }
}
```

---

### POST /posts/:id/like — 点赞/取消点赞

```
POST /api/v1/posts/1/like
Authorization: Bearer {token}
```

**请求体**: 无

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "likes": 43,
    "is_liked": true
  }
}
```

> 说明: 同一用户对同一帖子，第一次请求点赞(+1)，第二次请求取消点赞(-1)。通过 `post_likes` 表记录防重。

---

### DELETE /posts/:id — 删除帖子

```
DELETE /api/v1/posts/1
Authorization: Bearer {token}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "帖子已删除"
}
```

> 说明: 仅发帖人本人可删除。实现为软删除(status=0)。

---

## 运动模块 sports

### GET /sports/courses — 运动课程列表

```
GET /api/v1/sports/courses?category=all
```

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| category | string | 否 | all | all / stretch / strength |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "courses": [
      {
        "id": 1,
        "img": "https://example.com/course1.jpg",
        "alt": "睡前拉伸",
        "duration": "08:15",
        "title": "睡前久坐拉伸",
        "desc": "适合期末周，缓解颈椎压力",
        "intensity": "低强度",
        "intensityClass": "text-orange-500",
        "participants": "1.2k"
      }
    ]
  }
}
```

---

### GET /sports/medals — 勋章列表

```
GET /api/v1/sports/medals
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "medals": [
      { "id": 1, "label": "清晨跑者", "icon": "solar:sun-bold", "achieved": true },
      { "id": 2, "label": "十日坚持", "icon": "solar:fire-bold", "achieved": false },
      { "id": 3, "label": "体测满分", "icon": "solar:cup-star-bold", "achieved": false }
    ]
  }
}
```

> 当用户未登录时，所有 `achieved` 返回 false

---

### GET /sports/matches — 运动匹配列表

```
GET /api/v1/sports/matches?page=1&limit=20
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "sport": "羽毛球",
        "tagClass": "bg-orange-100 text-orange-600",
        "time": "14:00",
        "location": "体育馆",
        "desc": "三缺一，来个水平中等的校友！",
        "creator": "匿名用户A"
      }
    ],
    "total": 5,
    "page": 1,
    "limit": 20
  }
}
```

---

### POST /sports/matches — 发布匹配信息

```
POST /api/v1/sports/matches
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "sport_type": "羽毛球",
  "time": "14:00",
  "location": "体育馆",
  "desc": "三缺一，来个水平中等的校友！"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sport_type | string | 是 | 运动类型 |
| time | string | 是 | 时间段 |
| location | string | 是 | 地点 |
| desc | string | 是 | 描述说明 |

**成功响应** (201):
```json
{
  "code": 201,
  "message": "发布成功",
  "data": {
    "match": {
      "id": 3,
      "sport": "羽毛球",
      "tagClass": "bg-orange-100 text-orange-600",
      "time": "14:00",
      "location": "体育馆",
      "desc": "三缺一，来个水平中等的校友！",
      "creator": "匿名用户B"
    }
  }
}
```

---

## 资源模块 resources

### GET /resources/first-aid — 急救知识列表

```
GET /api/v1/resources/first-aid
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "title": "CPR心肺复苏",
        "desc": "关键时刻挽救生命",
        "icon": "mdi:heart-pulse",
        "bgClass": "bg-red-50",
        "borderClass": "border-red-100",
        "iconClass": "text-red-500",
        "iconHoverClass": "group-hover:bg-red-500 group-hover:text-white",
        "titleClass": "text-red-900",
        "descClass": "text-red-400"
      }
    ]
  }
}
```

> 说明: 样式类字段如 `bgClass`/`iconClass` 等存储在数据库中，后端直接返回。这是一种"内容即样式配置"的做法，适合项目初期快速开发。

---

### GET /resources/medicines — 常备药品分类

```
GET /api/v1/resources/medicines
```

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "title": "感冒发烧类",
        "desc": "对乙酰氨基酚(布洛芬)、复方氨酚烷胺片。若持续高烧请务必就医。",
        "icon": "mdi:thermometer",
        "iconBg": "bg-blue-100",
        "iconColor": "text-blue-600",
        "tag": "建议备选",
        "tagClass": "text-blue-500"
      }
    ]
  }
}
```

---

### GET /resources/facilities — 医疗设施列表

```
GET /api/v1/resources/facilities?type=医院&keyword=中心
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 按类型筛选 |
| keyword | string | 否 | 按名称/地址模糊搜索 |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "name": "开封市中心医院",
        "address": "河南省开封市鼓楼区自由路西段168号",
        "lat": 34.7908,
        "lng": 114.3580,
        "distance": "1.2km",
        "walk_time": "步行15分钟",
        "rating": "4.5",
        "type": "三甲医院",
        "tag": "急诊 24h",
        "tagClass": "text-blue-500 border border-blue-100",
        "tel": "0371-12345678"
      }
    ]
  }
}
```

---

### GET /resources/search — 综合搜索

```
GET /api/v1/resources/search?q=感冒
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |

**成功响应** (200):
```json
{
  "code": 200,
  "data": {
    "results": {
      "first_aid": [ ... ],
      "medicines": [ ... ],
      "facilities": [ ... ]
    }
  }
}
```

> 说明: 同时搜索急救知识、药品、医疗设施三个分类

---

## 心情模块 mood

### POST /mood/check-in — 每日心情打卡

```
POST /api/v1/mood/check-in
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "mood_type": "happy"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mood_type | string | 是 | happy / neutral / stressed / sad / tired |

**成功响应** (200):
```json
{
  "code": 200,
  "message": "今日心情已记录"
}
```

> 说明: 同一用户同一天只保留最新一条记录(upsert)

---

## 附录: 接口汇总表

### 无需认证的接口 (13个)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/login` | 登录 |
| POST | `/auth/register` | 注册 |
| GET | `/articles` | 文章列表 |
| GET | `/articles/featured` | 推荐文章 |
| GET | `/articles/:id` | 文章详情 |
| GET | `/meals` | 配餐建议 |
| GET | `/posts` | 匿名帖子列表 |
| GET | `/sports/courses` | 运动课程 |
| GET | `/sports/medals` | 勋章列表 |
| GET | `/sports/matches` | 运动匹配 |
| GET | `/resources/first-aid` | 急救知识 |
| GET | `/resources/medicines` | 药品分类 |
| GET | `/resources/facilities` | 医疗设施 |
| GET | `/resources/search` | 资源搜索 |

### 需要认证的接口 (17个)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/logout` | 登出 |
| GET | `/user/profile` | 个人信息 |
| PUT | `/user/profile/basic` | 更新基本信息 |
| PUT | `/user/profile/contact` | 更新联系方式 |
| POST | `/user/avatar` | 上传头像 |
| GET | `/health/checklist` | 健康清单 |
| PUT | `/health/checklist/:itemId` | 切换清单 |
| GET | `/health/water` | 饮水量 |
| POST | `/health/water` | 增加饮水 |
| GET | `/health/trend` | 身心趋势 |
| PUT | `/health/trend` | 更新趋势 |
| GET | `/health/chart` | 图表数据 |
| PUT | `/health/chart` | 更新图表 |
| POST | `/posts` | 发布匿名帖 |
| POST | `/posts/:id/like` | 点赞 |
| DELETE | `/posts/:id` | 删帖 |
| POST | `/sports/matches` | 发布匹配 |
| POST | `/mood/check-in` | 心情打卡 |

**共计**: 30个接口 (13公开 + 17需认证)
