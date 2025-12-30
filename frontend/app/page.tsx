import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-blue-900 mb-4">
          智能慢病管理系统
        </h1>
        <p className="text-lg text-blue-700 mb-8">
          基于 AI 的慢病管理平台 - 专为家庭医生设计
        </p>
        <div className="space-y-2 text-sm text-blue-600 mb-8">
          <p>✓ 后端：FastAPI + LlamaIndex + DeepSeek</p>
          <p>✓ 前端：Next.js 14+ + TypeScript + Shadcn UI</p>
          <p>✓ 数据库：Neon PostgreSQL</p>
        </div>

        {/* 添加导航按钮 */}
        <div className="flex gap-4 justify-center">
          <Link
            href="/patients"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            进入系统
          </Link>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-lg font-medium hover:bg-blue-50 transition-colors"
          >
            API 文档
          </a>
        </div>
      </div>
    </div>
  )
}
