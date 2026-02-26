<template>
  <div>
    <!-- Navigation Menu - Desktop -->
    <div class="hidden lg:flex items-center space-x-4 border-t pt-3">
      <router-link
        to="/staff"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
        exact
      >
        📊 Dashboard
      </router-link>
      <router-link
        to="/messages"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        💬 Messages
      </router-link>

      <router-link
        to="/staff/emergencies"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        🚨 Emergencies
      </router-link>
      <router-link
        to="/staff/students"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        👥 Students
      </router-link>
      <router-link
        to="/staff/prescribe"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        💊 Prescribe
      </router-link>
      <router-link
        to="/staff/adherence"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        📈 Adherence
      </router-link>
      <router-link
        to="/staff/followups"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        📋 Follow-Ups
      </router-link>
      <router-link
        to="/staff/analytics"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        📉 Analytics
      </router-link>
      <router-link
        v-if="authStore.user?.is_superuser"
        to="/admin-panel"
        active-class="text-cpsu-green font-semibold"
        class="text-gray-700 hover:text-cpsu-green font-medium"
      >
        ⚙️ Admin
      </router-link>
    </div>

    <!-- Navigation Menu - Mobile -->
    <div class="lg:hidden border-t pt-3 overflow-x-auto">
      <div class="flex space-x-3 min-w-max pb-2">
        <router-link
          to="/staff"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
          exact
        >
          📊 Dashboard
        </router-link>
        <router-link
          to="/messages"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          💬 Messages
        </router-link>

        <router-link
          to="/staff/emergencies"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          🚨 Emergencies
        </router-link>
        <router-link
          to="/staff/students"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          👥 Students
        </router-link>
        <router-link
          to="/staff/prescribe"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          💊 Prescribe
        </router-link>
        <router-link
          to="/staff/adherence"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          📈 Adherence
        </router-link>
        <router-link
          to="/staff/followups"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          📋 Follow-Ups
        </router-link>
        <router-link
          to="/staff/analytics"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          📉 Analytics
        </router-link>
        <router-link
          v-if="authStore.user?.is_superuser"
          to="/admin-panel"
          active-class="text-cpsu-green font-semibold bg-gray-50 rounded-md"
          class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap px-3 py-2"
        >
          ⚙️ Admin
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>
