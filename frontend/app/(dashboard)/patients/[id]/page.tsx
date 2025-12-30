'use client'

import { use, useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { VitalChart } from '@/components/VitalChart'
import { AIChat } from '@/components/AIChat'
import { api } from '@/lib/api'
import { MOCK_PATIENTS } from '@/lib/mockData'
import type { Patient } from '@/types'

export default function PatientDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const [patient, setPatient] = useState<Patient | null>(null)

  useEffect(() => {
    async function loadPatient() {
      try {
        // 尝试从后端获取患者信息
        const patients = await api.getPatients('doctor_001')
        const found = patients.find(p => p.id_number === id)
        if (found) {
          setPatient(found)
        } else {
          // 使用模拟数据
          const mockPatient = MOCK_PATIENTS.find(p => p.id_number === id)
          if (mockPatient) {
            setPatient(mockPatient)
          }
        }
      } catch (error) {
        // 出错时使用模拟数据
        const mockPatient = MOCK_PATIENTS.find(p => p.id_number === id)
        if (mockPatient) {
          setPatient(mockPatient)
        }
      }
    }

    loadPatient()
  }, [id])

  return (
    <div>
      {/* Breadcrumb */}
      <div className="mb-6">
        <Link
          href="/patients"
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4" />
          返回患者列表
        </Link>
        <h1 className="mt-2 text-2xl font-bold text-gray-900">
          {patient ? `患者详情 - ${patient.name}` : '患者详情'}
        </h1>
        <p className="mt-1 text-sm text-gray-500">身份证号：{id}</p>
      </div>

      {/* Split Layout: 左侧图表 60% + 右侧 AI 40% */}
      <div className="grid grid-cols-5 gap-6">
        {/* 左侧：图表区域 (3/5 = 60%) */}
        <div className="col-span-3">
          <VitalChart patientId={id} />
        </div>

        {/* 右侧：AI 对话区域 (2/5 = 40%) */}
        <div className="col-span-2">
          <div className="sticky top-20 h-[calc(100vh-8rem)]">
            <AIChat patientId={id} />
          </div>
        </div>
      </div>
    </div>
  )
}
