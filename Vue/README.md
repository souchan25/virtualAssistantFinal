# CPSU Health Assistant - Vue.js Frontend

**AI-powered health assistant frontend** built with Vue 3, TypeScript, Vite, and TailwindCSS.

---

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

**Development server:** http://localhost:5173

---

## 📋 Prerequisites

1. **Node.js 18+** installed
2. **Django backend** running on `http://localhost:8000`
3. **Environment variables** configured (see below)

---

## ⚙️ Environment Setup

Create `.env` file (already provided):

```env
# Django Backend API
VITE_API_BASE_URL=http://localhost:8000/api

# Rasa Chatbot (optional)
VITE_RASA_URL=http://localhost:5005

# App Configuration
VITE_APP_NAME=CPSU Health Assistant
VITE_APP_VERSION=1.0.0
```

For production, update `.env.production` with your deployment URLs.

---

## 🏗️ Project Structure

```
Vue/
├── src/
│   ├── views/              # Page components
│   │   ├── HomeView.vue            # Landing page
│   │   ├── DashboardView.vue       # Student dashboard
│   │   ├── SymptomCheckerView.vue  # Symptom checker tool
│   │   ├── ChatView.vue            # Chat interface
│   │   ├── HistoryView.vue         # Health history
│   │   ├── ProfileView.vue         # User profile
│   │   ├── NotFoundView.vue        # 404 page
│   │   ├── auth/
│   │   │   ├── LoginView.vue       # Login page
│   │   │   └── RegisterView.vue    # Registration page
│   │   └── staff/
│   │       └── StaffDashboardView.vue  # Staff portal
│   │
│   ├── stores/             # Pinia state management
│   │   ├── auth.ts                # Authentication store
│   │   ├── symptoms.ts            # Symptoms & predictions store
│   │   └── chat.ts                # Chat store
│   │
│   ├── services/           # API integration
│   │   └── api.ts                 # Axios instance with auth
│   │
│   ├── types/              # TypeScript types
│   │   └── index.ts               # All type definitions
│   │
│   ├── router/             # Vue Router
│   │   └── index.ts               # Route definitions
│   │
│   ├── App.vue             # Root component
│   ├── main.ts             # App entry point
│   └── style.css           # Global styles (TailwindCSS)
│
├── public/                 # Static assets
├── index.html              # HTML template
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # TailwindCSS config (CPSU colors)
├── tsconfig.json           # TypeScript config
└── package.json            # Dependencies
```

---

## 🎨 CPSU Branding

### Colors (Mighty Hornbills)

- **Earls Green** (Primary): `#006B3F` → `cpsu-green`
- **Lemon Yellow** (Secondary): `#FFF44F` → `cpsu-yellow`

### TailwindCSS Usage

```vue
<button class="btn-primary">Primary Action</button>
<button class="btn-secondary">Secondary Action</button>
<button class="btn-outline">Outline Button</button>

<div class="card">Standard Card</div>
<div class="card-bordered">Card with CPSU Green Border</div>

<input type="text" class="input-field">
```

---

## 📱 Features

### ✅ Implemented

1. **Authentication System**
   - Login/Register with school ID
   - Token-based auth (stored in localStorage)
   - Protected routes with navigation guards
   - Auto-logout on 401 errors

2. **Symptom Checker**
   - Multi-step form (Select Symptoms → Get Results)
   - Search functionality for 132+ symptoms
   - Real-time symptom selection
   - AI prediction with confidence scores
   - LLM validation display
   - Precautions and recommendations

3. **Chat Interface**
   - Real-time messaging with health bot
   - Session management
   - Quick action buttons
   - Auto-scroll to latest message
   - Typing indicators

4. **Health History**
   - View all past consultations
   - Filter and search (coming soon)
   - Delete records
   - Detailed view with precautions

5. **User Profile**
   - Update name, department, CPSU address
   - Read-only fields (school ID, role)
   - Success/error notifications

6. **Staff Dashboard**
   - Placeholder for staff features
   - Role-based access control

### 🚧 Coming Soon (Your Furnishing!)

- [ ] Enhanced animations and transitions
- [ ] Loading skeletons
- [ ] Advanced filtering and sorting
- [ ] Data visualizations (charts)
- [ ] Export functionality
- [ ] Mobile-responsive improvements
- [ ] Dark mode
- [ ] Accessibility (ARIA labels)
- [ ] Progressive Web App (PWA)

---

## 🔌 API Integration

All API calls use Axios with automatic token injection:

```typescript
// Example: Fetch symptoms
import api from '@/services/api'

const response = await api.get('/symptoms/available/')
// Token automatically added to headers
```

### Key Endpoints Used

- `POST /auth/login/` — Login
- `POST /auth/register/` — Register
- `GET /profile/` — Get user profile
- `POST /symptoms/submit/` — Submit symptoms for prediction
- `GET /symptoms/available/` — Get all symptoms
- `POST /chat/message/` — Send chat message
- `GET /symptoms/` — Get symptom history

---

## 🧪 Development Workflow

### Run Backend First

```bash
# Terminal 1: Django
cd ../Django
python manage.py runserver

# Terminal 2: Rasa (optional)
cd ../Rasa
rasa run actions
rasa run --enable-api --cors "*"

# Terminal 3: Vue.js
cd Vue
npm run dev
```

### Type Checking

```bash
npm run type-check
```

### Build for Production

```bash
npm run build
# Output: dist/
```

---

## 🛠️ State Management (Pinia)

### Auth Store

```typescript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Actions
await authStore.login({ school_id, password })
await authStore.register({ school_id, name, password })
await authStore.logout()

// State
authStore.isAuthenticated  // boolean
authStore.user             // User object
authStore.isStaff          // boolean
```

### Symptoms Store

```typescript
import { useSymptomsStore } from '@/stores/symptoms'

const symptomsStore = useSymptomsStore()

// Actions
await symptomsStore.fetchAvailableSymptoms()
await symptomsStore.submitSymptoms(['fever', 'cough'])
symptomsStore.toggleSymptom('headache')

// State
symptomsStore.availableSymptoms   // All symptoms
symptomsStore.selectedSymptoms    // User selection
symptomsStore.predictionResult    // Latest prediction
```

### Chat Store

```typescript
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()

// Actions
await chatStore.startSession()
await chatStore.sendMessage('I have a headache')
await chatStore.endSession()

// State
chatStore.messages     // Chat history
chatStore.sessionId    // Current session
```

---

## 🎯 Routing

### Public Routes

- `/` — Home (landing page)
- `/login` — Login
- `/register` — Register

### Protected Routes (Requires Auth)

- `/dashboard` — Student dashboard
- `/symptom-checker` — Symptom checker
- `/chat` — Chat interface
- `/history` — Health history
- `/profile` — User profile

### Staff Only

- `/staff` — Staff dashboard (requires `role: 'staff'`)

---

## 🔒 Security

- ✅ Token stored in `localStorage`
- ✅ Auto-refresh on page reload
- ✅ Auto-logout on 401 errors
- ✅ Protected routes with navigation guards
- ✅ CORS configured for Django backend

---

## 🎨 Customization Guide (Furnishing Tasks)

### 1. Add Animations

```vue
<!-- Example: Fade-in animation -->
<transition name="fade">
  <div v-if="show" class="card">Content</div>
</transition>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
```

### 2. Add Loading Skeletons

```vue
<div v-if="loading" class="animate-pulse space-y-4">
  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

### 3. Add Icons (Install Heroicons)

```bash
npm install @heroicons/vue
```

```vue
<script setup>
import { HeartIcon } from '@heroicons/vue/24/solid'
</script>

<template>
  <HeartIcon class="w-6 h-6 text-cpsu-green" />
</template>
```

### 4. Add Charts (Install Chart.js)

```bash
npm install chart.js vue-chartjs
```

---

## 📝 Next Steps for Furnishing

1. **Visual Polish**
   - Add smooth transitions between pages
   - Implement loading skeletons
   - Add micro-interactions (button hover effects, etc.)
   - Improve form validation feedback

2. **Enhanced UX**
   - Add success toasts/notifications
   - Implement better error handling UI
   - Add confirmation modals
   - Improve mobile responsiveness

3. **Data Visualization**
   - Add charts to dashboard (symptom trends)
   - Visualize confidence scores
   - Health statistics graphs

4. **Accessibility**
   - Add ARIA labels
   - Keyboard navigation
   - Screen reader support
   - Focus management

5. **Performance**
   - Lazy load components
   - Image optimization
   - Code splitting
   - Service worker (PWA)

---

## 🐛 Troubleshooting

### API Connection Issues

```bash
# Check if Django is running
curl http://localhost:8000/api/

# Check environment variables
cat .env
```

### TypeScript Errors

```bash
# Install dependencies
npm install

# Clear cache
rm -rf node_modules
npm install
```

### Build Errors

```bash
# Type check first
npm run type-check

# Then build
npm run build
```

---

## 📚 Tech Stack

- **Vue 3** — Progressive JavaScript framework
- **TypeScript** — Type safety
- **Vite** — Fast build tool
- **TailwindCSS** — Utility-first CSS
- **Pinia** — State management
- **Vue Router** — Routing
- **Axios** — HTTP client

---

## 🤝 Contributing

When adding new features:

1. Follow existing component structure
2. Use TypeScript types from `@/types`
3. Use Pinia stores for state management
4. Follow CPSU branding guidelines
5. Test with Django backend running
6. Update this README if needed

---

## 📄 License

Part of CPSU Virtual Health Assistant project.
