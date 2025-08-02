#!/bin/bash

# Whisper Killer Launcher Script
# Detects and closes any running instances before starting a new one

echo "🔍 Checking for running Whisper Killer instances..."

# Find any running Python processes with yap_gui.py
RUNNING_PIDS=$(pgrep -f "python.*yap_gui.py")

if [ ! -z "$RUNNING_PIDS" ]; then
    echo "⚠️  Found running instance(s): $RUNNING_PIDS"
    echo "🔄 Closing existing instance(s)..."
    
    # Kill the running processes
    for pid in $RUNNING_PIDS; do
        echo "   Stopping process $pid..."
        kill $pid 2>/dev/null
        
        # Wait a moment for graceful shutdown
        sleep 1
        
        # Force kill if still running
        if kill -0 $pid 2>/dev/null; then
            echo "   Force stopping process $pid..."
            kill -9 $pid 2>/dev/null
        fi
    done
    
    echo "✅ Existing instances closed"
    sleep 2
else
    echo "✅ No running instances found"
fi

echo "🚀 Starting Whisper Killer..."
echo ""

# Start the application
python3 yap_gui.py

# Check if the app started successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Whisper Killer started successfully"
else
    echo ""
    echo "❌ Failed to start Whisper Killer"
    exit 1
fi