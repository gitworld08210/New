# ============================================================
# 🤖 STEP 4: INSTAGRAM AUTO-REPLY BOT
# ============================================================
# Yeh script tumhare trained model ko Instagram se connect karta hai
# Auto-reply bot jo smart, varied replies deta hai
#
# ⚠️ WARNING: 
# - Sirf DUMMY/TEST account use karo, main account NAHI
# - Instagram automation se ban ho sakta hai
# - Yeh educational purpose ke liye hai
#
# Yeh script LOCAL computer pe run karo (Colab pe nahi)
# ============================================================

# ============ CELL 1: Install Dependencies ============
# Local machine pe run karo (not Colab)

# !pip install instagrapi Pillow requests

# Agar Ollama use kar rahe ho (recommended):
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull llama3.2:1b

# Agar trained model use kar rahe ho:
# ollama create mybot -f Modelfile

print("✅ Dependencies ready!")


# ============ CELL 2: Configuration ============

import os
import json
import time
import random
import re
from datetime import datetime, timedelta

# ===== YAHAN APNI DETAILS DALO =====

INSTAGRAM_USERNAME = "YOUR_USERNAME"      # Apna Instagram username
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"      # Apna Instagram password

# Model choice
USE_OLLAMA = True                          # True = Ollama (trained model), False = Keyword-based
OLLAMA_MODEL = "mybot"                     # Ollama model name (after ollama create)
OLLAMA_URL = "http://localhost:11434"       # Ollama server URL

# Bot settings
CHECK_INTERVAL = 30                        # Seconds mein - kitni baar check kare (30 = har 30 sec)
REPLY_DELAY_MIN = 3                        # Minimum delay before reply (seconds)
REPLY_DELAY_MAX = 15                       # Maximum delay before reply (natural lagega)
MAX_REPLIES_PER_HOUR = 20                  # Rate limit (ban se bachne ke liye)
IGNORED_USERS = []                         # In users ko reply mat karo ["user1", "user2"]
ONLY_REPLY_TO = []                         # Sirf in users ko reply karo (empty = sabko)

# ===== CONFIGURATION END =====

print("⚙️ Bot Configuration:")
print(f"   Username: {INSTAGRAM_USERNAME}")
print(f"   Model: {'Ollama - ' + OLLAMA_MODEL if USE_OLLAMA else 'Keyword-Based'}")
print(f"   Check every: {CHECK_INTERVAL} seconds")
print(f"   Reply delay: {REPLY_DELAY_MIN}-{REPLY_DELAY_MAX} seconds")
print(f"   Max replies/hour: {MAX_REPLIES_PER_HOUR}")


# ============ CELL 3: AI Reply Engine ============

import requests

class ReplyEngine:
    """Smart reply generate karta hai - Ollama ya Keyword-based."""
    
    def __init__(self, use_ollama=True, model_name="mybot"):
        self.use_ollama = use_ollama
        self.model_name = model_name
        self.conversation_history = {}  # Per-user history
        
        # Keyword-based fallback responses
        self.keyword_responses = {
            # Greetings
            "hi": ["Hey! Kya haal hai? 😊", "Hello! Bata kya scene hai?", "Hii! Sab theek? 😄"],
            "hello": ["Hello! Kaise ho? 😊", "Hey there! Kya chal raha?", "Hi! Bata kya kar rahe?"],
            "hey": ["Hey! Sab badhiya? 😄", "Heyy! Kya haal hai?", "Hey! Bata kya scene hai?"],
            "hii": ["Hii! Kya haal hai? 😊", "Hiiii! Bata kya chal raha?", "Heyy! Sab mast?"],
            
            # How are you
            "kaise ho": ["Main mast hoon! Tu bata? 😊", "Bilkul badhiya! Tera kya haal?", "Sab accha hai bhai! Tu suna?"],
            "how are you": ["I'm great! What about you? 😄", "Doing good! You tell?", "All good here! How's you?"],
            "kaisa hai": ["Sab mast hai bro! Tu bata?", "Ekdum first class! 😎 Tera kaisa?", "Badhiya yaar! Tu kaisa hai?"],
            
            # What doing
            "kya kar rahe": ["Bas chill kar raha tha! Tu bata? 😄", "Kuch nahi yaar, timepass. Tu kya kar raha?", "Phone dekh raha tha, ab tera message aaya! 😊"],
            "what are you doing": ["Nothing much, just chilling! You? 😄", "Was scrolling, now talking to you! 😊", "Just vibing! What about you?"],
            "kya chal raha": ["Kuch khaas nahi bro! Tu bata plan kya hai?", "Bas aise hi, tu suna kya chal raha?", "Timepass ho raha hai 😂 Tu bata?"],
            
            # Emotions
            "bore ho raha": ["Chal kuch fun karte hain! 🎮", "Game khele? Ya memes share kare? 😂", "Arey bore kyu! Baat kar mere saath 😄"],
            "sad": ["Kya hua? Bata mujhe, main hoon na ❤️", "Hey, it's okay. Main sun raha hoon 🤗", "Tension mat le, sab theek hoga. Baat kar?"],
            "happy": ["Yay! Kya baat hai! Bata kya hua? 🎉", "That's amazing! Share kar na! 😊", "Mujhe bhi khushi hui! Tell me more! 🥳"],
            "angry": ["Relax yaar! Deep breath. Kya hua? 😊", "Chill kar bhai! Bata kya problem hai?", "Arre gussa chhod, baat kar. Solve karte hain 💪"],
            
            # Time-based
            "good morning": ["Good morning! ☀️ Aaj ka din accha jaaye!", "Morning! Chai pi? ☕😊", "Suprabhat! Aaj kya plan hai? 🌞"],
            "good night": ["Good night! 🌙 Sweet dreams!", "Nighty night! Kal milte hain! 😴", "So ja yaar! Good night! 💤"],
            "good evening": ["Good evening! Kaisa raha din? 🌅", "Evening! Kya kar raha ab?", "Good evening! Dinner hua? 🍽️"],
            
            # Food
            "khana": ["Kya khaya? Mujhe bhi bhookh lagi! 🍕", "Aaj kya special banaya?", "Biryani khila de yaar! 😂"],
            "hungry": ["Kuch order kar le! Pizza? 🍕", "Maggi bana le instant! 😂", "Kya khane ka mann hai? Batao!"],
            
            # Love/Compliments
            "i love you": ["Aww! That's sweet! 😊❤️", "You're special to me too! 💕", "Love you too! 🥰"],
            "miss": ["Miss you too! 🥺", "Aww! Jaldi milte hain! ❤️", "Main bhi miss kar raha! 😊"],
            "cute": ["Hehe thanks! 😊", "No you're cuter! 🥰", "Aww shucks! 😊❤️"],
            
            # Entertainment
            "movie": ["Genre bata! Action? Comedy? Romance? 🎬", "Pushpa 2 dekhi? Mast hai! 🔥", "Netflix pe 'Wednesday' try kar! 📺"],
            "song": ["Mood kya hai? Chill? Party? Sad? 🎵", "Arijit Singh ka naya gaana sun! 🎶", "Bata kaunsa genre, suggest karta hoon!"],
            "game": ["Chalo khelte hain! 🎮 Kaunsa game?", "BGMI? Free Fire? Ya word game? 🎯", "Main ready hoon! Bol kya khelna hai? 💪"],
            
            # Thanks/Sorry
            "thank": ["Koi baat nahi! Dost hain! 🤝", "Arre thanks ki zarurat nahi! 😊", "Always welcome! Kabhi bhi bol! ❤️"],
            "sorry": ["Koi baat nahi yaar! All cool! 😊", "Chhod na! Sab theek hai! 🤗", "Already maaf! Tension mat le! ❤️"],
            
            # Bye
            "bye": ["Bye! Take care! 👋😊", "Bye bye! Jaldi baat karna! ❤️", "Chal phir! Milte hain! 👋"],
            "chalta": ["Okay! Apna khayal rakh! 😊", "Theek hai bro! Baad mein baat karte hain!", "Chal! Take care! ❤️"],
            
            # Jokes
            "joke": ["Teacher: Late kyu aaye? Student: Aapne kaha jaldi mat aana 😂", "Doctor: Kya problem hai? Patient: Log mujhe seriously nahi lete 😂", "Google se pucha 'how to be happy' - Result: Delete social media 😂😂"],
        }
        
        # Default responses for unknown inputs
        self.default_responses = [
            "Hmm interesting! Aur batao? 😊",
            "Accha! Phir kya hua? 🤔",
            "Haha nice! 😄 Aur kya chal raha?",
            "Sahi hai yaar! Bata aur? 😊",
            "Ohh accha! Tell me more! 🤗",
            "Waah! Mast! Aur kya naya? 😄",
            "Haan haan, bata bata! 😊",
            "That's cool! Aur suna? 🙌",
            "Okay okay! Phir? 😄",
            "Hmm samjha! Aur kuch? 🤔",
        ]
    
    def get_ollama_reply(self, user_message, username):
        """Ollama model se reply generate karta hai."""
        try:
            # Get conversation history for context
            history = self.conversation_history.get(username, [])[-5:]  # Last 5 messages
            
            # Build prompt
            system_prompt = """Tu ek friendly, caring aur fun dost hai. Tu Hinglish (Hindi + English mix) mein baat karta hai. 
Tu hamesha caring, supportive aur entertaining hai. Tu emojis use karta hai. 
Tu short aur natural replies deta hai (1-2 lines max). Tu har baar thoda alag reply deta hai."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add history
            for msg in history:
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Call Ollama API
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "num_predict": 100,
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                reply = response.json()["message"]["content"].strip()
                
                # Save to history
                if username not in self.conversation_history:
                    self.conversation_history[username] = []
                self.conversation_history[username].append({"role": "user", "content": user_message})
                self.conversation_history[username].append({"role": "assistant", "content": reply})
                
                # Keep history limited
                if len(self.conversation_history[username]) > 20:
                    self.conversation_history[username] = self.conversation_history[username][-10:]
                
                return reply
            else:
                print(f"  ⚠️ Ollama error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ⚠️ Ollama connection error: {e}")
            return None
    
    def get_keyword_reply(self, user_message):
        """Keyword matching se reply deta hai."""
        message_lower = user_message.lower().strip()
        
        # Check each keyword
        for keyword, responses in self.keyword_responses.items():
            if keyword in message_lower:
                return random.choice(responses)
        
        # Default response
        return random.choice(self.default_responses)
    
    def get_reply(self, user_message, username="unknown"):
        """Main reply function — Ollama try karta hai, fallback = keywords."""
        
        if self.use_ollama:
            reply = self.get_ollama_reply(user_message, username)
            if reply:
                return reply
            # Fallback to keyword if Ollama fails
            print("  ℹ️ Ollama failed, using keyword fallback")
        
        return self.get_keyword_reply(user_message)


# Test the engine
engine = ReplyEngine(use_ollama=USE_OLLAMA, model_name=OLLAMA_MODEL)

print("\n🧪 Testing Reply Engine:")
test_msgs = ["hi", "kaise ho?", "bore ho raha hoon", "good night"]
for msg in test_msgs:
    reply = engine.get_reply(msg, "test_user")
    print(f"  👤 {msg} → 🤖 {reply}")


# ============ CELL 4: Instagram Bot ============

from instagrapi import Client
from instagrapi.types import DirectThread, DirectMessage

class InstagramBot:
    """Instagram auto-reply bot."""
    
    def __init__(self, username, password, reply_engine):
        self.username = username
        self.password = password
        self.client = Client()
        self.reply_engine = reply_engine
        self.replied_messages = set()  # Track replied message IDs
        self.reply_count_hourly = 0
        self.hour_start = datetime.now()
        self.is_running = False
        
        # Session file for persistent login
        self.session_file = f"session_{username}.json"
    
    def login(self):
        """Instagram mein login karta hai."""
        print(f"\n🔐 Logging in as @{self.username}...")
        
        # Try loading existing session
        if os.path.exists(self.session_file):
            try:
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                print("✅ Logged in using saved session!")
                return True
            except Exception as e:
                print(f"  ⚠️ Saved session expired, doing fresh login...")
        
        # Fresh login
        try:
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)
            print("✅ Logged in successfully! Session saved.")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print("\n💡 Tips:")
            print("   - Username/password check karo")
            print("   - 2FA off karo temporarily")
            print("   - VPN try karo agar block ho raha")
            return False
    
    def check_rate_limit(self):
        """Rate limit check karta hai (ban se bachne ke liye)."""
        now = datetime.now()
        
        # Reset hourly counter
        if (now - self.hour_start).seconds >= 3600:
            self.reply_count_hourly = 0
            self.hour_start = now
        
        if self.reply_count_hourly >= MAX_REPLIES_PER_HOUR:
            print(f"  ⚠️ Rate limit reached ({MAX_REPLIES_PER_HOUR}/hour). Waiting...")
            return False
        
        return True
    
    def should_reply(self, thread, message):
        """Decide karta hai ki reply karna chahiye ya nahi."""
        
        # Already replied
        if message.id in self.replied_messages:
            return False
        
        # Message from self
        if str(message.user_id) == str(self.client.user_id):
            return False
        
        # Check ignored users
        sender_username = ""
        try:
            sender_info = self.client.user_info(message.user_id)
            sender_username = sender_info.username
        except:
            pass
        
        if sender_username in IGNORED_USERS:
            return False
        
        if ONLY_REPLY_TO and sender_username not in ONLY_REPLY_TO:
            return False
        
        # Only text messages (skip photos, reels, etc.)
        if not message.text:
            return False
        
        # Message too old (skip messages older than 5 minutes)
        if message.timestamp:
            msg_time = message.timestamp
            if isinstance(msg_time, (int, float)):
                msg_time = datetime.fromtimestamp(msg_time)
            if (datetime.now() - msg_time).seconds > 300:
                return False
        
        return True
    
    def process_threads(self):
        """Inbox check karta hai aur unread messages ka reply deta hai."""
        try:
            # Get direct inbox
            threads = self.client.direct_threads(amount=20)
            
            for thread in threads:
                # Get latest messages
                messages = self.client.direct_messages(thread.id, amount=5)
                
                for message in messages:
                    if self.should_reply(thread, message):
                        # Rate limit check
                        if not self.check_rate_limit():
                            return
                        
                        # Get sender info
                        sender = "unknown"
                        try:
                            sender_info = self.client.user_info(message.user_id)
                            sender = sender_info.username
                        except:
                            pass
                        
                        # Generate reply
                        reply = self.reply_engine.get_reply(message.text, sender)
                        
                        # Natural delay (taaki human jaisa lage)
                        delay = random.uniform(REPLY_DELAY_MIN, REPLY_DELAY_MAX)
                        print(f"  💬 @{sender}: {message.text}")
                        print(f"  🤖 Reply ({delay:.1f}s delay): {reply}")
                        time.sleep(delay)
                        
                        # Send reply
                        try:
                            self.client.direct_send(reply, thread_ids=[thread.id])
                            self.replied_messages.add(message.id)
                            self.reply_count_hourly += 1
                            print(f"  ✅ Sent! (Replies this hour: {self.reply_count_hourly}/{MAX_REPLIES_PER_HOUR})")
                        except Exception as e:
                            print(f"  ❌ Send failed: {e}")
                        
                        # Small delay between replies
                        time.sleep(2)
            
        except Exception as e:
            print(f"  ⚠️ Error checking inbox: {e}")
    
    def run(self):
        """Bot ko start karta hai — continuously inbox check karta hai."""
        if not self.login():
            return
        
        self.is_running = True
        print(f"\n{'='*50}")
        print(f"🤖 BOT IS RUNNING!")
        print(f"{'='*50}")
        print(f"   Checking inbox every {CHECK_INTERVAL} seconds")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while self.is_running:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] 📥 Checking inbox...")
                
                self.process_threads()
                
                # Wait before next check
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Bot stopped by user!")
            self.is_running = False
        
        print("👋 Bye! Bot is offline now.")
    
    def run_once(self):
        """Ek baar check karta hai (testing ke liye)."""
        if not self.login():
            return
        
        print("\n📥 Checking inbox (one-time)...")
        self.process_threads()
        print("✅ Done!")


# ============ CELL 5: Ollama Model Setup (if using trained model) ============

# Agar tumne Step 3 mein model train kiya hai, toh:

MODELFILE_CONTENT = """
FROM ./model_gguf/unsloth.Q4_K_M.gguf

# System prompt
SYSTEM "Tu ek friendly, caring aur fun dost hai. Tu Hinglish (Hindi + English mix) mein baat karta hai. Tu hamesha caring, supportive aur entertaining hai. Tu emojis use karta hai. Tu short aur natural replies deta hai (1-2 lines max). Tu har baar thoda alag reply deta hai."

# Parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER num_predict 100
PARAMETER repeat_penalty 1.2
"""

# Save Modelfile
with open("Modelfile", "w") as f:
    f.write(MODELFILE_CONTENT)

print("""
📋 Ollama Setup Instructions:
================================

1. Ollama install karo (agar nahi kiya):
   curl -fsSL https://ollama.com/install.sh | sh

2. GGUF file ko sahi jagah rakho:
   - Step 3 se downloaded .gguf file ko 'model_gguf/' folder mein rakho

3. Model create karo:
   ollama create mybot -f Modelfile

4. Test karo:
   ollama run mybot "hi kaise ho?"

5. Phir neeche wala cell run karo bot start karne ke liye!
""")


# ============ CELL 6: START THE BOT ============

# ⚠️ Pehle apna username/password CELL 2 mein dalo!

if INSTAGRAM_USERNAME == "YOUR_USERNAME":
    print("❌ ERROR: Pehle CELL 2 mein apna Instagram username/password dalo!")
    print("   INSTAGRAM_USERNAME aur INSTAGRAM_PASSWORD change karo")
else:
    # Create reply engine
    reply_engine = ReplyEngine(
        use_ollama=USE_OLLAMA,
        model_name=OLLAMA_MODEL
    )
    
    # Create bot
    bot = InstagramBot(
        username=INSTAGRAM_USERNAME,
        password=INSTAGRAM_PASSWORD,
        reply_engine=reply_engine
    )
    
    # Run bot
    # bot.run()        # ← Continuous mode (Ctrl+C to stop)
    # bot.run_once()   # ← One-time check (testing ke liye)
    
    print("✅ Bot ready! Uncomment bot.run() or bot.run_once() to start!")
    print("\n💡 Testing ke liye pehle bot.run_once() try karo")
    print("   Phir bot.run() se continuous mode mein chala do")


# ============ CELL 7: Test Mode (without Instagram) ============

print("\n" + "="*50)
print("🧪 TEST MODE - Instagram ke bina test karo")
print("="*50)

# Interactive testing
reply_engine_test = ReplyEngine(use_ollama=False)  # Keyword mode for testing

test_conversations = [
    "hi",
    "kaise ho?",
    "kya kar rahe ho?",
    "bore ho raha hoon yaar",
    "koi movie batao",
    "bahut sad hoon aaj",
    "good morning!",
    "i love you",
    "thank you so much",
    "good night!",
    "joke sunao koi",
    "khana khaya?",
    "tum kaun ho?",
    "bye bye",
]

print("\n🤖 Simulated Conversation:\n")
for msg in test_conversations:
    reply = reply_engine_test.get_reply(msg, "test_user")
    print(f"  👤 User: {msg}")
    print(f"  🤖 Bot:  {reply}")
    print()

print("✅ Test complete! Sab kaam kar raha hai!")
print("\n💡 Ab CELL 2 mein credentials dalo aur CELL 6 run karo bot start karne ke liye!")
