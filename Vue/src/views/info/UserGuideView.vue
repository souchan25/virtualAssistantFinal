<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center space-x-3 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-12 w-12 object-contain">
            <div>
              <h1 class="text-xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs text-gray-600">User Guide</p>
            </div>
          </router-link>
          <router-link to="/" class="text-cpsu-green hover:underline font-medium">← Back to Home</router-link>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-12 max-w-4xl">
      <h2 class="text-3xl font-heading font-bold text-cpsu-green mb-4">User Guide</h2>
      <p class="text-gray-600 mb-12">A step-by-step guide to using the CPSU Health Assistant</p>

      <div class="space-y-12">
        <!-- 1. Getting Started -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-cpsu-green text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">1</span>
            <h3 class="text-xl font-bold text-gray-900">Getting Started</h3>
          </div>
          <p class="text-gray-700 mb-4">Register with your School ID and password. Grant data consent to enable health features. After registration, log in to access your dashboard.</p>
          <p class="text-sm text-gray-500">Tip: Keep your School ID and password secure. Do not share them with others.</p>
        </section>

        <!-- 2. Dashboard -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-cpsu-green text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">2</span>
            <h3 class="text-xl font-bold text-gray-900">Dashboard</h3>
          </div>
          <p class="text-gray-700 mb-4">Your dashboard shows quick links to all features:</p>
          <ul class="list-disc pl-6 space-y-2 text-gray-700">
            <li><strong>Check Symptoms</strong> – AI-powered symptom analysis</li>
            <li><strong>My Medications</strong> – View prescriptions and adherence</li>
            <li><strong>Follow-Ups</strong> – Respond to health check-ins</li>
            <li><strong>Health Analytics</strong> – View your health trends</li>
            <li><strong>Chat Assistant</strong> – Talk to the health chatbot</li>
            <li><strong>View History</strong> – See past consultations</li>
          </ul>
        </section>

        <!-- 3. Symptom Checker -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-cpsu-green text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">3</span>
            <h3 class="text-xl font-bold text-gray-900">Symptom Checker</h3>
          </div>
          <p class="text-gray-700 mb-4">Select your symptoms from the list (or search for them). Click "Analyze Symptoms" to get AI predictions. You'll see possible conditions, confidence scores, and self-care tips. This is for information only—visit the clinic for proper diagnosis.</p>
        </section>

        <!-- 4. Chat Assistant -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-cpsu-green text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">4</span>
            <h3 class="text-xl font-bold text-gray-900">Chat Assistant</h3>
          </div>
          <p class="text-gray-700 mb-4">Describe your symptoms in the chat. The AI will ask follow-up questions (e.g., "How many days have you had the cough?") to provide better recommendations. Answer these to improve accuracy. If symptoms persist 3–5 days, visit the clinic.</p>
        </section>

        <!-- 5. Follow-Ups -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-cpsu-green text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">5</span>
            <h3 class="text-xl font-bold text-gray-900">Follow-Ups</h3>
          </div>
          <p class="text-gray-700 mb-4">After reporting symptoms, you'll receive a follow-up request. Go to the Follow-Ups page and respond with how you're feeling (e.g., Improved, Same, Worse). Add notes if needed. Clinic staff may review and add recommendations—check back for their feedback.</p>
        </section>

        <!-- 6. Emergency SOS -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-red-500 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">!</span>
            <h3 class="text-xl font-bold text-gray-900">Emergency SOS</h3>
          </div>
          <p class="text-gray-700 mb-4">For emergencies only. The SOS button sends your location and alert to clinic staff immediately. Use only for real emergencies.</p>
        </section>

        <!-- 7. Profile & Support -->
        <section class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <span class="bg-cpsu-green text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">6</span>
            <h3 class="text-xl font-bold text-gray-900">Profile & Support</h3>
          </div>
          <p class="text-gray-700 mb-4">Update your name, department, and address in Profile. For help, contact the CPSU Clinic (clinic@cpsu.edu.ph) or IT department.</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
