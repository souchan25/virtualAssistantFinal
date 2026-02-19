<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center space-x-4">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-14 w-14 object-contain">
            <div>
              <h1 class="text-2xl font-heading font-bold text-cpsu-green">CPSU Health Clinic</h1>
              <p class="text-sm text-gray-600">Follow-up Management</p>
            </div>
          </div>
          <button @click="$router.push('/staff')" class="btn-outline !py-2 !px-4">Back to Dashboard</button>
        </div>
        <!-- Navigation Menu -->
        <div class="flex items-center space-x-4 border-t pt-3">
          <router-link to="/staff" class="text-gray-700 hover:text-cpsu-green font-medium">
            📊 Dashboard
          </router-link>
          <router-link to="/staff/emergencies" class="text-gray-700 hover:text-cpsu-green font-medium">
            🚨 Emergencies
          </router-link>
          <router-link to="/staff/students" class="text-gray-700 hover:text-cpsu-green font-medium">
            👥 Students
          </router-link>
          <router-link to="/staff/prescribe" class="text-gray-700 hover:text-cpsu-green font-medium">
            💊 Prescribe
          </router-link>
          <router-link to="/staff/adherence" class="text-gray-700 hover:text-cpsu-green font-medium">
            📈 Adherence
          </router-link>
          <router-link to="/staff/followups" class="text-cpsu-green font-semibold">
            📋 Follow-Ups
          </router-link>
          <router-link to="/staff/analytics" class="text-gray-700 hover:text-cpsu-green font-medium">
            📉 Analytics
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Follow-up Management</h2>
        <p class="text-gray-600">Track and respond to student follow-ups</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card-bordered bg-white">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Needs Review</h3>
          <p class="text-3xl font-bold text-red-600">
            {{ followups.filter(f => ['needs_review', 'pending'].includes(f.status)).length }}
          </p>
        </div>
        <div class="card-bordered bg-white">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Pending Response</h3>
          <p class="text-3xl font-bold text-yellow-600">{{ followups.filter(f => f.status === 'pending').length }}</p>
        </div>
        <div class="card-bordered bg-white">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Reviewed</h3>
          <p class="text-3xl font-bold text-green-600">{{ followups.filter(f => f.status === 'reviewed').length }}</p>
        </div>
        <div class="card-bordered bg-white">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Total Follow-ups</h3>
          <p class="text-3xl font-bold text-cpsu-green">{{ followups.length }}</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-cpsu-green"></div>
        <p class="mt-4 text-gray-600">Loading follow-ups...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Follow-ups List -->
      <div v-else class="space-y-4">
        <div v-if="followups.length === 0" class="text-center py-12 bg-white rounded-lg border-2 border-gray-200">
          <p class="text-gray-500 text-lg">No follow-ups to display</p>
        </div>

        <div
          v-for="followup in followups"
          :key="followup.id"
          class="bg-white rounded-lg shadow-sm border-2 hover:border-cpsu-green transition-colors"
          :class="{
            'border-red-300': followup.status === 'needs_review',
            'border-yellow-300': followup.status === 'pending',
            'border-green-300': followup.status === 'reviewed',
            'border-gray-200': !['needs_review', 'pending', 'reviewed'].includes(followup.status)
          }"
        >
          <div class="p-6">
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h3 class="text-xl font-bold text-gray-900">{{ followup.student_name }}</h3>
                  <span
                    class="px-3 py-1 rounded-full text-sm font-medium"
                    :class="{
                      'bg-red-100 text-red-700': followup.status === 'needs_review',
                      'bg-yellow-100 text-yellow-700': followup.status === 'pending',
                      'bg-green-100 text-green-700': followup.status === 'reviewed'
                    }"
                  >
                    {{ formatStatus(followup.status) }}
                  </span>
                </div>
                <p class="text-gray-600">{{ followup.student_school_id }} • {{ followup.student_department }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-gray-600">Scheduled: {{ formatDate(followup.scheduled_date) }}</p>
                <p v-if="followup.completed_at" class="text-sm text-green-600">Completed: {{ formatDate(followup.completed_at) }}</p>
              </div>
            </div>

            <!-- Original Condition & Detailed Description -->
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
              <p class="text-sm text-gray-600 mb-2"><strong>Original Condition:</strong> {{ followup.original_condition || followup.symptom_disease || 'N/A' }}</p>
              <p class="text-sm text-gray-600 mb-2">
                <strong>Submitted:</strong> {{ formatDate(followup.created_at) }}
              </p>

              <!-- Detailed Symptom Description -->
              <div v-if="followup.symptom_details" class="mt-3 pt-3 border-t border-gray-200 space-y-2">
                <p class="text-sm text-gray-700">
                  <strong>Symptoms:</strong>
                  <span v-for="(s, i) in followup.symptom_details.symptoms" :key="i" class="inline-block px-2 py-0.5 bg-white border border-gray-300 rounded-full text-xs mr-1 mt-1">
                    {{ s.replace('_', ' ') }}
                  </span>
                </p>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <p><strong>Severity:</strong> {{ followup.symptom_details.severity }}</p>
                  <p><strong>Duration:</strong> {{ followup.symptom_details.duration_days }} day(s)</p>
                  <p><strong>Confidence:</strong> {{ followup.symptom_details.confidence_score ? (followup.symptom_details.confidence_score * 100).toFixed(1) + '%' : 'N/A' }}</p>
                  <p><strong>Communicable:</strong> {{ followup.symptom_details.is_communicable ? 'Yes' : 'No' }}</p>
                </div>
                <p v-if="followup.symptom_details.staff_diagnosis" class="text-sm text-blue-700">
                  <strong>Staff Diagnosis:</strong> {{ followup.symptom_details.staff_diagnosis }}
                </p>
                <p v-if="followup.symptom_details.icd10_code" class="text-xs text-gray-500">
                  <strong>ICD-10:</strong> {{ followup.symptom_details.icd10_code }}
                </p>
                <p v-if="followup.symptom_details.requires_referral" class="text-xs text-red-600 font-semibold">
                  ⚠ Referral Required
                </p>
              </div>
            </div>

            <!-- Student Response (if submitted) -->
            <div v-if="followup.student_response" class="bg-blue-50 rounded-lg p-4 mb-4">
              <p class="text-sm font-semibold text-gray-700 mb-2">Student Response:</p>
              <p class="text-sm text-gray-700 mb-2">{{ followup.student_response }}</p>
              <p v-if="followup.response_date" class="text-xs text-gray-600">
                Responded: {{ formatDate(followup.response_date) }}
              </p>
            </div>

            <!-- Staff Notes (if any) -->
            <div v-if="followup.staff_notes" class="bg-green-50 rounded-lg p-4 mb-4">
              <p class="text-sm font-semibold text-gray-700 mb-2">Staff Notes:</p>
              <p class="text-sm text-gray-700 mb-2">{{ followup.staff_notes }}</p>
              <p class="text-xs text-gray-600">By: {{ followup.reviewed_by_name }} on {{ formatDate(followup.reviewed_at) }}</p>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-3 pt-4 border-t">
              <button
                v-if="['needs_review', 'pending'].includes(followup.status)"
                @click="reviewFollowup(followup)"
                class="btn-primary flex-1"
              >
                📝 Review & Add Notes
              </button>
              <button
                v-else
                @click="viewFollowup(followup)"
                class="btn-outline flex-1"
              >
                📄 View Record
              </button>
              <button
                v-if="followup.symptom_record"
                @click="openEditDiagnosis(followup)"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                ✏️ Edit Diagnosis
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Diagnosis Modal -->
      <div v-if="editingFollowup" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[60] p-4" @click="editingFollowup = null">
        <div class="bg-white rounded-lg max-w-lg w-full" @click.stop>
          <div class="bg-blue-600 text-white p-5 rounded-t-lg">
            <h2 class="text-xl font-bold">Edit Final Diagnosis</h2>
            <p class="text-sm opacity-90">{{ editingFollowup.student_name }}</p>
          </div>
          <div class="p-6">
            <div class="mb-4 bg-gray-50 rounded-lg p-4 text-sm">
              <p><strong>AI Prediction:</strong> {{ editingFollowup.symptom_details?.predicted_disease || editingFollowup.original_condition || 'N/A' }}</p>
              <p v-if="editingFollowup.symptom_details"><strong>Symptoms:</strong> {{ editingFollowup.symptom_details.symptoms?.join(', ') }}</p>
            </div>
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Staff Final Diagnosis</label>
              <input v-model="editDiagnosis" type="text" class="input-field w-full" placeholder="Enter corrected diagnosis..." />
              <p class="text-xs text-gray-500 mt-1">This will override the AI prediction as the final diagnosis.</p>
            </div>
            <div class="flex gap-4">
              <button @click="submitDiagnosisEdit" :disabled="diagnosisSubmitting || !editDiagnosis.trim()" class="btn-primary flex-1">
                <span v-if="diagnosisSubmitting">Saving...</span>
                <span v-else>Save Diagnosis</span>
              </button>
              <button @click="editingFollowup = null" class="btn-outline flex-1">Cancel</button>
            </div>
            <p v-if="diagnosisSuccess" class="mt-3 text-sm text-green-600 font-medium">Diagnosis updated successfully!</p>
            <p v-if="diagnosisError" class="mt-3 text-sm text-red-600 font-medium">{{ diagnosisError }}</p>
          </div>
        </div>
      </div>

      <!-- Review Modal -->
      <div v-if="reviewingFollowup" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="closeReview">
        <div class="bg-white rounded-lg max-w-2xl w-full" @click.stop>
          <div class="bg-cpsu-green text-white p-6 rounded-t-lg">
            <h2 class="text-2xl font-bold">Review Follow-up</h2>
            <p class="text-sm opacity-90">{{ reviewingFollowup.student_name }}</p>
          </div>

          <div class="p-6">
            <!-- Original Info -->
            <div class="mb-6">
              <h3 class="font-semibold text-gray-900 mb-2">Original Condition</h3>
              <p class="text-gray-700 text-lg font-medium">{{ reviewingFollowup.original_condition || reviewingFollowup.symptom_disease || 'N/A' }}</p>

              <!-- Detailed description in modal -->
              <div v-if="reviewingFollowup.symptom_details" class="mt-3 bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                <p><strong>Symptoms:</strong>
                  <span v-for="(s, i) in reviewingFollowup.symptom_details.symptoms" :key="i" class="inline-block px-2 py-0.5 bg-white border border-gray-300 rounded-full text-xs mr-1 mt-1">
                    {{ s.replace('_', ' ') }}
                  </span>
                </p>
                <div class="grid grid-cols-2 gap-2">
                  <p><strong>Severity:</strong> {{ reviewingFollowup.symptom_details.severity }}</p>
                  <p><strong>Duration:</strong> {{ reviewingFollowup.symptom_details.duration_days }} day(s)</p>
                  <p><strong>Confidence:</strong> {{ reviewingFollowup.symptom_details.confidence_score ? (reviewingFollowup.symptom_details.confidence_score * 100).toFixed(1) + '%' : 'N/A' }}</p>
                  <p><strong>Communicable:</strong> {{ reviewingFollowup.symptom_details.is_communicable ? 'Yes' : 'No' }}</p>
                </div>
                <p v-if="reviewingFollowup.symptom_details.staff_diagnosis" class="text-blue-700">
                  <strong>Staff Diagnosis:</strong> {{ reviewingFollowup.symptom_details.staff_diagnosis }}
                </p>
              </div>
            </div>

            <!-- Student Response -->
            <div v-if="reviewingFollowup.student_response" class="mb-6 bg-blue-50 p-4 rounded-lg">
              <h3 class="font-semibold text-gray-900 mb-2">Student Response</h3>
              <p class="text-gray-700">{{ reviewingFollowup.student_response }}</p>
            </div>

            <!-- Staff Notes Input -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Staff Notes & Recommendations</label>
              <textarea
                v-model="staffNotes"
                rows="5"
                class="input-field w-full"
                placeholder="Add your clinical notes, recommendations, or next steps..."
              ></textarea>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-4">
              <button @click="submitReview" :disabled="submitting || !staffNotes.trim()" class="btn-primary flex-1">
                <span v-if="submitting">Submitting...</span>
                <span v-else>✅ Submit Review</span>
              </button>
              <button @click="closeReview" class="btn-outline flex-1">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

// State
const followups = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const reviewingFollowup = ref<any>(null)
const staffNotes = ref('')
const submitting = ref(false)

// Edit Diagnosis State
const editingFollowup = ref<any>(null)
const editDiagnosis = ref('')
const diagnosisSubmitting = ref(false)
const diagnosisSuccess = ref(false)
const diagnosisError = ref<string | null>(null)

// Methods
const fetchFollowups = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await api.get('/followups/needs-review/')
    console.log('FollowUps API Response:', response.data)
    followups.value = response.data || []
    console.log('Follow-ups loaded:', followups.value.length)
  } catch (err: any) {
    error.value = err.response?.data?.error || err.message || 'Failed to load follow-ups'
    console.error('Error fetching follow-ups:', err)
    console.error('Error details:', err.response?.data)
  } finally {
    loading.value = false
  }
}

const reviewFollowup = (followup: any) => {
  reviewingFollowup.value = followup
  staffNotes.value = ''
}

const viewFollowup = (followup: any) => {
  reviewingFollowup.value = followup
  staffNotes.value = followup.staff_notes || ''
}

const closeReview = () => {
  reviewingFollowup.value = null
  staffNotes.value = ''
}

const submitReview = async () => {
  if (!staffNotes.value.trim() || !reviewingFollowup.value) return

  submitting.value = true
  try {
    await api.post(`/followups/${reviewingFollowup.value.id}/review/`, {
      review_notes: staffNotes.value
    })
    await fetchFollowups()
    closeReview()
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to submit review'
    console.error('Error submitting review:', err)
  } finally {
    submitting.value = false
  }
}

const openEditDiagnosis = (followup: any) => {
  editingFollowup.value = followup
  editDiagnosis.value = followup.symptom_details?.staff_diagnosis || ''
  diagnosisSuccess.value = false
  diagnosisError.value = null
}

const submitDiagnosisEdit = async () => {
  if (!editDiagnosis.value.trim() || !editingFollowup.value) return

  diagnosisSubmitting.value = true
  diagnosisSuccess.value = false
  diagnosisError.value = null

  try {
    await api.patch(`/symptoms/${editingFollowup.value.symptom_record}/diagnosis/`, {
      staff_diagnosis: editDiagnosis.value.trim()
    })
    if (editingFollowup.value.symptom_details) {
      editingFollowup.value.symptom_details.staff_diagnosis = editDiagnosis.value.trim()
      editingFollowup.value.symptom_details.final_diagnosis = editDiagnosis.value.trim()
    }
    editingFollowup.value.original_condition = editDiagnosis.value.trim()
    diagnosisSuccess.value = true
    setTimeout(() => {
      editingFollowup.value = null
    }, 1200)
  } catch (err: any) {
    diagnosisError.value = err.response?.data?.error || 'Failed to update diagnosis'
    console.error('Error updating diagnosis:', err)
  } finally {
    diagnosisSubmitting.value = false
  }
}

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return 'N/A'
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    'needs_review': 'Needs Review',
    'pending': 'Pending Response',
    'reviewed': 'Reviewed',
    'completed': 'Completed'
  }
  return statusMap[status] || status
}

onMounted(() => {
  fetchFollowups()
})
</script>
