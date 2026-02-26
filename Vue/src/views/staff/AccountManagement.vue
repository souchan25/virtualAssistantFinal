<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Top bar -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-10 w-10 object-contain" />
          <div>
            <h1 class="text-lg font-heading font-bold text-cpsu-green">CPSU Admin Panel</h1>
            <p class="text-xs text-gray-500">Account Management</p>
          </div>
        </div>
        <div v-if="authenticated" class="flex items-center gap-3">
          <span class="text-sm text-gray-600 hidden sm:inline">Logged in as <strong>{{ adminUser?.name || adminUser?.school_id }}</strong></span>
          <button @click="logout" class="btn-outline !py-1.5 !px-3 text-sm">Logout</button>
        </div>
      </div>
    </nav>

    <!-- Login Screen -->
    <div v-if="!authenticated" class="flex items-center justify-center px-4" style="min-height: calc(100vh - 60px);">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-8">
        <div class="text-center mb-6">
          <div class="w-16 h-16 bg-cpsu-green/10 rounded-full flex items-center justify-center mx-auto mb-3">
            <span class="text-3xl">🔐</span>
          </div>
          <h2 class="text-xl font-bold text-gray-900">Admin Login</h2>
          <p class="text-sm text-gray-500 mt-1">Sign in with your admin account</p>
        </div>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">School ID</label>
            <input v-model="loginForm.school_id" type="text" class="input-field w-full" placeholder="Enter admin School ID" required autofocus>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input v-model="loginForm.password" type="password" class="input-field w-full" placeholder="Enter password" required>
          </div>
          <div v-if="loginError" class="bg-red-50 text-red-700 px-3 py-2 rounded-lg text-sm">{{ loginError }}</div>
          <button type="submit" :disabled="loginLoading" class="btn-primary w-full !py-3 text-sm font-semibold disabled:opacity-50">
            {{ loginLoading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
      </div>
    </div>

    <!-- Admin Panel Content -->
    <div v-else class="max-w-6xl mx-auto px-4 sm:px-6 py-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <span class="text-3xl">⚙️</span> Account Management
          </h2>
          <p class="text-gray-500 text-sm mt-1">Create and manage staff and student accounts</p>
        </div>
        <button @click="showCreate = true" class="btn-primary flex items-center gap-2 !py-2.5 !px-5">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
          </svg>
          Create Account
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-xl border p-4">
          <p class="text-xs font-medium text-gray-500 uppercase">Total</p>
          <p class="text-2xl font-bold text-gray-900 mt-1">{{ accounts.length }}</p>
        </div>
        <div class="bg-white rounded-xl border p-4">
          <p class="text-xs font-medium text-gray-500 uppercase">Staff</p>
          <p class="text-2xl font-bold text-blue-600 mt-1">{{ accounts.filter(a => a.role === 'staff').length }}</p>
        </div>
        <div class="bg-white rounded-xl border p-4">
          <p class="text-xs font-medium text-gray-500 uppercase">Students</p>
          <p class="text-2xl font-bold text-green-600 mt-1">{{ accounts.filter(a => a.role === 'student').length }}</p>
        </div>
        <div class="bg-white rounded-xl border p-4">
          <p class="text-xs font-medium text-gray-500 uppercase">Inactive</p>
          <p class="text-2xl font-bold text-red-500 mt-1">{{ accounts.filter(a => !a.is_active).length }}</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-xl border p-4 mb-4 flex flex-col sm:flex-row gap-3">
        <div class="relative flex-1">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input v-model="search" type="text" placeholder="Search by name or school ID..." class="w-full pl-9 pr-3 py-2 bg-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-cpsu-green/30 focus:bg-white transition" @input="debouncedFetch">
        </div>
        <select v-model="roleFilter" @change="fetchAccounts" class="px-3 py-2 bg-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-cpsu-green/30">
          <option value="">All Roles</option>
          <option value="staff">Staff</option>
          <option value="student">Student</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="w-10 h-10 border-4 border-gray-200 border-t-cpsu-green rounded-full animate-spin mx-auto"></div>
      </div>

      <!-- Accounts Table -->
      <div v-else class="bg-white rounded-xl border overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">User</th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">School ID</th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase hidden sm:table-cell">Role</th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase hidden md:table-cell">Department</th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Status</th>
                <th class="px-5 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="accounts.length === 0">
                <td colspan="6" class="px-5 py-8 text-center text-gray-400 text-sm">No accounts found</td>
              </tr>
              <tr v-for="acc in accounts" :key="acc.id" class="hover:bg-gray-50 transition">
                <td class="px-5 py-3">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs"
                      :class="acc.role === 'staff' ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'">
                      {{ getInitials(acc.name) }}
                    </div>
                    <div>
                      <p class="font-semibold text-gray-900 text-sm">{{ acc.name || 'Unnamed' }}</p>
                      <p v-if="acc.is_superuser" class="text-[10px] text-purple-600 font-medium">ADMIN</p>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-3 text-sm text-gray-700 font-mono">{{ acc.school_id }}</td>
                <td class="px-5 py-3 hidden sm:table-cell">
                  <span class="px-2 py-0.5 text-xs rounded-full font-medium"
                    :class="acc.role === 'staff' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'">
                    {{ acc.role }}
                  </span>
                </td>
                <td class="px-5 py-3 text-sm text-gray-600 hidden md:table-cell">
                  {{ acc.department ? acc.department.split(' ').map((w: string) => w[0]).join('') : '—' }}
                </td>
                <td class="px-5 py-3">
                  <span class="px-2 py-0.5 text-xs rounded-full font-medium"
                    :class="acc.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                    {{ acc.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-5 py-3 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <button @click="toggleAccount(acc)" :disabled="acc.is_superuser"
                      :title="acc.is_superuser ? 'Cannot modify admin' : (acc.is_active ? 'Deactivate' : 'Activate')"
                      class="p-1.5 rounded-lg hover:bg-gray-100 transition text-gray-400 hover:text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed">
                      <svg v-if="acc.is_active" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                      </svg>
                      <svg v-else class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                    <button @click="openResetPassword(acc)" :disabled="acc.is_superuser" title="Reset Password"
                      class="p-1.5 rounded-lg hover:bg-gray-100 transition text-gray-400 hover:text-yellow-600 disabled:opacity-30 disabled:cursor-not-allowed">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create Account Modal -->
    <Transition name="modal">
      <div v-if="showCreate" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center" @click="showCreate = false">
        <div class="fixed inset-0 bg-black/40 backdrop-blur-sm"></div>
        <div class="relative bg-white w-full sm:max-w-md sm:rounded-2xl rounded-t-2xl shadow-2xl animate-slide-up" @click.stop>
          <div class="flex items-center justify-between p-4 border-b bg-gray-50 sm:rounded-t-2xl">
            <h2 class="font-bold text-gray-900">Create New Account</h2>
            <button @click="showCreate = false" class="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-200 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <form @submit.prevent="createAccount" class="p-5 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select v-model="newAccount.role" class="input-field w-full">
                <option value="staff">Clinic Staff</option>
                <option value="student">Student</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">School ID <span class="text-red-500">*</span></label>
              <input v-model="newAccount.school_id" type="text" class="input-field w-full" placeholder="e.g. STAFF-001 or 2023-1234" required>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input v-model="newAccount.name" type="text" class="input-field w-full" placeholder="Juan Dela Cruz">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Department</label>
              <select v-model="newAccount.department" class="input-field w-full">
                <option value="">— None —</option>
                <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Password <span class="text-red-500">*</span></label>
              <input v-model="newAccount.password" type="password" class="input-field w-full" placeholder="Minimum 6 characters" required minlength="6">
            </div>
            <div v-if="createError" class="bg-red-50 text-red-700 px-3 py-2 rounded-lg text-sm">{{ createError }}</div>
            <div v-if="createSuccess" class="bg-green-50 text-green-700 px-3 py-2 rounded-lg text-sm flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
              {{ createSuccess }}
            </div>
            <button type="submit" :disabled="creating" class="btn-primary w-full !py-3 text-sm font-semibold disabled:opacity-50">
              {{ creating ? 'Creating...' : 'Create Account' }}
            </button>
          </form>
        </div>
      </div>
    </Transition>

    <!-- Reset Password Modal -->
    <Transition name="modal">
      <div v-if="resetTarget" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center" @click="resetTarget = null">
        <div class="fixed inset-0 bg-black/40 backdrop-blur-sm"></div>
        <div class="relative bg-white w-full sm:max-w-sm sm:rounded-2xl rounded-t-2xl shadow-2xl animate-slide-up" @click.stop>
          <div class="flex items-center justify-between p-4 border-b bg-gray-50 sm:rounded-t-2xl">
            <h2 class="font-bold text-gray-900 text-sm">Reset Password — {{ resetTarget.school_id }}</h2>
            <button @click="resetTarget = null" class="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-200 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <form @submit.prevent="resetPassword" class="p-5 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input v-model="newPassword" type="password" class="input-field w-full" placeholder="Minimum 6 characters" required minlength="6">
            </div>
            <div v-if="resetError" class="text-sm text-red-600">{{ resetError }}</div>
            <div v-if="resetSuccess" class="text-sm text-green-600">{{ resetSuccess }}</div>
            <button type="submit" :disabled="resetting" class="btn-primary w-full !py-2.5 text-sm disabled:opacity-50">
              {{ resetting ? 'Resetting...' : 'Reset Password' }}
            </button>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// Use raw axios for admin panel (separate from main app auth)
const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

const adminAxios = axios.create({
  baseURL: API_BASE,
})

// --- Auth state (self-contained, not using the main auth store) ---
const authenticated = ref(false)
const adminToken = ref('')
const adminUser = ref<any>(null)
const loginForm = ref({ school_id: '', password: '' })
const loginError = ref('')
const loginLoading = ref(false)

const handleLogin = async () => {
  loginLoading.value = true
  loginError.value = ''
  try {
    const res = await adminAxios.post('/auth/login/', loginForm.value)
    const user = res.data.user
    if (!user.is_superuser) {
      loginError.value = 'Access denied. Only admin accounts can access this panel.'
      return
    }
    adminToken.value = res.data.token
    adminUser.value = user
    adminAxios.defaults.headers.common['Authorization'] = `Token ${res.data.token}`
    authenticated.value = true
    fetchAccounts()
  } catch (e: any) {
    loginError.value = e.response?.data?.error || 'Invalid credentials'
  } finally {
    loginLoading.value = false
  }
}

const logout = () => {
  authenticated.value = false
  adminToken.value = ''
  adminUser.value = null
  loginForm.value = { school_id: '', password: '' }
  delete adminAxios.defaults.headers.common['Authorization']
}

// --- Accounts ---
const accounts = ref<any[]>([])
const loading = ref(false)
const search = ref('')
const roleFilter = ref('')

const showCreate = ref(false)
const creating = ref(false)
const createError = ref('')
const createSuccess = ref('')
const newAccount = ref({ school_id: '', password: '', name: '', role: 'staff', department: '' })

const resetTarget = ref<any>(null)
const newPassword = ref('')
const resetting = ref(false)
const resetError = ref('')
const resetSuccess = ref('')

const departments = [
  'College of Agriculture and Forestry',
  'College of Teacher Education',
  'College of Arts and Sciences',
  'College of Hospitality Management',
  'College of Engineering',
  'College of Computer Studies',
  'College of Criminal Justice Education',
]

const getInitials = (name: string) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

let debounceTimer: ReturnType<typeof setTimeout> | null = null
const debouncedFetch = () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchAccounts, 300)
}

const fetchAccounts = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (search.value.trim()) params.search = search.value.trim()
    if (roleFilter.value) params.role = roleFilter.value
    const res = await adminAxios.get('/admin/accounts/', { params })
    accounts.value = res.data.accounts || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const createAccount = async () => {
  creating.value = true
  createError.value = ''
  createSuccess.value = ''
  try {
    const res = await adminAxios.post('/admin/accounts/create/', newAccount.value)
    createSuccess.value = res.data.message
    newAccount.value = { school_id: '', password: '', name: '', role: 'staff', department: '' }
    fetchAccounts()
    setTimeout(() => { showCreate.value = false; createSuccess.value = '' }, 1500)
  } catch (e: any) {
    createError.value = e.response?.data?.error || 'Failed to create account'
  } finally {
    creating.value = false
  }
}

const toggleAccount = async (acc: any) => {
  if (!confirm(`${acc.is_active ? 'Deactivate' : 'Activate'} account ${acc.school_id}?`)) return
  try {
    const res = await adminAxios.patch(`/admin/accounts/${acc.school_id}/toggle/`)
    acc.is_active = res.data.is_active
  } catch (e: any) {
    alert(e.response?.data?.error || 'Failed to toggle account')
  }
}

const openResetPassword = (acc: any) => {
  resetTarget.value = acc
  newPassword.value = ''
  resetError.value = ''
  resetSuccess.value = ''
}

const resetPassword = async () => {
  if (!resetTarget.value) return
  resetting.value = true
  resetError.value = ''
  resetSuccess.value = ''
  try {
    const res = await adminAxios.post(`/admin/accounts/${resetTarget.value.school_id}/reset-password/`, { new_password: newPassword.value })
    resetSuccess.value = res.data.message
    setTimeout(() => { resetTarget.value = null }, 1500)
  } catch (e: any) {
    resetError.value = e.response?.data?.error || 'Failed to reset password'
  } finally {
    resetting.value = false
  }
}
</script>

<style scoped>
.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
@keyframes slide-up {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.25s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
