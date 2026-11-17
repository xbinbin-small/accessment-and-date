import type { MedicalRecord, Patient } from '@/types'

export const MOCK_PATIENTS: Patient[] = [
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

/** 在后端无记录时生成一组用于图表回退的检查数据 */
export const generateMockRecords = (patientId: string): MedicalRecord[] =>
  [0, 1, 2, 3, 4, 5].map((index) => ({
    id: index + 1,
    id_number: patientId,
    assessment_time: new Date(Date.now() - index * 30 * 24 * 60 * 60 * 1000).toISOString(),
    systolic_blood_pressure: 150 - index * 3,
    diastolic_pressure: 95 - index * 2,
    hba1c: Number((7.5 - index * 0.2).toFixed(1)),
    ldl_c: Number((2.5 + (index % 3) * 0.3).toFixed(1)),
    risk_level: index < 2 ? '高危' : '低危',
  }))
