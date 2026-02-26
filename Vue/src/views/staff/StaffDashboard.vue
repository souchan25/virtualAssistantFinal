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
                  Staff Dashboard - <router-link to="/profile" class="hover:text-cpsu-green hover:underline">{{ authStore.user?.name }}</router-link>
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
          <StaffNavigation />
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
          <!-- Error Alert -->
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-start">
            <span class="text-2xl mr-3">⚠️</span>
            <div>
              <p class="font-bold">Error Loading Data</p>
              <p>{{ error }}</p>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-8">
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

          <!-- Tabs -->
          <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200">
            <div class="border-b border-gray-200">
              <div class="flex flex-col sm:flex-row space-y-1 sm:space-y-0 sm:space-x-1 p-1">
                <button
                  @click="activeTab = 'overview'"
                  :class="[
                    'px-6 py-3 font-medium rounded-md sm:rounded-t-lg transition',
                    activeTab === 'overview'
                      ? 'bg-cpsu-green text-white'
                      : 'text-gray-600 hover:bg-gray-100',
                  ]"
                >
                  Overview
                </button>
                <button
                  @click="activeTab = 'reports'"
                  :class="[
                    'px-6 py-3 font-medium rounded-md sm:rounded-t-lg transition',
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

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
                                Dept
                              </th>
                              <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                              >
                                Symptoms
                              </th>
                              <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                              >
                                %
                              </th>
                            </tr>
                          </thead>
                          <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                              v-for="dept in stats.department_breakdown.slice(0, 5)"
                              :key="dept.department"
                              class="hover:bg-gray-50"
                            >
                              <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                              >
                                {{ dept.department.split(' ').map((w: any) => w[0]).join('') }} <!-- Initials -->
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
                        Recent Activity
                      </h3>

                      <div v-if="recentActivity.length === 0" class="text-center py-8 bg-gray-50 rounded-lg">
                        <p class="text-gray-600">No recent activity</p>
                      </div>

                      <div v-else class="space-y-3">
                        <div
                          v-for="(item, idx) in recentActivity"
                          :key="idx"
                          class="flex items-start p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition border-l-4"
                          :class="getActivityColor(item.type)"
                        >
                          <div class="flex-1">
                            <div class="flex justify-between">
                                <span class="font-bold text-sm text-gray-800">{{ item.title }}</span>
                                <span class="text-xs text-gray-500">{{ formatDate(item.date) }}</span>
                            </div>
                            <p class="text-sm text-gray-600">{{ item.desc }}</p>
                            <p class="text-xs text-gray-500 mt-1">{{ item.sub }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                </div>
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
import ReportsExport from "./ReportsExport.vue";
import StaffNavigation from "@/components/StaffNavigation.vue";
import clinicBg from "@/assets/images/clinic_background.jfif";

const router = useRouter();
const authStore = useAuthStore();

const activeTab = ref("overview");
const loading = ref(false);
const error = ref("");
const stats = ref<any>({});
const recentActivity = ref<any[]>([]);

onMounted(async () => {
  await loadDashboard();
});

async function loadDashboard() {
  loading.value = true;
  error.value = "";

  try {
    // Use Promise.allSettled to ensure dashboard loads even if one API fails
    const results = await Promise.allSettled([
      api.get("/staff/dashboard/"),
      api.get("/appointments/"),
      api.get("/messages/")
    ]);

    const [dashResult, apptResult, msgResult] = results;

    // Process Dashboard Stats
    if (dashResult.status === 'fulfilled') {
      stats.value = dashResult.value.data;
    } else {
      console.error("Failed to load dashboard stats:", dashResult.reason);
      error.value = "Failed to load dashboard statistics. Please check your connection.";
    }

    const activity = [];

    // Process Symptoms
    if (stats.value.recent_symptoms) {
        activity.push(...stats.value.recent_symptoms.map((s: any) => ({
            type: 'symptom',
            title: 'Symptom Report',
            desc: s.predicted_disease,
            sub: `${s.student_name} (${s.student_school_id})`,
            date: s.created_at
        })));
    }

    // Process Appointments
    if (apptResult.status === 'fulfilled' && apptResult.value.data) {
        // Handle pagination
        const appts = Array.isArray(apptResult.value.data) ? apptResult.value.data : (apptResult.value.data.results || []);
        const recentAppts = appts.filter((a: any) => a.status === 'pending').slice(0, 5);
        activity.push(...recentAppts.map((a: any) => ({
            type: 'appointment',
            title: 'Appointment Request',
            desc: a.purpose,
            sub: `${a.student_name} - ${a.scheduled_date}`,
            date: a.created_at
        })));
    } else if (apptResult.status === 'rejected') {
        console.error("Failed to load appointments:", apptResult.reason);
    }

    // Process Messages
    if (msgResult.status === 'fulfilled' && msgResult.value.data) {
        // Handle pagination
        const msgs = Array.isArray(msgResult.value.data) ? msgResult.value.data : (msgResult.value.data.results || []);
        const unreadMsgs = msgs.filter((m: any) => !m.is_read && m.recipient === authStore.user?.id).slice(0, 5);
        activity.push(...unreadMsgs.map((m: any) => ({
            type: 'message',
            title: 'New Message',
            desc: m.content,
            sub: `From ${m.sender_name}`,
            date: m.timestamp
        })));
    } else if (msgResult.status === 'rejected') {
        console.error("Failed to load messages:", msgResult.reason);
    }

    // Sort
    recentActivity.value = activity.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).slice(0, 10);

  } catch (err: any) {
    console.error("Unexpected error loading dashboard:", err);
    error.value = "An unexpected error occurred while loading the dashboard.";
  } finally {
    loading.value = false;
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr) return "N/A";
  const date = new Date(dateStr);
  const now = new Date();
  if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }
  return date.toLocaleDateString([], { month: "short", day: "numeric" });
}

function getActivityColor(type: string) {
    if (type === 'symptom') return 'border-red-500';
    if (type === 'appointment') return 'border-yellow-500';
    if (type === 'message') return 'border-blue-500';
    return 'border-gray-500';
}

async function handleLogout() {
  await authStore.logout();
  router.push("/login");
}
</script>
