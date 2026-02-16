import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import type { ChatMessage, ChatSession } from '@/types'

export const useChatStore = defineStore('chat', () => {
  // State
  const messages = ref<ChatMessage[]>([])
  const sessionId = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  async function startSession() {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/chat/start/')
      sessionId.value = response.data.session_id
      messages.value = []
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to start chat'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function sendMessage(message: string) {
    if (!sessionId.value) {
      await startSession()
    }

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now(),
      content: message,
      sender: 'user',
      timestamp: new Date().toISOString()
    }
    messages.value.push(userMessage)

    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/chat/message/', {
        message,
        session_id: sessionId.value
      })
      
      // Add bot response
      const botMessage: ChatMessage = {
        id: Date.now() + 1,
        content: response.data.response,
        sender: 'bot',
        timestamp: response.data.timestamp || new Date().toISOString(),
        metadata: response.data.metadata
      }
      messages.value.push(botMessage)
      
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to send message'
      
      // Add error message
      messages.value.push({
        id: Date.now() + 1,
        content: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true
      })
      
      throw err
    } finally {
      loading.value = false
    }
  }

  async function endSession() {
    if (!sessionId.value) return
    
    try {
      await api.post('/chat/end/', {
        session_id: sessionId.value
      })
    } catch (err) {
      console.error('Error ending session:', err)
    } finally {
      sessionId.value = null
      messages.value = []
    }
  }

  function clearMessages() {
    messages.value = []
  }

  return {
    messages,
    sessionId,
    loading,
    error,
    startSession,
    sendMessage,
    endSession,
    clearMessages
  }
})
