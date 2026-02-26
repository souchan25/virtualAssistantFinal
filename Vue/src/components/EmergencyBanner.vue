<template>
  <div v-if="activeAlert" class="bg-red-600 text-white px-4 py-3 shadow-lg fixed top-0 w-full z-[100] animate-pulse">
    <div class="container mx-auto flex justify-between items-center">
      <div class="flex items-center gap-3">
        <span class="text-2xl">🚨</span>
        <div>
          <p class="font-bold text-lg">EMERGENCY ALERT</p>
          <p class="text-sm opacity-90">{{ activeAlert.student_name }} at {{ activeAlert.location }}</p>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="respond" class="bg-white text-red-600 px-4 py-1 rounded font-bold hover:bg-gray-100">
          RESPOND
        </button>
        <button @click="dismiss" class="text-white hover:text-gray-200 font-bold text-xl px-2">
          ✕
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const activeAlert = ref<any>(null)
let pollInterval: any = null

const checkEmergencies = async () => {
  if (authStore.user?.role !== 'staff') {
      activeAlert.value = null
      return
  }

  try {
    const res = await api.get('/emergency/active/')
    const alerts = res.data.emergencies || []
    // Find active alerts
    const active = alerts.find((a: any) => a.status === 'active')
    if (active) {
        // Only update if ID changed to avoid re-showing dismissed ones?
        // For simplicity, we show if active. Dismiss hides it locally for session?
        // Or hides it until next poll?
        // Ideally we store 'dismissed_ids'.
        if (!dismissedIds.value.has(active.id)) {
            activeAlert.value = active
        }
    } else {
        activeAlert.value = null
    }
  } catch (e) {
    // silent fail
  }
}

const dismissedIds = ref(new Set())

const respond = () => {
  if (activeAlert.value) {
    router.push('/staff/emergencies')
    activeAlert.value = null
  }
}

const dismiss = () => {
  if (activeAlert.value) {
      dismissedIds.value.add(activeAlert.value.id)
      activeAlert.value = null
  }
}

watch(() => authStore.user, (u) => {
    if (u?.role === 'staff' && !pollInterval) {
        checkEmergencies()
        pollInterval = setInterval(checkEmergencies, 15000)
    } else if (u?.role !== 'staff' && pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
        activeAlert.value = null
    }
})

onMounted(() => {
  if (authStore.user?.role === 'staff') {
    checkEmergencies()
    pollInterval = setInterval(checkEmergencies, 15000)
  }
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>
