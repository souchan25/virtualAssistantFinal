<template>
  <div class="min-h-screen bg-gradient-to-br from-cpsu-green to-cpsu-green-dark">
    <!-- Header Navigation -->
    <nav class="container mx-auto px-6 py-6">
      <div class="flex justify-between items-center">
        <router-link to="/" class="flex items-center space-x-4 text-white">
          <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-16 w-16 object-contain">
          <div>
            <h1 class="text-2xl font-heading font-bold">CPSU Health Assistant</h1>
            <p class="text-sm text-cpsu-yellow">Central Philippines State University</p>
          </div>
        </router-link>
        <div class="space-x-4">
          <router-link to="/login" class="bg-white text-cpsu-green font-semibold px-6 py-2.5 rounded-lg hover:bg-gray-100 transition-colors duration-200">Login</router-link>
        </div>
      </div>
    </nav>

    <!-- Registration Form -->
    <div class="container mx-auto px-6 py-8 flex items-center justify-center">
      <div class="max-w-4xl w-full">
        <!-- Form Card -->
        <div class="bg-white rounded-lg shadow-xl p-8">
          <div class="text-center mb-6">
            <h2 class="text-3xl font-heading font-bold text-cpsu-green">Create Account</h2>
            <p class="mt-2 text-sm text-gray-600">Join CPSU Health Assistant</p>
          </div>

          <form @submit.prevent="handleRegister">
          <!-- Error Message -->
          <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm mb-4">
            {{ authStore.error }}
          </div>

          <!-- Form Fields in 2 Columns -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
            <!-- School ID -->
            <div>
              <label for="school-id" class="block text-sm font-medium text-gray-700 mb-2">
                School ID *
              </label>
              <input
                id="school-id"
                v-model="formData.school_id"
                type="text"
                required
                class="input-field"
                placeholder="e.g., 2024-001"
              />
            </div>

            <!-- Name -->
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                required
                class="input-field"
                placeholder="Juan Dela Cruz"
              />
            </div>

            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                class="input-field"
                placeholder="juan@example.com"
              />
            </div>

            <!-- Department -->
            <div>
              <label for="department" class="block text-sm font-medium text-gray-700 mb-2">
                Department
              </label>
              <select
                id="department"
                v-model="formData.department"
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

            <!-- Password -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Password *
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  minlength="8"
                  class="input-field pr-10"
                  placeholder="At least 8 characters"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                >
                  <span v-if="!showPassword">
                    <!-- Eye Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </span>
                  <span v-else>
                    <!-- Eye Slash Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                  </span>
                </button>
              </div>
              <!-- Password Requirements -->
              <div class="mt-1 text-xs space-y-1">
                <p :class="passwordLengthValid ? 'text-green-600' : 'text-gray-500'">
                  • At least 8 characters
                </p>
                <p :class="passwordSpecialCharValid ? 'text-green-600' : 'text-gray-500'">
                  • At least one special character
                </p>
              </div>
            </div>

            <!-- Confirm Password -->
            <div class="md:col-span-2">
              <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password *
              </label>
              <div class="relative">
                <input
                  id="confirm-password"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  required
                  class="input-field pr-10"
                  :class="{ 'border-red-500': confirmPassword && confirmPassword !== formData.password }"
                  placeholder="Re-enter password"
                />
                <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                >
                  <span v-if="!showConfirmPassword">
                    <!-- Eye Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </span>
                  <span v-else>
                    <!-- Eye Slash Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                  </span>
                </button>
              </div>
              <p v-if="confirmPassword && confirmPassword !== formData.password" class="mt-1 text-sm text-red-600">
                Passwords do not match
              </p>
            </div>
          </div>

          <!-- Data Consent -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <label class="flex items-start cursor-pointer">
              <input
                id="data-consent"
                v-model="formData.data_consent_given"
                type="checkbox"
                required
                class="mt-1 mr-3 h-4 w-4 text-cpsu-green border-gray-300 rounded focus:ring-cpsu-green"
              />
              <span class="text-sm text-gray-700">
                <strong class="text-gray-900">I consent to health data storage *</strong>
                <br />
                By checking this box, you agree to allow CPSU Health Assistant to store your health information 
                (symptoms, predictions, chat history) for providing personalized health recommendations and insights.
                You can revoke this consent anytime from your profile settings.
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.loading || (!!confirmPassword && confirmPassword !== formData.password) || !isPasswordValid"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed mb-4"
          >
            <span v-if="authStore.loading">Creating account...</span>
            <span v-else>Create Account</span>
          </button>

          <!-- Login Link -->
          <div class="text-center text-sm">
            <span class="text-gray-600">Already have an account?</span>
            <router-link to="/login" class="ml-1 text-cpsu-green font-semibold hover:text-cpsu-green-dark">
              Sign in here
            </router-link>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  school_id: '',
  name: '',
  email: '',
  password: '',
  department: '',
  data_consent_given: false
})

const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordLengthValid = computed(() => formData.value.password.length >= 8)
const passwordSpecialCharValid = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(formData.value.password))
const isPasswordValid = computed(() => passwordLengthValid.value && passwordSpecialCharValid.value)

async function handleRegister() {
  if (confirmPassword.value !== formData.value.password || !isPasswordValid.value) {
    return
  }

  // Include password_confirm in payload for Django validation
  const registrationData = {
    ...formData.value,
    password_confirm: confirmPassword.value
  }

  const success = await authStore.register(registrationData)
  
  if (success) {
    router.push('/dashboard')
  }
}
</script>
