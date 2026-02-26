import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import type { Symptom, PredictionResult, SymptomRecord } from '@/types'

export const useSymptomsStore = defineStore('symptoms', () => {
  // State
  const availableSymptoms = ref<Symptom[]>([])
  const selectedSymptoms = ref<string[]>([])
  const predictionResult = ref<PredictionResult | null>(null)
  const history = ref<SymptomRecord[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  async function fetchAvailableSymptoms() {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/symptoms/available/')
      availableSymptoms.value = response.data.symptoms || response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to load symptoms'
    } finally {
      loading.value = false
    }
  }

  async function submitSymptoms(
    symptoms: string[],
    generateInsights = true,
    options: {
      duration_days?: number
      severity?: number
      on_medication?: boolean
      patient_age?: number | null
      patient_sex?: string
    } = {}
  ) {
    loading.value = true
    error.value = null
    
    try {
      const payload: any = {
        symptoms,
        duration_days: options.duration_days || 1,
        severity: options.severity || 2,
        on_medication: options.on_medication || false,
        generate_insights: generateInsights
      }
      if (options.patient_age) payload.patient_age = options.patient_age
      if (options.patient_sex) payload.patient_sex = options.patient_sex

      const response = await api.post('/symptoms/submit/', payload)
      
      // Django API returns { prediction: {...}, record_id: ..., requires_referral: ... }
      // Extract the prediction object
      const data = response.data
      predictionResult.value = data.prediction || data
      
      return predictionResult.value
    } catch (err: any) {
      // Handle Django validation errors
      if (err.response?.data) {
        const errorData = err.response.data
        if (typeof errorData === 'object' && !errorData.error) {
          const firstError = Object.values(errorData)[0]
          error.value = Array.isArray(firstError) ? firstError[0] : String(firstError)
        } else {
          error.value = errorData.error || errorData.message || 'Prediction failed'
        }
      } else {
        error.value = 'Prediction failed. Please try again.'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchHistory() {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/symptoms/')
      history.value = response.data.results || response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to load history'
    } finally {
      loading.value = false
    }
  }

  async function deleteRecord(id: number) {
    try {
      await api.delete(`/symptoms/${id}/`)
      // Remove from local history
      history.value = history.value.filter(record => record.id !== id)
      return true
    } catch (err) {
      console.error('Error deleting record:', err)
      return false
    }
  }

  function toggleSymptom(symptom: string) {
    const index = selectedSymptoms.value.indexOf(symptom)
    if (index > -1) {
      selectedSymptoms.value.splice(index, 1)
    } else {
      selectedSymptoms.value.push(symptom)
    }
  }

  function clearSelection() {
    selectedSymptoms.value = []
    predictionResult.value = null
  }

  return {
    availableSymptoms,
    selectedSymptoms,
    predictionResult,
    history,
    loading,
    error,
    fetchAvailableSymptoms,
    submitSymptoms,
    fetchHistory,
    deleteRecord,
    toggleSymptom,
    clearSelection
  }
})
