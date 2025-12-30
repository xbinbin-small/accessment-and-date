/**
 * 类型定义文件
 */

export interface Patient {
  id_number: string
  name: string
  doctor: string
}

export interface MedicalRecord {
  id: number
  id_number: string
  assessment_time: string
  systolic_blood_pressure: number | null
  diastolic_pressure: number | null
  hba1c: number | null
  ldl_c: number | null
  risk_level: '低危' | '高危' | '极高危'
}

export interface ChatRequest {
  query: string
  patient_id?: string
}

export interface ChatResponse {
  answer: string
  generated_sql?: string
  data?: any[]
}
