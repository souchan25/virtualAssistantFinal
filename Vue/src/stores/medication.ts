import { defineStore } from 'pinia'
import { medicationService } from '@/services/medications'
import type { Medication, MedicationLog, MedicationCreateData, AdherenceStats } from '@/types'

interface MedicationState {
  medications: Medication[]
  todaysLogs: MedicationLog[]
  adherenceStats: AdherenceStats | null
  loading: boolean
  error: string | null
}

export const useMedicationStore = defineStore('medication', {
  state: (): MedicationState => ({
    medications: [],
    todaysLogs: [],
    adherenceStats: null,
    loading: false,
    error: null
  }),

  getters: {
    activeMedications: (state) => {
      if (!Array.isArray(state.medications)) return []
      return state.medications.filter(m => m.is_active)
    },
    
    inactiveMedications: (state) => {
      if (!Array.isArray(state.medications)) return []
      return state.medications.filter(m => !m.is_active)
    },
    
    pendingLogs: (state) => {
      if (!Array.isArray(state.todaysLogs)) return []
      return state.todaysLogs.filter(log => log.status === 'pending')
    },
    
    takenLogs: (state) => {
      if (!Array.isArray(state.todaysLogs)) return []
      return state.todaysLogs.filter(log => log.status === 'taken')
    },
    
    missedLogs: (state) => {
      if (!Array.isArray(state.todaysLogs)) return []
      return state.todaysLogs.filter(log => log.status === 'missed')
    },
    
    overdueLogs: (state) => {
      if (!Array.isArray(state.todaysLogs)) return []
      return state.todaysLogs.filter(log => log.is_overdue && log.status === 'pending')
    },
    
    todaysAdherence: (state) => {
      if (!Array.isArray(state.todaysLogs) || state.todaysLogs.length === 0) return 100
      const taken = state.todaysLogs.filter(log => log.status === 'taken').length
      return Math.round((taken / state.todaysLogs.length) * 100)
    }
  },

  actions: {
    async fetchMedications(studentId?: number) {
      this.loading = true
      this.error = null
      
      try {
        if (studentId) {
          this.medications = await medicationService.getMedicationsByStudent(studentId)
        } else {
          this.medications = await medicationService.getMedications()
        }
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to fetch medications'
        console.error('Error fetching medications:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchTodaysLogs() {
      this.loading = true
      this.error = null
      
      try {
        this.todaysLogs = await medicationService.getTodaysLogs()
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to fetch today\'s logs'
        console.error('Error fetching today\'s logs:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchAdherence(studentId?: number, startDate?: string, endDate?: string) {
      this.loading = true
      this.error = null
      
      try {
        this.adherenceStats = await medicationService.getAdherence(studentId, startDate, endDate)
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to fetch adherence statistics'
        console.error('Error fetching adherence:', error)
      } finally {
        this.loading = false
      }
    },

    async createMedication(data: MedicationCreateData) {
      this.loading = true
      this.error = null
      
      try {
        const medication = await medicationService.createMedication(data)
        this.medications.push(medication)
        return medication
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to create medication'
        console.error('Error creating medication:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async markLogAsTaken(logId: number, notes?: string) {
      this.loading = true
      this.error = null
      
      try {
        const updatedLog = await medicationService.markLogAsTaken(logId, notes)
        
        // Update log in todaysLogs
        const index = this.todaysLogs.findIndex(log => log.id === logId)
        if (index !== -1) {
          this.todaysLogs[index] = updatedLog
        }
        
        return updatedLog
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to mark medication as taken'
        console.error('Error marking medication as taken:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})
