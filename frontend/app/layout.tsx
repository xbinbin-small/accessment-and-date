import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '智能慢病管理系统',
  description: '基于 AI 的慢病管理平台 - 专为家庭医生设计',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  )
}
