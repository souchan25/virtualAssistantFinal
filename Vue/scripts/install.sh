#!/bin/bash
# Vue.js Frontend Installation Script for CPSU Health Assistant

echo "🏥 CPSU Health Assistant - Vue.js Frontend Setup"
echo "================================================"
echo ""

# Check if we're in the Vue directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found"
    echo "Please run this script from the Vue/ directory"
    exit 1
fi

echo "✅ Found package.json"
echo ""

# Check Node.js version
echo "🔍 Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version $NODE_VERSION detected"
    echo "Please upgrade to Node.js 18 or higher"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Check npm
echo "🔍 Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ npm $(npm -v) detected"
echo ""

# Check if Django backend is running
echo "🔍 Checking Django backend..."
if curl -s http://localhost:8000/api/ > /dev/null 2>&1; then
    echo "✅ Django backend is running on http://localhost:8000"
else
    echo "⚠️  Django backend is NOT running"
    echo "   Start it with: cd ../Django && python manage.py runserver"
    echo "   Continuing anyway..."
fi
echo ""

# Check .env file
echo "🔍 Checking .env file..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
    cat .env
else
    echo "❌ .env file not found"
    echo "Creating default .env file..."
    cat > .env << 'EOF'
# Django Backend API
VITE_API_BASE_URL=http://localhost:8000/api

# Rasa Chatbot (optional)
VITE_RASA_URL=http://localhost:5005

# App Configuration
VITE_APP_NAME=CPSU Health Assistant
VITE_APP_VERSION=1.0.0
EOF
    echo "✅ Created .env file"
fi
echo ""

# Install dependencies
echo "📦 Installing npm packages..."
echo "This may take a few minutes..."
echo ""

npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All packages installed successfully!"
else
    echo ""
    echo "❌ Package installation failed"
    exit 1
fi

echo ""
echo "================================================"
echo "🎉 Setup Complete!"
echo "================================================"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Start Django backend (if not running):"
echo "   cd ../Django && python manage.py runserver"
echo ""
echo "2. Start Vue.js development server:"
echo "   npm run dev"
echo ""
echo "3. Open browser:"
echo "   http://localhost:5173"
echo ""
echo "4. Register a test account and explore!"
echo ""
echo "📚 Documentation:"
echo "   - README.md     - Complete documentation"
echo "   - SETUP.md      - Setup guide"
echo "   - COMPLETE.md   - What's been built"
echo ""
echo "Happy coding! 🚀"
echo ""
