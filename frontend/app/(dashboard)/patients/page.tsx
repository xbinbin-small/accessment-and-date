'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { api } from '@/lib/api'
import type { Patient } from '@/types'

// 模拟数据用于演示
const MOCK_PATIENTS: Patient[] = [
  {
    id_number: '330123199001011234',
    name: '张三',
    doctor: 'doctor_001',
  },
  {
    id_number: '330123199002022345',
    name: '李四',
    doctor: 'doctor_001',
  },
  {
    id_number: '330123199003033456',
    name: '王五',
    doctor: 'doctor_001',
  },
]

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [useMockData, setUseMockData] = useState(false)
  const [dataSource, setDataSource] = useState<string>('未知')
  const [doctors, setDoctors] = useState<Array<{ doctor_id: string; patient_count: number }>>([])
  const [selectedDoctor, setSelectedDoctor] = useState<string>('doctor_001')
  const [viewMode, setViewMode] = useState<'by_doctor' | 'all'>('by_doctor')
  const [totalPatients, setTotalPatients] = useState<number>(0)

  // 加载医生列表
  useEffect(() => {
    async function loadDoctors() {
      try {
        const doctorList = await api.getAllDoctors()
        setDoctors(doctorList)
        console.log(`📋 获取了 ${doctorList.length} 位医生的信息`)
      } catch (err) {
        console.error('获取医生列表失败:', err)
      }
    }
    loadDoctors()
  }, [])

  // 加载患者数据
  useEffect(() => {
    async function loadPatients() {
      try {
        setError(null)
        setLoading(true)

        if (viewMode === 'all') {
          // 管理员视图：查看所有患者
          console.log('🔍 正在请求后端API: /api/patients (所有患者)')
          const response = await api.getAllPatients(100, 0)
          console.log('📥 后端返回数据:', response)

          setTotalPatients(response.total)
          setUseMockData(false)
          setDataSource(`Neon数据库 - 全部患者 (共${response.total}位)`)
          setPatients(response.patients)
        } else {
          // 按医生查看
          console.log(`🔍 正在请求后端API: /api/patients/${selectedDoctor}`)
          const data = await api.getPatients(selectedDoctor)
          console.log('📥 后端返回数据:', data)

          if (data.length === 0) {
            console.log('⚠️ 后端返回空数据，使用模拟数据')
            setUseMockData(true)
            setDataSource('模拟数据（后端返回空）')
            setPatients(MOCK_PATIENTS)
          } else {
            console.log(`✅ 从后端获取了 ${data.length} 位患者的真实数据`)
            setUseMockData(false)
            setDataSource(`Neon数据库 - 医生: ${selectedDoctor}`)
            setPatients(data)
          }
        }
      } catch (err) {
        console.error('❌ Failed to load patients:', err)
        setError('无法连接到后端服务，正在使用模拟数据演示')
        setUseMockData(true)
        setDataSource('模拟数据（连接失败）')
        setPatients(MOCK_PATIENTS)
      } finally {
        setLoading(false)
      }
    }

    loadPatients()
  }, [selectedDoctor, viewMode])

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="text-gray-500">加载中...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">患者管理</h1>
            <p className="mt-1 text-sm text-gray-500">
              {viewMode === 'all' ? `数据库共 ${totalPatients} 位患者` : `共 ${patients.length} 位患者`}
              {useMockData && (
                <span className="ml-2 text-orange-600">
                  （使用模拟数据演示）
                </span>
              )}
            </p>
            <p className="mt-1 text-xs text-gray-400">
              数据来源：<span className={useMockData ? "text-orange-500" : "text-green-600 font-medium"}>{dataSource}</span>
            </p>
          </div>

          {/* 视图切换和医生选择器 */}
          <div className="flex gap-3">
            {/* 视图模式切换 */}
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('by_doctor')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  viewMode === 'by_doctor'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                按医生查看
              </button>
              <button
                onClick={() => setViewMode('all')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  viewMode === 'all'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                查看全部患者
              </button>
            </div>

            {/* 医生选择器 */}
            {viewMode === 'by_doctor' && (
              <select
                value={selectedDoctor}
                onChange={(e) => setSelectedDoctor(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="doctor_001">doctor_001 (演示)</option>
                {doctors.map((doc) => (
                  <option key={doc.doctor_id} value={doc.doctor_id}>
                    {doc.doctor_id} ({doc.patient_count}位患者)
                  </option>
                ))}
              </select>
            )}
          </div>
        </div>

        {error && (
          <div className="mt-4 rounded-md bg-orange-50 p-3 text-sm text-orange-800">
            {error}
          </div>
        )}
      </div>

      <div className="rounded-lg bg-white shadow">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  姓名
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  身份证号
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  责任医生
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {patients.map((patient) => (
                <tr key={patient.id_number} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {patient.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {patient.id_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {patient.doctor}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <Link
                      href={`/patients/${patient.id_number}`}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      查看详情
                    </Link>
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
