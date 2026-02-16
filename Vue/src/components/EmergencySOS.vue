<template>
  <!-- Floating SOS Button - Visible on all pages -->
  <div class="fixed bottom-6 right-6 z-50">
    <button
      @click="showEmergencyModal = true"
      class="group relative bg-red-600 hover:bg-red-700 text-white rounded-full p-6 shadow-2xl transform transition-all duration-200 hover:scale-110 animate-pulse-slow"
      aria-label="Emergency SOS"
    >
      <span class="text-3xl">🚨</span>
      <span class="absolute -top-1 -right-1 flex h-4 w-4">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-4 w-4 bg-red-500"></span>
      </span>
    </button>
    
    <!-- Tooltip -->
    <div class="absolute bottom-full right-0 mb-2 hidden group-hover:block">
      <div class="bg-gray-900 text-white text-sm rounded py-2 px-3 whitespace-nowrap">
        Emergency SOS
      </div>
    </div>
  </div>

  <!-- Emergency Modal -->
  <Teleport to="body">
    <div
      v-if="showEmergencyModal"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-[100] p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg max-w-md w-full p-6 relative animate-fade-in">
        <!-- Close button -->
        <button
          @click="closeModal"
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <span class="text-2xl">&times;</span>
        </button>

        <!-- Header -->
        <div class="text-center mb-6">
          <div class="text-6xl mb-4">🚨</div>
          <h2 class="text-3xl font-bold text-red-600 mb-2">Emergency SOS</h2>
          <p class="text-gray-600">Help will be dispatched immediately</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="triggerEmergency" class="space-y-4">
          <!-- Location -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Your Location <span class="text-red-500">*</span>
            </label>
            <input
              v-model="emergency.location"
              type="text"
              placeholder="e.g., Main Building, Room 201"
              class="input-field"
              required
            />
            <p class="text-xs text-gray-500 mt-1">Building name and room number</p>
          </div>

          <!-- Description (Optional) -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              What's happening? (Optional)
            </label>
            <textarea
              v-model="emergency.description"
              placeholder="Brief description of the emergency"
              class="input-field"
              rows="3"
            ></textarea>
          </div>

          <!-- Symptoms (Optional) -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Symptoms (if any)
            </label>
            <input
              v-model="symptomsInput"
              type="text"
              placeholder="e.g., chest pain, difficulty breathing"
              class="input-field"
            />
            <p class="text-xs text-gray-500 mt-1">Separate with commas</p>
          </div>

          <!-- Error message -->
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {{ error }}
          </div>

          <!-- Buttons -->
          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="flex-1 btn-outline"
              :disabled="loading"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition disabled:opacity-50"
              :disabled="loading"
            >
              <span v-if="!loading">🚨 Send SOS</span>
              <span v-else class="flex items-center justify-center">
                <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sending...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>

  <!-- Success Notification -->
  <Teleport to="body">
    <div
      v-if="showSuccess"
      class="fixed top-6 right-6 z-[101] animate-slide-in-right"
    >
      <div class="bg-green-500 text-white px-6 py-4 rounded-lg shadow-2xl max-w-sm">
        <div class="flex items-start gap-3">
          <span class="text-2xl">✅</span>
          <div>
            <h3 class="font-bold mb-1">Help is on the way!</h3>
            <p class="text-sm">Clinic staff have been notified. Stay where you are.</p>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import api from '@/services/api'

const showEmergencyModal = ref(false)
const showSuccess = ref(false)
const loading = ref(false)
const error = ref('')

const emergency = ref({
  location: '',
  description: '',
})

const symptomsInput = ref('')

const closeModal = () => {
  if (!loading.value) {
    showEmergencyModal.value = false
    error.value = ''
  }
}

const triggerEmergency = async () => {
  loading.value = true
  error.value = ''

  try {
    // Parse symptoms from comma-separated input
    const symptoms = symptomsInput.value
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0)

    const response = await api.post('/emergency/trigger/', {
      location: emergency.value.location,
      description: emergency.value.description,
      symptoms: symptoms
    })

    // Success!
    showEmergencyModal.value = false
    showSuccess.value = true

    // Reset form
    emergency.value = { location: '', description: '' }
    symptomsInput.value = ''

    // Hide success message after 10 seconds
    setTimeout(() => {
      showSuccess.value = false
    }, 10000)

  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to send emergency alert. Please call clinic directly.'
    console.error('Emergency trigger error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}

@keyframes slide-in-right {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in-right {
  animation: slide-in-right 0.3s ease-out;
}
</style>
