# 智能慢病管理系统

<div align="center">

基于 AI 的慢病管理平台（SaaS 工作台）
专为家庭医生在 PC 桌面端使用设计

**[中文文档]** | [English](./README.en.md)

</div>

---

## 📋 项目简介

本项目是一个智能化的慢性病管理平台，通过大屏仪表盘形式，深度分析患者长期的生化检查数据。医生可以在一屏内对比多项生化指标，左侧查看数据图表，右侧实时与 AI 对话分析。

### 核心价值

- **高密度信息展示**: 医生可在一屏内对比多项生化指标
- **分屏协作**: 左侧查看数据图表，右侧实时与 AI 对话分析
- **批量管理**: 提供强大的表格视图来管理患者队列
- **AI 驱动**: 使用 DeepSeek 进行自然语言查询和医学分析

---

## 🏗️ 系统架构 (三层架构)

```
┌─────────────────────────────────────────────────────────┐
│  应用层 (Frontend)                                       │
│  Next.js 14+ | TypeScript | Shadcn UI | Tailwind        │
└───────────────────────┬─────────────────────────────────┘
                        │ REST API
┌───────────────────────┴─────────────────────────────────┐
│  大脑层 (Backend)                                        │
│  FastAPI | LlamaIndex | DeepSeek | Text-to-SQL         │
└───────────────────────┬─────────────────────────────────┘
                        │ SQL
┌───────────────────────┴─────────────────────────────────┐
│  数据层 (Database)                                       │
│  Neon PostgreSQL (Serverless)                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 前置要求

- **Node.js**: >= 18.0.0
- **Python**: >= 3.10
- **Poetry**: Python 包管理器
- **Neon 账号**: 用于 PostgreSQL 数据库
- **DeepSeek API Key**: 用于 AI 功能

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd mutli-medicaldata
```

### 2. 后端配置

#### 2.1 安装依赖

```bash
cd backend
poetry install
```

#### 2.2 配置环境变量

复制 `.env.example` 并重命名为 `.env`，然后填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Neon PostgreSQL 数据库配置
NEON_DB_URL=postgresql+psycopg2://user:password@host/database?sslmode=require

# 应用配置
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# CORS 配置（前端地址）
ALLOWED_ORIGINS=http://localhost:3000
```

#### 2.3 运行后端

```bash
# 开发模式
poetry run python -m app.main

# 或使用 uvicorn
poetry run uvicorn app.main:app --reload
```

后端将运行在 `http://localhost:8000`

API 文档：`http://localhost:8000/docs`

### 3. 前端配置

#### 3.1 安装依赖

```bash
cd frontend
npm install
# 或
pnpm install
```

#### 3.2 配置环境变量

复制 `.env.example` 并重命名为 `.env.local`：

```bash
cp .env.example .env.local
```

编辑 `.env.local` 文件：

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

#### 3.3 运行前端

```bash
npm run dev
# 或
pnpm dev
```

前端将运行在 `http://localhost:3000`

---

## 📚 技术栈

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 核心语言 |
| FastAPI | 0.115+ | Web 框架 |
| LlamaIndex | 0.12+ | AI 编排框架 |
| DeepSeek | V3/R1 | 大语言模型 |
| SQLAlchemy | 2.0+ | ORM |
| PostgreSQL (Neon) | - | 数据库 |
| Poetry | - | 依赖管理 |

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 15+ | React 框架 (App Router) |
| TypeScript | 5+ | 类型系统 |
| Shadcn UI | - | UI 组件库 |
| Tailwind CSS | 3.4+ | 样式框架 |
| Recharts | 2.14+ | 图表库 |
| TanStack Table | 8.20+ | 表格逻辑 |
| Zustand | 5+ | 状态管理 |
| Axios | - | HTTP 客户端 |

---

## 📁 项目结构

```
mutli-medicaldata/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── agent.py    # AI 对话接口
│   │   │   └── patients.py # 患者数据接口
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 环境配置
│   │   │   └── database.py # 数据库连接
│   │   ├── models/         # 数据库模型
│   │   │   └── models.py   # SQLAlchemy 模型
│   │   ├── schemas/        # Pydantic Schema
│   │   │   └── schemas.py  # 请求/响应模型
│   │   ├── services/       # 业务逻辑
│   │   │   └── text_to_sql.py # Text-to-SQL 服务
│   │   └── main.py         # 应用入口
│   ├── pyproject.toml      # Poetry 配置
│   └── .env.example        # 环境变量模板
│
├── frontend/               # 前端代码
│   ├── app/
│   │   ├── (dashboard)/    # Dashboard 布局
│   │   │   ├── layout.tsx  # Dashboard 布局组件
│   │   │   └── patients/   # 患者管理页面
│   │   │       ├── page.tsx       # 患者列表
│   │   │       └── [id]/page.tsx  # 患者详情
│   │   ├── layout.tsx      # 根布局
│   │   ├── page.tsx        # 首页
│   │   └── globals.css     # 全局样式
│   ├── components/         # React 组件
│   │   ├── Sidebar.tsx     # 侧边栏导航
│   │   ├── Header.tsx      # 顶部导航
│   │   ├── VitalChart.tsx  # 生化指标图表
│   │   └── AIChat.tsx      # AI 对话组件
│   ├── lib/
│   │   ├── api.ts          # API 客户端
│   │   └── utils.ts        # 工具函数
│   ├── types/
│   │   └── index.ts        # TypeScript 类型定义
│   ├── package.json        # 项目配置
│   ├── tsconfig.json       # TypeScript 配置
│   └── .env.example        # 环境变量模板
│
└── CLAUDE.md               # 项目白皮书
```

---

## 🔑 核心功能

### 1. AI 对话分析 (`POST /api/agent/chat`)

- 接收自然语言查询（如："这位患者最近的血压趋势如何？"）
- 自动生成 SQL 查询 Neon 数据库
- 返回 AI 分析结果和生成的 SQL（调试用）
- **安全保障**: SQL Guardrails 确保只执行 SELECT 查询

### 2. 患者管理 (`GET /api/patients/{doctor_id}`)

- 获取医生名下的患者列表
- 支持搜索、筛选、分页

### 3. 医疗记录查询 (`GET /api/records/{patient_id}`)

- 获取患者历史医疗记录
- 用于前端绘制趋势图表

### 4. 数据可视化

- 血压趋势图（折线图 + 正常范围参考线）
- 糖化血红蛋白趋势图
- 历史记录详细表格

---

## 🛡️ 安全规范

### 敏感信息管理

⚠️ **重要**: 所有 API Key、数据库密码、Secret Key **绝对不能**出现在代码中！

- 本地开发：所有机密信息存储在 `.env` 文件中
- `.env` 文件已加入 `.gitignore`，不会提交到 Git
- 这是医疗项目，日志中严禁打印患者真实姓名和完整身份证号

### SQL 安全防护 (Guardrails)

- **Read-Only**: 生成的 SQL 必须是 `SELECT` 语句
- **禁止操作**: `DROP`, `DELETE`, `UPDATE`, `INSERT` 等
- **强制限制**: 所有查询必须包含 `LIMIT 100`

---

## 🎨 UI/UX 设计规范

### 桌面端布局原则

- **整体结构**: "侧边栏 + 顶部导航 + 内容区"
- **分屏交互**:
  - 左侧 (60%): 复杂图表 + 数据表格
  - 右侧 (40%): AI 助手对话窗口
- **视觉密度**: High Density（高密度信息展示）
- **主题**: 医疗蓝/白配色，高危数据红色高亮

---

## 📊 数据库架构

### 表 A: `patients` (患者信息)

| 字段 | 类型 | 说明 |
|------|------|------|
| id_number | VARCHAR (PK) | 患者唯一标识（身份证号） |
| name | VARCHAR | 姓名 |
| doctor | VARCHAR | 责任医生 |

### 表 B: `medical_records` (检查记录)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL (PK) | 自增主键 |
| id_number | VARCHAR (FK) | 患者身份证号 |
| assessment_time | TIMESTAMP | 检查时间（关键时序字段） |
| systolic_blood_pressure | NUMERIC | 收缩压 |
| diastolic_pressure | NUMERIC | 舒张压 |
| hba1c | NUMERIC | 糖化血红蛋白 |
| ldl_c | NUMERIC | 低密度脂蛋白（可为空） |
| risk_level | VARCHAR | 风险等级（低危/高危/极高危） |

---

## 🧪 开发规范

### Python 代码规范

- 遵循 PEP 8
- 所有函数必须包含 Type Hints
- 复杂逻辑需要 Google Style Docstring
- 使用 `async/await` 处理 I/O 操作
- 使用 `poetry` 管理依赖
- 使用 `black` 和 `isort` 格式化代码

### TypeScript 代码规范

- 严格模式（strict mode）
- 所有组件使用 TypeScript
- 使用函数式组件 + Hooks
- 使用 Tailwind CSS（禁止内联样式）

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

[MIT License](LICENSE)

---

## 👥 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。

---

**Built with ❤️ for better chronic disease management**
