<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-cpsu-green text-white shadow-lg">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-2xl font-heading font-bold">Staff Dashboard</h1>
            <p class="text-sm text-cpsu-yellow">Clinic Management Portal</p>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/dashboard" class="text-white hover:text-cpsu-yellow">
              Student View
            </router-link>
            <button @click="handleLogout" class="btn-secondary !py-2 !px-4">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-heading font-bold text-gray-900">Staff Dashboard</h2>
        <p class="text-gray-600 mt-2">Monitor student health activities</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid md:grid-cols-4 gap-6 mb-8">
        <div class="card">
          <p class="text-gray-600 text-sm mb-1">Total Students</p>
          <p class="text-3xl font-bold text-cpsu-green">—</p>
        </div>
        <div class="card">
          <p class="text-gray-600 text-sm mb-1">Active Today</p>
          <p class="text-3xl font-bold text-cpsu-green">—</p>
        </div>
        <div class="card">
          <p class="text-gray-600 text-sm mb-1">Total Predictions</p>
          <p class="text-3xl font-bold text-cpsu-green">—</p>
        </div>
        <div class="card">
          <p class="text-gray-600 text-sm mb-1">This Week</p>
          <p class="text-3xl font-bold text-cpsu-green">—</p>
        </div>
      </div>

      <!-- Placeholder Message -->
      <div class="card text-center py-12">
        <div class="text-6xl mb-4">👨‍⚕️</div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Staff Dashboard Coming Soon</h3>
        <p class="text-gray-600">
          Full dashboard features including student directory, reports, and analytics will be available soon.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>
