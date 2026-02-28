<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Navigation Bar -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="max-w-5xl mx-auto px-4 py-3">
        <div class="flex items-center gap-3 sm:gap-4">
          <!-- Always visible back button to exit messages -->
          <button aria-label="Go Back" @click="goBack" class="text-gray-500 hover:text-cpsu-green transition-colors flex items-center gap-1" title="Go Back">
            <svg class="w-5 h-5 lg:w-6 lg:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            <span class="hidden sm:inline text-sm font-medium">Back</span>
          </button>

          <div class="h-6 w-px bg-gray-300"></div>

          <!-- Mobile: Back to conversation list -->
          <button aria-label="Back to conversation list" v-if="activeConversation" @click="activeConversation = null" class="text-gray-500 hover:text-cpsu-green transition-colors sm:hidden">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          
          <div class="flex-1 flex justify-between items-center">
            <div>
              <h1 class="text-lg font-heading font-bold text-cpsu-green flex items-center gap-2">
                {{ activeConversation ? activeConversation.name : 'Messages' }}
                <span v-if="activeConversation" class="text-[10px] sm:text-xs px-2 py-0.5 rounded-full font-medium" :class="activeConversation.role === 'staff' ? 'bg-blue-50 text-blue-600' : 'bg-green-50 text-green-600'">{{ activeConversation.role }}</span>
              </h1>
            </div>
            
            <div class="flex items-center gap-3">
              <div class="flex items-center gap-1.5 text-xs text-gray-400">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                Live
              </div>
              <button aria-label="New message" @click="showNewChat = true" class="bg-cpsu-green hover:bg-cpsu-green-dark text-white rounded-full p-1.5 sm:p-2 shadow transition-colors flex items-center justify-center" title="New message">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="flex-1 flex max-w-5xl mx-auto w-full overflow-hidden">
      <!-- Conversation List (Left Panel) -->
      <div
        class="bg-white border-r border-gray-200 flex flex-col"
        :class="[
          activeConversation ? 'hidden sm:flex sm:w-80 lg:w-96' : 'w-full sm:w-80 lg:w-96',
          'flex-shrink-0'
        ]"
      >
        <!-- Search -->
        <div class="p-3 border-b">
          <div class="relative">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search conversations..."
              class="w-full pl-9 pr-3 py-2 bg-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-cpsu-green/30 focus:bg-white transition"
            >
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex-1 flex items-center justify-center">
          <div class="w-8 h-8 border-4 border-gray-200 border-t-cpsu-green rounded-full animate-spin"></div>
        </div>

        <!-- Conversation List -->
        <div v-else class="flex-1 overflow-y-auto">
          <div v-if="filteredConversations.length === 0" class="text-center py-12 px-4">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-2xl">💬</span>
            </div>
            <p class="text-gray-500 text-sm">{{ searchQuery ? 'No conversations found' : 'No conversations yet' }}</p>
            <button @click="showNewChat = true" class="mt-3 text-cpsu-green text-sm font-medium hover:underline">
              Start a conversation
            </button>
          </div>

          <div
            v-for="conv in filteredConversations"
            :key="conv.userId"
            @click="openConversation(conv)"
            class="flex items-center gap-3 px-4 py-3 cursor-pointer transition-all duration-150 border-b border-gray-50"
            :class="[
              activeConversation?.userId === conv.userId
                ? 'bg-cpsu-green/5 border-l-3 border-l-cpsu-green'
                : 'hover:bg-gray-50'
            ]"
          >
            <!-- Avatar -->
            <div class="relative flex-shrink-0">
              <div
                class="w-11 h-11 rounded-full flex items-center justify-center font-bold text-sm"
                :class="conv.role === 'staff' ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'"
              >
                {{ getInitials(conv.name) }}
              </div>
              <span v-if="conv.unreadCount > 0" class="absolute -top-0.5 -right-0.5 w-5 h-5 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                {{ conv.unreadCount > 9 ? '9+' : conv.unreadCount }}
              </span>
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline">
                <h3 class="font-semibold text-gray-900 text-sm truncate" :class="{ 'font-bold': conv.unreadCount > 0 }">
                  {{ conv.name }}
                </h3>
                <span class="text-[11px] text-gray-400 flex-shrink-0 ml-2">{{ formatTime(conv.lastTimestamp) }}</span>
              </div>
              <div class="flex items-center gap-1 mt-0.5">
                <span class="text-[10px] px-1.5 py-0.5 rounded-full font-medium"
                  :class="conv.role === 'staff' ? 'bg-blue-50 text-blue-600' : 'bg-green-50 text-green-600'"
                >{{ conv.role }}</span>
                <p class="text-gray-500 text-xs truncate" :class="{ 'text-gray-800 font-medium': conv.unreadCount > 0 }">
                  {{ conv.lastMessage }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area (Right Panel) -->
      <div
        class="flex-1 flex flex-col bg-gray-50"
        :class="activeConversation ? 'flex' : 'hidden sm:flex'"
      >
        <!-- No conversation selected -->
        <div v-if="!activeConversation" class="flex-1 flex flex-col items-center justify-center text-gray-400 p-8">
          <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-500 mb-1">Select a conversation</h3>
          <p class="text-sm text-gray-400">Choose from the list or start a new chat</p>
        </div>

        <!-- Active Chat -->
        <template v-else>
          <!-- Chat Messages -->
          <div ref="chatContainer" class="flex-1 overflow-y-auto px-4 py-4 space-y-3" id="chat-scroll">
            <!-- Date separator -->
            <div v-for="(group, dateKey) in groupedMessages" :key="dateKey" class="space-y-2">
              <div class="flex items-center gap-3 my-3">
                <div class="flex-1 h-px bg-gray-200"></div>
                <span class="text-[11px] text-gray-400 font-medium bg-gray-50 px-2">{{ dateKey }}</span>
                <div class="flex-1 h-px bg-gray-200"></div>
              </div>

              <div
                v-for="msg in group"
                :key="msg.id"
                class="flex"
                :class="msg.sender === authStore.user?.id ? 'justify-end' : 'justify-start'"
              >
                <div
                  class="max-w-[75%] lg:max-w-[60%] px-4 py-2.5 rounded-2xl shadow-sm relative group"
                  :class="msg.sender === authStore.user?.id
                    ? 'bg-cpsu-green text-white rounded-br-md'
                    : 'bg-white text-gray-900 rounded-bl-md border border-gray-100'"
                >
                  <p class="text-[14px] leading-relaxed whitespace-pre-wrap break-words">{{ msg.content }}</p>
                  <div class="flex items-center justify-end gap-1 mt-1"
                    :class="msg.sender === authStore.user?.id ? 'text-green-200' : 'text-gray-400'"
                  >
                    <span class="text-[10px]">{{ formatMsgTime(msg.timestamp) }}</span>
                    <template v-if="msg.sender === authStore.user?.id">
                      <svg v-if="msg.is_read" class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M18 7l-1.41-1.41-6.34 6.34 1.41 1.41L18 7zm4.24-1.41L11.66 16.17 7.48 12l-1.41 1.41L11.66 19l12-12-1.42-1.41zM.41 13.41L6 19l1.41-1.41L1.83 12 .41 13.41z"/>
                      </svg>
                      <svg v-else class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                      </svg>
                    </template>
                  </div>
                </div>
              </div>
            </div>

            <!-- Typing / empty state -->
            <div v-if="conversationMessages.length === 0" class="text-center py-8">
              <p class="text-gray-400 text-sm">Start the conversation by sending a message</p>
            </div>
          </div>

          <!-- Message Input -->
          <div class="bg-white border-t p-3">
            <div class="flex items-end gap-2">
              <div class="flex-1 relative">
                <textarea
                  v-model="chatInput"
                  ref="chatInputRef"
                  rows="1"
                  class="w-full px-4 py-2.5 bg-gray-100 rounded-2xl text-sm resize-none focus:outline-none focus:ring-2 focus:ring-cpsu-green/30 focus:bg-white transition max-h-32"
                  placeholder="Type a message..."
                  @keydown.enter.exact.prevent="sendChatMessage"
                  @input="autoResize"
                ></textarea>
              </div>
              <button
                aria-label="Send message"
                @click="sendChatMessage"
                :disabled="!chatInput.trim() || sending"
                class="flex-shrink-0 bg-cpsu-green hover:bg-cpsu-green-dark text-white rounded-full p-2.5 transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed shadow-sm"
              >
                <svg v-if="!sending" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                </svg>
                <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- New Chat Modal -->
    <Transition name="modal">
      <div v-if="showNewChat" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center" @click="showNewChat = false">
        <div class="fixed inset-0 bg-black/40 backdrop-blur-sm"></div>
        <div class="relative bg-white w-full sm:max-w-md sm:rounded-2xl rounded-t-2xl shadow-2xl animate-slide-up" @click.stop>
          <div class="flex items-center justify-between p-4 border-b bg-gray-50 sm:rounded-t-2xl">
            <h2 class="font-bold text-gray-900">New Conversation</h2>
            <button aria-label="Close new chat modal" @click="showNewChat = false" class="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-200 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="p-5 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Enter School ID</label>
              <div class="flex gap-2">
                <input
                  v-model="newChatId"
                  type="text"
                  class="input-field flex-1"
                  :placeholder="authStore.user?.role === 'staff' ? 'e.g. 2023-1234' : 'Enter Staff ID'"
                  @keydown.enter.prevent="lookupAndStartChat"
                >
                <button @click="lookupAndStartChat" :disabled="!newChatId.trim() || lookupLoading" class="btn-primary !px-4 !py-2 text-sm disabled:opacity-50">
                  <span v-if="lookupLoading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin inline-block"></span>
                  <span v-else>Find</span>
                </button>
              </div>
            </div>
            <!-- Result -->
            <div v-if="lookupResult" class="bg-green-50 rounded-xl p-4 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm"
                  :class="lookupResult.role === 'staff' ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'"
                >{{ getInitials(lookupResult.name) }}</div>
                <div>
                  <h4 class="font-semibold text-gray-900 text-sm">{{ lookupResult.name }}</h4>
                  <p class="text-xs text-gray-500">{{ lookupResult.school_id }} · {{ lookupResult.role }}</p>
                </div>
              </div>
              <button @click="startConversationWith(lookupResult)" class="btn-primary !py-2 !px-4 text-sm">Chat</button>
            </div>
            <p v-if="lookupError" class="text-sm text-red-600">{{ lookupError }}</p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push(authStore.user?.role === 'staff' ? '/staff' : '/dashboard')
  }
}

// --- State ---
const allMessages = ref<any[]>([])
const loading = ref(false)
const sending = ref(false)
const searchQuery = ref('')
const chatInput = ref('')
const chatInputRef = ref<HTMLTextAreaElement | null>(null)
const chatContainer = ref<HTMLElement | null>(null)
const activeConversation = ref<any>(null)
const showNewChat = ref(false)
const newChatId = ref('')
const lookupResult = ref<any>(null)
const lookupLoading = ref(false)
const lookupError = ref<string | null>(null)

let pollInterval: ReturnType<typeof setInterval> | null = null

// --- Computed: Group messages by conversation partner ---
const conversations = computed(() => {
  const userId = authStore.user?.id
  const convMap: Record<string, any> = {}

  for (const msg of allMessages.value) {
    const partnerId = msg.sender === userId ? msg.recipient : msg.sender
    const partnerName = msg.sender === userId ? msg.recipient_name : msg.sender_name
    const partnerRole = msg.sender === userId ? msg.recipient_role : msg.sender_role

    if (!convMap[partnerId]) {
      convMap[partnerId] = {
        userId: partnerId,
        name: partnerName || 'Unknown',
        role: partnerRole || 'user',
        messages: [],
        lastTimestamp: msg.timestamp,
        lastMessage: '',
        unreadCount: 0,
      }
    }

    convMap[partnerId].messages.push(msg)

    // Track latest message and unread
    if (new Date(msg.timestamp) >= new Date(convMap[partnerId].lastTimestamp)) {
      convMap[partnerId].lastTimestamp = msg.timestamp
      convMap[partnerId].lastMessage = msg.content.length > 50 ? msg.content.slice(0, 50) + '...' : msg.content
    }
    if (!msg.is_read && msg.recipient === userId) {
      convMap[partnerId].unreadCount++
    }
  }

  return Object.values(convMap).sort(
    (a: any, b: any) => new Date(b.lastTimestamp).getTime() - new Date(a.lastTimestamp).getTime()
  )
})

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  const q = searchQuery.value.toLowerCase()
  return conversations.value.filter((c: any) =>
    c.name.toLowerCase().includes(q) || c.role.toLowerCase().includes(q)
  )
})

const conversationMessages = computed(() => {
  if (!activeConversation.value) return []
  const partnerId = activeConversation.value.userId
  const userId = authStore.user?.id
  return allMessages.value
    .filter((m: any) =>
      (m.sender === userId && m.recipient === partnerId) ||
      (m.sender === partnerId && m.recipient === userId)
    )
    .sort((a: any, b: any) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
})

const groupedMessages = computed(() => {
  const groups: Record<string, any[]> = {}
  for (const msg of conversationMessages.value) {
    const d = new Date(msg.timestamp)
    const now = new Date()
    let dateKey: string
    if (d.toDateString() === now.toDateString()) {
      dateKey = 'Today'
    } else {
      const yesterday = new Date(now)
      yesterday.setDate(yesterday.getDate() - 1)
      if (d.toDateString() === yesterday.toDateString()) {
        dateKey = 'Yesterday'
      } else {
        dateKey = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
      }
    }
    if (!groups[dateKey]) groups[dateKey] = []
    groups[dateKey].push(msg)
  }
  return groups
})

// --- Formatters ---
const formatTime = (ts: string) => {
  const d = new Date(ts)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const mins = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  if (mins < 1) return 'now'
  if (mins < 60) return `${mins}m`
  if (hours < 24) return `${hours}h`
  if (hours < 48) return 'yesterday'
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const formatMsgTime = (ts: string) => {
  return new Date(ts).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

const getInitials = (name: string) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

// --- API / Logic ---
const fetchMessages = async (silent = false) => {
  if (!silent) loading.value = true
  try {
    const res = await api.get('/messages/')
    allMessages.value = Array.isArray(res.data) ? res.data : (res.data.results || [])
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openConversation = async (conv: any) => {
  activeConversation.value = conv
  await nextTick()
  scrollToBottom()

  // Mark unread messages in this conversation as read
  const userId = authStore.user?.id
  const unread = allMessages.value.filter(
    (m: any) => m.recipient === userId && m.sender === conv.userId && !m.is_read
  )
  for (const msg of unread) {
    try {
      await api.patch(`/messages/${msg.id}/mark_read/`)
      msg.is_read = true
    } catch (e) { console.error(e) }
  }
}

const sendChatMessage = async () => {
  if (!chatInput.value.trim() || !activeConversation.value || sending.value) return
  sending.value = true
  try {
    await api.post('/messages/', {
      recipient: activeConversation.value.userId,
      content: chatInput.value.trim()
    })
    chatInput.value = ''
    resetTextarea()
    await fetchMessages(true)
    await nextTick()
    scrollToBottom()
  } catch (e: any) {
    console.error(e)
    alert(e.response?.data?.detail || 'Failed to send message')
  } finally {
    sending.value = false
  }
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const autoResize = () => {
  const el = chatInputRef.value
  if (el) {
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 128) + 'px'
  }
}

const resetTextarea = () => {
  if (chatInputRef.value) {
    chatInputRef.value.style.height = 'auto'
  }
}

// New chat lookup
const lookupAndStartChat = async () => {
  if (!newChatId.value.trim()) return
  lookupLoading.value = true
  lookupError.value = null
  lookupResult.value = null
  try {
    const res = await api.get(`/messages/user_search/?school_id=${newChatId.value.trim()}`)
    lookupResult.value = res.data
  } catch (e: any) {
    lookupError.value = e.response?.data?.error || 'User not found'
  } finally {
    lookupLoading.value = false
  }
}

const startConversationWith = (user: any) => {
  showNewChat.value = false
  newChatId.value = ''
  lookupResult.value = null

  // Check if conversation already exists
  const existing = conversations.value.find((c: any) => c.userId === user.id)
  if (existing) {
    openConversation(existing)
  } else {
    // Create a virtual conversation
    activeConversation.value = {
      userId: user.id,
      name: user.name,
      role: user.role,
      messages: [],
      lastTimestamp: new Date().toISOString(),
      lastMessage: '',
      unreadCount: 0,
    }
  }
  nextTick(() => chatInputRef.value?.focus())
}

// --- Polling ---
const startPolling = () => {
  pollInterval = setInterval(async () => {
    const prevCount = allMessages.value.length
    await fetchMessages(true)
    // Auto-scroll if new messages arrived in active conversation
    if (allMessages.value.length > prevCount && activeConversation.value) {
      await nextTick()
      scrollToBottom()
    }
  }, 5000)
}

// --- Lifecycle ---
onMounted(async () => {
  await fetchMessages()

  // Handle query params
  if (route.query.recipient) {
    const recipientId = route.query.recipient as string
    try {
      const res = await api.get(`/messages/user_search/?school_id=${recipientId}`)
      startConversationWith(res.data)
    } catch (e) {
      showNewChat.value = true
      newChatId.value = recipientId
    }
  }

  startPolling()
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})

// Watch for conversation changes to scroll
watch(conversationMessages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })
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
.border-l-3 {
  border-left-width: 3px;
}

/* Scrollbar styling */
#chat-scroll::-webkit-scrollbar {
  width: 6px;
}
#chat-scroll::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}
#chat-scroll::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
