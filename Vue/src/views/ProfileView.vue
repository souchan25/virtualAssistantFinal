<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green">
      <div class="container mx-auto px-4 sm:px-6 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/dashboard" class="flex items-center space-x-2 sm:space-x-4 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-10 w-10 sm:h-12 sm:w-12 object-contain">
            <div>
              <h1 class="text-lg sm:text-2xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs sm:text-sm text-gray-600">Mighty Hornbills</p>
            </div>
          </router-link>
          <div class="hidden lg:flex items-center space-x-4">
            <router-link to="/dashboard" class="text-gray-700 hover:text-cpsu-green">Dashboard</router-link>
            <router-link to="/symptom-checker" class="text-gray-700 hover:text-cpsu-green">Check Symptoms</router-link>
            <router-link to="/medications" class="text-gray-700 hover:text-cpsu-green">Medications</router-link>
            <router-link to="/followups" class="text-gray-700 hover:text-cpsu-green">Follow-Ups</router-link>
            <router-link to="/health-dashboard" class="text-gray-700 hover:text-cpsu-green">Analytics</router-link>
            <router-link to="/chat" class="text-gray-700 hover:text-cpsu-green">Chat</router-link>
            <router-link to="/history" class="text-gray-700 hover:text-cpsu-green">History</router-link>
            <router-link to="/profile" class="text-cpsu-green font-semibold">Profile</router-link>
          </div>
          <button class="lg:hidden text-cpsu-green text-2xl" @click="mobileMenuOpen = !mobileMenuOpen">
            ☰
          </button>
        </div>
        <!-- Mobile Menu -->
        <div v-if="mobileMenuOpen" class="lg:hidden mt-4 pb-4 space-y-2">
          <router-link to="/dashboard" class="block py-2 text-gray-700 hover:text-cpsu-green">Dashboard</router-link>
          <router-link to="/symptom-checker" class="block py-2 text-gray-700 hover:text-cpsu-green">Check Symptoms</router-link>
          <router-link to="/medications" class="block py-2 text-gray-700 hover:text-cpsu-green">Medications</router-link>
          <router-link to="/followups" class="block py-2 text-gray-700 hover:text-cpsu-green">Follow-Ups</router-link>
          <router-link to="/health-dashboard" class="block py-2 text-gray-700 hover:text-cpsu-green">Analytics</router-link>
          <router-link to="/chat" class="block py-2 text-gray-700 hover:text-cpsu-green">Chat</router-link>
          <router-link to="/history" class="block py-2 text-gray-700 hover:text-cpsu-green">History</router-link>
          <router-link to="/profile" class="block py-2 text-cpsu-green font-semibold">Profile</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8 max-w-7xl">
      <div class="mb-6">
        <router-link to="/dashboard" class="text-cpsu-green hover:underline mb-4 inline-block">
          ← Back to Dashboard
        </router-link>
        <h2 class="text-3xl font-heading font-bold text-gray-900">My Profile</h2>
        <p class="text-gray-600 mt-2">Manage your account information</p>
      </div>

      <!-- Profile Form -->
      <div class="card">
        <form @submit.prevent="handleUpdate">
          <!-- Success/Error Messages -->
          <div class="mb-4">
            <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-3">
              {{ successMessage }}
            </div>
            <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
              {{ authStore.error }}
            </div>
          </div>

          <!-- Form Fields in 2 Columns -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <!-- School ID (Read-only) -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                School ID
              </label>
              <input
                type="text"
                :value="authStore.user?.school_id"
                disabled
                class="input-field bg-gray-100 cursor-not-allowed"
              />
              <p class="text-xs text-gray-500 mt-1">School ID cannot be changed</p>
            </div>

            <!-- Role (Read-only) -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Role
              </label>
              <input
                type="text"
                :value="authStore.user?.role"
                disabled
                class="input-field bg-gray-100 cursor-not-allowed"
              />
            </div>

            <!-- Name -->
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                Full Name
              </label>
              <input
                id="name"
                v-model="profileData.name"
                type="text"
                required
                class="input-field"
              />
            </div>

            <!-- Department -->
            <div>
              <label for="department" class="block text-sm font-medium text-gray-700 mb-2">
                Department
              </label>
              <select
                id="department"
                v-model="profileData.department"
                class="input-field"
              >
                <option value="">Select department</option>
                <option>College of Agriculture and Forestry</option>
                <option>College of Teacher Education</option>
                <option>College of Arts and Sciences</option>
                <option>College of Hospitality Management</option>
                <option>College of Engineering</option>
                <option>College of Computer Studies</option>
                <option>College of Criminal Justice Education</option>
              </select>
            </div>

            <!-- CPSU Address -->
            <div>
              <label for="cpsu-address" class="block text-sm font-medium text-gray-700 mb-2">
                CPSU Address
              </label>
              <input
                id="cpsu-address"
                v-model="profileData.cpsu_address"
                type="text"
                class="input-field"
                placeholder="e.g., Dorm Building A, Room 201"
              />
            </div>

            <!-- Member Since -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Member Since
              </label>
              <input
                type="text"
                :value="formatDate(authStore.user?.date_joined)"
                disabled
                class="input-field bg-gray-100 cursor-not-allowed"
              />
            </div>
          </div>

          <!-- Data Consent Status -->\n          <div class="border-t pt-4 mb-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Privacy & Data Consent</h3>
            <div v-if="authStore.user?.data_consent_given" class="bg-green-50 border border-green-200 rounded-lg p-4">
              <div class="flex items-start">
                <span class="text-green-600 text-xl mr-3">✓</span>
                <div>
                  <p class="font-semibold text-green-900">Data consent granted</p>
                  <p class="text-sm text-green-700 mt-1">
                    You granted consent on {{ formatDate(authStore.user?.consent_date) }}. 
                    You can use symptom checker, AI chat, and all health features.
                  </p>
                </div>
              </div>
            </div>
            <div v-else class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div class="flex items-start">
                <span class="text-yellow-600 text-xl mr-3">⚠</span>
                <div class="flex-1">
                  <p class="font-semibold text-yellow-900">Data consent required</p>
                  <p class="text-sm text-yellow-700 mt-1 mb-3">
                    You need to grant consent to use symptom checker, AI chat, and health insights features.
                  </p>
                  <button
                    @click="handleConsentUpdate(true)"
                    type="button"
                    class="btn-primary !py-2 !px-4 text-sm"
                  >
                    Grant Consent Now
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="authStore.loading"
              class="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="authStore.loading">Updating...</span>
              <span v-else>Update Profile</span>
            </button>
            <router-link to="/dashboard" class="btn-outline flex-1 text-center">
              Cancel
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const successMessage = ref('')
const mobileMenuOpen = ref(false)

const profileData = ref({
  name: '',
  department: '',
  cpsu_address: ''
})

onMounted(() => {
  if (authStore.user) {
    profileData.value = {
      name: authStore.user.name || '',
      department: authStore.user.department || '',
      cpsu_address: authStore.user.cpsu_address || ''
    }
  }
})

async function handleUpdate() {
  successMessage.value = ''
  const success = await authStore.updateProfile(profileData.value)
  
  if (success) {
    successMessage.value = 'Profile updated successfully!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  }
}

async function handleConsentUpdate(consentGiven: boolean) {
  try {
    await api.post('/profile/consent/', { 
      data_consent_given: consentGiven 
    })
    
    // Refresh user profile
    await authStore.fetchProfile()
    
    successMessage.value = consentGiven 
      ? 'Data consent granted! You can now use all health features.' 
      : 'Data consent revoked.'
    
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err: any) {
    authStore.error = err.response?.data?.error || 'Failed to update consent'
  }
}

function formatDate(date: string | null | undefined): string {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString()
}
</script>
