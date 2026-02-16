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
              <p class="text-sm text-gray-600">Student Health Records</p>
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
          <router-link to="/staff/students" class="text-cpsu-green font-semibold">
            👥 Students
          </router-link>
          <router-link to="/staff/prescribe" class="text-gray-700 hover:text-cpsu-green font-medium">
            💊 Prescribe
          </router-link>
          <router-link to="/staff/adherence" class="text-gray-700 hover:text-cpsu-green font-medium">
            📈 Adherence
          </router-link>
          <router-link to="/staff/followups" class="text-gray-700 hover:text-cpsu-green font-medium">
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
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Student Health Records</h2>
        <p class="text-gray-600">View and manage student health information</p>
      </div>

      <!-- Search & Filter -->
      <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Search Student</label>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="School ID or Name..."
              class="input-field w-full"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Department</label>
            <select v-model="filterDepartment" class="input-field w-full">
              <option value="">All Departments</option>
              <option value="College of Agriculture and Forestry">College of Agriculture and Forestry</option>
              <option value="College of Teacher Education">College of Teacher Education</option>
              <option value="College of Arts and Sciences">College of Arts and Sciences</option>
              <option value="College of Hospitality Management">College of Hospitality Management</option>
              <option value="College of Engineering">College of Engineering</option>
              <option value="College of Computer Studies">College of Computer Studies</option>
              <option value="College of Criminal Justice Education">College of Criminal Justice Education</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Health Status</label>
            <select v-model="filterStatus" class="input-field w-full">
              <option value="">All Students</option>
              <option value="recent">Recent Symptoms (7 days)</option>
              <option value="medications">On Medications</option>
              <option value="followup">Pending Follow-ups</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-cpsu-green"></div>
        <p class="mt-4 text-gray-600">Loading students...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Students List -->
      <div v-else class="space-y-4">
        <div v-if="filteredStudents.length === 0" class="text-center py-12 bg-white rounded-lg border-2 border-gray-200">
          <p class="text-gray-500 text-lg">No students found matching your criteria</p>
        </div>

        <div
          v-for="student in filteredStudents"
          :key="student.id"
          class="bg-white rounded-lg shadow-sm border-2 border-gray-200 hover:border-cpsu-green transition-colors cursor-pointer"
          @click="viewStudentDetails(student)"
        >
          <div class="p-6">
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1">
                <h3 class="text-xl font-bold text-gray-900">{{ student.name }}</h3>
                <p class="text-gray-600">{{ student.school_id }} • {{ student.department }}</p>
              </div>
              <div class="flex gap-2">
                <span v-if="student.on_medication" class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  💊 On Meds
                </span>
                <span v-if="student.pending_followup" class="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm font-medium">
                  📋 Follow-up
                </span>
                <span v-if="student.recent_symptoms" class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-medium">
                  🩺 Recent Visit
                </span>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="grid grid-cols-4 gap-4 pt-4 border-t">
              <div>
                <p class="text-sm text-gray-600">Total Visits</p>
                <p class="text-lg font-semibold text-cpsu-green">{{ student.total_visits || 0 }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Last Visit</p>
                <p class="text-lg font-semibold text-gray-900">{{ formatDate(student.last_visit) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Medications</p>
                <p class="text-lg font-semibold text-blue-600">{{ student.medication_count || 0 }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Adherence</p>
                <p class="text-lg font-semibold" :class="getAdherenceColor(student.adherence_rate)">
                  {{ student.adherence_rate ? student.adherence_rate + '%' : 'N/A' }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Detail Modal -->
      <div v-if="selectedStudent" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="selectedStudent = null">
        <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
          <div class="sticky top-0 bg-white border-b-2 border-cpsu-green p-6">
            <div class="flex justify-between items-start">
              <div>
                <h2 class="text-2xl font-bold text-gray-900">{{ selectedStudent.name }}</h2>
                <p class="text-gray-600">{{ selectedStudent.school_id }} • {{ selectedStudent.department }}</p>
              </div>
              <button @click="selectedStudent = null" class="text-gray-400 hover:text-gray-600 text-2xl">×</button>
            </div>
          </div>

          <div class="p-6 space-y-6">
            <!-- Health Summary -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Health Summary</h3>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-600">Total Visits</p>
                  <p class="text-2xl font-bold text-cpsu-green">{{ selectedStudent.total_visits || 0 }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-600">Active Meds</p>
                  <p class="text-2xl font-bold text-blue-600">{{ selectedStudent.medication_count || 0 }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-600">Adherence</p>
                  <p class="text-2xl font-bold" :class="getAdherenceColor(selectedStudent.adherence_rate)">
                    {{ selectedStudent.adherence_rate ? selectedStudent.adherence_rate + '%' : 'N/A' }}
                  </p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-600">Last Visit</p>
                  <p class="text-lg font-semibold text-gray-900">{{ formatDate(selectedStudent.last_visit) }}</p>
                </div>
              </div>
            </div>

            <!-- Recent Symptoms -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Symptom Reports</h3>
              <div v-if="selectedStudent.recent_symptom_reports && selectedStudent.recent_symptom_reports.length > 0" class="space-y-3">
                <div
                  v-for="report in selectedStudent.recent_symptom_reports"
                  :key="report.id"
                  class="border-l-4 border-cpsu-green bg-gray-50 p-4"
                >
                  <div class="flex justify-between items-start mb-2">
                    <h4 class="font-semibold text-gray-900">{{ report.predicted_disease }}</h4>
                    <span class="text-sm text-gray-600">{{ formatDate(report.created_at) }}</span>
                  </div>
                  <p class="text-sm text-gray-700 mb-2">
                    <strong>Symptoms:</strong> {{ report.symptoms?.join(', ') || 'N/A' }}
                  </p>
                  <p class="text-sm text-gray-600">
                    <strong>Confidence:</strong> {{ report.confidence ? (report.confidence * 100).toFixed(1) + '%' : 'N/A' }}
                  </p>
                </div>
              </div>
              <p v-else class="text-gray-500 text-center py-4">No recent symptom reports</p>
            </div>

            <!-- Active Medications -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Active Medications</h3>
              <div v-if="selectedStudent.medications && selectedStudent.medications.length > 0" class="space-y-3">
                <div
                  v-for="med in selectedStudent.medications"
                  :key="med.id"
                  class="border-l-4 border-blue-500 bg-blue-50 p-4"
                >
                  <h4 class="font-semibold text-gray-900">{{ med.medication_name }}</h4>
                  <p class="text-sm text-gray-700">{{ med.dosage }} • {{ med.frequency }}</p>
                  <p class="text-sm text-gray-600">Start: {{ formatDate(med.start_date) }} • End: {{ formatDate(med.end_date) }}</p>
                </div>
              </div>
              <p v-else class="text-gray-500 text-center py-4">No active medications</p>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-4 pt-4 border-t">
              <button @click="prescribeMedication(selectedStudent)" class="btn-primary flex-1">
                💊 Prescribe Medication
              </button>
              <button @click="selectedStudent = null" class="btn-outline flex-1">
                Close
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

const router = useRouter()

// State
const students = ref<any[]>([])
const selectedStudent = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Filters
const searchQuery = ref('')
const filterDepartment = ref('')
const filterStatus = ref('')

// Filtered students
const filteredStudents = computed(() => {
  let filtered = students.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(s =>
      s.name?.toLowerCase().includes(query) ||
      s.school_id?.toLowerCase().includes(query)
    )
  }

  // Department filter
  if (filterDepartment.value) {
    filtered = filtered.filter(s => s.department === filterDepartment.value)
  }

  // Status filter
  if (filterStatus.value === 'recent') {
    filtered = filtered.filter(s => s.recent_symptoms)
  } else if (filterStatus.value === 'medications') {
    filtered = filtered.filter(s => s.on_medication)
  } else if (filterStatus.value === 'followup') {
    filtered = filtered.filter(s => s.pending_followup)
  }

  return filtered
})

// Methods
const fetchStudents = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await api.get('/staff/students/')
    console.log('Student API Response:', response.data)
    students.value = response.data.students || []
    console.log('Students loaded:', students.value.length)
  } catch (err: any) {
    error.value = err.response?.data?.error || err.message || 'Failed to load students'
    console.error('Error fetching students:', err)
    console.error('Error details:', err.response?.data)
  } finally {
    loading.value = false
  }
}

const viewStudentDetails = (student: any) => {
  selectedStudent.value = student
}

const prescribeMedication = (student: any) => {
  router.push({
    name: 'staff-prescribe',
    query: { student_id: student.school_id }
  })
}

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return 'N/A'
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getAdherenceColor = (rate: number | null | undefined) => {
  if (rate === null || rate === undefined) return 'text-gray-500'
  if (rate >= 90) return 'text-green-600'
  if (rate >= 75) return 'text-yellow-600'
  return 'text-red-600'
}

onMounted(() => {
  fetchStudents()
})
</script>
