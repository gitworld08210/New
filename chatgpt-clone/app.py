# ============================================================
# 🚀 MyAI Backend — Flask Server + Ollama Integration
# ============================================================
# Yeh tumhare trained model ko website se connect karta hai
# 
# Run: python app.py
# Open: http://localhost:5000
# ============================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import time
import random
import os

app = Flask(__name__)
CORS(app)

# ===== CONFIGURATION =====

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mybot")  # Tumhara trained model
FALLBACK_MODEL = "llama3.2:1b"  # Agar mybot load nahi hua toh

# System prompt — Tumhare bot ki personality
SYSTEM_PROMPT = """Tu ek friendly, caring aur fun dost hai. Tu Hinglish (Hindi + English mix) mein baat karta hai. 
Tu hamesha caring, supportive aur entertaining hai. Tu emojis use karta hai. 
Tu short aur natural replies deta hai (1-3 lines max). Tu har baar thoda alag reply deta hai.
Tu kabhi boring generic reply nahi deta. Tu real insaan jaisa feel deta hai."""

# Chat history per session (in-memory)
chat_sessions = {}

# Keyword fallback (agar Ollama unavailable ho)
KEYWORD_RESPONSES = {
    "hi": ["Hey! Kya haal hai? 😊", "Hello! Bata kya scene hai?", "Hii! Sab theek? 😄"],
    "hello": ["Hello! Kaise ho? 😊", "Hey there! Kya chal raha?", "Hi! Bata kya kar rahe?"],
    "hey": ["Hey! Sab badhiya? 😄", "Heyy! Kya haal hai?", "Hey! Bata kya scene hai?"],
    "kaise ho": ["Main mast hoon! Tu bata? 😊", "Bilkul badhiya! Tera kya haal?", "Sab accha hai bhai! Tu suna?"],
    "how are you": ["I'm great! What about you? 😄", "Doing good! You tell?", "All good here! How's you?"],
    "kya kar rahe": ["Bas chill kar raha tha! Tu bata? 😄", "Kuch nahi yaar, timepass. Tu kya kar raha?", "Tere liye wait kar raha tha! 😊"],
    "bore ho raha": ["Chal kuch fun karte hain! 🎮", "Game khele? Ya memes share kare? 😂", "Mere saath baat kar, bore nahi hoga! 😄"],
    "sad": ["Kya hua? Bata mujhe, main hoon na ❤️", "Hey, it's okay. Main sun raha hoon 🤗", "Tension mat le, sab theek hoga 💪"],
    "happy": ["Yay! Kya baat hai! Bata kya hua? 🎉", "That's amazing! Share kar na! 😊", "Mujhe bhi khushi hui! 🥳"],
    "good morning": ["Good morning! ☀️ Aaj ka din accha jaaye!", "Morning! Chai pi? ☕😊", "GM! Aaj kya plan hai? 🌞"],
    "good night": ["Good night! 🌙 Sweet dreams!", "Nighty night! Kal milte hain! 😴", "So ja yaar! Good night! 💤"],
    "joke": ["Teacher: Late kyu aaye? Student: Aapne kaha jaldi mat aana 😂", "Google se pucha 'how to be happy' — Result: Delete social media 😂😂", "Doctor: Kya problem? Patient: Log mujhe seriously nahi lete 😂"],
    "thank": ["Koi baat nahi! Dost hain! 🤝", "Arre thanks ki zarurat nahi! 😊", "Always welcome! ❤️"],
    "bye": ["Bye! Take care! 👋😊", "Bye bye! Jaldi baat karna! ❤️", "Chal phir! Milte hain! 👋"],
    "love": ["Aww! That's sweet! 😊❤️", "You're special to me too! 💕", "Love you too! 🥰"],
    "movie": ["Genre bata! Action? Comedy? Romance? 🎬", "Pushpa 2 dekhi? Mast hai! 🔥", "Netflix pe 'Wednesday' try kar! 📺"],
    "song": ["Mood kya hai? Chill? Party? Sad? 🎵", "Arijit Singh ka naya gaana sun! 🎶", "Kaunsa genre pasand hai?"],
    "game": ["Chalo khelte hain! 🎮 Kaunsa game?", "BGMI? Free Fire? Ya word game? 🎯", "Main ready hoon! 💪"],
    "khana": ["Kya khaya? Mujhe bhi bhookh lagi! 🍕", "Biryani ka mood hai! 😋", "Aaj kya special banaya?"],
}

DEFAULT_RESPONSES = [
    "Hmm interesting! Aur batao? 😊",
    "Accha! Phir kya hua? 🤔",
    "Haha nice! 😄 Aur kya chal raha?",
    "Sahi hai yaar! Bata aur? 😊",
    "Ohh accha! Tell me more! 🤗",
    "Waah! Mast! Aur kya naya? 😄",
    "That's cool! Aur suna? 🙌",
    "Hmm samjha! Aur kuch? 🤔",
    "Nice bhai! Continue kar? 😊",
    "Interesting! Mujhe aur batao 😄",
]


# ===== HELPER FUNCTIONS =====

def get_ollama_response(message, chat_id):
    """Ollama model se reply generate karta hai."""
    try:
        # Get or create session history
        if chat_id not in chat_sessions:
            chat_sessions[chat_id] = []
        
        history = chat_sessions[chat_id][-10:]  # Last 10 messages for context
        
        # Build messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        # Try primary model first, then fallback
        for model in [MODEL_NAME, FALLBACK_MODEL]:
            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/chat",
                    json={
                        "model": model,
                        "messages": messages,
                        "stream": False,
                        "options": {
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "num_predict": 150,
                            "repeat_penalty": 1.2,
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    reply = response.json()["message"]["content"].strip()
                    
                    # Save to history
                    chat_sessions[chat_id].append({"role": "user", "content": message})
                    chat_sessions[chat_id].append({"role": "assistant", "content": reply})
                    
                    # Limit history size
                    if len(chat_sessions[chat_id]) > 30:
                        chat_sessions[chat_id] = chat_sessions[chat_id][-20:]
                    
                    return reply
            except:
                continue
        
        return None
        
    except Exception as e:
        print(f"Ollama error: {e}")
        return None


def get_keyword_response(message):
    """Keyword-based fallback response."""
    message_lower = message.lower().strip()
    
    for keyword, responses in KEYWORD_RESPONSES.items():
        if keyword in message_lower:
            return random.choice(responses)
    
    return random.choice(DEFAULT_RESPONSES)


def check_ollama_status():
    """Check if Ollama is running and model is available."""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = [m["name"] for m in response.json().get("models", [])]
            return {
                "status": "online",
                "models": models,
                "active_model": MODEL_NAME if MODEL_NAME in models else (FALLBACK_MODEL if FALLBACK_MODEL in models else None)
            }
    except:
        pass
    return {"status": "offline", "models": [], "active_model": None}


# ===== ROUTES =====

@app.route('/')
def index():
    """Main page serve karta hai."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat API — message receive karta hai, reply deta hai."""
    data = request.json
    message = data.get('message', '').strip()
    chat_id = data.get('chat_id', 'default')
    
    if not message:
        return jsonify({"error": "Empty message"}), 400
    
    # Try Ollama first
    reply = get_ollama_response(message, chat_id)
    
    # Fallback to keywords if Ollama fails
    if not reply:
        reply = get_keyword_response(message)
    
    return jsonify({
        "reply": reply,
        "chat_id": chat_id,
        "model": MODEL_NAME,
        "timestamp": int(time.time())
    })


@app.route('/api/status', methods=['GET'])
def status():
    """Server aur model ka status check karta hai."""
    ollama_info = check_ollama_status()
    return jsonify({
        "server": "online",
        "ollama": ollama_info,
        "model": MODEL_NAME,
        "fallback": "keyword-based"
    })


@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Chat history clear karta hai."""
    data = request.json
    chat_id = data.get('chat_id', 'default')
    
    if chat_id in chat_sessions:
        del chat_sessions[chat_id]
    
    return jsonify({"status": "cleared"})


# ===== START SERVER =====

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════╗
║           🤖 MyAI Server Starting            ║
╠══════════════════════════════════════════════╣
║                                              ║
║   URL:    http://localhost:5000               ║
║   Model:  {model:<30}     ║
║                                              ║
╚══════════════════════════════════════════════╝
""".format(model=MODEL_NAME))
    
    # Check Ollama status
    ollama_status = check_ollama_status()
    if ollama_status["status"] == "online":
        print(f"✅ Ollama: Connected")
        print(f"   Models: {', '.join(ollama_status['models'][:5])}")
        if ollama_status["active_model"]:
            print(f"   Active: {ollama_status['active_model']}")
        else:
            print(f"   ⚠️ Model '{MODEL_NAME}' not found. Using keyword fallback.")
            print(f"      Run: ollama pull {FALLBACK_MODEL}")
    else:
        print(f"⚠️ Ollama: Not running (using keyword fallback)")
        print(f"   Install: curl -fsSL https://ollama.com/install.sh | sh")
        print(f"   Start:   ollama serve")
    
    print(f"\n🌐 Open in browser: http://localhost:5000")
    print(f"   Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
