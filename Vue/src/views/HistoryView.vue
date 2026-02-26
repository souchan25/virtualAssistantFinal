<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-3 sm:py-4">
        <div class="flex justify-between items-center">
          <router-link to="/dashboard" class="flex items-center space-x-2 sm:space-x-4 text-cpsu-green flex-shrink-0">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-10 w-10 sm:h-12 sm:w-12 object-contain flex-shrink-0">
            <div class="hidden sm:block">
              <h1 class="text-lg sm:text-xl lg:text-2xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs sm:text-sm text-gray-600 hidden md:block">Mighty Hornbills</p>
            </div>
          </router-link>
          
          <!-- Desktop Navigation -->
          <div class="hidden xl:flex items-center space-x-1 lg:space-x-2">
            <router-link to="/dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Dashboard</router-link>
            <router-link to="/symptom-checker" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Check Symptoms</router-link>
            <router-link to="/medications" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Medications</router-link>
            <router-link to="/followups" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Follow-Ups</router-link>
            <router-link to="/health-dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Analytics</router-link>
            <router-link to="/chat" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">AI Assistant</router-link>
            <router-link to="/history" class="text-cpsu-green font-semibold px-2 lg:px-3 py-2 text-sm whitespace-nowrap">History</router-link>
            <router-link to="/profile" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Profile</router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="xl:hidden text-cpsu-green p-2 -mr-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile/Tablet Menu -->
        <div v-if="mobileMenuOpen" class="xl:hidden mt-3 pt-3 pb-2 space-y-2 border-t border-gray-200">
          <router-link to="/dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Dashboard</router-link>
          <router-link to="/symptom-checker" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Check Symptoms</router-link>
          <router-link to="/medications" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Medications</router-link>
          <router-link to="/followups" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Follow-Ups</router-link>
          <router-link to="/health-dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Analytics</router-link>
          <router-link to="/chat" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">AI Assistant</router-link>
          <router-link to="/history" class="block px-4 py-2 text-cpsu-green font-semibold hover:bg-gray-100 rounded text-sm">History</router-link>
          <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Profile</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-6 sm:py-8 max-w-6xl">
      <div class="mb-6 sm:mb-8">
        <router-link to="/dashboard" class="text-cpsu-green hover:underline mb-3 sm:mb-4 inline-block text-sm sm:text-base">
          ← Back to Dashboard
        </router-link>
        <h2 class="text-2xl sm:text-3xl font-heading font-bold text-gray-900">Health History</h2>
        <p class="text-gray-600 mt-2 text-sm sm:text-base">View and manage your past consultations</p>
      </div>

      <!-- Loading State -->
      <div v-if="symptomsStore.loading" class="text-center py-12 sm:py-16">
        <div class="spinner w-12 h-12 sm:w-16 sm:h-16 mx-auto"></div>
        <p class="text-gray-600 mt-4 text-sm sm:text-base">Loading your history...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="symptomsStore.history.length === 0" class="card text-center py-12 sm:py-16">
        <div class="text-5xl sm:text-6xl mb-4">📋</div>
        <h3 class="text-lg sm:text-xl font-bold text-gray-900 mb-2">No History Yet</h3>
        <p class="text-gray-600 mb-6 text-sm sm:text-base">You haven't checked any symptoms yet</p>
        <router-link to="/symptom-checker" class="btn-primary inline-block text-sm sm:text-base">
          Check Symptoms Now
        </router-link>
      </div>

      <!-- History List -->
      <div v-else class="space-y-3 sm:space-y-4">
        <div
          v-for="record in symptomsStore.history"
          :key="record.id"
          class="card p-4 sm:p-6 hover:shadow-lg transition-shadow"
        >
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3 sm:gap-4 mb-4">
            <div class="flex-1 min-w-0">
              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 mb-2 flex-wrap">
                <h3 class="text-lg sm:text-xl font-bold text-cpsu-green truncate">{{ record.staff_diagnosis || record.predicted_disease }}</h3>
                <span class="px-2 sm:px-3 py-1 bg-cpsu-green text-white text-xs sm:text-sm rounded-full whitespace-nowrap">
                  {{ getConfidence(record) }}% confidence
                </span>
                <span v-if="record.staff_diagnosis" class="px-2 sm:px-3 py-1 bg-blue-100 text-blue-800 text-xs sm:text-sm rounded-full whitespace-nowrap">
                  ✏️ Staff Verified
                </span>
                <span v-else-if="record.llm_validated" class="px-2 sm:px-3 py-1 bg-blue-100 text-blue-800 text-xs sm:text-sm rounded-full whitespace-nowrap">
                  ✅ AI Validated
                </span>
              </div>
              <p v-if="record.staff_diagnosis" class="text-xs text-gray-500 mb-1">
                AI Prediction: {{ record.predicted_disease }}
              </p>
              <p class="text-xs sm:text-sm text-gray-500">
                {{ new Date(record.created_at).toLocaleString() }}
              </p>
              <p class="text-xs sm:text-sm text-gray-600 mt-1">
                {{ record.symptoms.length }} symptom{{ record.symptoms.length > 1 ? 's' : '' }} reported
              </p>
            </div>
            <button
              @click="deleteRecord(record.id)"
              class="text-red-600 hover:text-red-800 px-2 sm:px-3 py-1 hover:bg-red-50 rounded transition-colors text-xs sm:text-sm whitespace-nowrap flex-shrink-0"
              title="Delete record"
            >
              🗑️ Delete
            </button>
          </div>

          <!-- Symptoms -->
          <div class="mb-4">
            <p class="text-xs sm:text-sm font-medium text-gray-700 mb-2">Reported Symptoms:</p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="symptom in record.symptoms"
                :key="symptom"
                class="px-2 sm:px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs sm:text-sm"
              >
                {{ symptom }}
              </span>
            </div>
          </div>

          <!-- Top 3 Predictions -->
          <div v-if="record.top_predictions && record.top_predictions.length > 1" class="mb-4">
            <p class="text-xs sm:text-sm font-medium text-gray-700 mb-2">Other Possible Conditions:</p>
            <div class="space-y-2">
              <div
                v-for="(pred, index) in record.top_predictions.slice(1, 3)"
                :key="index"
                class="flex items-center justify-between p-2 sm:p-3 bg-gray-50 rounded-lg text-xs sm:text-sm"
              >
                <span class="text-gray-800 truncate">{{ pred.disease }}</span>
                <span class="text-gray-600 font-medium flex-shrink-0 ml-2">{{ (pred.confidence * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div v-if="record.description" class="mb-4 p-3 sm:p-4 bg-blue-50 rounded-lg">
            <p class="text-xs sm:text-sm font-medium text-gray-900 mb-1">Description:</p>
            <p class="text-xs sm:text-sm text-gray-700">{{ record.description }}</p>
          </div>

          <!-- Precautions -->
          <div v-if="record.precautions && record.precautions.length > 0">
            <p class="text-xs sm:text-sm font-medium text-gray-900 mb-2">Precautions:</p>
            <ul class="space-y-1">
              <li
                v-for="(precaution, index) in record.precautions"
                :key="index"
                class="text-xs sm:text-sm text-gray-700 flex items-start gap-2"
              >
                <span class="text-cpsu-green flex-shrink-0">✓</span>
                <span>{{ precaution }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSymptomsStore } from '@/stores/symptoms'
import type { SymptomRecord } from '@/types'

const symptomsStore = useSymptomsStore()
const mobileMenuOpen = ref(false)

onMounted(async () => {
  await symptomsStore.fetchHistory()
})

function getConfidence(record: SymptomRecord): string {
  // Django uses confidence_score, fallback to confidence for older records
  const conf = record.confidence_score ?? record.confidence ?? 0
  return (conf * 100).toFixed(1)
}

async function deleteRecord(id: number) {
  if (confirm('Are you sure you want to delete this record?')) {
    await symptomsStore.deleteRecord(id)
  }
}
</script>
