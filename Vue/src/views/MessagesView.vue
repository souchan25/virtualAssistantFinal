<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-xl font-bold text-cpsu-green">Messages</h1>
          <button @click="$router.go(-1)" class="text-gray-600 hover:text-gray-900">Back</button>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-4 py-6">
      <!-- Tabs -->
      <div class="flex space-x-4 mb-6 border-b">
        <button
          v-for="tab in ['Inbox', 'Sent', 'Compose']"
          :key="tab"
          @click="currentTab = tab"
          class="pb-2 px-4 font-medium transition-colors"
          :class="currentTab === tab ? 'border-b-2 border-cpsu-green text-cpsu-green' : 'text-gray-500 hover:text-gray-700'"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-cpsu-green border-t-transparent"></div>
      </div>

      <!-- Inbox & Sent Lists -->
      <div v-else-if="currentTab === 'Inbox' || currentTab === 'Sent'">
        <div v-if="messages.length === 0" class="text-center py-12 text-gray-500">
          No messages found.
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="bg-white p-4 rounded-lg shadow border cursor-pointer hover:border-cpsu-green transition-all"
            :class="{ 'bg-blue-50 border-l-4 border-l-cpsu-green': !msg.is_read && currentTab === 'Inbox' }"
            @click="openMessage(msg)"
          >
            <div class="flex justify-between items-start mb-2">
              <div>
                <span class="font-bold text-gray-900">
                  {{ currentTab === 'Inbox' ? (msg.sender_name || 'Unknown') : 'To: ' + (msg.recipient_name || 'Unknown') }}
                </span>
                <span class="text-xs text-gray-500 ml-2" v-if="currentTab === 'Inbox'">
                  ({{ msg.sender_role }})
                </span>
              </div>
              <span class="text-xs text-gray-500">{{ formatDate(msg.timestamp) }}</span>
            </div>
            <p class="text-gray-700 line-clamp-2 text-sm">{{ msg.content }}</p>
          </div>
        </div>
      </div>

      <!-- Compose Form -->
      <div v-else-if="currentTab === 'Compose'" class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-bold mb-4">New Message</h2>

        <!-- Staff sends to Student (by ID) -->
        <div class="mb-4" v-if="authStore.user?.role === 'staff'">
          <label class="block text-sm font-medium text-gray-700 mb-1">Recipient (School ID)</label>
          <input v-model="newMessage.recipient_id" type="text" class="input-field w-full" placeholder="Enter Student School ID (e.g. 2023-1234)">
          <p class="text-xs text-gray-500 mt-1">System will lookup student by ID.</p>
        </div>

        <!-- Student sends to Staff (generic or list) -->
        <div class="mb-4" v-else>
           <label class="block text-sm font-medium text-gray-700 mb-1">Recipient</label>
           <input v-model="newMessage.recipient_id" type="text" class="input-field w-full" placeholder="Enter Staff School ID">
           <p class="text-xs text-gray-500 mt-1">Enter the ID of the staff member you wish to contact.</p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Message</label>
          <textarea v-model="newMessage.content" rows="6" class="input-field w-full" placeholder="Type your message..."></textarea>
        </div>

        <button @click="sendMessage" :disabled="sending || !newMessage.content || !newMessage.recipient_id" class="btn-primary w-full justify-center">
          <span v-if="sending">Sending...</span>
          <span v-else>Send Message</span>
        </button>
        <p v-if="sendError" class="mt-2 text-sm text-red-600">{{ sendError }}</p>
      </div>
    </div>

    <!-- Message Detail Modal -->
    <div v-if="selectedMessage" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="selectedMessage = null">
      <div class="bg-white rounded-lg max-w-lg w-full p-6 shadow-xl" @click.stop>
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="font-bold text-lg">{{ selectedMessage.sender_name }} <span class="text-sm font-normal text-gray-500">({{ selectedMessage.sender_role }})</span></h3>
            <p class="text-sm text-gray-600">{{ formatDate(selectedMessage.timestamp) }}</p>
          </div>
          <button @click="selectedMessage = null" class="text-gray-400 hover:text-gray-600 text-2xl">×</button>
        </div>
        <div class="bg-gray-50 p-4 rounded-lg mb-6 max-h-60 overflow-y-auto">
          <p class="text-gray-800 whitespace-pre-wrap">{{ selectedMessage.content }}</p>
        </div>
        <div class="flex justify-end gap-2">
          <button @click="selectedMessage = null" class="btn-outline">Close</button>
          <button @click="replyTo(selectedMessage)" class="btn-primary">Reply</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const currentTab = ref('Inbox')
const messages = ref<any[]>([])
const loading = ref(false)
const selectedMessage = ref<any>(null)

// Compose state
const sending = ref(false)
const sendError = ref<string | null>(null)
const newMessage = ref({
  recipient_id: '',
  content: ''
})

const formatDate = (ts: string) => {
  return new Date(ts).toLocaleString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

const fetchMessages = async () => {
  loading.value = true
  try {
    const res = await api.get('/messages/')
    const allMsgs = res.data
    const userId = authStore.user?.id

    if (currentTab.value === 'Inbox') {
      messages.value = allMsgs.filter((m: any) => m.recipient === userId)
    } else if (currentTab.value === 'Sent') {
      messages.value = allMsgs.filter((m: any) => m.sender === userId)
    }

    // Sort descending by timestamp
    messages.value.sort((a: any, b: any) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openMessage = async (msg: any) => {
  selectedMessage.value = msg
  if (!msg.is_read && msg.recipient === authStore.user?.id) {
    try {
      await api.patch(`/messages/${msg.id}/mark_read/`)
      msg.is_read = true
    } catch (e) { console.error(e) }
  }
}

const sendMessage = async () => {
  if (!newMessage.value.recipient_id || !newMessage.value.content) return
  sending.value = true
  sendError.value = null

  try {
    let recipientPk = null

    // Attempt lookup (Staff -> Student)
    if (authStore.user?.role === 'staff') {
       try {
         const res = await api.get(`/staff/students/?search=${newMessage.value.recipient_id}`)
         const students = res.data.results || res.data.students || []
         const student = students.find((s: any) => s.school_id === newMessage.value.recipient_id)
         if (student) recipientPk = student.id
       } catch (e) { console.warn('Lookup failed', e) }
    }

    if (!recipientPk) {
        sendError.value = 'Could not find user with that School ID. (Feature in progress)'
        sending.value = false
        return
    }

    await api.post('/messages/', {
      recipient: recipientPk,
      content: newMessage.value.content
    })

    newMessage.value.content = ''
    newMessage.value.recipient_id = ''
    currentTab.value = 'Sent'
  } catch (e: any) {
    console.error(e)
    sendError.value = e.response?.data?.error || 'Failed to send message'
  } finally {
    sending.value = false
  }
}

const replyTo = (msg: any) => {
  let targetId = msg.sender
  // Not fully implemented as explained in previous turn
  alert("Reply is not fully implemented yet.")
  selectedMessage.value = null
}

watch(currentTab, (val) => {
  if (val === 'Inbox' || val === 'Sent') fetchMessages()
})

onMounted(() => {
  if (route.query.tab) {
    currentTab.value = route.query.tab as string
  }
  if (route.query.recipient) {
    newMessage.value.recipient_id = route.query.recipient as string
  }
  if (currentTab.value === 'Inbox' || currentTab.value === 'Sent') {
    fetchMessages()
  }
})
</script>
