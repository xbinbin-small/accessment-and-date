# 前端 - 智能慢病管理系统

基于 Next.js 14+ 的桌面端 Web 应用

---

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
# 或
pnpm install
```

### 2. 配置环境变量

复制 `.env.example` 并重命名为 `.env.local`：

```bash
cp .env.example .env.local
```

编辑 `.env.local` 文件：

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. 运行开发服务器

```bash
npm run dev
# 或
pnpm dev
```

访问 `http://localhost:3000`

---

## 📁 项目结构

```
frontend/
├── app/                       # Next.js App Router
│   ├── (dashboard)/          # Dashboard 布局组
│   │   ├── layout.tsx        # Dashboard 布局组件
│   │   └── patients/         # 患者管理
│   │       ├── page.tsx      # 患者列表页
│   │       └── [id]/page.tsx # 患者详情页
│   ├── layout.tsx            # 根布局
│   ├── page.tsx              # 首页
│   └── globals.css           # 全局样式
├── components/               # React 组件
│   ├── Sidebar.tsx          # 侧边栏导航
│   ├── Header.tsx           # 顶部导航
│   ├── VitalChart.tsx       # 生化指标图表
│   └── AIChat.tsx           # AI 对话组件
├── lib/
│   ├── api.ts               # API 客户端
│   └── utils.ts             # 工具函数
├── types/
│   └── index.ts             # TypeScript 类型定义
└── public/                  # 静态资源
```

---

## 🎨 核心功能

### 1. 患者列表页 (`/patients`)

- 展示医生名下的所有患者
- 支持搜索、筛选
- 点击"查看详情"跳转到患者详情页

### 2. 患者详情页 (`/patients/[id]`)

**左右分屏设计**：

- **左侧 (60%)**: 数据可视化
  - 血压趋势图（折线图 + 正常范围参考线）
  - 糖化血红蛋白趋势图
  - 历史记录详细表格

- **右侧 (40%)**: AI 助手
  - 实时对话窗口
  - 支持自然语言提问
  - 展示 AI 分析结果

### 3. 桌面端布局

- **侧边栏**: 固定左侧导航
  - 患者管理
  - 风险预警
  - 数据分析
  - 系统设置

- **顶部导航**: 搜索、通知、用户信息

---

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 15+ | React 框架 (App Router) |
| TypeScript | 5+ | 类型系统 |
| Tailwind CSS | 3.4+ | 样式框架 |
| Shadcn UI | - | UI 组件库 |
| Recharts | 2.14+ | 数据可视化 |
| TanStack Table | 8.20+ | 表格逻辑 |
| Zustand | 5+ | 状态管理 |
| Axios | - | HTTP 客户端 |

---

## 📊 数据流

```
用户交互
   ↓
React 组件
   ↓
API 客户端 (lib/api.ts)
   ↓
后端 FastAPI
   ↓
DeepSeek AI + Neon DB
   ↓
返回数据
   ↓
React 组件更新
   ↓
UI 渲染
```

---

## 🎨 UI/UX 设计原则

### 布局规范

- **密度**: High Density（高密度信息展示）
- **字体**: 正文 14px，标题 16px-24px
- **主题**: 医疗蓝/白配色
- **交互**: 支持快捷键（Enter 发送，Esc 关闭）

### 颜色系统

```css
/* 主色调 */
primary: #3b82f6 (蓝色)

/* 风险等级 */
低危: #10b981 (绿色)
高危: #f59e0b (橙色)
极高危: #ef4444 (红色)

/* 中性色 */
text: #111827
muted: #6b7280
border: #e5e7eb
```

---

## 🔧 开发技巧

### 调试 API 调用

```typescript
// lib/api.ts 中的 API 客户端自动打印请求日志
// 查看浏览器控制台查看详细信息
```

### 使用 TypeScript

```typescript
// types/index.ts 包含所有类型定义
import type { Patient, MedicalRecord } from '@/types'

const patient: Patient = { ... }
```

### Tailwind CSS 工具类

```typescript
import { cn } from '@/lib/utils'

// 合并类名
<div className={cn('base-class', condition && 'conditional-class')} />
```

---

## 📦 构建与部署

### 构建生产版本

```bash
npm run build
# 或
pnpm build
```

### 启动生产服务器

```bash
npm run start
# 或
pnpm start
```

### 静态导出（可选）

如果需要静态网站：

```bash
# 1. 在 next.config.ts 中添加
output: 'export'

# 2. 运行构建
npm run build

# 3. 部署 out/ 目录
```

---

## 🧪 代码质量

### 运行 Lint

```bash
npm run lint
# 或
pnpm lint
```

### TypeScript 类型检查

```bash
npx tsc --noEmit
```

---

## 🚨 常见问题

### 1. API 调用失败

**错误**: `Network Error` 或 `CORS error`

**解决**:
- 检查后端是否运行在 `http://localhost:8000`
- 检查 `.env.local` 中的 `NEXT_PUBLIC_API_BASE_URL`
- 确认后端 CORS 配置正确

### 2. 图表不显示

**错误**: Recharts 警告或空白图表

**解决**:
- 检查数据格式是否正确
- 确认 API 返回的数据不为空
- 查看浏览器控制台错误

### 3. 样式问题

**错误**: Tailwind CSS 类不生效

**解决**:
- 运行 `npm run dev` 重启开发服务器
- 检查 `tailwind.config.ts` 配置
- 确认 `globals.css` 已导入

---

## 📝 开发规范

- 使用 TypeScript 严格模式
- 所有组件使用函数式组件 + Hooks
- 使用 `'use client'` 标记客户端组件
- 使用 Tailwind CSS（禁止内联样式）
- 遵循 Next.js App Router 最佳实践

---

**Built with ❤️ for better healthcare**
