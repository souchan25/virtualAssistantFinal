<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center space-x-4">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-14 w-14 object-contain">
            <div>
              <h1 class="text-2xl font-heading font-bold text-cpsu-green">CPSU Health Clinic</h1>
              <p class="text-sm text-gray-600">Health Analytics & Trends</p>
            </div>
          </div>
          <button @click="$router.push('/staff')" class="btn-outline !py-2 !px-4">Back to Dashboard</button>
        </div>
        <!-- Navigation Menu -->
        <div class="flex items-center space-x-4 border-t pt-3">
          <router-link to="/staff" class="text-gray-700 hover:text-cpsu-green font-medium">
            📊 Dashboard
          </router-link>
          <router-link to="/staff/emergencies" class="text-gray-700 hover:text-cpsu-green font-medium">
            🚨 Emergencies
          </router-link>
          <router-link to="/staff/students" class="text-gray-700 hover:text-cpsu-green font-medium">
            👥 Students
          </router-link>
          <router-link to="/staff/prescribe" class="text-gray-700 hover:text-cpsu-green font-medium">
            💊 Prescribe
          </router-link>
          <router-link to="/staff/adherence" class="text-gray-700 hover:text-cpsu-green font-medium">
            📈 Adherence
          </router-link>
          <router-link to="/staff/followups" class="text-gray-700 hover:text-cpsu-green font-medium">
            📋 Follow-Ups
          </router-link>
          <router-link to="/staff/analytics" class="text-cpsu-green font-semibold">
            📉 Analytics
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Health Analytics & Trends</h2>
        <p class="text-gray-600">Comprehensive health insights and disease patterns</p>
      </div>

      <!-- Date Range Selector -->
      <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-4 mb-6">
        <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-700">Time Period:</label>
          <button
            v-for="period in (['7d', '30d', '90d', '1y'] as const)"
            :key="period"
            @click="selectedPeriod = period"
            :class="['px-4 py-2 rounded-lg font-medium transition', selectedPeriod === period ? 'bg-cpsu-green text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200']"
          >
            {{ period === '7d' ? 'Last 7 Days' : period === '30d' ? 'Last 30 Days' : period === '90d' ? 'Last 3 Months' : 'Last Year' }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-cpsu-green"></div>
        <p class="mt-4 text-gray-600">Loading analytics...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Charts and Stats -->
      <div v-else class="space-y-6">
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="card-bordered bg-white">
            <h3 class="text-sm font-semibold text-gray-600 mb-2">Total Consultations</h3>
            <p class="text-3xl font-bold text-cpsu-green">{{ stats.total_consultations || 0 }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ selectedPeriod === '7d' ? 'This week' : 'Selected period' }}</p>
          </div>
          <div class="card-bordered bg-white">
            <h3 class="text-sm font-semibold text-gray-600 mb-2">Unique Patients</h3>
            <p class="text-3xl font-bold text-blue-600">{{ stats.unique_patients || 0 }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ selectedPeriod === '7d' ? 'This week' : 'Selected period' }}</p>
          </div>
          <div class="card-bordered bg-white">
            <h3 class="text-sm font-semibold text-gray-600 mb-2">Emergency Alerts</h3>
            <p class="text-3xl font-bold text-red-600">{{ stats.emergency_alerts || 0 }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ selectedPeriod === '7d' ? 'This week' : 'Selected period' }}</p>
          </div>
          <div class="card-bordered bg-white">
            <h3 class="text-sm font-semibold text-gray-600 mb-2">Prescriptions</h3>
            <p class="text-3xl font-bold text-purple-600">{{ stats.prescriptions || 0 }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ selectedPeriod === '7d' ? 'This week' : 'Selected period' }}</p>
          </div>
        </div>

        <!-- Top Diseases Chart -->
        <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Top 10 Diagnosed Conditions</h3>
          <div class="h-80">
            <Bar :data="topDiseasesChartData" :options="barChartOptions" />
          </div>
        </div>

        <!-- Consultations Trend -->
        <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Consultation Trends</h3>
          <div class="h-80">
            <Line :data="consultationTrendData" :options="lineChartOptions" />
          </div>
        </div>

        <!-- Department Distribution -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">Consultations by Department</h3>
            <div class="h-80">
              <Pie :data="departmentChartData" :options="pieChartOptions" />
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">Symptom Severity Distribution</h3>
            <div class="h-80">
              <Doughnut :data="severityChartData" :options="doughnutChartOptions" />
            </div>
          </div>
        </div>

        <!-- Common Symptoms Table -->
        <div class="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Most Common Symptoms</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rank</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Symptom</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Occurrences</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">% of Total</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(symptom, index) in stats.common_symptoms" :key="symptom.symptom">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ index + 1 }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ symptom.symptom }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ symptom.count }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div class="flex items-center">
                      <span class="mr-2">{{ symptom.percentage }}%</span>
                      <div class="w-24 bg-gray-200 rounded-full h-2">
                        <div class="bg-cpsu-green h-2 rounded-full" :style="{ width: symptom.percentage + '%' }"></div>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Bar, Line, Pie, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import api from '@/services/api'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

// State
const selectedPeriod = ref<'7d' | '30d' | '90d' | '1y'>('30d')
const loading = ref(false)
const error = ref<string | null>(null)
const stats = ref<any>({
  total_consultations: 0,
  unique_patients: 0,
  emergency_alerts: 0,
  prescriptions: 0,
  common_symptoms: [],
  top_diseases: [],
  consultation_trend: [],
  department_breakdown: [],
  severity_distribution: {}
})

// Chart Options
const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top' as const
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'right' as const
    }
  }
}

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'right' as const
    }
  }
}

// Chart Data
const topDiseasesChartData = computed(() => ({
  labels: stats.value.top_diseases?.map((d: any) => d.disease) || [],
  datasets: [{
    label: 'Cases',
    data: stats.value.top_diseases?.map((d: any) => d.count) || [],
    backgroundColor: '#006B3F',
    borderColor: '#004d2d',
    borderWidth: 1
  }]
}))

const consultationTrendData = computed(() => ({
  labels: stats.value.consultation_trend?.map((t: any) => t.date) || [],
  datasets: [{
    label: 'Consultations',
    data: stats.value.consultation_trend?.map((t: any) => t.count) || [],
    borderColor: '#006B3F',
    backgroundColor: 'rgba(0, 107, 63, 0.1)',
    tension: 0.4
  }]
}))

const departmentChartData = computed(() => ({
  labels: stats.value.department_breakdown?.map((d: any) => d.department) || [],
  datasets: [{
    data: stats.value.department_breakdown?.map((d: any) => d.count) || [],
    backgroundColor: [
      '#006B3F',
      '#FFF44F',
      '#3B82F6',
      '#EF4444',
      '#8B5CF6',
      '#10B981'
    ]
  }]
}))

const severityChartData = computed(() => ({
  labels: ['Mild', 'Moderate', 'Severe', 'Critical'],
  datasets: [{
    data: [
      stats.value.severity_distribution?.mild || 0,
      stats.value.severity_distribution?.moderate || 0,
      stats.value.severity_distribution?.severe || 0,
      stats.value.severity_distribution?.critical || 0
    ],
    backgroundColor: [
      '#10B981',
      '#FFF44F',
      '#F59E0B',
      '#EF4444'
    ]
  }]
}))

// Methods
const fetchAnalytics = async () => {
  loading.value = true
  error.value = null

  try {
    // Call the real analytics endpoint
    const response = await api.get('/staff/analytics/', {
      params: { period: selectedPeriod.value }
    })

    console.log('Analytics API Response:', response.data)
    const data = response.data

    // Map real data to stats
    stats.value = {
      total_consultations: data.summary.total_consultations || 0,
      unique_patients: data.summary.unique_patients || 0,
      emergency_alerts: data.summary.emergency_alerts || 0,
      prescriptions: data.summary.prescriptions || 0,
      common_symptoms: data.common_symptoms || [],
      top_diseases: data.top_conditions?.map((c: any) => ({
        disease: c.predicted_disease,
        count: c.count
      })) || [],
      consultation_trend: data.consultation_trends?.map((t: any) => ({
        date: new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        count: t.count
      })) || [],
      department_breakdown: data.department_breakdown?.map((d: any) => ({
        department: d.student__department || 'Unknown',
        count: d.count
      })) || [],
      severity_distribution: data.severity_distribution || {
        mild: 0,
        moderate: 0,
        severe: 0,
        critical: 0
      }
    }
    
    console.log('Stats updated:', stats.value)
  } catch (err: any) {
    error.value = err.response?.data?.error || err.message || 'Failed to load analytics'
    console.error('Error fetching analytics:', err)
    console.error('Error details:', err.response?.data)
  } finally {
    loading.value = false
  }
}

// Watch period changes
watch(selectedPeriod, () => {
  fetchAnalytics()
})

onMounted(() => {
  fetchAnalytics()
})
</script>
