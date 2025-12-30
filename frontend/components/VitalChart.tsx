'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { generateMockRecords } from '@/lib/mockData'
import type { MedicalRecord } from '@/types'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'

interface VitalChartProps {
  patientId: string
}

export function VitalChart({ patientId }: VitalChartProps) {
  const [records, setRecords] = useState<MedicalRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [useMockData, setUseMockData] = useState(false)

  useEffect(() => {
    async function loadRecords() {
      try {
        const data = await api.getMedicalRecords(patientId)

        if (data.length === 0) {
          // 如果后端返回空数据，使用模拟数据
          setUseMockData(true)
          setRecords(generateMockRecords(patientId))
        } else {
          // 反转数组，使时间从旧到新排列（适合图表展示）
          setRecords(data.reverse())
        }
      } catch (error) {
        console.error('Failed to load records:', error)
        // 发生错误时使用模拟数据
        setUseMockData(true)
        setRecords(generateMockRecords(patientId))
      } finally {
        setLoading(false)
      }
    }

    loadRecords()
  }, [patientId])

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="text-gray-500">加载中...</div>
      </div>
    )
  }

  // 准备图表数据
  const chartData = records.map((record) => ({
    date: new Date(record.assessment_time).toLocaleDateString('zh-CN'),
    收缩压: record.systolic_blood_pressure,
    舒张压: record.diastolic_pressure,
    糖化血红蛋白: record.hba1c ? record.hba1c * 10 : null, // 放大10倍便于显示
    LDL: record.ldl_c,
  }))

  return (
    <div className="space-y-6">
      {/* 模拟数据提示 */}
      {useMockData && (
        <div className="rounded-md bg-orange-50 p-3 text-sm text-orange-800">
          正在使用模拟数据演示（后端暂无数据）
        </div>
      )}

      {/* 血压趋势 */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">血压趋势</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" fontSize={12} />
            <YAxis fontSize={12} />
            <Tooltip />
            <Legend />
            {/* 正常范围参考线 */}
            <ReferenceLine y={140} stroke="#ef4444" strokeDasharray="3 3" />
            <ReferenceLine y={90} stroke="#ef4444" strokeDasharray="3 3" />
            <Line
              type="monotone"
              dataKey="收缩压"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="舒张压"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
        <p className="mt-2 text-xs text-gray-500">
          参考范围：收缩压 &lt; 140 mmHg，舒张压 &lt; 90 mmHg
        </p>
      </div>

      {/* 糖化血红蛋白趋势 */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">
          糖化血红蛋白 (HbA1c)
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" fontSize={12} />
            <YAxis fontSize={12} />
            <Tooltip />
            <Legend />
            <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" />
            <Line
              type="monotone"
              dataKey="糖化血红蛋白"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
        <p className="mt-2 text-xs text-gray-500">
          参考范围：&lt; 7.0%（图中显示为 &lt; 70）
        </p>
      </div>

      {/* 历史记录表格 */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">历史记录</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left font-medium text-gray-500">
                  检查时间
                </th>
                <th className="px-4 py-2 text-left font-medium text-gray-500">
                  血压
                </th>
                <th className="px-4 py-2 text-left font-medium text-gray-500">
                  HbA1c
                </th>
                <th className="px-4 py-2 text-left font-medium text-gray-500">
                  LDL-C
                </th>
                <th className="px-4 py-2 text-left font-medium text-gray-500">
                  风险等级
                </th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {records.reverse().map((record) => (
                <tr key={record.id} className="hover:bg-gray-50">
                  <td className="px-4 py-2 text-gray-900">
                    {new Date(record.assessment_time).toLocaleString('zh-CN')}
                  </td>
                  <td className="px-4 py-2 text-gray-700">
                    {record.systolic_blood_pressure}/{record.diastolic_pressure}
                  </td>
                  <td className="px-4 py-2 text-gray-700">
                    {record.hba1c ? `${record.hba1c}%` : '-'}
                  </td>
                  <td className="px-4 py-2 text-gray-700">
                    {record.ldl_c || '-'}
                  </td>
                  <td className="px-4 py-2">
                    <span
                      className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${
                        record.risk_level === '极高危'
                          ? 'bg-red-100 text-red-800'
                          : record.risk_level === '高危'
                            ? 'bg-orange-100 text-orange-800'
                            : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {record.risk_level}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
