#!/bin/bash
# ==========================================
# 🤖 INSTAGRAM BOT — AUTO RESTART WRAPPER
# ==========================================
# Yeh script bot ko chalata hai.
# Agar crash ho toh 30 sec baad KHUD restart karta hai.
# Agar code update ho toh auto git pull karta hai.
#
# Usage: bash start.sh
# Stop: Ctrl+C do baar dabao
# ==========================================

cd "$(dirname "$0")/.."

echo "🤖 Instagram Bot Auto-Restart Mode"
echo "   Bot crash hoga toh 30 sec mein khud restart hoga"
echo "   Ctrl+C do baar = permanently band"
echo ""

while true; do
    echo "🔄 Starting bot..."
    git pull --quiet 2>/dev/null
    python instagram-ai-bot/run_bot.py
    
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "🛑 Bot manually stopped."
        break
    fi
    
    echo ""
    echo "⚠️ Bot crashed! Restarting in 30 seconds..."
    echo "   (Ctrl+C to stop permanently)"
    sleep 30
done
