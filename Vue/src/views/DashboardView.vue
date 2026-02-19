<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav
      class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40"
    >
      <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-3 sm:py-4">
        <div class="flex justify-between items-center">
          <!-- Logo Section -->
          <div
            class="flex items-center space-x-2 sm:space-x-4 min-w-0 flex-shrink-0"
          >
            <img
              src="@/assets/images/cpsu-logo.png"
              alt="CPSU Logo"
              class="h-10 w-10 sm:h-12 sm:w-12 object-contain flex-shrink-0"
            />
            <div class="hidden sm:block">
              <h1
                class="text-lg sm:text-xl lg:text-2xl font-heading font-bold text-cpsu-green truncate"
              >
                CPSU Health Assistant
              </h1>
              <p class="text-xs sm:text-sm text-gray-600 hidden md:block">
                Welcome, {{ authStore.userName }}
              </p>
            </div>
          </div>

          <!-- Desktop Navigation -->
          <div class="hidden xl:flex items-center space-x-1 lg:space-x-2">
            <router-link
              to="/dashboard"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Dashboard</router-link
            >
            <router-link
              to="/symptom-checker"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Check Symptoms</router-link
            >
            <router-link
              to="/medications"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Medications</router-link
            >
            <router-link
              to="/followups"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Follow-Ups</router-link
            >
            <router-link
              to="/health-dashboard"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Analytics</router-link
            >
            <router-link
              to="/chat"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Chat</router-link
            >
            <router-link
              to="/history"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >History</router-link
            >
            <router-link
              to="/profile"
              class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm lg:text-base whitespace-nowrap"
              >Profile</router-link
            >
            <button
              @click="handleLogout"
              class="btn-outline !py-2 !px-3 text-sm"
            >
              Logout
            </button>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="xl:hidden text-cpsu-green p-2 -mr-2"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Mobile/Tablet Menu -->
        <div
          v-if="mobileMenuOpen"
          class="xl:hidden mt-3 pt-3 pb-2 space-y-2 border-t border-gray-200"
        >
          <router-link
            to="/dashboard"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Dashboard</router-link
          >
          <router-link
            to="/symptom-checker"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Check Symptoms</router-link
          >
          <router-link
            to="/medications"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Medications</router-link
          >
          <router-link
            to="/followups"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Follow-Ups</router-link
          >
          <router-link
            to="/health-dashboard"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Analytics</router-link
          >
          <router-link
            to="/chat"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Chat</router-link
          >
          <router-link
            to="/history"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >History</router-link
          >
          <router-link
            to="/profile"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm"
            >Profile</router-link
          >
          <button
            @click="handleLogout"
            class="w-full text-left px-4 py-2 text-cpsu-green hover:bg-gray-100 rounded font-semibold text-sm"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>

    <!-- Dashboard Content -->
    <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-6 sm:py-8">
      <div class="mb-6 sm:mb-8">
        <h2 class="text-2xl sm:text-3xl font-heading font-bold text-gray-900">
          Dashboard
        </h2>
        <p class="text-gray-600 mt-1 sm:mt-2 text-sm sm:text-base">
          Your health overview and quick actions
        </p>
      </div>

      <!-- Quick Actions -->
      <div
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8"
      >
        <router-link
          to="/symptom-checker"
          class="card-bordered hover:shadow-xl transition-shadow p-4 sm:p-6"
        >
          <div class="text-3xl sm:text-4xl mb-3 sm:mb-4">🩺</div>
          <h3
            class="text-base sm:text-xl font-bold text-cpsu-green mb-1 sm:mb-2"
          >
            Check Symptoms
          </h3>
          <p class="text-sm sm:text-base text-gray-600">
            Get AI-powered disease predictions
          </p>
        </router-link>

        <router-link
          to="/medications"
          class="card-bordered hover:shadow-xl transition-shadow p-4 sm:p-6"
        >
          <div class="text-3xl sm:text-4xl mb-3 sm:mb-4">💊</div>
          <h3
            class="text-base sm:text-xl font-bold text-cpsu-green mb-1 sm:mb-2"
          >
            My Medications
          </h3>
          <p class="text-sm sm:text-base text-gray-600">
            Track prescriptions and adherence
          </p>
        </router-link>

        <router-link
          to="/followups"
          class="card-bordered hover:shadow-xl transition-shadow p-4 sm:p-6"
        >
          <div class="text-3xl sm:text-4xl mb-3 sm:mb-4">📋</div>
          <h3
            class="text-base sm:text-xl font-bold text-cpsu-green mb-1 sm:mb-2"
          >
            Follow-Ups
          </h3>
          <p class="text-sm sm:text-base text-gray-600">
            Respond to health check-ins
          </p>
        </router-link>

        <router-link
          to="/health-dashboard"
          class="card-bordered hover:shadow-xl transition-shadow p-4 sm:p-6"
        >
          <div class="text-3xl sm:text-4xl mb-3 sm:mb-4">📊</div>
          <h3
            class="text-base sm:text-xl font-bold text-cpsu-green mb-1 sm:mb-2"
          >
            Health Analytics
          </h3>
          <p class="text-sm sm:text-base text-gray-600">
            View your health progress trends
          </p>
        </router-link>

        <router-link
          to="/chat"
          class="card-bordered hover:shadow-xl transition-shadow p-4 sm:p-6"
        >
          <div class="text-3xl sm:text-4xl mb-3 sm:mb-4">💬</div>
          <h3
            class="text-base sm:text-xl font-bold text-cpsu-green mb-1 sm:mb-2"
          >
            Chat Assistant
          </h3>
          <p class="text-sm sm:text-base text-gray-600">
            Talk to our health chatbot
          </p>
        </router-link>

        <router-link
          to="/history"
          class="card-bordered hover:shadow-xl transition-shadow p-4 sm:p-6"
        >
          <div class="text-3xl sm:text-4xl mb-3 sm:mb-4">📜</div>
          <h3
            class="text-base sm:text-xl font-bold text-cpsu-green mb-1 sm:mb-2"
          >
            View History
          </h3>
          <p class="text-sm sm:text-base text-gray-600">
            See your past consultations
          </p>
        </router-link>
      </div>

      <!-- Recent Activity -->
      <div class="card p-4 sm:p-6">
        <h3 class="text-lg sm:text-xl font-bold text-gray-900 mb-4">
          Recent Activity
        </h3>

        <div v-if="symptomsStore.loading" class="text-center py-8">
          <div class="spinner w-12 h-12 mx-auto"></div>
        </div>

        <div
          v-else-if="symptomsStore.history.length === 0"
          class="text-center py-8 text-gray-500"
        >
          <p class="text-sm sm:text-base">No recent activity</p>
          <router-link
            to="/symptom-checker"
            class="text-cpsu-green hover:underline mt-2 inline-block text-sm"
          >
            Start by checking your symptoms
          </router-link>
        </div>

        <div v-else class="space-y-3 sm:space-y-4">
          <div
            v-for="record in symptomsStore.history.slice(0, 5)"
            :key="record.id"
            class="border-l-4 border-cpsu-yellow pl-3 sm:pl-4 py-2 hover:bg-gray-50 overflow-hidden"
          >
            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2"
            >
              <div class="flex-1 min-w-0">
                <p
                  class="font-semibold text-gray-900 text-sm sm:text-base truncate"
                >
                  {{ record.predicted_disease }}
                </p>
                <p class="text-xs sm:text-sm text-gray-600">
                  Confidence:
                  {{
                    (
                      (record.confidence_score ?? record.confidence ?? 0) * 100
                    ).toFixed(1)
                  }}%
                </p>
                <p class="text-xs text-gray-500 mt-1">
                  {{ new Date(record.created_at).toLocaleString() }}
                </p>
              </div>
              <span
                class="px-2 py-1 bg-cpsu-green text-white text-xs rounded-full whitespace-nowrap flex-shrink-0"
              >
                {{ record.symptoms.length }} symptoms
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useSymptomsStore } from "@/stores/symptoms";

const router = useRouter();
const authStore = useAuthStore();
const symptomsStore = useSymptomsStore();
const mobileMenuOpen = ref(false);

onMounted(async () => {
  await symptomsStore.fetchHistory();
});

async function handleLogout() {
  await authStore.logout();
  router.push("/login");
}
</script>
