// User & Authentication Types
export interface User {
  id: number
  school_id: string
  name: string
  role: 'student' | 'staff' | 'clinic_staff' | 'dev'
  department?: string
  cpsu_address?: string
  year_level?: number
  course?: string
  data_consent_given: boolean
  consent_date?: string | null
  date_joined: string
}

export interface LoginCredentials {
  school_id: string
  password: string
}

export interface RegisterData {
  school_id: string
  password: string
  password_confirm: string
  name: string
  department?: string
  cpsu_address?: string
  year_level?: number
  course?: string
  data_consent_given?: boolean
}

// Symptoms & Prediction Types
export interface Symptom {
  name: string
  display_name?: string
  severity?: number
}

export interface PredictionResult {
  predicted_disease: string
  confidence: number
  confidence_score?: number  // Django API uses confidence_score
  description?: string
  precautions?: string[]
  severity_score?: number
  ml_confidence?: number
  llm_validated?: boolean  // Django API returns llm_validated
  llm_validation?: {
    agrees_with_ml: boolean
    confidence_boost: number
    reasoning?: string
  }
  top_predictions?: Array<{
    disease: string
    confidence: number
  }>
  recommendations?: string[]
  timestamp: string
}

export interface SymptomRecord {
  id: number
  symptoms: string[]
  predicted_disease: string
  staff_diagnosis?: string
  final_diagnosis?: string
  confidence_score: number  // Django uses confidence_score, not confidence
  confidence?: number  // Legacy support
  top_predictions?: Array<{
    disease: string
    confidence: number
  }>
  llm_validated?: boolean
  created_at: string
  description?: string
  precautions?: string[]
}

// Chat Types
export interface ChatMessage {
  id: number
  content: string
  sender: 'user' | 'bot'
  timestamp: string
  metadata?: any
  isError?: boolean
}

export interface ChatSession {
  session_id: string
  created_at: string
}

// Staff Dashboard Types
export interface DashboardStats {
  total_students: number
  active_sessions: number
  total_predictions: number
  common_conditions: Array<{
    disease: string
    count: number
  }>
  recent_activity: Array<{
    student_name: string
    disease: string
    timestamp: string
  }>
}

// Medication Types
export interface Medication {
  id: number
  student: number
  student_name?: string
  name: string
  dosage: string
  frequency: string
  schedule_times: string[]  // ["08:00", "14:00", "20:00"]
  start_date: string
  end_date: string
  instructions?: string
  side_effects?: string
  prescribed_by: number
  prescribed_by_name?: string
  is_active: boolean
  created_at: string
  recent_logs?: MedicationLog[]
  adherence_rate?: number
}

export interface MedicationLog {
  id: number
  medication: number
  medication_name?: string
  scheduled_date: string
  scheduled_time: string
  taken_at?: string | null
  status: 'pending' | 'taken' | 'missed'
  notes?: string
  is_overdue?: boolean
}

export interface MedicationCreateData {
  student_id: number
  name: string
  dosage: string
  frequency: string
  schedule_times: string[]
  start_date: string
  end_date: string
  instructions?: string
  side_effects?: string
}

export interface AdherenceStats {
  total_doses: number
  taken_doses: number
  missed_doses: number
  adherence_percentage: number
  medications: Array<{
    medication_name: string
    adherence_rate: number
  }>
}

// Follow-Up Types
export interface FollowUpSymptomDetails {
  symptoms: string[]
  duration_days: number
  severity: string
  severity_value: number
  predicted_disease: string
  staff_diagnosis: string
  final_diagnosis: string
  confidence_score: number | null
  top_predictions: Array<{ disease: string; confidence: number }> | null
  is_communicable: boolean
  is_acute: boolean
  icd10_code: string
  requires_referral: boolean
  created_at: string | null
}

export interface FollowUp {
  id: string
  symptom_record: number
  student: number
  student_name?: string
  student_school_id?: string
  symptom_disease?: string
  scheduled_date: string
  status: 'pending' | 'completed' | 'overdue' | 'cancelled' | 'reviewed'
  response_date?: string | null
  outcome?: 'improved' | 'same' | 'worse' | 'resolved' | null
  notes?: string
  still_experiencing_symptoms?: boolean | null
  new_symptoms?: string[]
  requires_appointment?: boolean
  review_notes?: string
  is_overdue?: boolean
  days_until_due?: number
  symptom_details?: FollowUpSymptomDetails | null
  created_at: string
}

export interface FollowUpResponse {
  outcome: 'improved' | 'same' | 'worse' | 'resolved'
  notes?: string
  still_experiencing_symptoms: boolean
  new_symptoms?: string[]
}

// API Response Types
export interface ApiResponse<T> {
  data: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
