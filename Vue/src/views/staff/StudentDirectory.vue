<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <input
        v-model="filters.search"
        type="text"
        placeholder="Search by name or ID..."
        class="input-field"
        @input="debouncedSearch"
      />
      
      <select v-model="filters.department" @change="loadStudents" class="input-field">
        <option value="">All Departments</option>
        <option value="College of Agriculture and Forestry">College of Agriculture and Forestry</option>
        <option value="College of Teacher Education">College of Teacher Education</option>
        <option value="College of Arts and Sciences">College of Arts and Sciences</option>
        <option value="College of Hospitality Management">College of Hospitality Management</option>
        <option value="College of Engineering">College of Engineering</option>
        <option value="College of Computer Studies">College of Computer Studies</option>
        <option value="College of Criminal Justice Education">College of Criminal Justice Education</option>
      </select>
      
      <select v-model="filters.has_symptoms" @change="loadStudents" class="input-field">
        <option value="">All Students</option>
        <option value="true">With Health Records</option>
        <option value="false">No Health Records</option>
      </select>
      
      <button @click="clearFilters" class="btn-outline">Clear Filters</button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-600">Loading students...</p>
    </div>

    <!-- Students Table -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">School ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Department</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Year Level</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Consultation</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Records</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="student in students" :key="student.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ student.school_id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ student.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ student.department || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ student.year_level || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ student.symptom_records?.[0]?.created_at ? formatDate(student.symptom_records[0].created_at) : 'No records' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                {{ student.symptom_records?.length || 0 }} records
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button @click="viewStudent(student)" class="text-cpsu-green hover:underline">View Details</button>
            </td>
          </tr>
          <tr v-if="students.length === 0">
            <td colspan="7" class="px-6 py-8 text-center text-gray-500">
              No students found matching your filters
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Student Detail Modal -->
    <div v-if="selectedStudent" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="selectedStudent = null">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ selectedStudent.name }}</h3>
            <p class="text-sm text-gray-600">{{ selectedStudent.school_id }} - {{ selectedStudent.department }}</p>
          </div>
          <button @click="selectedStudent = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 space-y-6">
          <!-- Student Info -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Course</p>
              <p class="font-medium">{{ selectedStudent.course || 'Not specified' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Year Level</p>
              <p class="font-medium">{{ selectedStudent.year_level || 'Not specified' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">CPSU Address</p>
              <p class="font-medium">{{ selectedStudent.cpsu_address || 'Not specified' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Total Consultations</p>
              <p class="font-medium">{{ selectedStudent.symptom_records?.length || 0 }}</p>
            </div>
          </div>

          <!-- Health Records -->
          <div>
            <h4 class="font-semibold text-gray-900 mb-3">Health Records</h4>
            <div class="space-y-3">
              <div v-for="record in selectedStudent.symptom_records" :key="record.id" class="border border-gray-200 rounded-lg p-4">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h5 class="font-medium text-gray-900">{{ record.predicted_disease }}</h5>
                    <p class="text-sm text-gray-600">Confidence: {{ (record.confidence_score * 100).toFixed(1) }}%</p>
                  </div>
                  <p class="text-sm text-gray-500">{{ formatDate(record.created_at) }}</p>
                </div>
                <div class="mt-2">
                  <p class="text-sm text-gray-700"><strong>Symptoms:</strong> {{ record.symptoms.join(', ') }}</p>
                  <p class="text-sm text-gray-700"><strong>Duration:</strong> {{ record.duration_days }} days</p>
                  <p class="text-sm text-gray-700"><strong>Severity:</strong> {{ getSeverityLabel(record.severity) }}</p>
                </div>
                <div v-if="record.requires_referral" class="mt-2">
                  <span class="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">⚠️ Referral Required</span>
                </div>
              </div>
              <div v-if="!selectedStudent.symptom_records || selectedStudent.symptom_records.length === 0" class="text-center py-8 text-gray-500">
                No health records found
              </div>
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

const students = ref<any[]>([])
const selectedStudent = ref<any>(null)
const loading = ref(false)

const filters = ref({
  search: '',
  department: '',
  has_symptoms: ''
})

let searchTimeout: ReturnType<typeof setTimeout>

onMounted(() => {
  loadStudents()
})

async function loadStudents() {
  loading.value = true
  try {
    const params: any = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.department) params.department = filters.value.department
    if (filters.value.has_symptoms) params.has_symptoms = filters.value.has_symptoms

    const response = await api.get('/staff/students/', { params })
    students.value = response.data
  } catch (error) {
    console.error('Failed to load students:', error)
  } finally {
    loading.value = false
  }
}

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadStudents()
  }, 300)
}

function clearFilters() {
  filters.value = {
    search: '',
    department: '',
    has_symptoms: ''
  }
  loadStudents()
}

function viewStudent(student: any) {
  selectedStudent.value = student
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function getSeverityLabel(severity: number): string {
  const labels = ['Mild', 'Moderate', 'Severe', 'Critical']
  return labels[severity] || 'Unknown'
}
</script>
