# 前端技术栈

- **Framework**: Next.js 14+ (App Router 模式)。
- **Language**: TypeScript (严格模式)。
- **UI Component**: Shadcn UI (基于 Radix UI)。
- **Styling**: Tailwind CSS。
- **Data Fetching**: SWR 或 TanStack Query (用于自动轮询和缓存)。
- **Charts**: Recharts (专为 React 设计，适合移动端)。


# 桌面端增强库
- **Table Logic**: `@tanstack/react-table` 
  - *原因*: 桌面端需要处理复杂的患者列表（排序、过滤、分页），这是处理 Headless Table 的行业标准。
- **State Management**: `Zustand` (可选)
  - *原因*: 桌面端交互复杂（比如在左侧选中患者，右侧聊天框上下文要变），需要全局状态管理。