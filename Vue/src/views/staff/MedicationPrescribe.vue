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
              <p class="text-sm text-gray-600">Medication Prescription</p>
            </div>
          </div>
          <button @click="$router.push('/staff')" class="btn-outline !py-2 !px-4">Back to Dashboard</button>
        </div>
        <StaffNavigation />
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Prescribe Medication</h2>
          <p class="text-gray-600">Create medication prescription for student</p>
        </div>

      <!-- Error Alert -->
      <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
        <div class="flex items-center">
          <span class="text-red-700">{{ error }}</span>
          <button @click="error = null" class="ml-auto text-red-500 hover:text-red-700">✕</button>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
        <div class="flex items-center">
          <span class="text-green-700">{{ successMessage }}</span>
          <button @click="successMessage = null" class="ml-auto text-green-500 hover:text-green-700">✕</button>
        </div>
      </div>

      <!-- Prescription Form -->
      <form @submit.prevent="submitPrescription" class="bg-white rounded-lg border-2 border-cpsu-green p-8">
        <!-- Student Selection -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">
            Student School ID <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.student_school_id"
            type="text"
            placeholder="e.g., 2024-0001"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
            required
          />
          <p class="mt-1 text-sm text-gray-500">Enter the student's school ID</p>
        </div>

        <!-- Medication Name -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">
            Medication Name <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.name"
            type="text"
            placeholder="e.g., Amoxicillin"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
            required
          />
        </div>

        <!-- Dosage -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">
            Dosage <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.dosage"
            type="text"
            placeholder="e.g., 500mg"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
            required
          />
        </div>

        <!-- Frequency -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">
            Frequency <span class="text-red-500">*</span>
          </label>
          <select
            v-model="form.frequency"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
            required
          >
            <option value="">Select frequency</option>
            <option value="Once daily">Once daily</option>
            <option value="Twice daily">Twice daily</option>
            <option value="Three times daily">Three times daily</option>
            <option value="Four times daily">Four times daily</option>
            <option value="Every 4 hours">Every 4 hours</option>
            <option value="Every 6 hours">Every 6 hours</option>
            <option value="Every 8 hours">Every 8 hours</option>
            <option value="As needed">As needed</option>
          </select>
        </div>

        <!-- Schedule Times -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">
            Schedule Times <span class="text-red-500">*</span>
          </label>
          <div class="space-y-2 mb-3">
            <div v-for="(time, index) in form.schedule_times" :key="index" class="flex gap-2">
              <input
                v-model="form.schedule_times[index]"
                type="time"
                class="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
                required
              />
              <button
                v-if="form.schedule_times.length > 1"
                @click="removeScheduleTime(index)"
                type="button"
                class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
              >
                Remove
              </button>
            </div>
          </div>
          <button
            @click="addScheduleTime"
            type="button"
            class="px-4 py-2 bg-cpsu-yellow text-cpsu-green font-semibold rounded-lg hover:bg-yellow-400 transition"
          >
            + Add Time
          </button>
          <p class="mt-2 text-sm text-gray-500">Specify times when medication should be taken</p>
        </div>

        <!-- Date Range -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <label class="block text-gray-700 font-semibold mb-2">
              Start Date <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.start_date"
              type="date"
              :min="today"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
              required
            />
          </div>
          <div>
            <label class="block text-gray-700 font-semibold mb-2">
              End Date <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.end_date"
              type="date"
              :min="form.start_date || today"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none"
              required
            />
          </div>
        </div>

        <!-- Instructions -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">
            Instructions
          </label>
          <textarea
            v-model="form.instructions"
            rows="3"
            placeholder="e.g., Take with food, avoid alcohol"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none resize-none"
          ></textarea>
        </div>

        <!-- Side Effects -->
        <div class="mb-8">
          <label class="block text-gray-700 font-semibold mb-2">
            Possible Side Effects
          </label>
          <textarea
            v-model="form.side_effects"
            rows="3"
            placeholder="e.g., Nausea, dizziness, headache"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-cpsu-green focus:outline-none resize-none"
          ></textarea>
        </div>

        <!-- Form Actions -->
        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 bg-cpsu-green text-white font-semibold py-3 px-6 rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Creating Prescription...</span>
            <span v-else>Create Prescription</span>
          </button>
          <button
            type="button"
            @click="resetForm"
            class="px-6 py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition"
          >
            Reset
          </button>
        </div>
      </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import StaffNavigation from '@/components/StaffNavigation.vue'

interface PrescriptionForm {
  student_school_id: string
  name: string
  dosage: string
  frequency: string
  schedule_times: string[]
  start_date: string
  end_date: string
  instructions: string
  side_effects: string
}

const route = useRoute()

const loading = ref(false)
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)

const form = ref<PrescriptionForm>({
  student_school_id: '',
  name: '',
  dosage: '',
  frequency: '',
  schedule_times: ['08:00'],
  start_date: '',
  end_date: '',
  instructions: '',
  side_effects: ''
})

const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const addScheduleTime = () => {
  form.value.schedule_times.push('12:00')
}

const removeScheduleTime = (index: number) => {
  form.value.schedule_times.splice(index, 1)
}

const resetForm = () => {
  form.value = {
    student_school_id: '',
    name: '',
    dosage: '',
    frequency: '',
    schedule_times: ['08:00'],
    start_date: '',
    end_date: '',
    instructions: '',
    side_effects: ''
  }
  error.value = null
  successMessage.value = null
}

// Prefill from query param (when coming from Student Records)
onMounted(() => {
  const schoolIdFromQuery = route.query.student_id as string
  if (schoolIdFromQuery) {
    form.value.student_school_id = schoolIdFromQuery
  }
})

const submitPrescription = async () => {
  loading.value = true
  error.value = null
  successMessage.value = null

  try {
    // Basic required field checks
    if (!form.value.start_date || !form.value.end_date) {
      throw new Error('Start date and end date are required')
    }
    if (!form.value.name || !form.value.dosage || !form.value.frequency) {
      throw new Error('Name, dosage, and frequency are required')
    }

    // First, get student ID from school_id
    const studentResponse = await api.get('/staff/students/', {
      params: { search: form.value.student_school_id }
    })

    const studentsData = studentResponse.data?.students || studentResponse.data || []
    const studentList = Array.isArray(studentsData) ? studentsData : []

    if (studentList.length === 0) {
      throw new Error('Student not found with this school ID')
    }

    const student = studentList[0]
    if (!student || !student.id) {
      throw new Error('Invalid student data received')
    }

    const studentId = student.id

    // Create prescription data
    const prescriptionData = {
      student: studentId, // serializer expects "student"
      name: form.value.name,
      dosage: form.value.dosage,
      frequency: form.value.frequency,
      schedule_times: form.value.schedule_times,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      instructions: form.value.instructions || undefined,
      side_effects: form.value.side_effects || undefined
    }

    // Submit prescription
    await api.post('/medications/create/', prescriptionData)

    successMessage.value = `Prescription created successfully for ${form.value.student_school_id}`
    resetForm()
  } catch (err: any) {
    error.value = err.response?.data?.error || err.message || 'Failed to create prescription'
    console.error('Error creating prescription:', err)
  } finally {
    loading.value = false
  }
}
</script>
