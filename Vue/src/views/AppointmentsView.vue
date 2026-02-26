<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-xl font-bold text-cpsu-green">Appointments</h1>
          <button @click="$router.go(-1)" class="text-gray-600 hover:text-gray-900">Back</button>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-4 py-6">
      <!-- Tabs -->
      <div class="flex space-x-4 mb-6 border-b">
        <button
          v-for="tab in ['Upcoming', 'History', 'Request']"
          :key="tab"
          @click="currentTab = tab"
          class="pb-2 px-4 font-medium transition-colors"
          :class="currentTab === tab ? 'border-b-2 border-cpsu-green text-cpsu-green' : 'text-gray-500 hover:text-gray-700'"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-cpsu-green border-t-transparent"></div>
      </div>

      <!-- List -->
      <div v-else-if="currentTab === 'Upcoming' || currentTab === 'History'">
        <div v-if="filteredAppointments.length === 0" class="text-center py-12 text-gray-500">
          No {{ currentTab.toLowerCase() }} appointments.
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="apt in filteredAppointments"
            :key="apt.id"
            class="bg-white p-4 rounded-lg shadow border"
            :class="getStatusClass(apt.status)"
          >
            <div class="flex justify-between items-start mb-2">
              <div>
                <h3 class="font-bold text-gray-900">{{ apt.purpose }}</h3>
                <p class="text-sm text-gray-600">
                  <span v-if="authStore.user?.role === 'staff'">Student: {{ apt.student_name }}</span>
                  <span v-else>With: {{ apt.staff_name || 'Clinic Staff' }}</span>
                </p>
                <p class="text-xs text-gray-500 mt-1" v-if="apt.notes">{{ apt.notes }}</p>
              </div>
              <div class="text-right">
                <p class="font-bold text-cpsu-green">{{ formatDate(apt.scheduled_date) }}</p>
                <p class="text-sm text-gray-600">{{ formatTime(apt.scheduled_time) }}</p>
              </div>
            </div>
            <div class="flex justify-between items-center mt-2">
              <span class="px-2 py-1 rounded text-xs font-semibold uppercase" :class="getStatusBadgeClass(apt.status)">
                {{ apt.status_display }}
              </span>
              <div v-if="authStore.user?.role === 'staff' && apt.status === 'pending'">
                <button @click="confirmAppointment(apt)" class="btn-primary text-xs px-3 py-1">Confirm</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Request Form -->
      <div v-else-if="currentTab === 'Request'" class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-bold mb-4">Request Appointment</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input v-model="newAppointment.date" type="date" class="input-field w-full" :min="minDate">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Time</label>
            <input v-model="newAppointment.time" type="time" class="input-field w-full">
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Purpose</label>
          <select v-model="newAppointment.purpose" class="input-field w-full">
            <option value="Consultation">General Consultation</option>
            <option value="Follow-up">Follow-up</option>
            <option value="Medical Certificate">Medical Certificate</option>
            <option value="Dental">Dental Checkup</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
          <textarea v-model="newAppointment.notes" rows="3" class="input-field w-full" placeholder="Additional details..."></textarea>
        </div>

        <button @click="createAppointment" :disabled="submitting || !isValid" class="btn-primary w-full justify-center">
          {{ submitting ? 'Submitting...' : 'Request Appointment' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const currentTab = ref('Upcoming')
const appointments = ref<any[]>([])
const loading = ref(false)
const submitting = ref(false)

const newAppointment = ref({
  date: '',
  time: '',
  purpose: 'Consultation',
  notes: ''
})

const minDate = new Date().toISOString().split('T')[0]

const isValid = computed(() => {
  return newAppointment.value.date && newAppointment.value.time && newAppointment.value.purpose
})

const filteredAppointments = computed(() => {
  const now = new Date()
  now.setHours(0,0,0,0) // Compare dates only roughly or precise?
  // Let's rely on scheduled_date
  return appointments.value.filter(apt => {
    const aptDate = new Date(apt.scheduled_date)
    // Add time component? apt.scheduled_time is 'HH:MM:SS'
    // Let's just compare dates for simplicity of 'Upcoming'

    // Status based filter is better
    if (currentTab.value === 'Upcoming') {
      return (aptDate >= now || apt.status === 'pending') && apt.status !== 'cancelled' && apt.status !== 'completed'
    } else {
      return aptDate < now || apt.status === 'cancelled' || apt.status === 'completed'
    }
  }).sort((a, b) => {
    return new Date(a.scheduled_date).getTime() - new Date(b.scheduled_date).getTime()
  })
})

const fetchAppointments = async () => {
  loading.value = true
  try {
    const res = await api.get('/appointments/')
    appointments.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const createAppointment = async () => {
  submitting.value = true
  try {
    await api.post('/appointments/', {
      scheduled_date: newAppointment.value.date,
      scheduled_time: newAppointment.value.time,
      purpose: newAppointment.value.purpose,
      notes: newAppointment.value.notes
    })
    newAppointment.value = { date: '', time: '', purpose: 'Consultation', notes: '' }
    currentTab.value = 'Upcoming'
    fetchAppointments()
  } catch (e) {
    console.error(e)
    alert('Failed to create appointment')
  } finally {
    submitting.value = false
  }
}

const confirmAppointment = async (apt: any) => {
  if (!confirm('Confirm this appointment?')) return
  try {
    await api.patch(`/appointments/${apt.id}/confirm/`)
    fetchAppointments()
  } catch (e) {
    console.error(e)
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
}

const formatTime = (time: string) => {
  if (!time) return ''
  const [h, m] = time.split(':')
  const hour = parseInt(h)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const hour12 = hour % 12 || 12
  return `${hour12}:${m} ${ampm}`
}

const getStatusClass = (status: string) => {
  if (status === 'confirmed') return 'border-l-4 border-l-green-500'
  if (status === 'pending') return 'border-l-4 border-l-yellow-500'
  return 'border-l-4 border-l-gray-300'
}

const getStatusBadgeClass = (status: string) => {
  const map: any = {
    confirmed: 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    cancelled: 'bg-red-100 text-red-800',
    completed: 'bg-gray-100 text-gray-800'
  }
  return map[status] || 'bg-gray-100'
}

onMounted(() => {
  fetchAppointments()
})
</script>
