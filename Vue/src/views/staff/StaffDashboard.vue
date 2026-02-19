<template>
  <div
    class="min-h-screen relative"
    :style="{
      backgroundImage: `url(${clinicBg})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed',
    }"
  >
    <!-- Overlay for readability -->
    <div class="absolute inset-0 bg-black/40 pointer-events-none"></div>
    <!-- Content wrapper sits above overlay -->
    <div class="relative z-10 min-h-screen">
      <!-- Navigation -->
      <nav class="bg-white shadow-sm border-b-2 border-cpsu-green">
        <div class="container mx-auto px-4 sm:px-6 py-4">
          <div class="flex justify-between items-center mb-4">
            <div class="flex items-center space-x-2 sm:space-x-4">
              <img
                src="@/assets/images/cpsu-logo.png"
                alt="CPSU Logo"
                class="h-10 w-10 sm:h-14 sm:w-14 object-contain"
              />
              <div>
                <h1
                  class="text-lg sm:text-2xl font-heading font-bold text-cpsu-green"
                >
                  CPSU Health Clinic
                </h1>
                <p class="text-xs sm:text-sm text-gray-600">
                  Staff Dashboard - {{ authStore.user?.name }}
                </p>
              </div>
            </div>
            <button
              @click="handleLogout"
              class="btn-outline !py-2 !px-3 sm:!px-4 text-sm"
            >
              Logout
            </button>
          </div>
          <!-- Navigation Menu - Desktop -->
          <div class="hidden lg:flex items-center space-x-4 border-t pt-3">
            <router-link
              to="/staff"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              📊 Dashboard
            </router-link>
            <router-link
              to="/staff/emergencies"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              🚨 Emergencies
            </router-link>
            <router-link
              to="/staff/students"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              👥 Students
            </router-link>
            <router-link
              to="/staff/prescribe"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              💊 Prescribe
            </router-link>
            <router-link
              to="/staff/adherence"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              📈 Adherence
            </router-link>
            <router-link
              to="/staff/followups"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              📋 Follow-Ups
            </router-link>
            <router-link
              to="/staff/analytics"
              class="text-gray-700 hover:text-cpsu-green font-medium"
            >
              📉 Analytics
            </router-link>
          </div>
          <!-- Navigation Menu - Mobile -->
          <div class="lg:hidden border-t pt-3 overflow-x-auto">
            <div class="flex space-x-3 min-w-max">
              <router-link
                to="/staff"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                📊 Dashboard
              </router-link>
              <router-link
                to="/staff/emergencies"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                🚨 Emergencies
              </router-link>
              <router-link
                to="/staff/students"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                👥 Students
              </router-link>
              <router-link
                to="/staff/prescribe"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                💊 Prescribe
              </router-link>
              <router-link
                to="/staff/adherence"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                📈 Adherence
              </router-link>
              <router-link
                to="/staff/followups"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                📋 Follow-Ups
              </router-link>
              <router-link
                to="/staff/analytics"
                class="text-gray-700 hover:text-cpsu-green font-medium text-sm whitespace-nowrap"
              >
                📉 Analytics
              </router-link>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main Content -->
      <div class="container mx-auto px-4 sm:px-6 py-8">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div
            class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-cpsu-green border-t-transparent"
          ></div>
          <p class="mt-4 text-gray-600">Loading dashboard...</p>
        </div>

        <div v-else>
          <!-- Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="card-bordered bg-white hover:shadow-lg transition">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-semibold text-gray-600 mb-2">
                    Total Students
                  </h3>
                  <p class="text-3xl font-bold text-cpsu-green">
                    {{ stats.total_students || 0 }}
                  </p>
                </div>
                <div class="text-4xl">👥</div>
              </div>
            </div>

            <div class="card-bordered bg-white hover:shadow-lg transition">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-semibold text-gray-600 mb-2">
                    Today's Consultations
                  </h3>
                  <p class="text-3xl font-bold text-blue-600">
                    {{ stats.students_with_symptoms_today || 0 }}
                  </p>
                </div>
                <div class="text-4xl">📋</div>
              </div>
            </div>

            <div class="card-bordered bg-white hover:shadow-lg transition">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-semibold text-gray-600 mb-2">
                    This Week (7 Days)
                  </h3>
                  <p class="text-3xl font-bold text-purple-600">
                    {{ stats.students_with_symptoms_7days || 0 }}
                  </p>
                </div>
                <div class="text-4xl">📊</div>
              </div>
            </div>

            <div class="card-bordered bg-white hover:shadow-lg transition">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-semibold text-gray-600 mb-2">
                    Pending Referrals
                  </h3>
                  <p class="text-3xl font-bold text-red-600">
                    {{ stats.pending_referrals || 0 }}
                  </p>
                </div>
                <div class="text-4xl">🚨</div>
              </div>
            </div>
          </div>

          <!-- Top Insight -->
          <div
            v-if="stats.top_insight"
            class="card-bordered bg-gradient-to-r from-cpsu-yellow to-yellow-300 mb-8"
          >
            <div class="flex items-start space-x-3">
              <div class="text-3xl">🔍</div>
              <div>
                <h3 class="font-semibold text-cpsu-green mb-2">
                  Top Health Concern
                </h3>
                <p class="text-lg text-gray-800">{{ stats.top_insight }}</p>
              </div>
            </div>
          </div>

          <!-- Monthly Summary -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="card bg-white border-l-4 border-cpsu-green">
              <h3 class="text-sm font-semibold text-gray-600 mb-2">
                This Month (30 Days)
              </h3>
              <p class="text-2xl font-bold text-cpsu-green">
                {{ stats.students_with_symptoms_30days || 0 }} students
              </p>
              <p class="text-sm text-gray-500 mt-1">Had consultations</p>
            </div>

            <div class="card bg-white border-l-4 border-blue-500">
              <h3 class="text-sm font-semibold text-gray-600 mb-2">
                Active Rate
              </h3>
              <p class="text-2xl font-bold text-blue-600">
                {{
                  stats.total_students > 0
                    ? (
                        (stats.students_with_symptoms_30days /
                          stats.total_students) *
                        100
                      ).toFixed(1)
                    : 0
                }}%
              </p>
              <p class="text-sm text-gray-500 mt-1">
                Students consulted this month
              </p>
            </div>

            <div class="card bg-white border-l-4 border-purple-500">
              <h3 class="text-sm font-semibold text-gray-600 mb-2">
                Departments
              </h3>
              <p class="text-2xl font-bold text-purple-600">
                {{ stats.department_breakdown?.length || 0 }}
              </p>
              <p class="text-sm text-gray-500 mt-1">Active departments</p>
            </div>
          </div>

          <!-- Tabs -->
          <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200">
            <div class="border-b border-gray-200">
              <div class="flex space-x-1 p-1">
                <button
                  @click="activeTab = 'overview'"
                  :class="[
                    'px-6 py-3 font-medium rounded-t-lg transition',
                    activeTab === 'overview'
                      ? 'bg-cpsu-green text-white'
                      : 'text-gray-600 hover:bg-gray-100',
                  ]"
                >
                  Overview
                </button>
                <button
                  @click="activeTab = 'students'"
                  :class="[
                    'px-6 py-3 font-medium rounded-t-lg transition',
                    activeTab === 'students'
                      ? 'bg-cpsu-green text-white'
                      : 'text-gray-600 hover:bg-gray-100',
                  ]"
                >
                  Student Directory
                </button>
                <button
                  @click="activeTab = 'reports'"
                  :class="[
                    'px-6 py-3 font-medium rounded-t-lg transition',
                    activeTab === 'reports'
                      ? 'bg-cpsu-green text-white'
                      : 'text-gray-600 hover:bg-gray-100',
                  ]"
                >
                  Reports & Export
                </button>
              </div>
            </div>

            <div class="p-6">
              <!-- Overview Tab -->
              <div v-if="activeTab === 'overview'" class="space-y-6">
                <!-- Department Breakdown -->
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 mb-4">
                    Department Breakdown (Last 30 Days)
                  </h3>

                  <!-- Empty State -->
                  <div
                    v-if="
                      !stats.department_breakdown ||
                      stats.department_breakdown.length === 0
                    "
                    class="text-center py-8 bg-gray-50 rounded-lg"
                  >
                    <div class="text-5xl mb-3">🏢</div>
                    <p class="text-gray-600">No department data available</p>
                  </div>

                  <!-- Department Table -->
                  <div v-else class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                      <thead class="bg-gray-50">
                        <tr>
                          <th
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                          >
                            Department
                          </th>
                          <th
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                          >
                            Total Students
                          </th>
                          <th
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                          >
                            With Symptoms
                          </th>
                          <th
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                          >
                            % Affected
                          </th>
                        </tr>
                      </thead>
                      <tbody class="bg-white divide-y divide-gray-200">
                        <tr
                          v-for="dept in stats.department_breakdown"
                          :key="dept.department"
                          class="hover:bg-gray-50"
                        >
                          <td
                            class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                          >
                            {{ dept.department }}
                          </td>
                          <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                          >
                            {{ dept.total_students }}
                          </td>
                          <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                          >
                            {{ dept.students_with_symptoms }}
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap text-sm">
                            <span
                              class="px-2 py-1 rounded"
                              :class="
                                dept.percentage >= 30
                                  ? 'bg-red-100 text-red-800'
                                  : dept.percentage >= 15
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : 'bg-green-100 text-green-800'
                              "
                            >
                              {{ dept.percentage }}%
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <!-- Recent Activity -->
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 mb-4">
                    Recent Consultations
                  </h3>

                  <!-- Empty State -->
                  <div
                    v-if="
                      !stats.recent_symptoms ||
                      stats.recent_symptoms.length === 0
                    "
                    class="text-center py-8 bg-gray-50 rounded-lg"
                  >
                    <div class="text-5xl mb-3">📋</div>
                    <p class="text-gray-600">No recent consultations</p>
                  </div>

                  <!-- Recent Records -->
                  <div v-else class="space-y-3">
                    <div
                      v-for="record in stats.recent_symptoms"
                      :key="record.id"
                      class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                    >
                      <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-1">
                          <p class="font-medium text-gray-900">
                            {{ record.student_name || "Student" }}
                          </p>
                          <span class="text-xs text-gray-500">{{
                            record.student_school_id || ""
                          }}</span>
                        </div>
                        <p class="text-sm text-gray-600 font-semibold">
                          {{ record.predicted_disease }}
                        </p>
                        <div class="flex items-center space-x-2 mt-1">
                          <span
                            class="text-xs px-2 py-1 rounded"
                            :class="
                              record.confidence_score >= 0.8
                                ? 'bg-green-100 text-green-800'
                                : record.confidence_score >= 0.6
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : 'bg-red-100 text-red-800'
                            "
                          >
                            {{ (record.confidence_score * 100).toFixed(1) }}%
                            confidence
                          </span>
                          <span
                            v-if="record.requires_referral"
                            class="text-xs px-2 py-1 bg-red-100 text-red-800 rounded"
                          >
                            🚨 Referral Required
                          </span>
                        </div>
                        <p class="text-xs text-gray-500 mt-1">
                          Symptoms: {{ record.symptoms?.join(", ") || "N/A" }}
                        </p>
                      </div>
                      <div class="text-right ml-4">
                        <p class="text-sm text-gray-600">
                          {{ formatDate(record.created_at) }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Students Tab -->
              <div v-if="activeTab === 'students'">
                <StudentDirectory />
              </div>

              <!-- Reports Tab -->
              <div v-if="activeTab === 'reports'">
                <ReportsExport />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import StudentDirectory from "./StudentDirectory.vue";
import ReportsExport from "./ReportsExport.vue";
import clinicBg from "@/assets/images/clinic_background.jfif";

const router = useRouter();
const authStore = useAuthStore();

const activeTab = ref("overview");
const loading = ref(false);
const stats = ref<any>({
  total_students: 0,
  students_with_symptoms_today: 0,
  students_with_symptoms_7days: 0,
  students_with_symptoms_30days: 0,
  pending_referrals: 0,
  top_insight: "",
  department_breakdown: [],
  recent_symptoms: [],
});

onMounted(async () => {
  await loadDashboard();
});

async function loadDashboard() {
  loading.value = true;
  try {
    console.log("Loading Staff Dashboard...");
    const response = await api.get("/staff/dashboard/");
    console.log("Dashboard API Response:", response.data);
    stats.value = response.data;
  } catch (error: any) {
    console.error("Failed to load dashboard:", error);
    console.error("Error details:", error.response?.data);
  } finally {
    loading.value = false;
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr) return "N/A";
  const date = new Date(dateStr);
  return (
    date.toLocaleDateString() +
    " " +
    date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  );
}

async function handleLogout() {
  await authStore.logout();
  router.push("/login");
}
</script>
