<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-3 sm:py-4">
        <div class="flex justify-between items-center">
          <router-link to="/dashboard" class="flex items-center space-x-2 sm:space-x-4 text-cpsu-green flex-shrink-0">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-10 w-10 sm:h-12 sm:w-12 object-contain flex-shrink-0">
            <div class="hidden sm:block">
              <h1 class="text-lg sm:text-xl lg:text-2xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs sm:text-sm text-gray-600 hidden md:block">Central Philippines State University</p>
            </div>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden xl:flex items-center space-x-1 lg:space-x-2">
            <router-link to="/dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Dashboard</router-link>
            <router-link to="/symptom-checker" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Check Symptoms</router-link>
            <router-link to="/medications" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Medications</router-link>
            <router-link to="/followups" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Follow-Ups</router-link>
            <router-link to="/health-dashboard" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Analytics</router-link>
            <router-link to="/chat" class="text-cpsu-green font-semibold px-2 lg:px-3 py-2 text-sm whitespace-nowrap">AI Assistant</router-link>
            <router-link to="/history" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">History</router-link>
            <router-link to="/profile" class="text-gray-700 hover:text-cpsu-green px-2 lg:px-3 py-2 text-sm whitespace-nowrap">Profile</router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="xl:hidden text-cpsu-green p-2 -mr-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile/Tablet Menu -->
        <div v-if="mobileMenuOpen" class="xl:hidden mt-3 pt-3 pb-2 space-y-2 border-t border-gray-200">
          <router-link to="/dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Dashboard</router-link>
          <router-link to="/symptom-checker" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Check Symptoms</router-link>
          <router-link to="/medications" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Medications</router-link>
          <router-link to="/followups" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Follow-Ups</router-link>
          <router-link to="/health-dashboard" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Analytics</router-link>
          <router-link to="/chat" class="block px-4 py-2 text-cpsu-green font-semibold hover:bg-gray-100 rounded text-sm">AI Assistant</router-link>
          <router-link to="/history" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">History</router-link>
          <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded text-sm">Profile</router-link>
        </div>
      </div>
    </nav>

    <!-- Chat Header -->
    <div class="bg-gradient-to-r from-cpsu-green to-cpsu-green-dark text-white px-3 sm:px-4 lg:px-6 py-3 sm:py-4 shadow-md">
      <div class="container mx-auto flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
        <div class="flex items-center space-x-2 sm:space-x-3">
          <div class="w-10 h-10 sm:w-12 sm:h-12 bg-cpsu-yellow rounded-full flex items-center justify-center text-xl sm:text-2xl flex-shrink-0">
            🤖
          </div>
          <div class="min-w-0">
            <h2 class="text-lg sm:text-2xl font-heading font-bold truncate">Health Chat Assistant</h2>
            <p class="text-xs sm:text-sm text-cpsu-yellow hidden sm:block">AI-powered health support</p>
          </div>
        </div>
        <button
          v-if="chatStore.messages.length > 0"
          @click="clearChat"
          class="text-white bg-white/20 hover:bg-white hover:text-cpsu-green px-3 sm:px-4 py-2 rounded-lg transition-all font-semibold text-sm flex items-center space-x-1 sm:space-x-2 justify-center flex-shrink-0"
        >
          <span>🗑️</span>
          <span class="hidden sm:inline">Clear Chat</span>
        </button>
      </div>
    </div>

    <!-- Chat Container - Full Width -->
    <div class="flex-1 flex flex-col bg-gray-100 min-h-0">
      <!-- Messages Area - Full Width -->
      <div class="flex-1 overflow-y-auto py-4 sm:py-6" ref="messagesContainer">
        <div class="container mx-auto px-3 sm:px-4 lg:px-6 max-w-6xl">
          <!-- Welcome Message -->
          <div v-if="chatStore.messages.length === 0" class="text-center py-12 sm:py-20">
            <div class="w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full mx-auto mb-4 sm:mb-6 flex items-center justify-center text-4xl sm:text-5xl shadow-lg">
              🤖
            </div>
            <h3 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2 sm:mb-3">Welcome to Health Chat!</h3>
            <p class="text-gray-600 text-sm sm:text-lg mb-6 sm:mb-8">I'm your AI health assistant. How can I help you today?</p>
            <div class="flex flex-wrap justify-center gap-2 sm:gap-3">
              <button
                v-for="action in quickActions"
                :key="action"
                @click="sendQuickMessage(action)"
                class="px-3 sm:px-6 py-2 sm:py-3 bg-white border-2 border-cpsu-green text-cpsu-green rounded-lg hover:bg-cpsu-green hover:text-white transition-all shadow-sm hover:shadow-md font-semibold text-xs sm:text-sm"
              >
                {{ action }}
              </button>
            </div>
          </div>

          <!-- Chat Messages -->
          <div class="space-y-4 sm:space-y-6">
            <div
              v-for="message in chatStore.messages"
              :key="message.id"
              :class="['flex', message.sender === 'user' ? 'justify-end' : 'justify-start']"
            >
              <!-- AI Message with Avatar -->
              <div v-if="message.sender === 'bot'" class="flex items-start space-x-2 sm:space-x-3 w-full sm:max-w-4xl">
                <!-- AI Avatar -->
                <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full flex items-center justify-center text-white text-sm sm:text-xl shadow-md">
                  🤖
                </div>
                
                <!-- AI Message Content -->
                <div class="flex-1 min-w-0">
                  <div class="bg-white rounded-2xl rounded-tl-none shadow-md border border-gray-200 overflow-hidden">
                    <div class="p-3 sm:p-5 text-xs sm:text-sm" v-html="formatBotMessage(message.content)"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-1 sm:mt-2 ml-1 sm:ml-2">
                    {{ new Date(message.timestamp).toLocaleTimeString() }}
                  </p>
                </div>
              </div>

              <!-- User Message -->
              <div v-else class="flex items-start space-x-2 sm:space-x-3 w-full sm:max-w-2xl justify-end">
                <div class="flex-1 min-w-0">
                  <div
                    :class="[
                      'rounded-2xl rounded-tr-none shadow-md px-3 sm:px-5 py-2 sm:py-3 text-xs sm:text-sm',
                      message.isError
                        ? 'bg-red-500 text-white'
                        : 'bg-cpsu-yellow text-cpsu-green'
                    ]"
                  >
                    <p class="whitespace-pre-wrap font-medium break-words">{{ message.content }}</p>
                  </div>
                  <p class="text-xs text-gray-500 mt-1 sm:mt-2 mr-1 sm:mr-2 text-right">
                    {{ new Date(message.timestamp).toLocaleTimeString() }}
                  </p>
                </div>
                
                <!-- User Avatar -->
                <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 bg-cpsu-yellow rounded-full flex items-center justify-center text-cpsu-green text-sm sm:text-xl font-bold shadow-md">
                  👤
                </div>
              </div>
            </div>
          </div>

          <!-- Loading Indicator -->
          <div v-if="chatStore.loading" class="flex justify-start">
            <div class="flex items-start space-x-2 sm:space-x-3 w-full sm:max-w-4xl">
              <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full flex items-center justify-center text-white text-sm sm:text-xl shadow-md">
                🤖
              </div>
              <div class="bg-white rounded-2xl rounded-tl-none shadow-md border border-gray-200 px-3 sm:px-5 py-3 sm:py-4">
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-cpsu-green rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-cpsu-green rounded-full animate-bounce" style="animation-delay: 0.15s"></div>
                  <div class="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-cpsu-green rounded-full animate-bounce" style="animation-delay: 0.3s"></div>
                  <span class="text-gray-600 ml-1 sm:ml-2 text-xs sm:text-base">Thinking...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area - Full Width Bottom -->
      <div class="bg-white border-t-2 border-gray-200 shadow-lg flex-shrink-0">
        <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-3 sm:py-4 max-w-6xl w-full">
          <form @submit.prevent="sendMessage" class="flex gap-2 sm:gap-3 items-center">
            <input
              v-model="messageInput"
              type="text"
              placeholder="Type your health question here..."
              class="flex-1 px-3 sm:px-5 py-2 sm:py-3 border-2 border-gray-300 rounded-full focus:border-cpsu-green focus:ring-2 focus:ring-cpsu-green/20 outline-none transition-all text-gray-900 text-xs sm:text-lg"
              :disabled="chatStore.loading"
            />
            <button
              type="submit"
              :disabled="!messageInput.trim() || chatStore.loading"
              class="bg-cpsu-green text-white px-4 sm:px-8 py-2 sm:py-3 rounded-full font-bold text-xs sm:text-lg hover:bg-cpsu-green-dark transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg flex items-center space-x-1 sm:space-x-2 flex-shrink-0 whitespace-nowrap"
            >
              <span class="hidden sm:inline">Send</span>
              <span>📤</span>
            </button>
          </form>
          
          <!-- Quick Actions -->
          <div v-if="chatStore.messages.length > 0" class="mt-3 flex flex-wrap gap-2">
            <span class="text-xs text-gray-600 font-medium w-full">Quick questions:</span>
            <button
              v-for="action in quickActions"
              :key="action"
              @click="sendQuickMessage(action)"
              :disabled="chatStore.loading"
              class="text-xs px-3 py-1 border-2 border-cpsu-green/30 text-cpsu-green rounded-full hover:bg-cpsu-green hover:text-white transition-all disabled:opacity-50 font-medium"
            >
              {{ action }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { useChatStore } from '@/stores/chat'
import DOMPurify from 'dompurify' // Security: Use DOMPurify to sanitize HTML content

const chatStore = useChatStore()
const messageInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)
const mobileMenuOpen = ref(false)

const quickActions = [
  'I have a headache',
  'I feel tired',
  'I have fever',
  'Tell me about common cold'
]

function formatBotMessage(content: string): string {
  // Parse the structured health response
  let html = content

  // Format diagnosis section
  html = html.replace(/🏥\s*\*\*Diagnosis Analysis\*\*/g, '<div class="mb-6"><div class="flex items-center space-x-2 mb-4"><span class="text-3xl">🏥</span><h3 class="text-xl font-bold text-cpsu-green">Diagnosis Analysis</h3></div>')
  
  // Format condition and confidence
  html = html.replace(/\*\*Condition\*\*:\s*([^\n]+)/g, '<div class="bg-cpsu-green/10 rounded-lg p-4 mb-3"><div class="flex items-center justify-between"><div><span class="text-sm text-gray-600">Condition</span><div class="text-2xl font-bold text-cpsu-green mt-1">$1</div></div>')
  html = html.replace(/\*\*Confidence\*\*:\s*(\d+)%\s*✅\s*\(AI Validated\)/g, '<div class="text-right"><span class="text-sm text-gray-600">Confidence</span><div class="text-2xl font-bold text-cpsu-green mt-1">$1%</div><span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full mt-1 inline-block">✅ AI Validated</span></div></div></div>')
  
  // Format description
  html = html.replace(/\*\*Description\*\*:\s*([^\n]+(?:\n(?!\*\*)[^\n]+)*)/g, '<div class="bg-gray-50 rounded-lg p-4 mb-4"><div class="text-sm text-gray-600 mb-2 font-semibold">Description</div><p class="text-gray-700 leading-relaxed">$1</p></div>')
  
  // Format precautions
  html = html.replace(/\*\*Recommended Precautions\*\*:\s*/g, '<div class="mb-4"><div class="text-sm font-semibold text-gray-800 mb-3 flex items-center"><span class="text-xl mr-2">💊</span>Recommended Precautions</div><ul class="space-y-2">')
  html = html.replace(/(\d+)\.\s*([^\n]+)/g, '<li class="flex items-start space-x-3"><span class="flex-shrink-0 w-6 h-6 bg-cpsu-green text-white rounded-full flex items-center justify-center text-xs font-bold">$1</span><span class="text-gray-700 flex-1">$2</span></li>')
  
  // Format important notice
  html = html.replace(/⚕️\s*\*\*Important\*\*:\s*([^\n]+)/g, '</ul></div><div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4"><div class="flex items-start space-x-2"><span class="text-xl">⚕️</span><div><div class="font-semibold text-yellow-800 mb-1">Important Notice</div><p class="text-sm text-yellow-700">$1</p></div></div></div>')
  
  // Format other possibilities
  html = html.replace(/\*\*Other Possibilities\*\*:\s*/g, '<div class="border-t border-gray-200 pt-4"><div class="text-sm font-semibold text-gray-700 mb-3">Other Possibilities</div><ul class="space-y-2">')
  html = html.replace(/•\s*([^\(]+)\((\d+)%\)/g, '<li class="flex items-center justify-between text-sm"><span class="text-gray-700">• $1</span><span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-xs font-semibold">$2%</span></li>')
  
  // Close any open divs
  if (html.includes('<ul class="space-y-2">') && !html.includes('</ul></div></div>')) {
    html += '</ul></div></div>'
  }
  
  // Format bold text that wasn't caught
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold text-gray-800">$1</strong>')
  
  // Format line breaks
  html = html.replace(/\n/g, '<br>')
  
  // Security: Sanitize the final HTML to prevent XSS vulnerabilities
  return DOMPurify.sanitize(html)
}

async function sendMessage() {
  if (!messageInput.value.trim()) return
  
  const message = messageInput.value
  messageInput.value = ''
  
  await chatStore.sendMessage(message)
  scrollToBottom()
}

function sendQuickMessage(message: string) {
  messageInput.value = message
  sendMessage()
}

async function clearChat() {
  if (confirm('Are you sure you want to clear this conversation?')) {
    await chatStore.endSession()
    chatStore.clearMessages()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Auto-scroll when new messages arrive
watch(() => chatStore.messages.length, () => {
  scrollToBottom()
})
</script>
