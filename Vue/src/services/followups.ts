import api from './api'
import type { FollowUp, FollowUpResponse } from '@/types'

export const followupService = {
  // Get all follow-ups for current user
  async getFollowUps(status?: string): Promise<FollowUp[]> {
    const params: any = {}
    if (status) params.status = status
    
    const response = await api.get('/followups/', { params })
    return response.data
  },

  // Get pending follow-ups only
  async getPendingFollowUps(): Promise<FollowUp[]> {
    const response = await api.get('/followups/pending/')
    return response.data
  },

  // Submit response to follow-up
  async respondToFollowUp(id: string, response: FollowUpResponse): Promise<FollowUp> {
    const res = await api.post(`/followups/${id}/respond/`, response)
    return res.data.followup
  },

  // Staff review of follow-up (staff only)
  async reviewFollowUp(
    id: string,
    reviewNotes: string,
    requiresAppointment: boolean
  ): Promise<FollowUp> {
    const response = await api.post(`/followups/${id}/review/`, {
      review_notes: reviewNotes,
      requires_appointment: requiresAppointment
    })
    return response.data.followup
  },

  // Get follow-ups needing review (staff only)
  async getNeedsReview(): Promise<FollowUp[]> {
    const response = await api.get('/followups/needs-review/')
    return response.data
  }
}
