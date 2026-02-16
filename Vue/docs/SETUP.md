Vue.js Frontend Setup Guide

Quick start guide for the CPSU Health Assistant Vue.js frontend.

## 🚀 First-Time Setup

```bash
# 1. Navigate to Vue directory
cd Vue

# 2. Install dependencies
npm install

# 3. Verify .env file exists
cat .env
# Should show:
# VITE_API_BASE_URL=http://localhost:8000/api
# VITE_RASA_URL=http://localhost:5005

# 4. Start development server
npm run dev
```

**Expected output:**
```
  VITE v5.1.6  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

## ✅ Prerequisites Checklist

Before running the Vue frontend, make sure:

- [x] Node.js 18+ installed (`node --version`)
- [x] Django backend running on http://localhost:8000
- [x] ML model trained (`ML/models/disease_predictor_v2.pkl` exists)
- [x] Django database migrated

## 🧪 Testing the Frontend

### 1. Test Landing Page
Visit: http://localhost:5173/

Should see:
- CPSU Health Assistant branding
- Green and yellow colors
- Login/Register buttons

### 2. Test Registration
1. Click "Register"
2. Fill form:
   - School ID: `2024-TEST-001`
   - Name: `Test User`
   - Password: `testpass123`
   - Department: Select any
3. Click "Create Account"
4. Should redirect to `/dashboard`

### 3. Test Symptom Checker
1. Click "Check Symptoms" card
2. Search and select symptoms: `fever`, `cough`, `fatigue`
3. Click "Get Prediction"
4. Should see:
   - Predicted disease
   - Confidence percentage
   - Description
   - Precautions
   - LLM validation (if enabled in Django)

### 4. Test Chat
1. Go to Chat page
2. Type: "I have a headache"
3. Send message
4. Should receive bot response

### 5. Test History
1. Go to History page
2. Should see your symptom check from step 3
3. Can delete records

## 🔧 Common Issues & Solutions

### Issue: "Cannot find module 'vue'"
**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: API calls fail (Network Error)
**Check:**
1. Django is running: `curl http://localhost:8000/api/`
2. CORS enabled in Django settings
3. Check browser console for CORS errors

**Fix Django CORS:**
```python
# Django/health_assistant/settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Add this
    'http://localhost:3000',
]
```

### Issue: 401 Unauthorized after login
**Solution:**
- Token might be invalid
- Clear localStorage: Open DevTools → Application → Local Storage → Clear
- Re-login

### Issue: TypeScript errors
**Solution:**
```bash
npm run type-check
# Fix errors shown, then:
npm run dev
```

### Issue: Styles not loading
**Solution:**
```bash
# Rebuild TailwindCSS
npm run build
npm run dev
```

## 📁 Project Structure Quick Reference

```
Vue/
├── src/
│   ├── views/                    # 👁️ Pages you see in browser
│   │   ├── HomeView.vue          # Landing page (/)
│   │   ├── DashboardView.vue     # Main dashboard (/dashboard)
│   │   ├── SymptomCheckerView.vue # Symptom checker (/symptom-checker)
│   │   ├── ChatView.vue          # Chat interface (/chat)
│   │   ├── HistoryView.vue       # Health history (/history)
│   │   ├── ProfileView.vue       # User profile (/profile)
│   │   └── auth/
│   │       ├── LoginView.vue     # Login (/login)
│   │       └── RegisterView.vue  # Register (/register)
│   │
│   ├── stores/                   # 🗄️ State management (Pinia)
│   │   ├── auth.ts               # User authentication
│   │   ├── symptoms.ts           # Symptom data & predictions
│   │   └── chat.ts               # Chat messages
│   │
│   ├── services/                 # 🔌 API calls
│   │   └── api.ts                # Axios instance (handles auth)
│   │
│   ├── types/                    # 📝 TypeScript types
│   │   └── index.ts
│   │
│   └── router/                   # 🛣️ Routes
│       └── index.ts
│
├── .env                          # Environment variables
├── tailwind.config.js            # CPSU colors configured
└── package.json                  # Dependencies
```

## 🎨 Quick Customization Examples

### Add a new page

**1. Create view file:**
```vue
<!-- src/views/AboutView.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <h1 class="text-3xl font-heading font-bold text-cpsu-green">About</h1>
  </div>
</template>

<script setup lang="ts">
// Component logic here
</script>
```

**2. Add route:**
```typescript
// src/router/index.ts
{
  path: '/about',
  name: 'about',
  component: () => import('@/views/AboutView.vue'),
  meta: { requiresAuth: false }
}
```

**3. Add navigation link:**
```vue
<router-link to="/about">About</router-link>
```

### Add a new API endpoint

**1. Update types:**
```typescript
// src/types/index.ts
export interface MyNewType {
  id: number
  name: string
}
```

**2. Create store (optional):**
```typescript
// src/stores/myStore.ts
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useMyStore = defineStore('my-store', () => {
  async function fetchData() {
    const response = await api.get('/my-endpoint/')
    return response.data
  }
  
  return { fetchData }
})
```

**3. Use in component:**
```vue
<script setup lang="ts">
import { useMyStore } from '@/stores/myStore'

const myStore = useMyStore()
const data = await myStore.fetchData()
</script>
```

### Use CPSU branding

```vue
<template>
  <!-- Primary button (Green background, white text) -->
  <button class="btn-primary">Submit</button>
  
  <!-- Secondary button (Yellow background, green text) -->
  <button class="btn-secondary">Cancel</button>
  
  <!-- Outline button (Green border, green text) -->
  <button class="btn-outline">Learn More</button>
  
  <!-- Card with green border -->
  <div class="card-bordered">
    <h3 class="text-cpsu-green">Card Title</h3>
  </div>
  
  <!-- Input field -->
  <input type="text" class="input-field" />
</template>
```

## 🧹 Development Commands

```bash
# Install dependencies
npm install

# Start dev server (hot reload)
npm run dev

# Type check (find TypeScript errors)
npm run type-check

# Build for production
npm run build

# Preview production build
npm run preview

# Lint and fix
npm run lint
```

## 📚 Learn More

- **Vue 3 Docs:** https://vuejs.org/
- **TypeScript:** https://www.typescriptlang.org/
- **Vite:** https://vitejs.dev/
- **TailwindCSS:** https://tailwindcss.com/
- **Pinia:** https://pinia.vuejs.org/
- **Vue Router:** https://router.vuejs.org/

## 🤝 Need Help?

1. Check `Vue/README.md` for detailed documentation
2. Check Django backend is running
3. Check browser console for errors
4. Verify `.env` file has correct API URL
5. Try clearing localStorage and re-login

---

**You're all set!** Start the dev server and begin building the frontend. 🎉
