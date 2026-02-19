<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center space-x-3 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-12 w-12 object-contain">
            <div>
              <h1 class="text-xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs text-gray-600">Privacy Policy</p>
            </div>
          </router-link>
          <router-link to="/" class="text-cpsu-green hover:underline font-medium">← Back to Home</router-link>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-12 max-w-4xl">
      <h2 class="text-3xl font-heading font-bold text-cpsu-green mb-8">Privacy Policy</h2>
      <p class="text-sm text-gray-500 mb-8">Last updated: February 2025</p>

      <div class="prose prose-lg max-w-none space-y-6 text-gray-700">
        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">1. Information We Collect</h3>
          <p>When you use the CPSU Health Assistant, we collect:</p>
          <ul class="list-disc pl-6 space-y-2 mt-2">
            <li><strong>Account information:</strong> School ID, name, department, and CPSU address</li>
            <li><strong>Health data:</strong> Symptoms you report, AI predictions, follow-up responses, and medication records</li>
            <li><strong>Usage data:</strong> Chat sessions, symptom checker usage, and system interactions</li>
          </ul>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">2. How We Use Your Information</h3>
          <p>Your data is used to:</p>
          <ul class="list-disc pl-6 space-y-2 mt-2">
            <li>Provide AI-powered health assessments and recommendations</li>
            <li>Schedule and manage follow-up appointments with clinic staff</li>
            <li>Track medication adherence and prescriptions</li>
            <li>Improve our services and support clinic operations</li>
          </ul>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">3. Data Sharing</h3>
          <p>Your health information is shared only with authorized CPSU clinic staff who need it to provide care. We do not sell or share your data with third parties for marketing purposes.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">4. Data Consent</h3>
          <p>You must grant data consent before using health features. You may revoke consent at any time through your profile settings. Revoking consent may limit your access to certain features.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">5. Data Security</h3>
          <p>We implement industry-standard security measures to protect your information, including encryption, access controls, and audit logging. See our <router-link to="/data-security" class="text-cpsu-green hover:underline">Data Security</router-link> page for details.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">6. Contact Us</h3>
          <p>For privacy-related questions, contact the CPSU Clinic or IT department at clinic@cpsu.edu.ph.</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
