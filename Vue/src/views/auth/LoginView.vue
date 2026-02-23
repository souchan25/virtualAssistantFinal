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
          <router-link to="/register" class="bg-white text-cpsu-green font-semibold px-6 py-2.5 rounded-lg hover:bg-gray-100 transition-colors duration-200">Register</router-link>
        </div>
      </div>
    </nav>

    <!-- Login Form -->
    <div class="container mx-auto px-6 py-12 flex items-center justify-center">
      <div class="max-w-md w-full">
        <!-- Form Card -->
        <div class="bg-white rounded-lg shadow-xl p-8">
          <div class="text-center mb-8">
            <h2 class="text-3xl font-heading font-bold text-cpsu-green">Sign In</h2>
            <p class="mt-2 text-sm text-gray-600">Access your health dashboard</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Error Message -->
          <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
            {{ authStore.error }}
          </div>

          <!-- School ID -->
          <div>
            <label for="school-id" class="block text-sm font-medium text-gray-700 mb-2">
              School ID
            </label>
            <input
              id="school-id"
              v-model="credentials.school_id"
              type="text"
              required
              class="input-field"
              :class="{ 'input-error': authStore.error }"
              placeholder="Enter your school ID"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="credentials.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-field pr-10"
                :class="{ 'input-error': authStore.error }"
                placeholder="Enter your password"
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
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.loading"
            class="w-full btn-primary"
          >
            <span v-if="authStore.loading">Signing in...</span>
            <span v-else>Sign In</span>
          </button>

          <!-- Register Link -->
          <div class="text-center text-sm">
            <span class="text-gray-600">Don't have an account?</span>
            <router-link to="/register" class="ml-1 text-cpsu-green font-semibold hover:text-cpsu-green-dark">
              Register here
            </router-link>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const credentials = ref({
  school_id: '',
  password: ''
})

const showPassword = ref(false)

async function handleLogin() {
  const success = await authStore.login(credentials.value)
  
  if (success) {
    // Redirect based on user role
    const user = authStore.user
    if (user?.role === 'clinic_staff' || user?.role === 'dev') {
      router.push('/staff')
    } else {
      const redirect = route.query.redirect as string || '/dashboard'
      router.push(redirect)
    }
  }
}
</script>
