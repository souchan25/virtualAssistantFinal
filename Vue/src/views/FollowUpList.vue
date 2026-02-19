<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-3 sm:py-4">
        <div class="flex justify-between items-center">
          <router-link to="/dashboard" class="flex items-center space-x-2 sm:space-x-4 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-10 w-10 sm:h-12 sm:w-12 object-contain">
            <div class="hidden sm:block">
              <h1 class="text-lg sm:text-xl lg:text-2xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs sm:text-sm text-gray-600">Central Philippines State University</p>
            </div>
          </router-link>

          <div class="hidden xl:flex items-center space-x-1 lg:space-x-2">
            <router-link to="/dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Dashboard</router-link>
            <router-link to="/symptom-checker" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Check Symptoms</router-link>
            <router-link to="/medications" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Medications</router-link>
            <router-link to="/followups" class="text-cpsu-green font-semibold px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Follow-Ups</router-link>
            <router-link to="/health-dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Analytics</router-link>
            <router-link to="/chat" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Chat</router-link>
            <router-link to="/history" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">History</router-link>
            <router-link to="/profile" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap">Profile</router-link>
          </div>

          <button @click="mobileMenuOpen = !mobileMenuOpen" class="xl:hidden text-cpsu-green p-2 -mr-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="mobileMenuOpen" class="xl:hidden mt-3 pt-3 pb-2 space-y-2 border-t border-gray-200">
          <router-link to="/dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Dashboard</router-link>
          <router-link to="/symptom-checker" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Check Symptoms</router-link>
          <router-link to="/medications" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Medications</router-link>
          <router-link to="/followups" class="block px-4 py-2 text-cpsu-green font-semibold hover:bg-gray-100 rounded text-sm">Follow-Ups</router-link>
          <router-link to="/health-dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Analytics</router-link>
          <router-link to="/chat" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Chat</router-link>
          <router-link to="/history" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">History</router-link>
          <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Profile</router-link>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Back Button -->
      <router-link to="/dashboard" class="inline-flex items-center text-cpsu-green hover:text-green-700 mb-6">
        <span class="text-2xl mr-2">←</span>
        <span class="font-semibold">Back to Dashboard</span>
      </router-link>

      <h1 class="text-3xl font-bold text-cpsu-green mb-8">📋 My Follow-Ups</h1>

    <!-- Error Alert -->
    <div v-if="followupStore.error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
      <div class="flex items-center">
        <span class="text-red-700">{{ followupStore.error }}</span>
        <button @click="followupStore.clearError" class="ml-auto text-red-500 hover:text-red-700">✕</button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="followupStore.loading && pendingFollowUps.length === 0" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-cpsu-green border-t-transparent"></div>
      <p class="mt-4 text-gray-600">Loading follow-ups...</p>
    </div>

    <!-- Pending Follow-Ups Section -->
    <div v-else class="mb-8">
      <h2 class="text-2xl font-semibold text-cpsu-green mb-4">⏰ Pending Responses</h2>
      
      <!-- Empty State -->
      <div v-if="pendingFollowUps.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
        <p class="text-gray-600">✅ No pending follow-ups! You're all caught up.</p>
      </div>

      <!-- Follow-Up Cards -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="followup in pendingFollowUps"
          :key="followup.id"
          class="bg-white rounded-lg border-2 p-6"
          :class="followup.is_overdue ? 'border-red-500 bg-red-50' : 'border-cpsu-green'"
        >
          <div class="flex items-start justify-between mb-4">
            <div>
              <h3 class="text-xl font-bold text-cpsu-green mb-1">{{ getFollowupDiagnosis(followup) }}</h3>
              <p v-if="followup.symptom_details?.staff_diagnosis" class="text-xs text-blue-600 mb-1">
                ✏️ Staff corrected (AI: {{ followup.symptom_disease }})
              </p>
              <p class="text-sm text-gray-600">
                Due: {{ formatDate(followup.scheduled_date) }}
                <span v-if="followup.is_overdue" class="text-red-600 font-semibold ml-2">
                  ({{ Math.abs(followup.days_until_due!) }} days overdue)
                </span>
                <span v-else class="text-gray-500 ml-2">
                  (in {{ followup.days_until_due }} days)
                </span>
              </p>
            </div>
            <span class="text-3xl">{{ followup.is_overdue ? '⚠️' : '📅' }}</span>
          </div>

          <button
            @click="openResponseModal(followup)"
            class="w-full bg-cpsu-yellow text-cpsu-green font-semibold py-3 px-6 rounded-lg hover:bg-yellow-400 transition"
          >
            Respond Now
          </button>
        </div>
      </div>
    </div>

    <!-- Completed Follow-Ups Section -->
    <div v-if="completedFollowUps.length > 0">
      <h2 class="text-2xl font-semibold text-gray-700 mb-4">✅ Completed Follow-Ups</h2>
      <div class="space-y-4">
        <div
          v-for="followup in completedFollowUps"
          :key="followup.id"
          class="bg-gray-50 rounded-lg border border-gray-300 p-5"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-800 mb-2">
                {{ getFollowupDiagnosis(followup) }}
              </h3>
              <p v-if="followup.symptom_details?.staff_diagnosis" class="text-xs text-blue-600 mb-2">
                ✏️ Staff corrected (AI: {{ followup.symptom_disease }})
              </p>
              <p class="text-sm text-gray-600 mb-2">
                Responded: {{ formatDate(followup.response_date!) }}
              </p>
              <div class="flex items-center gap-2 mb-2">
                <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold"
                      :class="getOutcomeBadgeClass(followup.outcome!)">
                  {{ getOutcomeText(followup.outcome!) }}
                </span>
                <span v-if="followup.requires_appointment" class="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-blue-200 text-blue-800">
                  Appointment Needed
                </span>
              </div>
              <p v-if="followup.notes" class="text-sm text-gray-700 italic mb-3">
                "{{ followup.notes }}"
              </p>

              <!-- Staff Review Feedback -->
              <div v-if="followup.review_notes" class="mt-3 bg-green-50 border-l-4 border-green-500 p-4 rounded-r-lg">
                <p class="text-sm font-semibold text-green-800 mb-1">🩺 Clinic Staff Notes:</p>
                <p class="text-sm text-green-700">{{ followup.review_notes }}</p>
              </div>

              <!-- Symptom Details Summary -->
              <div v-if="followup.symptom_details" class="mt-3 text-xs text-gray-500 flex flex-wrap gap-3">
                <span>Duration: {{ followup.symptom_details.duration_days }} day(s)</span>
                <span>Severity: {{ followup.symptom_details.severity }}</span>
                <span v-if="followup.symptom_details.confidence_score">
                  Confidence: {{ (followup.symptom_details.confidence_score * 100).toFixed(0) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Response Modal -->
    <div
      v-if="showResponseModal && selectedFollowUp"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-lg max-w-2xl w-full p-8">
        <h2 class="text-2xl font-bold text-cpsu-green mb-6">Follow-Up Response</h2>
        
        <div class="mb-6 bg-gray-50 p-4 rounded-lg">
          <p class="font-semibold text-gray-800">Original Condition: {{ selectedFollowUp.symptom_disease }}</p>
          <p class="text-sm text-gray-600">Scheduled: {{ formatDate(selectedFollowUp.scheduled_date) }}</p>
        </div>

        <form @submit.prevent="submitResponse">
          <!-- Outcome Selection -->
          <div class="mb-6">
            <label class="block text-gray-700 font-semibold mb-2">
              How are you feeling? <span class="text-red-500">*</span>
            </label>
            <select
              v-model="responseForm.outcome"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
              required
            >
              <option value="">Select status</option>
              <option value="resolved">Fully Recovered ✅</option>
              <option value="improved">Feeling Better 📈</option>
              <option value="same">No Change 😐</option>
              <option value="worse">Feeling Worse 📉</option>
            </select>
          </div>

          <!-- Still Experiencing Symptoms -->
          <div class="mb-6">
            <label class="block text-gray-700 font-semibold mb-2">
              Still experiencing original symptoms? <span class="text-red-500">*</span>
            </label>
            <div class="flex gap-4">
              <label class="flex items-center">
                <input
                  v-model="responseForm.still_experiencing_symptoms"
                  type="radio"
                  :value="true"
                  class="mr-2"
                  required
                />
                <span>Yes</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="responseForm.still_experiencing_symptoms"
                  type="radio"
                  :value="false"
                  class="mr-2"
                  required
                />
                <span>No</span>
              </label>
            </div>
          </div>

          <!-- Notes -->
          <div class="mb-6">
            <label class="block text-gray-700 font-semibold mb-2">
              Additional Notes
            </label>
            <textarea
              v-model="responseForm.notes"
              rows="4"
              placeholder="Describe your current condition..."
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none resize-none"
            ></textarea>
          </div>

          <!-- Form Actions -->
          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="submitting"
              class="flex-1 bg-cpsu-green text-white font-semibold py-3 px-6 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
            >
              <span v-if="submitting">Submitting...</span>
              <span v-else>Submit Response</span>
            </button>
            <button
              type="button"
              @click="closeResponseModal"
              class="px-6 py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useFollowUpStore } from '@/stores/followup'
import type { FollowUp, FollowUpResponse } from '@/types'

const followupStore = useFollowUpStore()
const mobileMenuOpen = ref(false)

// State
const showResponseModal = ref(false)
const selectedFollowUp = ref<FollowUp | null>(null)
const submitting = ref(false)

const responseForm = ref<FollowUpResponse>({
  outcome: '' as any,
  notes: '',
  still_experiencing_symptoms: false,
  new_symptoms: []
})

// Computed
const pendingFollowUps = computed(() => followupStore.pendingFollowUps)
const completedFollowUps = computed(() => followupStore.completedFollowUps)

// Methods
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getOutcomeBadgeClass = (outcome: string) => {
  const classes: Record<string, string> = {
    resolved: 'bg-green-200 text-green-800',
    improved: 'bg-blue-200 text-blue-800',
    same: 'bg-yellow-200 text-yellow-800',
    worse: 'bg-red-200 text-red-800'
  }
  return classes[outcome] || 'bg-gray-200 text-gray-800'
}

const getFollowupDiagnosis = (followup: FollowUp) => {
  if (followup.symptom_details?.staff_diagnosis) return followup.symptom_details.staff_diagnosis
  if (followup.symptom_details?.final_diagnosis) return followup.symptom_details.final_diagnosis
  return followup.symptom_disease || 'N/A'
}

const getOutcomeText = (outcome: string) => {
  const texts: Record<string, string> = {
    resolved: 'Fully Recovered',
    improved: 'Improved',
    same: 'No Change',
    worse: 'Worsened'
  }
  return texts[outcome] || outcome
}

const openResponseModal = (followup: FollowUp) => {
  selectedFollowUp.value = followup
  responseForm.value = {
    outcome: '' as any,
    notes: '',
    still_experiencing_symptoms: false,
    new_symptoms: []
  }
  showResponseModal.value = true
}

const closeResponseModal = () => {
  showResponseModal.value = false
  selectedFollowUp.value = null
}

const submitResponse = async () => {
  if (!selectedFollowUp.value) return
  
  submitting.value = true
  
  try {
    await followupStore.respondToFollowUp(selectedFollowUp.value.id, responseForm.value)
    closeResponseModal()
    // Refresh both lists
    await Promise.all([
      followupStore.fetchPendingFollowUps(),
      followupStore.fetchFollowUps()
    ])
  } catch (error) {
    console.error('Error submitting response:', error)
  } finally {
    submitting.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    followupStore.fetchPendingFollowUps(),
    followupStore.fetchFollowUps()
  ])
})
</script>
