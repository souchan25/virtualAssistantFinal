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
              <p class="text-sm text-gray-600">Medication Adherence Monitor</p>
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
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Medication Adherence Monitor</h2>
        <p class="text-gray-600">Track student medication compliance and identify at-risk patients</p>
      </div>

      <!-- Overall Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card-bordered bg-white">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Students on Meds</h3>
          <p class="text-3xl font-bold text-cpsu-green">{{ overallStats.total_students || 0 }}</p>
        </div>
        <div class="card-bordered bg-green-50 border-green-300">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Good Adherence (≥90%)</h3>
          <p class="text-3xl font-bold text-green-600">{{ overallStats.good_adherence || 0 }}</p>
        </div>
        <div class="card-bordered bg-yellow-50 border-yellow-300">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Fair Adherence (75-89%)</h3>
          <p class="text-3xl font-bold text-yellow-600">{{ overallStats.fair_adherence || 0 }}</p>
        </div>
        <div class="card-bordered bg-red-50 border-red-300">
          <h3 class="text-sm font-semibold text-gray-600 mb-2">Poor Adherence (<75%)</h3>
          <p class="text-3xl font-bold text-red-600">{{ overallStats.poor_adherence || 0 }}</p>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 mb-6">
        <div class="flex border-b">
          <button
            @click="activeTab = 'all'"
            :class="['px-6 py-3 font-medium', activeTab === 'all' ? 'bg-cpsu-green text-white' : 'text-gray-600 hover:bg-gray-100']"
          >
            All Students
          </button>
          <button
            @click="activeTab = 'poor'"
            :class="['px-6 py-3 font-medium', activeTab === 'poor' ? 'bg-red-600 text-white' : 'text-gray-600 hover:bg-gray-100']"
          >
            🚨 Poor Adherence
          </button>
          <button
            @click="activeTab = 'fair'"
            :class="['px-6 py-3 font-medium', activeTab === 'fair' ? 'bg-yellow-600 text-white' : 'text-gray-600 hover:bg-gray-100']"
          >
            ⚠️ Fair Adherence
          </button>
          <button
            @click="activeTab = 'good'"
            :class="['px-6 py-3 font-medium', activeTab === 'good' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-gray-100']"
          >
            ✅ Good Adherence
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-cpsu-green"></div>
        <p class="mt-4 text-gray-600">Loading adherence data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Student List -->
      <div v-else class="space-y-4">
        <div v-if="filteredStudents.length === 0" class="text-center py-12 bg-white rounded-lg border-2 border-gray-200">
          <p class="text-gray-500 text-lg">No students in this category</p>
        </div>

        <div
          v-for="student in filteredStudents"
          :key="student.id"
          class="bg-white rounded-lg shadow-sm border-2 hover:border-cpsu-green transition-colors"
          :class="{
            'border-red-300': student.adherence_rate < 75,
            'border-yellow-300': student.adherence_rate >= 75 && student.adherence_rate < 90,
            'border-green-300': student.adherence_rate >= 90,
            'border-gray-200': student.adherence_rate === null
          }"
        >
          <div class="p-6">
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h3 class="text-xl font-bold text-gray-900">{{ student.name }}</h3>
                  <span
                    class="px-4 py-1 rounded-full text-sm font-bold"
                    :class="{
                      'bg-red-100 text-red-700': student.adherence_rate < 75,
                      'bg-yellow-100 text-yellow-700': student.adherence_rate >= 75 && student.adherence_rate < 90,
                      'bg-green-100 text-green-700': student.adherence_rate >= 90
                    }"
                  >
                    {{ student.adherence_rate !== null ? student.adherence_rate + '%' : 'N/A' }}
                  </span>
                </div>
                <p class="text-gray-600">{{ student.school_id }} • {{ student.department }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-gray-600">Active Meds: {{ student.active_medications || 0 }}</p>
                <p class="text-sm text-gray-600">Missed Doses: {{ student.missed_doses || 0 }}</p>
              </div>
            </div>

            <!-- Adherence Bar -->
            <div class="mb-4">
              <div class="flex justify-between text-sm text-gray-600 mb-1">
                <span>Adherence Rate</span>
                <span class="font-semibold">{{ student.adherence_rate }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-3">
                <div
                  class="h-3 rounded-full transition-all"
                  :class="{
                    'bg-red-500': student.adherence_rate < 75,
                    'bg-yellow-500': student.adherence_rate >= 75 && student.adherence_rate < 90,
                    'bg-green-500': student.adherence_rate >= 90
                  }"
                  :style="{ width: student.adherence_rate + '%' }"
                ></div>
              </div>
            </div>

            <!-- Medications List -->
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
              <p class="text-sm font-semibold text-gray-700 mb-2">Current Medications:</p>
              <div class="space-y-2">
                <div
                  v-for="med in student.medications"
                  :key="med.id"
                  class="flex justify-between items-center text-sm"
                >
                  <div>
                    <span class="font-medium text-gray-900">{{ med.medication_name }}</span>
                    <span class="text-gray-600"> • {{ med.dosage }}</span>
                  </div>
                  <span
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="{
                      'bg-red-100 text-red-700': med.adherence < 75,
                      'bg-yellow-100 text-yellow-700': med.adherence >= 75 && med.adherence < 90,
                      'bg-green-100 text-green-700': med.adherence >= 90
                    }"
                  >
                    {{ med.adherence }}%
                  </span>
                </div>
              </div>
            </div>

            <!-- Recent Activity -->
            <div v-if="student.recent_logs" class="bg-blue-50 rounded-lg p-4 mb-4">
              <p class="text-sm font-semibold text-gray-700 mb-2">Recent Activity (Last 7 Days):</p>
              <div class="flex items-center gap-4 text-sm">
                <div>
                  <span class="text-green-700 font-semibold">{{ student.recent_logs.taken || 0 }}</span>
                  <span class="text-gray-600"> taken</span>
                </div>
                <div>
                  <span class="text-red-700 font-semibold">{{ student.recent_logs.missed || 0 }}</span>
                  <span class="text-gray-600"> missed</span>
                </div>
                <div>
                  <span class="text-yellow-700 font-semibold">{{ student.recent_logs.pending || 0 }}</span>
                  <span class="text-gray-600"> pending</span>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-3 pt-4 border-t">
              <button @click="contactStudent(student)" class="btn-outline flex-1">
                📧 Contact Student
              </button>
              <button @click="viewDetails(student)" class="btn-primary flex-1">
                📊 View Full Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import StaffNavigation from '@/components/StaffNavigation.vue'

const router = useRouter()

// State
const students = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const activeTab = ref<'all' | 'poor' | 'fair' | 'good'>('all')

// Computed
const overallStats = computed(() => {
  const total = students.value.length
  const good = students.value.filter(s => s.adherence_rate >= 90).length
  const fair = students.value.filter(s => s.adherence_rate >= 75 && s.adherence_rate < 90).length
  const poor = students.value.filter(s => s.adherence_rate < 75).length

  return {
    total_students: total,
    good_adherence: good,
    fair_adherence: fair,
    poor_adherence: poor
  }
})

const filteredStudents = computed(() => {
  if (activeTab.value === 'poor') {
    return students.value.filter(s => s.adherence_rate < 75)
  } else if (activeTab.value === 'fair') {
    return students.value.filter(s => s.adherence_rate >= 75 && s.adherence_rate < 90)
  } else if (activeTab.value === 'good') {
    return students.value.filter(s => s.adherence_rate >= 90)
  }
  return students.value
})

// Methods
const fetchAdherenceData = async () => {
  loading.value = true
  error.value = null

  try {
    // Get students with medication data
    const response = await api.get('/staff/students/', {
      params: { has_symptoms: 'true' }
    })
    
    // Filter students who are on medication (have active medications)
    const allStudents = Array.isArray(response.data) ? response.data : (response.data.students || [])
    students.value = allStudents.filter((s: any) => 
      s.active_medications && s.active_medications > 0 && s.adherence_rate !== null
    )
    
    console.log('Adherence data loaded:', students.value.length, 'students')
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to load adherence data'
    console.error('Error fetching adherence data:', err)
  } finally {
    loading.value = false
  }
}

const contactStudent = (student: any) => {
  // In a real app, this would open an email/SMS interface
  alert(`Contact feature for ${student.name} will be implemented`)
}

const viewDetails = (student: any) => {
  router.push({
    name: 'staff-students',
    query: { student_id: student.school_id }
  })
}

onMounted(() => {
  fetchAdherenceData()
})
</script>
