<template>
  <div class="space-y-6">
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <h3 class="font-semibold text-blue-900 mb-2">📊 Export Health Reports</h3>
      <p class="text-sm text-blue-800">Generate and download reports for clinic records and analysis</p>
    </div>

    <!-- Date Range Filters -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
        <input v-model="filters.start_date" type="date" class="input-field" />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
        <input v-model="filters.end_date" type="date" class="input-field" />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Format</label>
        <select v-model="exportFormat" class="input-field">
          <option value="json">JSON</option>
          <option value="csv">CSV</option>
          <option value="excel">Excel</option>
        </select>
      </div>
    </div>

    <!-- Export Buttons -->
    <div class="flex space-x-4">
      <button @click="generateReport" :disabled="loading" class="btn-primary">
        {{ loading ? 'Generating...' : '📥 Generate Report' }}
      </button>
      <button @click="clearDates" class="btn-outline">Clear Dates</button>
    </div>

    <!-- Preview -->
    <div v-if="reportData" class="space-y-4">
      <div class="bg-white border-2 border-cpsu-green rounded-lg p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Report Summary</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <p class="text-sm text-gray-600">Total Records</p>
            <p class="text-2xl font-bold text-cpsu-green">{{ reportData.record_count }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600">Date Range</p>
            <p class="text-sm font-medium">{{ filters.start_date || 'All' }} to {{ filters.end_date || 'Now' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600">Unique Students</p>
            <p class="text-2xl font-bold text-blue-600">{{ uniqueStudents }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600">Common Condition</p>
            <p class="text-sm font-medium">{{ mostCommonDisease }}</p>
          </div>
        </div>
        
        <button @click="downloadReport" class="btn-primary">
          📥 Download {{ exportFormat.toUpperCase() }}
        </button>
      </div>

      <!-- Data Preview -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 max-h-96 overflow-auto">
        <h4 class="font-semibold text-gray-900 mb-3">Data Preview (First 10 records)</h4>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Student ID</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Disease</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Confidence</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Symptoms</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(record, index) in (reportData?.data || []).slice(0, 10)" :key="index">
                <td class="px-4 py-2 whitespace-nowrap">{{ formatDate(record.created_at) }}</td>
                <td class="px-4 py-2 whitespace-nowrap">{{ record.student_id || 'N/A' }}</td>
                <td class="px-4 py-2">{{ record.predicted_disease }}</td>
                <td class="px-4 py-2 whitespace-nowrap">{{ (record.confidence_score * 100).toFixed(1) }}%</td>
                <td class="px-4 py-2">{{ (record.symptoms || []).slice(0, 3).join(', ') }}{{ record.symptoms?.length > 3 ? '...' : '' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      <p class="text-gray-500">Select date range and click "Generate Report" to preview data</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import api from '@/services/api'

const loading = ref(false)
const exportFormat = ref('json')
const reportData = ref<any>(null)

const filters = ref({
  start_date: '',
  end_date: ''
})

async function generateReport() {
  loading.value = true
  try {
    const params: any = { format: 'json' }  // Always get JSON for preview
    if (filters.value.start_date) params.start_date = filters.value.start_date
    if (filters.value.end_date) params.end_date = filters.value.end_date

    const response = await api.get('/staff/export/', { params })
    reportData.value = response.data
  } catch (error) {
    console.error('Failed to generate report:', error)
    alert('Failed to generate report')
  } finally {
    loading.value = false
  }
}

async function downloadReport() {
  if (exportFormat.value === 'json') {
    // JSON: use local data
    if (!reportData.value?.data) return
    const content = JSON.stringify(reportData.value.data, null, 2)
    const filename = `health_report_${new Date().toISOString().split('T')[0]}.json`
    const blob = new Blob([content], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    window.URL.revokeObjectURL(url)
  } else {
    // CSV/Excel: download from API
    try {
      loading.value = true
      const params: any = { format: exportFormat.value }
      if (filters.value.start_date) params.start_date = filters.value.start_date
      if (filters.value.end_date) params.end_date = filters.value.end_date

      const response = await api.get('/staff/export/', {
        params,
        responseType: 'blob',
        headers: {
          'Accept':
            exportFormat.value === 'excel'
              ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
              : 'text/csv'
        }
      })

      const ext = exportFormat.value === 'excel' ? 'xlsx' : 'csv'
      const filename = `health_report_${new Date().toISOString().split('T')[0]}.${ext}`
      const url = window.URL.createObjectURL(response.data)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download report')
    } finally {
      loading.value = false
    }
  }
}

function clearDates() {
  filters.value = {
    start_date: '',
    end_date: ''
  }
  reportData.value = null
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString()
}

const uniqueStudents = computed(() => {
  if (!reportData.value?.data || !Array.isArray(reportData.value.data)) return 0
  const studentIds = new Set(reportData.value.data.map((r: any) => r.student))
  return studentIds.size
})

const mostCommonDisease = computed(() => {
  if (!reportData.value?.data || !Array.isArray(reportData.value.data) || reportData.value.data.length === 0) return 'N/A'
  
  const counts: Record<string, number> = {}
  reportData.value.data.forEach((r: any) => {
    if (r.predicted_disease) {
      counts[r.predicted_disease] = (counts[r.predicted_disease] || 0) + 1
    }
  })
  
  const entries = Object.entries(counts)
  if (entries.length === 0) return 'N/A'
  
  const max = entries.reduce((a, b) => a[1] > b[1] ? a : b)
  return `${max[0]} (${max[1]})`
})
</script>
