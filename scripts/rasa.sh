#!/bin/bash
# ==========================================
# CPSU Rasa Management Script
# ==========================================
# Usage: ./scripts/rasa.sh [command]
# Commands: action, main, train, shell, all

# Get project root (parent of scripts folder)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RASA_DIR="$PROJECT_ROOT/Rasa"
PYTHON="$PROJECT_ROOT/venv/Scripts/python.exe"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  CPSU Rasa Management Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if venv exists
if [ ! -f "$PYTHON" ]; then
    echo -e "${RED}ERROR: Virtual environment not found!${NC}"
    echo "Expected: $PYTHON"
    echo "Run: python -m venv venv && pip install -r requirements.txt"
    exit 1
fi

# Check if Rasa directory exists
if [ ! -d "$RASA_DIR" ]; then
    echo -e "${RED}ERROR: Rasa directory not found!${NC}"
    exit 1
fi

cd "$RASA_DIR"

show_help() {
    echo "Usage: ./scripts/rasa.sh [command]"
    echo ""
    echo "Commands:"
    echo "  action  - Start Rasa action server (port 5055)"
    echo "  main    - Start Rasa main server (port 5005)"
    echo "  train   - Train Rasa model"
    echo "  shell   - Interactive Rasa shell for testing"
    echo "  all     - Start both action and main servers"
    echo "  status  - Check if servers are running"
    echo "  help    - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/rasa.sh action   # Start action server"
    echo "  ./scripts/rasa.sh train    # Train new model"
    echo "  ./scripts/rasa.sh all      # Start both servers"
}

start_action() {
    echo -e "${BLUE}Starting Rasa Action Server...${NC}"
    echo "Port: 5055"
    echo ""
    "$PYTHON" -m rasa run actions
}

start_main() {
    echo -e "${BLUE}Starting Rasa Main Server...${NC}"
    echo "Port: 5005"
    echo ""
    
    # Find latest model
    LATEST_MODEL=$(ls -t models/*.tar.gz 2>/dev/null | head -1)
    
    if [ -z "$LATEST_MODEL" ]; then
        echo -e "${YELLOW}WARNING: No trained model found!${NC}"
        echo "Run: ./scripts/rasa.sh train"
        exit 1
    fi
    
    echo "Model: $LATEST_MODEL"
    echo ""
    "$PYTHON" -m rasa run --model "$LATEST_MODEL" --enable-api --cors "*" --port 5005
}

train_model() {
    echo -e "${BLUE}Training Rasa Model...${NC}"
    echo "This may take a few minutes..."
    echo ""
    "$PYTHON" -m rasa train
}

start_shell() {
    echo -e "${BLUE}Starting Rasa Shell...${NC}"
    echo "Type your messages to test the bot."
    echo "Type '/stop' to exit."
    echo ""
    "$PYTHON" -m rasa shell
}

check_status() {
    echo -e "${BLUE}Checking server status...${NC}"
    echo ""
    
    # Check action server
    if curl -s http://localhost:5055 > /dev/null 2>&1; then
        echo -e "Action Server (5055): ${GREEN}RUNNING${NC}"
    else
        echo -e "Action Server (5055): ${RED}NOT RUNNING${NC}"
    fi
    
    # Check main server
    if curl -s http://localhost:5005 > /dev/null 2>&1; then
        echo -e "Main Server (5005):   ${GREEN}RUNNING${NC}"
    else
        echo -e "Main Server (5005):   ${RED}NOT RUNNING${NC}"
    fi
    
    echo ""
    
    # List models
    echo "Trained models:"
    ls -lt models/*.tar.gz 2>/dev/null | head -3 || echo "  (none found)"
}

start_all() {
    echo -e "${BLUE}Starting both servers...${NC}"
    echo ""
    echo -e "${YELLOW}NOTE: This will start action server in background${NC}"
    echo ""
    
    # Start action server in background
    "$PYTHON" -m rasa run actions &
    ACTION_PID=$!
    echo "Action server started (PID: $ACTION_PID)"
    
    # Wait a moment for action server to start
    sleep 3
    
    # Start main server (foreground)
    start_main
}

# Parse command
case "${1:-help}" in
    action)
        start_action
        ;;
    main)
        start_main
        ;;
    train)
        train_model
        ;;
    shell|test)
        start_shell
        ;;
    all)
        start_all
        ;;
    status)
        check_status
        ;;
    help|--help|-h|*)
        show_help
        ;;
esac

