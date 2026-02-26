<template>
  <div id="app" class="min-h-screen">
    <EmergencyBanner />
    <RouterView />
    
    <!-- Emergency SOS Button (shows only when logged in) -->
    <EmergencySOS v-if="authStore.isAuthenticated && authStore.user?.role === 'student'" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import EmergencySOS from '@/components/EmergencySOS.vue'
import EmergencyBanner from '@/components/EmergencyBanner.vue'

const authStore = useAuthStore()

onMounted(() => {
  // Check if user is already logged in (token in localStorage)
  authStore.checkAuth()
})
</script>
