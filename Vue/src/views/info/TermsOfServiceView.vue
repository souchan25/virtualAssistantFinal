<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center space-x-3 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-12 w-12 object-contain">
            <div>
              <h1 class="text-xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs text-gray-600">Terms of Service</p>
            </div>
          </router-link>
          <router-link to="/" class="text-cpsu-green hover:underline font-medium">← Back to Home</router-link>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-12 max-w-4xl">
      <h2 class="text-3xl font-heading font-bold text-cpsu-green mb-8">Terms of Service</h2>
      <p class="text-sm text-gray-500 mb-8">Last updated: February 2025</p>

      <div class="prose prose-lg max-w-none space-y-6 text-gray-700">
        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">1. Acceptance of Terms</h3>
          <p>By registering and using the CPSU Health Assistant, you agree to these Terms of Service. This system is provided by Central Philippines State University for its students and clinic staff.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">2. Eligibility</h3>
          <p>You must be a registered CPSU student or authorized clinic staff member to use this system. You must provide accurate information during registration and keep your account credentials secure.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">3. Medical Disclaimer</h3>
          <p><strong>Important:</strong> The CPSU Health Assistant provides AI-powered health information and is not a substitute for professional medical advice. Predictions are for informational purposes only. Always consult clinic staff or a healthcare provider for diagnosis and treatment. In emergencies, use the SOS feature or contact emergency services.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">4. Acceptable Use</h3>
          <p>You agree to:</p>
          <ul class="list-disc pl-6 space-y-2 mt-2">
            <li>Use the system only for legitimate health-related purposes</li>
            <li>Provide accurate symptom and health information</li>
            <li>Not misuse the emergency SOS feature</li>
            <li>Not attempt to access other users' data or compromise system security</li>
          </ul>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">5. Account Responsibility</h3>
          <p>You are responsible for all activity under your account. Keep your School ID and password confidential. Report any unauthorized access to the CPSU IT department immediately.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">6. Changes to Terms</h3>
          <p>CPSU may update these terms. Continued use of the system after changes constitutes acceptance. Significant changes will be communicated to users.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">7. Contact</h3>
          <p>For questions about these terms, contact clinic@cpsu.edu.ph or the CPSU IT department.</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
