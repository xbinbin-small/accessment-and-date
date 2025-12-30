'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Users, Activity, Settings, BarChart3 } from 'lucide-react'

const sidebarItems = [
  {
    title: '患者管理',
    href: '/patients',
    icon: Users,
  },
  {
    title: '风险预警',
    href: '/alerts',
    icon: Activity,
  },
  {
    title: '数据分析',
    href: '/analytics',
    icon: BarChart3,
  },
  {
    title: '系统设置',
    href: '/settings',
    icon: Settings,
  },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-white">
      {/* Logo */}
      <div className="flex h-16 items-center border-b px-6">
        <h1 className="text-xl font-bold text-blue-900">慢病管理系统</h1>
      </div>

      {/* Navigation */}
      <nav className="space-y-1 p-4">
        {sidebarItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-50 text-blue-900'
                  : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
              )}
            >
              <Icon className="h-5 w-5" />
              {item.title}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
