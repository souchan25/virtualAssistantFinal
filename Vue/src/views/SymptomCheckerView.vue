c<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-3 sm:py-4">
        <div class="flex justify-between items-center">
          <router-link to="/dashboard" class="text-cpsu-green flex-shrink-0">
            <h1 class="text-lg sm:text-xl lg:text-2xl font-heading font-bold">CPSU Health Assistant</h1>
            <p class="text-xs sm:text-sm text-gray-600 hidden sm:block">Mighty Hornbills</p>
          </router-link>
          
          <!-- Desktop Navigation -->
          <div class="hidden xl:flex items-center space-x-1 lg:space-x-2">
            <router-link to="/dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Dashboard</router-link>
            <router-link to="/symptom-checker" class="text-cpsu-green font-semibold px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Check Symptoms</router-link>
            <router-link to="/medications" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Medications</router-link>
            <router-link to="/followups" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Follow-Ups</router-link>
            <router-link to="/health-dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Analytics</router-link>
            <router-link to="/chat" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Chat</router-link>
            <router-link to="/history" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">History</router-link>
            <router-link to="/profile" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Profile</router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button class="xl:hidden text-cpsu-green p-2 -mr-2" @click="mobileMenuOpen = !mobileMenuOpen">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile/Tablet Menu -->
        <div v-if="mobileMenuOpen" class="xl:hidden mt-3 pt-3 pb-2 space-y-2 border-t border-gray-200">
          <router-link to="/dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Dashboard</router-link>
          <router-link to="/symptom-checker" class="block px-4 py-2 text-cpsu-green font-semibold hover:bg-gray-100 rounded text-sm">Check Symptoms</router-link>
          <router-link to="/medications" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Medications</router-link>
          <router-link to="/followups" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Follow-Ups</router-link>
          <router-link to="/health-dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Analytics</router-link>
          <router-link to="/chat" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Chat</router-link>
          <router-link to="/history" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">History</router-link>
          <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Profile</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-6 sm:py-8 w-full">
      <div class="mb-6 sm:mb-8">
        <router-link to="/dashboard" class="text-cpsu-green hover:underline mb-3 sm:mb-4 inline-block text-sm sm:text-base">
          ← Back to Dashboard
        </router-link>
        <h2 class="text-2xl sm:text-3xl font-heading font-bold text-gray-900">Symptom Checker</h2>
        <p class="text-gray-600 mt-2 text-sm sm:text-base">Select your symptoms to get AI-powered health insights</p>
      </div>

      <!-- Step Indicator -->
      <div class="mb-6 sm:mb-8 overflow-x-auto">
        <div class="flex items-center justify-center space-x-2 min-w-max px-2">
          <div :class="['flex items-center flex-shrink-0', currentStep >= 1 ? 'text-cpsu-green' : 'text-gray-400']">
            <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-full border-2 flex items-center justify-center font-bold text-xs sm:text-sm flex-shrink-0"
                 :class="currentStep >= 1 ? 'border-cpsu-green bg-cpsu-green text-white' : 'border-gray-400'">
              1
            </div>
            <span class="ml-1 sm:ml-2 font-medium text-xs sm:text-base whitespace-nowrap">Select Symptoms</span>
          </div>
          <div class="w-6 sm:w-8 lg:w-12 h-1 bg-gray-300 flex-shrink-0" :class="{ 'bg-cpsu-green': currentStep >= 2 }"></div>
          <div :class="['flex items-center flex-shrink-0', currentStep >= 2 ? 'text-cpsu-green' : 'text-gray-400']">
            <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-full border-2 flex items-center justify-center font-bold text-xs sm:text-sm flex-shrink-0"
                 :class="currentStep >= 2 ? 'border-cpsu-green bg-cpsu-green text-white' : 'border-gray-400'">
              2
            </div>
            <span class="ml-1 sm:ml-2 font-medium text-xs sm:text-base whitespace-nowrap">Get Results</span>
          </div>
        </div>
      </div>

      <!-- Step 1: Symptom Selection -->
      <div v-if="currentStep === 1" class="card p-4 sm:p-6">
        <h3 class="text-lg sm:text-xl font-bold text-gray-900 mb-4">Select Your Symptoms</h3>
        
        <!-- Search -->
        <div class="mb-6">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search symptoms..."
            class="input-field text-sm sm:text-base"
          />
        </div>

        <!-- Selected Symptoms -->
        <div v-if="symptomsStore.selectedSymptoms.length > 0" class="mb-6">
          <p class="text-xs sm:text-sm font-medium text-gray-700 mb-2">Selected ({{ symptomsStore.selectedSymptoms.length }}):</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="symptom in symptomsStore.selectedSymptoms"
              :key="symptom"
              class="px-2 sm:px-3 py-1 bg-cpsu-green text-white rounded-full text-xs sm:text-sm flex items-center gap-1 sm:gap-2"
            >
              <span class="truncate">{{ formatSymptomName(symptom) }}</span>
              <button @click="symptomsStore.toggleSymptom(symptom)" class="hover:text-cpsu-yellow flex-shrink-0">✕</button>
            </span>
          </div>
        </div>

        <!-- Symptoms Grid -->
        <div v-if="symptomsStore.loading" class="text-center py-8">
          <div class="spinner w-12 h-12 mx-auto"></div>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 sm:gap-3 max-h-96 overflow-y-auto">
          <button
            v-for="symptom in filteredSymptoms"
            :key="symptom"
            @click="symptomsStore.toggleSymptom(symptom)"
            class="px-3 sm:px-4 py-2 sm:py-3 rounded-lg border-2 text-left transition-all text-xs sm:text-sm"
            :class="symptomsStore.selectedSymptoms.includes(symptom)
              ? 'border-cpsu-green bg-cpsu-green text-white'
              : 'border-gray-300 hover:border-cpsu-green'"
          >
            {{ formatSymptomName(symptom) }}
          </button>
        </div>

        <!-- Actions -->
        <div class="mt-6 flex flex-col sm:flex-row gap-3 sm:gap-4 justify-between">
          <button
            v-if="symptomsStore.selectedSymptoms.length > 0"
            @click="symptomsStore.clearSelection"
            class="btn-outline text-xs sm:text-sm"
          >
            Clear All
          </button>
          <button
            :disabled="symptomsStore.selectedSymptoms.length === 0"
            @click="getPrediction"
            class="btn-primary text-xs sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Get Prediction ({{ symptomsStore.selectedSymptoms.length }})
          </button>
        </div>
      </div>

      <!-- Step 2: Results -->
      <div v-if="currentStep === 2 && symptomsStore.predictionResult" class="space-y-4 sm:space-y-6">
        <!-- Main Result -->
        <div class="card-bordered p-4 sm:p-6">
          <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-4">
            <div class="min-w-0">
              <h3 class="text-xl sm:text-2xl font-bold text-cpsu-green break-words">{{ symptomsStore.predictionResult.predicted_disease }}</h3>
              <p class="text-gray-600 mt-1 text-sm">Based on {{ symptomsStore.selectedSymptoms.length }} symptoms</p>
            </div>
            <div class="text-right flex-shrink-0">
              <div class="text-2xl sm:text-3xl font-bold text-cpsu-green">
                {{ getConfidencePercent() }}%
              </div>
              <p class="text-xs sm:text-sm text-gray-600">Confidence</p>
              <span v-if="symptomsStore.predictionResult.llm_validated" class="inline-block mt-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                ✅ AI Validated
              </span>
            </div>
          </div>

          <!-- Top Predictions -->
          <div v-if="symptomsStore.predictionResult.top_predictions && symptomsStore.predictionResult.top_predictions.length > 1" class="mb-4">
            <h4 class="font-semibold text-gray-900 mb-3 text-sm sm:text-base">Other Possible Conditions:</h4>
            <div class="space-y-2">
              <div
                v-for="(pred, index) in symptomsStore.predictionResult.top_predictions.slice(1, 3)"
                :key="index"
                class="flex items-center justify-between p-2 sm:p-3 bg-gray-50 rounded-lg text-sm"
              >
                <span class="text-gray-800 truncate">{{ pred.disease }}</span>
                <span class="text-gray-600 font-medium flex-shrink-0 ml-2">{{ (pred.confidence * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div v-if="symptomsStore.predictionResult.description" class="mb-4 p-3 sm:p-4 bg-blue-50 rounded-lg">
            <h4 class="font-semibold text-gray-900 mb-2 text-sm sm:text-base">Description:</h4>
            <p class="text-gray-700 text-sm">{{ symptomsStore.predictionResult.description }}</p>
          </div>

          <!-- LLM Validation -->
          <div v-if="symptomsStore.predictionResult.llm_validation" class="mb-4 p-3 sm:p-4 bg-green-50 border border-green-200 rounded-lg">
            <h4 class="font-semibold text-green-900 mb-2 text-sm sm:text-base">✅ AI Validation:</h4>
            <p class="text-green-800 text-sm">{{ symptomsStore.predictionResult.llm_validation.reasoning || 'Prediction validated by multiple AI models' }}</p>
          </div>
        </div>

        <!-- Precautions -->
        <div v-if="symptomsStore.predictionResult.precautions" class="card p-4 sm:p-6">
          <h4 class="font-semibold text-gray-900 mb-3 text-sm sm:text-base">Recommended Precautions:</h4>
          <ul class="space-y-2">
            <li
              v-for="(precaution, index) in symptomsStore.predictionResult.precautions"
              :key="index"
              class="flex items-start gap-2"
            >
              <span class="text-cpsu-green flex-shrink-0">✓</span>
              <span class="text-gray-700 text-sm">{{ precaution }}</span>
            </li>
          </ul>
        </div>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row gap-3 sm:gap-4">
          <button @click="startOver" class="btn-outline text-xs sm:text-sm flex-1">
            Check Again
          </button>
          <router-link to="/chat" class="btn-secondary text-xs sm:text-sm text-center flex-1">
            Talk to Health Assistant
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSymptomsStore } from '@/stores/symptoms'

const router = useRouter()
const authStore = useAuthStore()
const symptomsStore = useSymptomsStore()

const currentStep = ref(1)
const searchQuery = ref('')
const mobileMenuOpen = ref(false)

const filteredSymptoms = computed(() => {
  if (!searchQuery.value) {
    return symptomsStore.availableSymptoms.map((s: any) => typeof s === 'string' ? s : s.name)
  }
  
  return symptomsStore.availableSymptoms
    .map((s: any) => typeof s === 'string' ? s : s.name)
    .filter((symptom: string) => 
      symptom.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
})

onMounted(async () => {
  await symptomsStore.fetchAvailableSymptoms()
})

async function getPrediction() {
  try {
    await symptomsStore.submitSymptoms(symptomsStore.selectedSymptoms, true)
    currentStep.value = 2
  } catch (error) {
    console.error('Prediction failed:', error)
  }
}

function startOver() {
  symptomsStore.clearSelection()
  currentStep.value = 1
  searchQuery.value = ''
}

function getConfidencePercent(): string {
  const result = symptomsStore.predictionResult
  if (!result) return '0.0'
  
  // Try confidence_score first (Django API), fallback to confidence, default to 0
  const confidence = result.confidence_score ?? result.confidence ?? 0
  return (confidence * 100).toFixed(1)
}

function formatSymptomName(symptom: string): string {
  // Replace underscores with spaces and capitalize each word
  return symptom
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>
