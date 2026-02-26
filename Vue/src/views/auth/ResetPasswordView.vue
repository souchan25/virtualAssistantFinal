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
      </div>
    </nav>

    <!-- Reset Password Form -->
    <div class="container mx-auto px-6 py-12 flex items-center justify-center">
      <div class="max-w-md w-full">
        <!-- Form Card -->
        <div class="bg-white rounded-lg shadow-xl p-8">
          <div class="text-center mb-8">
            <h2 class="text-3xl font-heading font-bold text-cpsu-green">Create New Password</h2>
            <p class="mt-2 text-sm text-gray-600">Please enter your new password below</p>
          </div>

          <form @submit.prevent="handleReset" class="space-y-6">
            <!-- Success Message -->
            <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm text-center">
              {{ successMsg }}
              <div class="mt-3">
                <router-link to="/login" class="text-cpsu-green font-bold underline hover:text-cpsu-green-dark">
                  Click here to log in
                </router-link>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="errorMsg" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {{ errorMsg }}
            </div>

            <div v-if="!successMsg">
              <!-- New Password -->
              <div class="mb-4">
                <label for="new-password" class="block text-sm font-medium text-gray-700 mb-2">
                  New Password
                </label>
                <input
                  id="new-password"
                  v-model="newPassword"
                  type="password"
                  required
                  minlength="6"
                  class="input-field"
                  placeholder="At least 6 characters"
                />
              </div>

              <!-- Confirm Password -->
              <div class="mb-6">
                <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
                  Confirm Password
                </label>
                <input
                  id="confirm-password"
                  v-model="confirmPassword"
                  type="password"
                  required
                  minlength="6"
                  class="input-field"
                  placeholder="Re-enter your password"
                />
              </div>

              <!-- Submit Button -->
              <button
                type="submit"
                :disabled="loading"
                class="w-full btn-primary flex justify-center items-center h-11"
              >
                <span v-if="loading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span v-else>Reset Password</span>
              </button>
            </div>
            
            <div v-if="!successMsg" class="text-center mt-4 text-sm">
              <router-link to="/login" class="text-gray-600 hover:text-cpsu-green">
                Return to sign in
              </router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const uid = ref('')
const token = ref('')

onMounted(() => {
  // Extract uid and token from the URL query params
  uid.value = route.query.uid as string || ''
  token.value = route.query.token as string || ''

  if (!uid.value || !token.value) {
    errorMsg.value = 'Invalid or missing password reset link. Please request a new link.'
  }
})

async function handleReset() {
  errorMsg.value = ''
  
  if (!uid.value || !token.value) {
    errorMsg.value = 'Invalid link.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match.'
    return
  }

  if (newPassword.value.length < 6) {
    errorMsg.value = 'Password must be at least 6 characters.'
    return
  }

  loading.value = true

  try {
    const res = await api.post('/auth/reset-password-confirm/', {
      uid: uid.value,
      token: token.value,
      new_password: newPassword.value
    })
    
    successMsg.value = res.data.message || 'Password reset successfully!'
    newPassword.value = ''
    confirmPassword.value = ''
    
    // Auto redirect back to login after 3 seconds
    setTimeout(() => {
      if (router.currentRoute.value.path === '/reset-password') {
        router.push('/login')
      }
    }, 3000)
    
  } catch (err: any) {
    errorMsg.value = err.response?.data?.error || 'Failed to reset password. The link may have expired.'
  } finally {
    loading.value = false
  }
}
</script>
