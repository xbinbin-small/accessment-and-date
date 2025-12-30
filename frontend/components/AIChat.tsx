'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { Send } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sql?: string
}

interface AIChatProps {
  patientId: string
}

export function AIChat({ patientId }: AIChatProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await api.chat({
        query: userMessage,
        patient_id: patientId,
      })

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.answer,
          sql: response.generated_sql,
        },
      ])
    } catch (error) {
      console.error('Chat failed:', error)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '抱歉，AI 处理出错了。请稍后再试。',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-full flex-col rounded-lg bg-white shadow">
      {/* Header */}
      <div className="border-b px-6 py-4">
        <h3 className="text-lg font-semibold text-gray-900">AI 助手</h3>
        <p className="text-sm text-gray-500">
          询问患者的健康趋势、风险评估等
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center text-gray-400">
            <div className="text-center">
              <p className="mb-2">向 AI 助手提问</p>
              <p className="text-sm">
                例如："这位患者最近的血压趋势如何？"
              </p>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="whitespace-pre-wrap text-sm">{message.content}</p>
                {message.sql && (
                  <details className="mt-2">
                    <summary className="cursor-pointer text-xs text-gray-600">
                      查看生成的 SQL
                    </summary>
                    <pre className="mt-2 overflow-x-auto rounded bg-gray-800 p-2 text-xs text-white">
                      {message.sql}
                    </pre>
                  </details>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="rounded-lg bg-gray-100 px-4 py-2">
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" />
                <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400 delay-75" />
                <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400 delay-150" />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="输入您的问题..."
            className="flex-1 rounded-lg border border-gray-200 px-4 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
            发送
          </button>
        </div>
      </form>
    </div>
  )
}
