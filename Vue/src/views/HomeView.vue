<template>
  <div class="min-h-screen bg-white">
    <!-- Sticky Navigation Bar -->
    <nav class="sticky top-0 z-50 bg-white shadow-md">
      <div class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-3">
            <img src="@/assets/images/cpsu-logo.png" alt="CPSU Logo" class="h-14 w-14 object-contain">
            <div>
              <h1 class="text-xl font-heading font-bold text-cpsu-green">CPSU Health Assistant</h1>
              <p class="text-xs text-gray-600">Central Philippines State University</p>
            </div>
          </div>
          
          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-8">
            <a @click="scrollToSection('home')" class="nav-link cursor-pointer">Home</a>
            <a @click="scrollToSection('about')" class="nav-link cursor-pointer">About</a>
            <a @click="scrollToSection('features')" class="nav-link cursor-pointer">Features</a>
            <a @click="scrollToSection('walkthrough')" class="nav-link cursor-pointer">How It Works</a>
            <a @click="scrollToSection('contact')" class="nav-link cursor-pointer">Contact</a>
          </div>

          <div class="hidden md:flex space-x-3">
            <router-link to="/login" class="text-cpsu-green font-semibold px-5 py-2 rounded-lg hover:bg-gray-100 transition-colors">
              Login
            </router-link>
            <router-link to="/register" class="bg-cpsu-green text-white font-semibold px-5 py-2 rounded-lg hover:bg-cpsu-green-dark transition-colors">
              Register
            </router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden text-cpsu-green">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile Menu -->
        <div v-if="mobileMenuOpen" class="md:hidden mt-4 pb-4 border-t border-gray-200">
          <div class="flex flex-col space-y-3 mt-4">
            <a @click="scrollToSection('home'); mobileMenuOpen = false" class="nav-link cursor-pointer">Home</a>
            <a @click="scrollToSection('about'); mobileMenuOpen = false" class="nav-link cursor-pointer">About</a>
            <a @click="scrollToSection('features'); mobileMenuOpen = false" class="nav-link cursor-pointer">Features</a>
            <a @click="scrollToSection('walkthrough'); mobileMenuOpen = false" class="nav-link cursor-pointer">How It Works</a>
            <a @click="scrollToSection('contact'); mobileMenuOpen = false" class="nav-link cursor-pointer">Contact</a>
            <router-link to="/login" class="btn-outline !border-cpsu-green !text-cpsu-green text-center">Login</router-link>
            <router-link to="/register" class="bg-cpsu-green text-white font-semibold px-5 py-2.5 rounded-lg text-center hover:bg-cpsu-green-dark transition-colors">Register</router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="bg-gradient-to-br from-cpsu-green to-cpsu-green-dark text-white py-20 md:py-32">
      <div class="container mx-auto px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-4xl md:text-6xl font-heading font-bold mb-6 animate-fade-in">
            Your AI-Powered Health Companion
          </h2>
          <p class="text-lg md:text-xl mb-8 text-gray-100">
            Get instant health insights with <span class="text-cpsu-yellow font-bold">90-98% accuracy</span> using our hybrid ML + LLM prediction system
          </p>
          
          <div class="flex flex-col sm:flex-row justify-center gap-4 mb-12">
            <router-link to="/register" class="bg-cpsu-yellow text-cpsu-green font-bold text-lg px-10 py-4 rounded-lg hover:bg-cpsu-yellow-dark transition-all transform hover:scale-105 shadow-lg">
              Get Started Free
            </router-link>
            <button @click="scrollToSection('walkthrough')" class="btn-outline text-lg px-10 py-4 !text-white !border-white hover:!bg-white hover:!text-cpsu-green">
              See How It Works
            </button>
          </div>

          <!-- Quick Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16">
            <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div class="text-3xl font-bold text-cpsu-yellow">132+</div>
              <div class="text-sm text-gray-200">Symptoms Tracked</div>
            </div>
            <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div class="text-3xl font-bold text-cpsu-yellow">41</div>
              <div class="text-sm text-gray-200">Disease Conditions</div>
            </div>
            <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div class="text-3xl font-bold text-cpsu-yellow">98%</div>
              <div class="text-sm text-gray-200">Accuracy Rate</div>
            </div>
            <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div class="text-3xl font-bold text-cpsu-yellow">24/7</div>
              <div class="text-sm text-gray-200">Availability</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-20 bg-gray-50">
      <div class="container mx-auto px-6">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-4xl font-heading font-bold text-cpsu-green text-center mb-12">About CPSU Health Assistant</h2>
          
          <div class="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 class="text-2xl font-bold text-gray-800 mb-4">Empowering CPSU Students with Smart Healthcare</h3>
              <p class="text-gray-600 mb-4">
                The CPSU Virtual Health Assistant is a cutting-edge AI-powered platform designed specifically for Central Philippines State University students. Our mission is to provide accessible, accurate, and instant health insights to the Mighty Hornbills community.
              </p>
              <p class="text-gray-600 mb-4">
                Built with hybrid machine learning and large language model technology, we combine the speed of traditional ML predictions with the intelligence of modern AI to deliver unparalleled accuracy in health assessments.
              </p>
              <div class="flex items-center space-x-2 text-cpsu-green font-semibold">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span>Free for all CPSU students</span>
              </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-8">
              <h4 class="text-xl font-bold text-cpsu-green mb-4">Our Values</h4>
              <ul class="space-y-3">
                <li class="flex items-start">
                  <span class="text-cpsu-yellow mr-2">✓</span>
                  <span class="text-gray-700"><strong>Accessibility:</strong> Healthcare for every student</span>
                </li>
                <li class="flex items-start">
                  <span class="text-cpsu-yellow mr-2">✓</span>
                  <span class="text-gray-700"><strong>Accuracy:</strong> Evidence-based predictions</span>
                </li>
                <li class="flex items-start">
                  <span class="text-cpsu-yellow mr-2">✓</span>
                  <span class="text-gray-700"><strong>Privacy:</strong> Your health data is secure</span>
                </li>
                <li class="flex items-start">
                  <span class="text-cpsu-yellow mr-2">✓</span>
                  <span class="text-gray-700"><strong>Innovation:</strong> Cutting-edge AI technology</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-white">
      <div class="container mx-auto px-6">
        <div class="max-w-6xl mx-auto">
          <h2 class="text-4xl font-heading font-bold text-cpsu-green text-center mb-4">Powerful Features</h2>
          <p class="text-gray-600 text-center mb-12 max-w-2xl mx-auto">
            Everything you need to monitor and manage your health, all in one intelligent platform
          </p>
          
          <div class="grid md:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div class="feature-card group">
              <div class="text-5xl mb-4 transform group-hover:scale-110 transition-transform">🤖</div>
              <h3 class="text-xl font-bold text-gray-800 mb-3">Hybrid AI Prediction</h3>
              <p class="text-gray-600 mb-4">
                Our unique system combines machine learning with large language models to achieve 90-98% accuracy in disease prediction.
              </p>
              <ul class="text-sm text-gray-500 space-y-1">
                <li>• Fast ML predictions (&lt;100ms)</li>
                <li>• LLM validation for accuracy</li>
                <li>• Multi-provider fallback system</li>
              </ul>
            </div>

            <!-- Feature 2 -->
            <div class="feature-card group">
              <div class="text-5xl mb-4 transform group-hover:scale-110 transition-transform">💬</div>
              <h3 class="text-xl font-bold text-gray-800 mb-3">Intelligent Chatbot</h3>
              <p class="text-gray-600 mb-4">
                Chat naturally with our Rasa-powered AI assistant. Get answers to health questions instantly.
              </p>
              <ul class="text-sm text-gray-500 space-y-1">
                <li>• 132+ symptom recognition</li>
                <li>• Natural language understanding</li>
                <li>• Emergency detection & alerts</li>
              </ul>
            </div>

            <!-- Feature 3 -->
            <div class="feature-card group">
              <div class="text-5xl mb-4 transform group-hover:scale-110 transition-transform">🔍</div>
              <h3 class="text-xl font-bold text-gray-800 mb-3">Symptom Checker</h3>
              <p class="text-gray-600 mb-4">
                Interactive symptom selection tool that helps you describe what you're experiencing accurately.
              </p>
              <ul class="text-sm text-gray-500 space-y-1">
                <li>• Step-by-step guidance</li>
                <li>• Search & filter symptoms</li>
                <li>• Instant analysis results</li>
              </ul>
            </div>

            <!-- Feature 4 -->
            <div class="feature-card group">
              <div class="text-5xl mb-4 transform group-hover:scale-110 transition-transform">📊</div>
              <h3 class="text-xl font-bold text-gray-800 mb-3">Health History</h3>
              <p class="text-gray-600 mb-4">
                Track all your health consultations and see trends in your symptoms over time.
              </p>
              <ul class="text-sm text-gray-500 space-y-1">
                <li>• Complete consultation records</li>
                <li>• Search & filter history</li>
                <li>• Export your data anytime</li>
              </ul>
            </div>

            <!-- Feature 5 -->
            <div class="feature-card group">
              <div class="text-5xl mb-4 transform group-hover:scale-110 transition-transform">🚨</div>
              <h3 class="text-xl font-bold text-gray-800 mb-3">Emergency SOS</h3>
              <p class="text-gray-600 mb-4">
                One-tap emergency alert system that notifies clinic staff immediately when you need urgent help.
              </p>
              <ul class="text-sm text-gray-500 space-y-1">
                <li>• GPS location tracking</li>
                <li>• Instant staff notification</li>
                <li>• Quick response prioritization</li>
              </ul>
            </div>

            <!-- Feature 6 -->
            <div class="feature-card group">
              <div class="text-5xl mb-4 transform group-hover:scale-110 transition-transform">💊</div>
              <h3 class="text-xl font-bold text-gray-800 mb-3">Medication Tracking</h3>
              <p class="text-gray-600 mb-4">
                Manage prescriptions, set reminders, and track medication adherence effortlessly.
              </p>
              <ul class="text-sm text-gray-500 space-y-1">
                <li>• Smart reminders</li>
                <li>• Adherence monitoring</li>
                <li>• Staff-prescribed medications</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works / Walkthrough Section -->
    <section id="walkthrough" class="py-20 bg-gradient-to-br from-cpsu-green/5 to-cpsu-yellow/5">
      <div class="container mx-auto px-6">
        <div class="max-w-5xl mx-auto">
          <h2 class="text-4xl font-heading font-bold text-cpsu-green text-center mb-4">How It Works</h2>
          <p class="text-gray-600 text-center mb-16 max-w-2xl mx-auto">
            Get started in 3 simple steps and access AI-powered health insights instantly
          </p>
          
          <!-- Walkthrough Steps -->
          <div class="space-y-12">
            <!-- Step 1 -->
            <div class="flex flex-col md:flex-row items-center gap-8">
              <div class="md:w-1/2">
                <div class="flex items-center mb-4">
                  <div class="bg-cpsu-green text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mr-4">1</div>
                  <h3 class="text-2xl font-bold text-gray-800">Create Your Account</h3>
                </div>
                <p class="text-gray-600 mb-4">
                  Register using your CPSU school ID. Your account is secure, and your health data is kept private and confidential.
                </p>
                <ul class="text-gray-600 space-y-2">
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Enter your school ID and create a password
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Verify your student status
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Complete your profile with basic information
                  </li>
                </ul>
              </div>
              <div class="md:w-1/2">
                <div class="bg-white rounded-lg shadow-xl p-8 border-2 border-cpsu-green/20">
                  <div class="text-6xl text-center mb-4">📝</div>
                  <div class="space-y-3">
                    <div class="bg-gray-100 rounded p-3">
                      <div class="text-xs text-gray-500 mb-1">School ID</div>
                      <div class="bg-white rounded px-3 py-2 text-gray-400">2024-XXXXX</div>
                    </div>
                    <div class="bg-gray-100 rounded p-3">
                      <div class="text-xs text-gray-500 mb-1">Password</div>
                      <div class="bg-white rounded px-3 py-2 text-gray-400">••••••••</div>
                    </div>
                    <button class="w-full bg-cpsu-green text-white py-2 rounded-lg font-semibold">Sign Up</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="flex flex-col md:flex-row-reverse items-center gap-8">
              <div class="md:w-1/2">
                <div class="flex items-center mb-4">
                  <div class="bg-cpsu-green text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mr-4">2</div>
                  <h3 class="text-2xl font-bold text-gray-800">Describe Your Symptoms</h3>
                </div>
                <p class="text-gray-600 mb-4">
                  Choose your preferred method: use our interactive symptom checker or chat naturally with our AI assistant about how you're feeling.
                </p>
                <ul class="text-gray-600 space-y-2">
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Select from 132+ recognized symptoms
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Chat naturally with the AI assistant
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Add severity and duration details
                  </li>
                </ul>
              </div>
              <div class="md:w-1/2">
                <div class="bg-white rounded-lg shadow-xl p-6 border-2 border-cpsu-green/20">
                  <div class="text-4xl text-center mb-4">🔍</div>
                  <div class="space-y-3">
                    <div class="flex flex-wrap gap-2">
                      <span class="bg-cpsu-green text-white px-3 py-1 rounded-full text-sm">Fever</span>
                      <span class="bg-cpsu-green text-white px-3 py-1 rounded-full text-sm">Cough</span>
                      <span class="bg-cpsu-green text-white px-3 py-1 rounded-full text-sm">Fatigue</span>
                    </div>
                    <div class="bg-gray-50 rounded-lg p-4">
                      <div class="text-xs text-gray-500 mb-2">💬 Or chat with AI:</div>
                      <div class="bg-white rounded p-3 text-sm text-gray-600 italic">
                        "I have a headache and feel tired..."
                      </div>
                    </div>
                    <button class="w-full bg-cpsu-yellow text-cpsu-green py-2 rounded-lg font-semibold">Analyze Symptoms</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="flex flex-col md:flex-row items-center gap-8">
              <div class="md:w-1/2">
                <div class="flex items-center mb-4">
                  <div class="bg-cpsu-green text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mr-4">3</div>
                  <h3 class="text-2xl font-bold text-gray-800">Get Instant Health Insights</h3>
                </div>
                <p class="text-gray-600 mb-4">
                  Receive AI-powered predictions with 90-98% accuracy, complete with health recommendations, precautions, and next steps.
                </p>
                <ul class="text-gray-600 space-y-2">
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    View predicted conditions with confidence scores
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Get personalized health precautions
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Track your consultation history
                  </li>
                  <li class="flex items-center">
                    <span class="text-cpsu-yellow mr-2">→</span>
                    Request clinic follow-up if needed
                  </li>
                </ul>
              </div>
              <div class="md:w-1/2">
                <div class="bg-white rounded-lg shadow-xl p-6 border-2 border-cpsu-green/20">
                  <div class="text-4xl text-center mb-4">✅</div>
                  <div class="bg-gradient-to-br from-cpsu-green/10 to-cpsu-yellow/10 rounded-lg p-4 mb-3">
                    <div class="text-xs text-gray-500 mb-1">Prediction Result</div>
                    <div class="text-lg font-bold text-cpsu-green">Common Cold</div>
                    <div class="text-sm text-gray-600 mt-1">Confidence: 94%</div>
                  </div>
                  <div class="bg-gray-50 rounded-lg p-3 mb-3">
                    <div class="text-xs font-semibold text-gray-700 mb-2">Precautions:</div>
                    <ul class="text-xs text-gray-600 space-y-1">
                      <li>✓ Get adequate rest</li>
                      <li>✓ Stay hydrated</li>
                      <li>✓ Avoid cold environments</li>
                    </ul>
                  </div>
                  <button class="w-full bg-cpsu-green text-white py-2 rounded-lg text-sm font-semibold">View Full Report</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Additional Info -->
          <div class="mt-16 bg-white rounded-lg shadow-lg p-8 border-l-4 border-cpsu-yellow">
            <h4 class="text-xl font-bold text-gray-800 mb-3">🎯 What Happens Next?</h4>
            <div class="grid md:grid-cols-2 gap-4 text-gray-600">
              <div>
                <strong class="text-cpsu-green">Track Your Health:</strong> All consultations are saved in your history for future reference.
              </div>
              <div>
                <strong class="text-cpsu-green">Get Medications:</strong> Clinic staff can prescribe medications directly through the system.
              </div>
              <div>
                <strong class="text-cpsu-green">Emergency Support:</strong> Use the SOS button for immediate assistance from clinic staff.
              </div>
              <div>
                <strong class="text-cpsu-green">Follow-ups:</strong> Receive notifications for scheduled follow-up appointments.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Technology Section -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl font-heading font-bold text-cpsu-green mb-4">Powered by Advanced AI Technology</h2>
          <p class="text-gray-600 mb-12">
            Our system combines multiple cutting-edge technologies to deliver the most accurate health predictions
          </p>
          
          <div class="grid md:grid-cols-4 gap-6">
            <div class="tech-badge">
              <div class="text-3xl mb-2">🧠</div>
              <div class="font-semibold text-gray-800">Machine Learning</div>
              <div class="text-xs text-gray-500">scikit-learn</div>
            </div>
            <div class="tech-badge">
              <div class="text-3xl mb-2">🤖</div>
              <div class="font-semibold text-gray-800">Large Language Models</div>
              <div class="text-xs text-gray-500">Gemini, Groq, Cohere</div>
            </div>
            <div class="tech-badge">
              <div class="text-3xl mb-2">💬</div>
              <div class="font-semibold text-gray-800">Rasa Framework</div>
              <div class="text-xs text-gray-500">NLU Chatbot</div>
            </div>
            <div class="tech-badge">
              <div class="text-3xl mb-2">⚡</div>
              <div class="font-semibold text-gray-800">Real-time Processing</div>
              <div class="text-xs text-gray-500">&lt;100ms response</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Meet the Team Section -->
    <section class="py-20 bg-gradient-to-br from-cpsu-green/5 to-cpsu-yellow/5">
      <div class="container mx-auto px-6">
        <div class="max-w-6xl mx-auto">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-heading font-bold text-cpsu-green mb-4">Meet the Development Team</h2>
            <p class="text-gray-600 max-w-2xl mx-auto mb-2">
              This project is a thesis work developed by dedicated Computer Science students from Central Philippines State University
            </p>
            <div class="inline-block bg-cpsu-yellow/20 border-2 border-cpsu-yellow rounded-lg px-6 py-3 mt-4">
              <p class="text-cpsu-green font-bold text-lg">🎓 Thesis Project 2025-2026</p>
              <p class="text-sm text-gray-700">Bachelor of Science in Information Technology</p>
            </div>
          </div>

         <!-- Team Members Grid -->
          <div class="grid md:grid-cols-2 gap-8 mb-12">
            <!-- Team Member 1 - You can customize these -->
            <div class="team-card">
              <div class="w-24 h-24 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold">
                👨‍💻
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-1">Eugene Pausa</h3>
              <p class="text-cpsu-green font-semibold mb-2">Member</p>
            </div>

            <!-- Team Member 2 -->
            <div class="team-card">
              <div class="w-24 h-24 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold">
                👨‍💻
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-1">Charry Jane Cuenca</h3>
              <p class="text-cpsu-green font-semibold mb-2">Member</p>
            </div>

            <!-- Team Member 3 -->
            <div class="team-card">
              <div class="w-24 h-24 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold">
                👨‍💻
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-1">Jonel Roy Talapiero</h3>
              <p class="text-cpsu-green font-semibold mb-2">Member</p>
            </div>

            <!-- Add more team members as needed -->
            <div class="team-card">
              <div class="w-24 h-24 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold">
                👩‍💻
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-1">Rodelyn Sumagaysay</h3>
              <p class="text-cpsu-green font-semibold mb-2">Members</p>
            </div>
          </div>

          <!-- Thesis Advisors -->
          <div class="bg-white rounded-lg shadow-lg p-8 border-l-4 border-cpsu-green">
            <h3 class="text-2xl font-bold text-cpsu-green mb-6 text-center">Thesis Advisors & Acknowledgments</h3>
            <div class="grid md:grid-cols-2 gap-6">
              <div class="text-center">
                <div class="w-20 h-20 bg-cpsu-yellow rounded-full mx-auto mb-3 flex items-center justify-center text-cpsu-green text-2xl font-bold">
                  👨‍🏫
                </div>
                <h4 class="font-bold text-gray-800">JUFEL M. CASTULO</h4>
                <p class="text-sm text-gray-600">Thesis Advisor</p>
                <p class="text-xs text-gray-500 mt-2">Computer Studies Department</p>
              </div>
              <div class="text-center">
                <div class="w-20 h-20 bg-cpsu-yellow rounded-full mx-auto mb-3 flex items-center justify-center text-cpsu-green text-2xl font-bold">
                  👨‍⚕️
                </div>
                <h4 class="font-bold text-gray-800">KRISTINE C. DURAN, RN, MAN</h4>
                <p class="text-sm text-gray-600">University Clinic Head</p>
                <p class="text-xs text-gray-500 mt-2">CPSU Health Services</p>
              </div>
            </div>
            <div class="mt-6 pt-6 border-t border-gray-200 text-center text-gray-600">
              <p class="text-sm italic">
                Special thanks to the CPSU Clinic staff, faculty members, and all students who participated in testing and providing valuable feedback for this project.
              </p>
            </div>
          </div>

          <!-- Project Info -->
          <div class="mt-8 grid md:grid-cols-3 gap-6">
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-3xl mb-2">📚</div>
              <h4 class="font-bold text-gray-800 mb-2">Academic Year</h4>
              <p class="text-cpsu-green font-semibold">2025-2026</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-3xl mb-2">🏫</div>
              <h4 class="font-bold text-gray-800 mb-2">Department</h4>
              <p class="text-cpsu-green font-semibold">Computer Studies</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
              <div class="text-3xl mb-2">🎯</div>
              <h4 class="font-bold text-gray-800 mb-2">Project Type</h4>
              <p class="text-cpsu-green font-semibold">Undergraduate Thesis</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20 bg-gradient-to-br from-cpsu-green to-cpsu-green-dark text-white">
      <div class="container mx-auto px-6">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-4xl font-heading font-bold text-center mb-4">Get In Touch</h2>
          <p class="text-gray-100 text-center mb-12">
            Have questions? Need support? We're here to help the CPSU community
          </p>
          
          <div class="grid md:grid-cols-2 gap-8">
            <!-- Contact Info -->
            <div class="space-y-6">
              <div class="flex items-start space-x-4">
                <div class="bg-cpsu-yellow text-cpsu-green rounded-full p-3 flex-shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-bold mb-1">Location</h4>
                  <p class="text-gray-200">Central Philippines State University<br>Kabankalan City, Negros Occidental</p>
                </div>
              </div>

              <div class="flex items-start space-x-4">
                <div class="bg-cpsu-yellow text-cpsu-green rounded-full p-3 flex-shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-bold mb-1">Email</h4>
                  <p class="text-gray-200">clinic@cpsu.edu.ph<br>health.assistant@cpsu.edu.ph</p>
                </div>
              </div>

              <div class="flex items-start space-x-4">
                <div class="bg-cpsu-yellow text-cpsu-green rounded-full p-3 flex-shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-bold mb-1">Clinic Hours</h4>
                  <p class="text-gray-200">Monday - Friday: 8:00 AM - 5:00 PM<br>Emergency SOS: 24/7</p>
                </div>
              </div>

              <div class="flex items-start space-x-4">
                <div class="bg-cpsu-yellow text-cpsu-green rounded-full p-3 flex-shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-bold mb-1">Emergency</h4>
                  <p class="text-gray-200">Hotline: (034) XXX-XXXX<br>Use in-app SOS for GPS-tracked alerts</p>
                </div>
              </div>
            </div>

            <!-- Quick Links & Support -->
            <div class="bg-white/10 backdrop-blur-sm rounded-lg p-6">
              <h3 class="text-xl font-bold mb-4">Quick Links</h3>
              <div class="space-y-3 mb-6">
                <router-link to="/privacy-policy" class="block text-cpsu-yellow hover:underline">Privacy Policy</router-link>
                <router-link to="/terms-of-service" class="block text-cpsu-yellow hover:underline">Terms of Service</router-link>
                <router-link to="/data-security" class="block text-cpsu-yellow hover:underline">Data Security</router-link>
                <router-link to="/faqs" class="block text-cpsu-yellow hover:underline">FAQs</router-link>
                <router-link to="/user-guide" class="block text-cpsu-yellow hover:underline">User Guide</router-link>
              </div>
              
              <h3 class="text-xl font-bold mb-4">Support</h3>
              <p class="text-gray-200 mb-4">
                For technical support or questions about the system, please contact the CPSU Clinic or IT department.
              </p>
              <router-link to="/register" class="inline-block bg-cpsu-yellow text-cpsu-green font-bold px-6 py-3 rounded-lg hover:bg-cpsu-yellow-dark transition-colors">
                Get Started Now →
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 py-8">
      <div class="container mx-auto px-6">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <p>&copy; 2025 CPSU Health Assistant. All rights reserved.</p>
            <p class="text-sm">Built with ❤️ for the Central Philippines State University</p>
          </div>
          <div class="flex flex-wrap justify-center gap-4 md:gap-6">
            <router-link to="/privacy-policy" class="hover:text-cpsu-yellow transition-colors">Privacy Policy</router-link>
            <router-link to="/terms-of-service" class="hover:text-cpsu-yellow transition-colors">Terms of Service</router-link>
            <router-link to="/data-security" class="hover:text-cpsu-yellow transition-colors">Data Security</router-link>
            <router-link to="/faqs" class="hover:text-cpsu-yellow transition-colors">FAQs</router-link>
            <router-link to="/user-guide" class="hover:text-cpsu-yellow transition-colors">User Guide</router-link>
            <a href="#" class="hover:text-cpsu-yellow transition-colors">Facebook</a>
            <a href="#" class="hover:text-cpsu-yellow transition-colors">Twitter</a>
            <a href="#" class="hover:text-cpsu-yellow transition-colors">Instagram</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const mobileMenuOpen = ref(false)

const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<style scoped>
.nav-link {
  @apply text-gray-700 hover:text-cpsu-green font-medium transition-colors;
}

.feature-card {
  @apply bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-cpsu-green/30;
}

.tech-badge {
  @apply bg-gray-50 rounded-lg p-4 hover:bg-cpsu-green/5 transition-colors;
}

.team-card {
  @apply bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-cpsu-green/30 hover:-translate-y-1;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out;
}
</style>
