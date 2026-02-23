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
              <p class="text-sm text-gray-600">Emergency Management</p>
            </div>
          </div>
          <button @click="$router.push('/staff')" class="btn-outline !py-2 !px-4">Back to Dashboard</button>
        </div>
        <StaffNavigation />
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <span class="text-4xl">🚨</span>
          Emergency Alerts Dashboard
        </h2>
        <p class="text-gray-600 mt-2">Monitor and respond to student emergencies</p>
      </div>

    <!-- Active Emergencies (Critical!) -->
    <div v-if="activeEmergencies.length > 0" class="mb-8">
      <h2 class="text-2xl font-bold text-red-600 mb-4 flex items-center gap-2">
        <span class="animate-pulse">🔴</span>
        Active Emergencies ({{ activeEmergencies.length }})
      </h2>
      
      <div class="space-y-4">
        <div
          v-for="emergency in activeEmergencies"
          :key="emergency.id"
          class="bg-red-50 border-2 border-red-500 rounded-lg p-6 shadow-lg animate-pulse-border"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-xl font-bold text-gray-900 mb-1">
                {{ emergency.student_name }}
                <span class="text-sm text-gray-600">({{ emergency.student_school_id }})</span>
              </h3>
              <p class="text-sm text-gray-600">{{ emergency.student_department }}</p>
            </div>
            <span
              class="px-4 py-2 rounded-full text-sm font-semibold"
              :class="{
                'bg-red-600 text-white': emergency.status === 'active',
                'bg-yellow-500 text-white': emergency.status === 'responding'
              }"
            >
              {{ emergency.status_display }}
            </span>
          </div>

          <div class="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-sm font-semibold text-gray-700">📍 Location:</p>
              <p class="text-lg font-bold text-cpsu-green">{{ emergency.location }}</p>
            </div>
            <div>
              <p class="text-sm font-semibold text-gray-700">⏰ Time:</p>
              <p class="text-gray-900">{{ formatTime(emergency.created_at) }}</p>
              <p class="text-sm text-gray-600">{{ getTimeAgo(emergency.created_at) }}</p>
            </div>
          </div>

          <div v-if="emergency.description" class="mb-4">
            <p class="text-sm font-semibold text-gray-700 mb-1">Description:</p>
            <p class="text-gray-900">{{ emergency.description }}</p>
          </div>

          <div v-if="emergency.symptoms && emergency.symptoms.length > 0" class="mb-4">
            <p class="text-sm font-semibold text-gray-700 mb-2">Symptoms:</p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="symptom in emergency.symptoms"
                :key="symptom"
                class="px-3 py-1 bg-red-200 text-red-800 rounded-full text-sm"
              >
                {{ symptom }}
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-4 border-t border-red-200">
            <button
              v-if="emergency.status === 'active'"
              @click="respondToEmergency(emergency.id)"
              class="btn-primary flex-1"
              :disabled="loading"
            >
              ✋ I'm Responding
            </button>
            <button
              @click="resolveEmergency(emergency.id, false)"
              class="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded-lg transition flex-1"
              :disabled="loading"
            >
              ✅ Resolved
            </button>
            <button
              @click="resolveEmergency(emergency.id, true)"
              class="btn-outline flex-1"
              :disabled="loading"
            >
              ❌ False Alarm
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- No Active Emergencies -->
    <div v-else class="bg-green-50 border border-green-200 rounded-lg p-8 text-center mb-8">
      <span class="text-6xl mb-4 block">✅</span>
      <h3 class="text-xl font-bold text-green-800 mb-2">All Clear!</h3>
      <p class="text-green-700">No active emergencies at this time</p>
    </div>

    <!-- Emergency History -->
    <div>
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Emergency History</h2>
      
      <div v-if="loading && history.length === 0" class="text-center py-8">
        <div class="spinner w-12 h-12 mx-auto"></div>
      </div>

      <div v-else-if="history.length === 0" class="text-center py-8 text-gray-500">
        <p>No emergency history</p>
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="emergency in history"
          :key="emergency.id"
          class="card-bordered hover:shadow-lg transition"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h3 class="font-bold text-gray-900">{{ emergency.student_name }}</h3>
                <span
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="{
                    'bg-green-100 text-green-800': emergency.status === 'resolved',
                    'bg-gray-100 text-gray-800': emergency.status === 'false_alarm'
                  }"
                >
                  {{ emergency.status_display }}
                </span>
              </div>
              
              <p class="text-sm text-gray-600 mb-1">
                📍 {{ emergency.location }}
              </p>
              
              <p class="text-xs text-gray-500">
                {{ formatTime(emergency.created_at) }}
                <span v-if="emergency.response_time_minutes">
                  • Response time: {{ emergency.response_time_minutes }} min
                </span>
              </p>

              <p v-if="emergency.resolution_notes" class="text-sm text-gray-700 mt-2 italic">
                "{{ emergency.resolution_notes }}"
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import api from '@/services/api'
import StaffNavigation from '@/components/StaffNavigation.vue'

interface Emergency {
  id: string
  student_school_id: string
  student_name: string
  student_department: string
  location: string
  symptoms: string[]
  description: string
  status: string
  status_display: string
  priority: number
  responded_by_name: string | null
  response_time: string | null
  response_time_minutes: number | null
  resolved_at: string | null
  resolution_notes: string
  created_at: string
  updated_at: string
}

const activeEmergencies = ref<Emergency[]>([])
const history = ref<Emergency[]>([])
const loading = ref(false)
let refreshInterval: number | null = null

const fetchActiveEmergencies = async () => {
  try {
    const response = await api.get('/emergency/active/')
    activeEmergencies.value = response.data.emergencies
  } catch (error) {
    console.error('Failed to fetch active emergencies:', error)
  }
}

const fetchHistory = async () => {
  loading.value = true
  try {
    const response = await api.get('/emergency/history/?page_size=20')
    history.value = response.data.emergencies
  } catch (error) {
    console.error('Failed to fetch emergency history:', error)
  } finally {
    loading.value = false
  }
}

const respondToEmergency = async (emergencyId: string) => {
  loading.value = true
  try {
    await api.patch(`/emergency/${emergencyId}/respond/`)
    await fetchActiveEmergencies()
  } catch (error) {
    console.error('Failed to respond to emergency:', error)
    alert('Failed to update emergency status')
  } finally {
    loading.value = false
  }
}

const resolveEmergency = async (emergencyId: string, isFalseAlarm: boolean) => {
  const notes = prompt(
    isFalseAlarm 
      ? 'False alarm - Add notes (optional):' 
      : 'Emergency resolved - Add resolution notes:'
  )
  
  if (notes === null) return // User cancelled

  loading.value = true
  try {
    await api.patch(`/emergency/${emergencyId}/resolve/`, {
      notes: notes,
      false_alarm: isFalseAlarm
    })
    await fetchActiveEmergencies()
    await fetchHistory()
  } catch (error) {
    console.error('Failed to resolve emergency:', error)
    alert('Failed to resolve emergency')
  } finally {
    loading.value = false
  }
}

const formatTime = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const getTimeAgo = (dateString: string) => {
  const minutes = Math.floor((Date.now() - new Date(dateString).getTime()) / 60000)
  if (minutes < 1) return 'Just now'
  if (minutes === 1) return '1 minute ago'
  if (minutes < 60) return `${minutes} minutes ago`
  const hours = Math.floor(minutes / 60)
  if (hours === 1) return '1 hour ago'
  return `${hours} hours ago`
}

onMounted(() => {
  fetchActiveEmergencies()
  fetchHistory()
  
  // Auto-refresh every 10 seconds
  refreshInterval = window.setInterval(() => {
    fetchActiveEmergencies()
  }, 10000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
@keyframes pulse-border {
  0%, 100% {
    border-color: #ef4444;
  }
  50% {
    border-color: #f87171;
  }
}

.animate-pulse-border {
  animation: pulse-border 2s ease-in-out infinite;
}
</style>
