<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b-2 border-cpsu-green sticky top-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center space-x-3 text-cpsu-green">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-12 w-12 object-contain">
            <div>
              <h1 class="text-xl font-heading font-bold">CPSU Health Assistant</h1>
              <p class="text-xs text-gray-600">Data Security</p>
            </div>
          </router-link>
          <router-link to="/" class="text-cpsu-green hover:underline font-medium">← Back to Home</router-link>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-12 max-w-4xl">
      <h2 class="text-3xl font-heading font-bold text-cpsu-green mb-8">Data Security</h2>
      <p class="text-sm text-gray-500 mb-8">How we protect your health information</p>

      <div class="prose prose-lg max-w-none space-y-6 text-gray-700">
        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">1. Encryption</h3>
          <p>All data transmitted between your device and our servers uses HTTPS (TLS/SSL) encryption. Passwords are hashed and never stored in plain text.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">2. Access Controls</h3>
          <p>Access to health data is restricted by role:</p>
          <ul class="list-disc pl-6 space-y-2 mt-2">
            <li><strong>Students:</strong> Can view and manage only their own records</li>
            <li><strong>Clinic Staff:</strong> Can view student health records needed for care</li>
            <li><strong>Administrators:</strong> Limited to user management and system monitoring</li>
          </ul>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">3. Audit Logging</h3>
          <p>We maintain audit logs of sensitive actions, including data access, modifications, and login attempts. This helps detect and investigate any unauthorized activity.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">4. Data Storage</h3>
          <p>Health records are stored in a secure database with restricted access. Medical data is intentionally excluded from the standard admin panel to minimize exposure.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">5. AI & Third-Party Services</h3>
          <p>When we use AI providers (e.g., Cohere, Groq) for symptom analysis, we send only the minimum necessary data. We do not share identifiable health information with third parties for marketing.</p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">6. Your Role</h3>
          <p>You can help protect your data by:</p>
          <ul class="list-disc pl-6 space-y-2 mt-2">
            <li>Keeping your password private and changing it if compromised</li>
            <li>Logging out when using shared devices</li>
            <li>Reporting any suspicious activity to the IT department</li>
          </ul>
        </section>

        <section>
          <h3 class="text-xl font-bold text-gray-900 mb-3">7. Questions</h3>
          <p>For security concerns, contact the CPSU IT department or clinic@cpsu.edu.ph.</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
