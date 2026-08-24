#!/bin/bash
#!/data/data/com.termux/files/usr/bin/bash
# ==========================================
# 🤖 INSTAGRAM BOT — SAFE TERMUX LAUNCHER
# ==========================================
# Default: ek hi attempt. Crash par automatic login retry nahi.
# Optional: AUTO_RESTART=1 bash instagram-ai-bot/start.sh
# Stop: Ctrl+C
# ==========================================

set -u
cd "$(dirname "$0")/.."

if [ "${AUTO_RESTART:-0}" != "1" ]; then
    echo "🤖 Instagram Bot — single test run"
    echo "   Crash/login error par automatic retry nahi hoga."
    exec python instagram-ai-bot/run_bot.py
fi

echo "🤖 Instagram Bot — manual restart mode"
while true; do
    python instagram-ai-bot/run_bot.py
    exit_code=$?
    if [ "$exit_code" -eq 0 ]; then
        echo "🛑 Bot stopped."
        exit 0
    fi
    echo "⚠️ Bot failed. 5 minutes wait; Ctrl+C se band karo."
    sleep 300
done
