import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { getToken, setToken, removeToken } from '@/services/tokenService'
import type { User, LoginCredentials, RegisterData } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(getToken())
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userName = computed(() => user.value?.name || '')

  // Actions
  async function login(credentials: LoginCredentials, rememberMe: boolean = false) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/login/', credentials)
      token.value = response.data.token
      user.value = response.data.user
      
      // Save token to storage based on remember me preference
      setToken(response.data.token, rememberMe)
      
      return true
    } catch (err: any) {
      // Handle Django validation errors
      if (err.response?.data) {
        const errorData = err.response.data
        
        // Field-specific errors
        if (typeof errorData === 'object' && !errorData.error) {
          const firstError = Object.values(errorData)[0]
          error.value = Array.isArray(firstError) ? firstError[0] : String(firstError)
        } else {
          // General error message
          error.value = errorData.error || errorData.message || 'Login failed'
        }
      } else {
        error.value = 'Login failed. Please try again.'
      }
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(data: RegisterData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/register/', data)
      token.value = response.data.token
      user.value = response.data.user
      
      // Save token to localStorage by default for registration
      setToken(response.data.token, true)
      
      return true
    } catch (err: any) {
      // Handle Django validation errors (field-specific or general)
      if (err.response?.data) {
        const errorData = err.response.data
        
        // Field-specific errors (e.g., {"school_id": ["This field is required"]})
        if (typeof errorData === 'object' && !errorData.error) {
          const firstError = Object.values(errorData)[0]
          error.value = Array.isArray(firstError) ? firstError[0] : String(firstError)
        } else {
          // General error message
          error.value = errorData.error || errorData.message || 'Registration failed'
        }
      } else {
        error.value = 'Registration failed. Please try again.'
      }
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await api.post('/auth/logout/')
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear state regardless of API call success
      user.value = null
      token.value = null
      removeToken()
    }
  }

  async function fetchProfile() {
    if (!token.value) return
    
    try {
      const response = await api.get('/profile/')
      user.value = response.data
    } catch (err) {
      console.error('Error fetching profile:', err)
      // If token is invalid, clear auth state
      if ((err as any).response?.status === 401) {
        await logout()
      }
    }
  }

  async function checkAuth() {
    if (token.value) {
      await fetchProfile()
    }
  }

  async function updateProfile(data: Partial<User>) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.patch('/profile/', data)
      user.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Update failed'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    userName,
    login,
    register,
    logout,
    fetchProfile,
    checkAuth,
    updateProfile
  }
})
