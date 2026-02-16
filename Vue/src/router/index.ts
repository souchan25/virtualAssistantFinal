import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { requiresAuth: false, guestOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { requiresAuth: false, guestOnly: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/symptom-checker',
    name: 'symptom-checker',
    component: () => import('@/views/SymptomCheckerView.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('@/views/ChatView.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('@/views/HistoryView.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/staff',
    name: 'staff-dashboard',
    component: () => import('@/views/staff/StaffDashboard.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/staff/emergencies',
    name: 'staff-emergencies',
    component: () => import('@/views/staff/EmergencyDashboard.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/staff/students',
    name: 'staff-students',
    component: () => import('@/views/staff/StudentRecords.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/staff/prescribe',
    name: 'staff-prescribe',
    component: () => import('@/views/staff/MedicationPrescribe.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/staff/adherence',
    name: 'staff-adherence',
    component: () => import('@/views/staff/AdherenceMonitor.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/staff/followups',
    name: 'staff-followups',
    component: () => import('@/views/staff/FollowUpManagement.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/staff/analytics',
    name: 'staff-analytics',
    component: () => import('@/views/staff/AnalyticsDashboard.vue'),
    meta: { requiresAuth: true, requiresStaff: true }
  },
  {
    path: '/medications',
    name: 'medications',
    component: () => import('@/views/MedicationList.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/followups',
    name: 'followups',
    component: () => import('@/views/FollowUpList.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/health-dashboard',
    name: 'health-dashboard',
    component: () => import('@/views/HealthDashboard.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  
  // Redirect authenticated users away from guest-only pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    // Redirect based on user role
    if (authStore.user?.role === 'staff') {
      next({ name: 'staff-dashboard' })
    } else {
      next({ name: 'dashboard' })
    }
    return
  }
  
  // Check if route requires staff permissions
  if (to.meta.requiresStaff && authStore.user?.role !== 'staff') {
    next({ name: 'dashboard' })
    return
  }
  
  // Check if route requires student permissions
  if (to.meta.requiresStudent && authStore.user?.role !== 'student') {
    next({ name: 'staff-dashboard' })
    return
  }
  
  next()
})

export default router
