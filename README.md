# 康伴生活 (UniHealth)

> 大学生校园健康一站式服务平台

## 项目结构

```
KangBan-backend/   # Flask 后端
KangBan-vue3/       # Vue 3 前端
```

## 快速启动

### 后端

```bash
cd KangBan-backend
python -m venv venv 
source venv/Scripts/activate   # cd KangBan-backend 并在 Git Bash 激活虚拟环境
pip install -r requirements.txt //只用在第一次运行
.\venv\Scripts\Activate.ps1  #cd D:\软件工程项目\KangBanLife\KangBan-backend 并在 Windows PowerShell 激活虚拟环境
cp .env.example .env            # 编辑 .env 填入你的 API 密钥
python seed_data.py             # 初始化数据库和种子数据
python app.py                   # 启动在 http://localhost:5000
```

### 前端

```bash
cd KangBan-vue3
npm install //只用在第一次运行
npm run dev                     # 启动在 http://localhost:3000
```

## 配置说明

| 配置项 | 文件 | 说明 |
|--------|------|------|
| ARK_API_KEY | `.env` | 火山引擎 ARK API 密钥（不填则 AI 聊天回退到规则引擎） |
| ARK_ENDPOINT_ID | `.env` | 火山引擎端点 ID |
| JWT_SECRET_KEY | `.env` | JWT 签名密钥（生产环境务必更换） |
| 高德地图 key | `index.html` | 高德地图 JS API 密钥（替换 `您的高德地图API密钥`） |

## 详细文档

参见 `plan/` 目录中的设计文档和评审材料。
