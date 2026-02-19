<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center space-x-3 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-12 w-12 object-contain">
            <div>
              <h1 class="text-xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs text-gray-600">Frequently Asked Questions</p>
            </div>
          </router-link>
          <router-link to="/" class="text-cpsu-green hover:underline font-medium">← Back to Home</router-link>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-12 max-w-4xl">
      <h2 class="text-3xl font-heading font-bold text-cpsu-green mb-8">Frequently Asked Questions</h2>

      <div class="space-y-6">
        <div v-for="(faq, index) in faqs" :key="index" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-2">{{ faq.question }}</h3>
          <p class="text-gray-700">{{ faq.answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const faqs = [
  {
    question: 'How do I register?',
    answer: 'Click "Register" on the homepage. Enter your School ID, create a password, and provide your name, department, and address. You must grant data consent to use health features.'
  },
  {
    question: 'What is the Symptom Checker?',
    answer: 'The Symptom Checker lets you select symptoms and receive AI-powered disease predictions. Results include possible conditions, confidence scores, and self-care tips. This is for informational purposes only—always consult clinic staff for proper diagnosis.'
  },
  {
    question: 'How does the Chat Assistant work?',
    answer: 'The Chat Assistant is an AI health chatbot. Describe your symptoms in natural language and receive follow-up questions, predictions, and recommendations. Your responses help improve the assessment. If symptoms persist 3–5 days, visit the clinic.'
  },
  {
    question: 'What are Follow-ups?',
    answer: 'After you report symptoms, the system schedules a follow-up (usually 3 days later). You can respond with how you\'re feeling. Clinic staff may review your response and add notes. Check your Follow-Ups page to respond.'
  },
  {
    question: 'How do I use the Emergency SOS?',
    answer: 'The SOS button sends an immediate alert to clinic staff with your location. Use it only for real emergencies. False alarms may be subject to university policies.'
  },
  {
    question: 'Can I delete my health history?',
    answer: 'Yes. In the History page, you can delete individual symptom records. Note that some data may be retained for clinic records and audit purposes.'
  },
  {
    question: 'Who can see my health data?',
    answer: 'Only you and authorized CPSU clinic staff can view your health records. Staff access is limited to what is needed for care. See our Privacy Policy and Data Security pages for details.'
  },
  {
    question: 'How do I change my password?',
    answer: 'Contact the CPSU IT department or clinic to reset your password. Use your School ID to log in.'
  },
  {
    question: 'What if the AI prediction seems wrong?',
    answer: 'AI predictions are estimates, not diagnoses. Clinic staff can correct the diagnosis after reviewing your case. If you disagree with a prediction, discuss it with clinic staff during your visit.'
  },
  {
    question: 'Where can I get help?',
    answer: 'For technical issues, contact the CPSU IT department. For health-related questions, visit the campus clinic or email clinic@cpsu.edu.ph.'
  }
]
</script>
