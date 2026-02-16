# Vue.js Frontend - Quick Reference

## 🚀 Common Commands

```bash
npm install              # Install dependencies
npm run dev              # Start dev server (http://localhost:5173)
npm run build            # Build for production
npm run preview          # Preview production build
npm run type-check       # Check TypeScript errors
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/views/` | All page components |
| `src/stores/` | Pinia state management |
| `src/services/api.ts` | API integration with Django |
| `src/types/index.ts` | TypeScript type definitions |
| `src/router/index.ts` | Route definitions |
| `tailwind.config.js` | CPSU colors configured |

## 🎨 CPSU Branding Classes

```html
<!-- Buttons -->
<button class="btn-primary">Primary (Green)</button>
<button class="btn-secondary">Secondary (Yellow)</button>
<button class="btn-outline">Outline (Green border)</button>

<!-- Cards -->
<div class="card">Standard card</div>
<div class="card-bordered">Card with green border</div>

<!-- Forms -->
<input type="text" class="input-field">
<input type="text" class="input-field input-error">

<!-- Loading -->
<div class="spinner w-12 h-12"></div>

<!-- Colors -->
<div class="bg-cpsu-green">Green background</div>
<div class="bg-cpsu-yellow">Yellow background</div>
<div class="text-cpsu-green">Green text</div>
```

## 🗄️ Pinia Stores

### Auth Store
```typescript
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// Actions
await auth.login({ school_id, password })
await auth.register({ school_id, name, password })
await auth.logout()
await auth.updateProfile({ name, department })

// State
auth.isAuthenticated  // boolean
auth.user            // User object
auth.isStaff         // boolean
auth.loading         // boolean
auth.error           // string | null
```

### Symptoms Store
```typescript
import { useSymptomsStore } from '@/stores/symptoms'

const symptoms = useSymptomsStore()

// Actions
await symptoms.fetchAvailableSymptoms()
await symptoms.submitSymptoms(['fever', 'cough'], true)
await symptoms.fetchHistory()
symptoms.toggleSymptom('headache')
symptoms.clearSelection()

// State
symptoms.availableSymptoms   // Symptom[]
symptoms.selectedSymptoms    // string[]
symptoms.predictionResult    // PredictionResult | null
symptoms.history            // SymptomRecord[]
```

### Chat Store
```typescript
import { useChatStore } from '@/stores/chat'

const chat = useChatStore()

// Actions
await chat.startSession()
await chat.sendMessage('I have a headache')
await chat.endSession()

// State
chat.messages      // ChatMessage[]
chat.sessionId     // string | null
chat.loading       // boolean
```

## 🔌 API Calls

```typescript
import api from '@/services/api'

// GET
const response = await api.get('/symptoms/available/')

// POST
const response = await api.post('/symptoms/submit/', {
  symptoms: ['fever', 'cough']
})

// PATCH
const response = await api.patch('/profile/', {
  name: 'New Name'
})

// DELETE
await api.delete('/symptoms/123/')
```

## 🛣️ Routes

| Path | Component | Auth Required |
|------|-----------|---------------|
| `/` | HomeView | No |
| `/login` | LoginView | No (guest only) |
| `/register` | RegisterView | No (guest only) |
| `/dashboard` | DashboardView | Yes |
| `/symptom-checker` | SymptomCheckerView | Yes |
| `/chat` | ChatView | Yes |
| `/history` | HistoryView | Yes |
| `/profile` | ProfileView | Yes |
| `/staff` | StaffDashboardView | Yes (staff only) |

## 📝 TypeScript Types

```typescript
import type { 
  User,
  LoginCredentials,
  RegisterData,
  Symptom,
  PredictionResult,
  SymptomRecord,
  ChatMessage
} from '@/types'
```

## 🎯 Vue 3 Composition API

```vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

// Reactive state
const count = ref(0)
const name = ref('John')

// Computed
const doubled = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})

// Watchers
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`)
})
</script>
```

## 🔄 Component Communication

### Emit Events
```vue
<!-- Child.vue -->
<script setup lang="ts">
const emit = defineEmits<{
  submit: [data: string]
}>()

function handleClick() {
  emit('submit', 'data')
}
</script>

<!-- Parent.vue -->
<template>
  <Child @submit="handleSubmit" />
</template>
```

### Props
```vue
<script setup lang="ts">
const props = defineProps<{
  title: string
  count?: number
}>()
</script>
```

## 🎨 TailwindCSS Quick Ref

```html
<!-- Layout -->
<div class="container mx-auto px-6 py-8">
<div class="flex items-center justify-between">
<div class="grid grid-cols-3 gap-6">

<!-- Spacing -->
<div class="p-4">Padding all sides</div>
<div class="px-6 py-8">Padding x and y</div>
<div class="m-4">Margin</div>
<div class="space-y-4">Vertical spacing between children</div>

<!-- Typography -->
<h1 class="text-3xl font-bold text-cpsu-green">Title</h1>
<p class="text-gray-600 text-sm">Small text</p>

<!-- Colors -->
<div class="bg-white text-gray-900">
<div class="bg-cpsu-green text-white">
<div class="border-2 border-cpsu-yellow">

<!-- Responsive -->
<div class="w-full md:w-1/2 lg:w-1/3">
```

## ⚙️ Environment Variables

```typescript
// Access in code
const apiUrl = import.meta.env.VITE_API_BASE_URL
const appName = import.meta.env.VITE_APP_NAME

// Must start with VITE_ to be accessible
```

## 🐛 Common Issues

### Issue: Module not found
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: API 401 Unauthorized
```javascript
// Clear localStorage
localStorage.removeItem('auth_token')
// Re-login
```

### Issue: TypeScript errors
```bash
npm run type-check
```

### Issue: Vite not starting
```bash
# Kill port 5173
# Windows: netstat -ano | findstr :5173
# Linux/Mac: lsof -ti:5173 | xargs kill
```

## 📚 Helpful Links

- Vue 3: https://vuejs.org/
- Pinia: https://pinia.vuejs.org/
- TailwindCSS: https://tailwindcss.com/
- Vite: https://vitejs.dev/
- TypeScript: https://www.typescriptlang.org/

---

**Pro Tip:** Keep this file open while developing! 🚀
