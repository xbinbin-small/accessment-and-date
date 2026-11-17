import axios from 'axios'
import type { ChatRequest, ChatResponse, MedicalRecord, Patient } from '@/types'

const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000',
})

interface DoctorSummary {
  doctor_id: string
  patient_count: number
}

interface PatientListResponse {
  total: number
  offset: number
  limit: number
  patients: Patient[]
}

/** 获取医生列表及各自的患者数量 */
const getAllDoctors = async (): Promise<DoctorSummary[]> => {
  const { data } = await client.get<DoctorSummary[]>('/api/doctors')
  return data
}

/** 分页获取全部患者 */
const getAllPatients = async (limit = 100, offset = 0): Promise<PatientListResponse> => {
  const { data } = await client.get<PatientListResponse>('/api/patients', {
    params: { limit, offset },
  })
  return data
}

/** 获取某位医生名下的患者 */
const getPatients = async (doctorId: string): Promise<Patient[]> => {
  const { data } = await client.get<Patient[]>(`/api/patients/${encodeURIComponent(doctorId)}`)
  return data
}

/** 获取患者历史检查记录 */
const getMedicalRecords = async (patientId: string): Promise<MedicalRecord[]> => {
  const { data } = await client.get<MedicalRecord[]>(
    `/api/records/${encodeURIComponent(patientId)}`
  )
  return data
}

/** 向 AI 助手发送自然语言问题 */
const chat = async (payload: ChatRequest): Promise<ChatResponse> => {
  const { data } = await client.post<ChatResponse>('/api/agent/chat', payload)
  return data
}

export const api = {
  getAllDoctors,
  getAllPatients,
  getPatients,
  getMedicalRecords,
  chat,
}
