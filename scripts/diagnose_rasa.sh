#!/bin/bash
# Diagnostic script for Rasa integration issues
# Run this to check if Rasa is properly configured

echo "🔍 CPSU Rasa Integration Diagnostic"
echo "======================================"
echo ""

# Check 1: Django server
echo "1. Checking Django server..."
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "   ✅ Django is running on http://localhost:8000"
else
    echo "   ❌ Django is NOT running"
    echo "      Start it: cd Django && python manage.py runserver"
fi
echo ""

# Check 2: Rasa server status
echo "2. Checking Rasa server status..."
if curl -s http://localhost:5005/status > /dev/null 2>&1; then
    echo "   ✅ Rasa server is running on http://localhost:5005"
    
    # Get model info
    MODEL_INFO=$(curl -s http://localhost:5005/status | python3 -m json.tool 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "   Server status:"
        echo "$MODEL_INFO" | grep -E "(model|version)" | sed 's/^/      /'
    fi
else
    echo "   ❌ Rasa server is NOT running"
    echo "      Start it: cd Rasa && bash start_server.sh"
fi
echo ""

# Check 3: Rasa action server
echo "3. Checking Rasa action server..."
if curl -s http://localhost:5055/health > /dev/null 2>&1; then
    echo "   ✅ Rasa action server is running on http://localhost:5055"
else
    echo "   ❌ Rasa action server is NOT running"
    echo "      Start it: cd Rasa && rasa run actions"
fi
echo ""

# Check 4: Trained models
echo "4. Checking for trained Rasa models..."
cd Rasa 2>/dev/null || { echo "   ❌ Rasa directory not found"; exit 1; }

if [ -d "models" ]; then
    MODEL_COUNT=$(ls -1 models/*.tar.gz 2>/dev/null | wc -l)
    if [ "$MODEL_COUNT" -gt 0 ]; then
        echo "   ✅ Found $MODEL_COUNT trained model(s)"
        LATEST=$(ls -t models/*.tar.gz 2>/dev/null | head -1)
        echo "      Latest: $(basename $LATEST)"
        echo "      Date: $(stat -c %y "$LATEST" 2>/dev/null | cut -d' ' -f1)"
    else
        echo "   ❌ No trained models found"
        echo "      Train a model: rasa train"
    fi
else
    echo "   ❌ models/ directory not found"
fi
echo ""

# Check 5: Test Rasa webhook
echo "5. Testing Rasa webhook..."
if curl -s http://localhost:5005/webhooks/rest/webhook > /dev/null 2>&1; then
    echo "   ✅ Rasa webhook endpoint is accessible"
    
    # Try sending a test message
    echo "   Testing with sample message..."
    RESPONSE=$(curl -s -X POST http://localhost:5005/webhooks/rest/webhook \
        -H "Content-Type: application/json" \
        -d '{"sender":"test","message":"hello"}')
    
    if echo "$RESPONSE" | grep -q "text"; then
        echo "   ✅ Rasa responded to test message"
        echo "      Response: $(echo "$RESPONSE" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d[0]["text"] if d else "empty")' 2>/dev/null)"
    elif [ -z "$RESPONSE" ] || [ "$RESPONSE" = "[]" ]; then
        echo "   ⚠️  Rasa returned empty response"
        echo "      This means: Agent is not loaded/trained"
        echo "      Fix: Stop Rasa, run 'rasa train', then start with 'bash start_server.sh'"
    else
        echo "   ⚠️  Unexpected response: $RESPONSE"
    fi
else
    echo "   ❌ Cannot reach Rasa webhook"
fi
echo ""

# Summary
echo "======================================"
echo "📋 Summary & Next Steps"
echo "======================================"
echo ""

# Determine what needs to be done
NEEDS_TRAINING=false
NEEDS_RASA_SERVER=false
NEEDS_ACTION_SERVER=false

if ! curl -s http://localhost:5005/status > /dev/null 2>&1; then
    NEEDS_RASA_SERVER=true
fi

if ! curl -s http://localhost:5055/health > /dev/null 2>&1; then
    NEEDS_ACTION_SERVER=true
fi

if [ "$MODEL_COUNT" -eq 0 ] 2>/dev/null || [ -z "$MODEL_COUNT" ]; then
    NEEDS_TRAINING=true
fi

if [ "$NEEDS_TRAINING" = true ]; then
    echo "⚠️  Rasa model needs training:"
    echo "   cd Rasa && rasa train"
    echo ""
fi

if [ "$NEEDS_RASA_SERVER" = true ]; then
    echo "⚠️  Start Rasa server:"
    echo "   cd Rasa && bash start_server.sh"
    echo "   (Or: rasa run --enable-api --cors \"*\")"
    echo ""
fi

if [ "$NEEDS_ACTION_SERVER" = true ]; then
    echo "⚠️  Start Rasa action server (in separate terminal):"
    echo "   cd Rasa && rasa run actions"
    echo ""
fi

if [ "$NEEDS_TRAINING" = false ] && [ "$NEEDS_RASA_SERVER" = false ] && [ "$NEEDS_ACTION_SERVER" = false ]; then
    echo "✅ Everything looks good!"
    echo ""
    echo "If you're still seeing empty responses:"
    echo "1. Check Rasa logs: tail -f Rasa/rasa_server.log"
    echo "2. Restart Rasa server: Ctrl+C, then bash start_server.sh"
    echo "3. Verify Django can connect: curl http://localhost:5005/status"
fi

echo ""
echo "======================================"
