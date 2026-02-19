import { defineStore } from 'pinia'
import { followupService } from '@/services/followups'
import type { FollowUp, FollowUpResponse } from '@/types'

interface FollowUpState {
  followUps: FollowUp[]
  pendingFollowUps: FollowUp[]
  needsReview: FollowUp[]
  loading: boolean
  error: string | null
}

export const useFollowUpStore = defineStore('followup', {
  state: (): FollowUpState => ({
    followUps: [],
    pendingFollowUps: [],
    needsReview: [],
    loading: false,
    error: null
  }),

  getters: {
    overdueFollowUps: (state) => state.pendingFollowUps.filter(f => f.is_overdue),
    upcomingFollowUps: (state) => state.pendingFollowUps.filter(f => !f.is_overdue),
    completedFollowUps: (state) => state.followUps.filter(f =>
      f.status === 'completed' || f.status === 'reviewed'
    ),
    
    totalPending: (state) => state.pendingFollowUps.length,
    totalOverdue: (state) => state.pendingFollowUps.filter(f => f.is_overdue).length
  },

  actions: {
    async fetchFollowUps(status?: string) {
      this.loading = true
      this.error = null
      
      try {
        this.followUps = await followupService.getFollowUps(status)
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to fetch follow-ups'
        console.error('Error fetching follow-ups:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchPendingFollowUps() {
      this.loading = true
      this.error = null
      
      try {
        this.pendingFollowUps = await followupService.getPendingFollowUps()
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to fetch pending follow-ups'
        console.error('Error fetching pending follow-ups:', error)
      } finally {
        this.loading = false
      }
    },

    async respondToFollowUp(id: string, response: FollowUpResponse) {
      this.loading = true
      this.error = null
      
      try {
        const updatedFollowUp = await followupService.respondToFollowUp(id, response)
        
        // Remove from pending list
        this.pendingFollowUps = this.pendingFollowUps.filter(f => f.id !== id)
        
        // Add to completed list
        const index = this.followUps.findIndex(f => f.id === id)
        if (index !== -1) {
          this.followUps[index] = updatedFollowUp
        } else {
          this.followUps.push(updatedFollowUp)
        }
        
        return updatedFollowUp
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to submit response'
        console.error('Error responding to follow-up:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchNeedsReview() {
      this.loading = true
      this.error = null
      
      try {
        this.needsReview = await followupService.getNeedsReview()
      } catch (error: any) {
        this.error = error.response?.data?.error || 'Failed to fetch reviews'
        console.error('Error fetching needs review:', error)
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})
