# ============================================================
# 🤖 INSTAGRAM AUTO-REPLY BOT v2 — DM + GROUP CHAT SUPPORT
# ============================================================
# Features:
# - Personal DM auto-reply ✅
# - Group chat auto-reply ✅
# - Trained model (Ollama) ya Keyword-based ✅
# - Smart group logic (mention/question detect) ✅
# - Rate limiting (ban se protection) ✅
# - Natural delays ✅
# - Per-user conversation memory ✅
#
# ⚠️ WARNING:
# - Sirf TEST/DUMMY account use karo
# - Main account pe BAN ho sakta hai
# - Educational purpose ke liye hai
#
# Run: python 04_instagram_bot_v2.py
# ============================================================

# !pip install instagrapi requests

import os
import json
import time
import random
import re
from datetime import datetime, timedelta

# ╔══════════════════════════════════════════════════╗
# ║  CONFIGURATION — YAHAN APNI DETAILS DALO        ║
# ╚══════════════════════════════════════════════════╝

INSTAGRAM_USERNAME = "YOUR_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"

# Model settings
USE_OLLAMA = False  # True = Ollama AI model, False = Keyword-based (no setup needed)
OLLAMA_MODEL = "mybot"
OLLAMA_URL = "http://localhost:11434"

# DM Settings
REPLY_TO_DMS = True
DM_CHECK_INTERVAL = 30  # Seconds mein
DM_REPLY_DELAY_MIN = 3
DM_REPLY_DELAY_MAX = 12
DM_MAX_REPLIES_PER_HOUR = 20

# GROUP CHAT Settings
REPLY_TO_GROUPS = True
GROUP_CHECK_INTERVAL = 45  # Groups thoda kam frequently check karo
GROUP_REPLY_DELAY_MIN = 5
GROUP_REPLY_DELAY_MAX = 20  # Groups mein zyada natural delay
GROUP_MAX_REPLIES_PER_HOUR = 10  # Groups mein kam reply (ban se bachne ke liye)
REPLY_ONLY_WHEN_MENTIONED = True  # True = sirf @mention pe reply, False = har relevant message pe
REPLY_TO_QUESTIONS = True  # Questions ka auto-reply (even without mention)
BOT_TRIGGER_WORDS = ["bot", "bro", "yaar", "bhai"]  # In words pe bhi reply

# Safety
IGNORED_USERS = []  # ["spam_user1", "spam_user2"]
ONLY_REPLY_TO = []  # Empty = sabko reply, ya specific users ki list
IGNORED_GROUPS = []  # Group thread IDs to ignore
MAX_MESSAGE_AGE = 300  # 5 min se purane messages skip

# ╔══════════════════════════════════════════════════╗
# ║  REPLY ENGINE — Smart Replies Generate Karta Hai ║
# ╚══════════════════════════════════════════════════╝

import requests

class SmartReplyEngine:
    def __init__(self, use_ollama=False, model_name="mybot"):
        self.use_ollama = use_ollama
        self.model_name = model_name
        self.conversation_history = {}

        self.keyword_responses = {
            "hi": ["Hey! Kya haal hai? 😊", "Hello! Bata kya scene hai?", "Hii! Sab theek? 😄", "Hey bro! Kya chal raha?"],
            "hii": ["Hiii! 😄 Kya scene hai?", "Heyy! Kaisa hai tu?", "Hii! Bata kya ho raha? 😊"],
            "hello": ["Hello! Kaise ho? 😊", "Hey there! Kya chal raha?", "Hi! Bata kya kar rahe?", "Hello bro!"],
            "hey": ["Hey! Sab badhiya? 😄", "Heyy! Kya haal hai?", "Hey! Bata kya scene hai?"],
            "kaise ho": ["Main mast hoon! Tu bata? 😊", "Bilkul badhiya! Tera kya haal?", "Sab accha hai bhai! Tu suna?", "Ekdum first class! Tu bata?"],
            "how are you": ["I'm great! What about you? 😄", "Doing good! You tell?", "All good here! How's you?", "Mast hoon! And you?"],
            "kaisa hai": ["Sab mast hai bro! Tu bata?", "Ekdum top pe! 😎 Tera kaisa?", "Badhiya yaar! Tu kaisa hai?"],
            "kya kar rahe": ["Bas chill kar raha tha! Tu bata? 😄", "Kuch nahi yaar, timepass. Tu?", "Phone dekh raha tha, ab tera msg aaya! 😊"],
            "what are you doing": ["Nothing much, just chilling! You? 😄", "Was scrolling, now talking to you! 😊", "Just vibing! What about you?"],
            "kya chal raha": ["Kuch khaas nahi bro! Tu bata?", "Bas aise hi, tu suna?", "Timepass ho raha hai 😂 Tu bata?"],
            "bore ho raha": ["Chal kuch fun karte hain! 🎮", "Game khele? Ya memes? 😂", "Mere saath baat kar, bore nahi hoga! 😄"],
            "bored": ["Let's do something fun! 🎮", "Wanna play a game? 😄", "I'm here! Let's chat 😊"],
            "sad": ["Kya hua? Bata mujhe, main hoon na ❤️", "Hey, it's okay. Main sun raha hoon 🤗", "Tension mat le, sab theek hoga 💪"],
            "happy": ["Yay! Kya baat hai! 🎉", "That's amazing! 😊", "Mujhe bhi khushi hui! 🥳"],
            "angry": ["Relax yaar! Deep breath. Kya hua? 😊", "Chill kar bhai! Bata problem kya hai?", "Gussa chhod, baat kar 💪"],
            "good morning": ["Good morning! ☀️ Aaj ka din accha jaaye!", "Morning! Chai pi? ☕😊", "GM! Aaj kya plan hai? 🌞"],
            "good night": ["Good night! 🌙 Sweet dreams!", "Nighty night! Kal milte hain! 😴", "So ja yaar! Good night! 💤"],
            "good evening": ["Good evening! Kaisa raha din? 🌅", "Evening! Kya scene hai ab?", "Good evening! Dinner hua?"],
            "i love you": ["Aww! That's sweet! 😊❤️", "You're special! 💕", "Love you too! 🥰"],
            "miss": ["Miss you too! 🥺", "Aww! Jaldi milte hain! ❤️", "Main bhi miss kar raha! 😊"],
            "cute": ["Hehe thanks! 😊", "No you're cuter! 🥰", "Aww shucks! 😊❤️"],
            "movie": ["Genre bata! Action? Comedy? 🎬", "Pushpa 2 dekhi? Mast hai! 🔥", "Netflix pe Wednesday try kar! 📺"],
            "song": ["Mood kya hai? Chill? Party? 🎵", "Arijit ka naya gaana sun! 🎶", "Genre bata, suggest karta hoon!"],
            "game": ["Chalo khelte hain! 🎮", "BGMI? Free Fire? 🎯", "Main ready hoon! Bol kya khele? 💪"],
            "khana": ["Kya khaya? Mujhe bhi bhookh! 🍕", "Biryani ka mood hai! 😋", "Aaj kya banaya?"],
            "hungry": ["Kuch order kar! Pizza? 🍕", "Maggi bana le! 😂", "Kya khane ka mann hai?"],
            "thank": ["Koi baat nahi! Dost hain! 🤝", "Thanks ki zarurat nahi! 😊", "Always welcome! ❤️"],
            "sorry": ["Koi baat nahi yaar! 😊", "Sab cool hai! 🤗", "Already maaf! ❤️"],
            "bye": ["Bye! Take care! 👋😊", "Bye bye! Jaldi baat karna! ❤️", "Chal phir! Milte hain! 👋"],
            "joke": ["Teacher: Late kyu? Student: Aapne kaha jaldi mat aana 😂", "Google: How to be happy? → Delete social media 😂", "Doctor: Problem? Patient: Log mujhe seriously nahi lete 😂"],
            "lol": ["😂😂😂", "Hahaha! 🤣", "Bahut funny! 😂"],
            "haha": ["😂😂", "Haha mast! 🤣", "😄😄"],
            "ok": ["👍", "Theek hai! 😊", "Okay! 👌"],
            "hmm": ["Kya soch raha hai? 🤔", "Bata na! 😊", "Hmm kya? Bol! 😄"],
            "kya": ["Bol bata! 😊", "Haan bata kya hua?", "Kya hua? Sab theek? 😄"],
            "haan": ["Accha! Phir? 😊", "Okay okay! 👍", "Mast! Aur bata? 😄"],
            "nahi": ["Kyu nahi? 🤔", "Accha theek hai! 😊", "Okay no problem! 👍"],
            "love": ["❤️❤️", "Love! 💕", "Aww! 🥰"],
            "photo": ["Mast photo hai! 🔥", "Bohot acchi! 😍", "Fire! 🔥🔥"],
            "reel": ["Mast reel hai! 🔥😂", "Haha share karte reh! 😄", "Bohot sahi! 🤣"],
        }

        self.default_responses = [
            "Hmm interesting! Aur batao? 😊",
            "Accha! Phir kya hua? 🤔",
            "Haha nice! 😄",
            "Sahi hai yaar! 😊",
            "Ohh accha! Tell me more! 🤗",
            "Waah! Mast! 😄",
            "That's cool! 🙌",
            "Hmm samjha! 🤔",
            "Nice bhai! 😊",
            "Interesting! 😄",
            "👍🔥",
            "Haha! 😂",
            "Sahi baat hai! 💯",
        ]

        self.group_short_responses = [
            "😂😂", "🔥🔥", "Haha!", "Sahi hai!", "Mast! 😄",
            "👍", "💯", "True! 😂", "Bahut sahi!", "Agreed! 😊",
            "Lol 😂", "Nice!", "Ekdum!", "Haan bhai!", "😄😄",
        ]

    def get_ollama_reply(self, message, username):
        try:
            history = self.conversation_history.get(username, [])[-6:]
            system_prompt = "Tu ek friendly, caring dost hai. Hinglish mein short reply de (1-2 lines). Emojis use kar. Natural aur varied reply de."
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": message})
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": self.model_name, "messages": messages, "stream": False, "options": {"temperature": 0.8, "top_p": 0.9, "num_predict": 80, "repeat_penalty": 1.3}},
                timeout=30
            )
            if response.status_code == 200:
                reply = response.json()["message"]["content"].strip()
                if username not in self.conversation_history:
                    self.conversation_history[username] = []
                self.conversation_history[username].append({"role": "user", "content": message})
                self.conversation_history[username].append({"role": "assistant", "content": reply})
                if len(self.conversation_history[username]) > 20:
                    self.conversation_history[username] = self.conversation_history[username][-10:]
                return reply
        except Exception as e:
            print(f"  Ollama error: {e}")
        return None

    def get_keyword_reply(self, message, is_group=False):
        message_lower = message.lower().strip()
        for keyword, responses in self.keyword_responses.items():
            if keyword in message_lower:
                return random.choice(responses)
        if is_group:
            return random.choice(self.group_short_responses)
        return random.choice(self.default_responses)

    def get_reply(self, message, username="unknown", is_group=False):
        if self.use_ollama:
            reply = self.get_ollama_reply(message, username)
            if reply:
                return reply
        return self.get_keyword_reply(message, is_group)


# ╔══════════════════════════════════════════════════╗
# ║  GROUP CHAT LOGIC — Smart Detection              ║
# ╚══════════════════════════════════════════════════╝

class GroupChatLogic:
    """Decide karta hai ki group mein reply karna chahiye ya nahi."""

    def __init__(self, bot_username):
        self.bot_username = bot_username.lower()
        self.question_patterns = [
            r'\?$',
            r'kya\s',
            r'kaise\s',
            r'kahan\s',
            r'kab\s',
            r'kaun\s',
            r'kitna\s',
            r'how\s',
            r'what\s',
            r'where\s',
            r'when\s',
            r'who\s',
            r'why\s',
            r'which\s',
            r'suggest',
            r'recommend',
            r'batao',
            r'bolo',
            r'sunao',
        ]

    def should_reply_in_group(self, message_text, sender_username):
        """Decide karta hai ki group message ka reply karna chahiye ya nahi."""
        if not message_text:
            return False, "empty"

        text = message_text.lower().strip()

        # 1. Check if bot is mentioned (@username)
        if f"@{self.bot_username}" in text:
            return True, "mentioned"

        # 2. Check trigger words
        if REPLY_ONLY_WHEN_MENTIONED:
            for word in BOT_TRIGGER_WORDS:
                if word in text:
                    # Only reply 30% of the time for trigger words (natural)
                    if random.random() < 0.3:
                        return True, "trigger_word"
            return False, "not_mentioned"

        # 3. Check if it's a question
        if REPLY_TO_QUESTIONS:
            for pattern in self.question_patterns:
                if re.search(pattern, text):
                    # Reply to 40% of questions (don't spam)
                    if random.random() < 0.4:
                        return True, "question"

        # 4. Random engagement (5% chance for any message)
        if random.random() < 0.05:
            return True, "random_engage"

        return False, "skip"


# ╔══════════════════════════════════════════════════╗
# ║  INSTAGRAM BOT — DM + GROUP SUPPORT              ║
# ╚══════════════════════════════════════════════════╝

from instagrapi import Client

class InstagramBotV2:
    def __init__(self, username, password, reply_engine):
        self.username = username
        self.password = password
        self.client = Client()
        self.reply_engine = reply_engine
        self.group_logic = GroupChatLogic(username)
        self.replied_messages = set()
        self.dm_reply_count = 0
        self.group_reply_count = 0
        self.hour_start = datetime.now()
        self.is_running = False
        self.session_file = f"session_{username}.json"

    def login(self):
        print(f"\n🔐 Logging in as @{self.username}...")
        if os.path.exists(self.session_file):
            try:
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                print("✅ Logged in (saved session)!")
                return True
            except:
                print("  Session expired, fresh login...")
        try:
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)
            print("✅ Logged in successfully!")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print("   Tips: 2FA off karo, VPN try karo, password check karo")
            return False

    def reset_hourly_counters(self):
        now = datetime.now()
        if (now - self.hour_start).seconds >= 3600:
            self.dm_reply_count = 0
            self.group_reply_count = 0
            self.hour_start = now

    def process_inbox(self):
        """Inbox check karta hai — DMs aur Groups dono."""
        try:
            threads = self.client.direct_threads(amount=20)
            for thread in threads:
                is_group = thread.is_group if hasattr(thread, 'is_group') else (len(thread.users) > 1)

                if is_group and not REPLY_TO_GROUPS:
                    continue
                if not is_group and not REPLY_TO_DMS:
                    continue
                if str(thread.id) in IGNORED_GROUPS:
                    continue

                messages = self.client.direct_messages(thread.id, amount=5)
                for message in messages:
                    self.process_message(thread, message, is_group)

        except Exception as e:
            print(f"  ⚠️ Inbox error: {e}")

    def process_message(self, thread, message, is_group):
        """Ek message process karta hai."""
        # Skip if already replied
        if message.id in self.replied_messages:
            return
        # Skip own messages
        if str(message.user_id) == str(self.client.user_id):
            return
        # Skip non-text
        if not message.text:
            return
        # Skip old messages
        if message.timestamp:
            msg_time = message.timestamp
            if hasattr(msg_time, 'timestamp'):
                age = (datetime.now() - msg_time).total_seconds()
            else:
                age = (datetime.now() - datetime.fromtimestamp(msg_time)).total_seconds()
            if age > MAX_MESSAGE_AGE:
                return

        # Get sender info
        sender = "unknown"
        try:
            sender_info = self.client.user_info(message.user_id)
            sender = sender_info.username
        except:
            pass

        # Check ignored/allowed users
        if sender in IGNORED_USERS:
            return
        if ONLY_REPLY_TO and sender not in ONLY_REPLY_TO:
            return

        # Rate limit check
        self.reset_hourly_counters()

        if is_group:
            # GROUP LOGIC
            if self.group_reply_count >= GROUP_MAX_REPLIES_PER_HOUR:
                return

            should_reply, reason = self.group_logic.should_reply_in_group(message.text, sender)
            if not should_reply:
                return

            # Generate reply
            reply = self.reply_engine.get_reply(message.text, sender, is_group=True)
            delay = random.uniform(GROUP_REPLY_DELAY_MIN, GROUP_REPLY_DELAY_MAX)

            print(f"  👥 GROUP | @{sender}: {message.text[:50]}")
            print(f"     Reason: {reason} | Delay: {delay:.0f}s")
            print(f"     🤖 Reply: {reply}")

            time.sleep(delay)

            try:
                self.client.direct_send(reply, thread_ids=[thread.id])
                self.replied_messages.add(message.id)
                self.group_reply_count += 1
                print(f"     ✅ Sent! (Group replies: {self.group_reply_count}/{GROUP_MAX_REPLIES_PER_HOUR})")
            except Exception as e:
                print(f"     ❌ Send failed: {e}")

        else:
            # DM LOGIC
            if self.dm_reply_count >= DM_MAX_REPLIES_PER_HOUR:
                return

            reply = self.reply_engine.get_reply(message.text, sender, is_group=False)
            delay = random.uniform(DM_REPLY_DELAY_MIN, DM_REPLY_DELAY_MAX)

            print(f"  💬 DM | @{sender}: {message.text[:50]}")
            print(f"     🤖 Reply ({delay:.0f}s): {reply}")

            time.sleep(delay)

            try:
                self.client.direct_send(reply, thread_ids=[thread.id])
                self.replied_messages.add(message.id)
                self.dm_reply_count += 1
                print(f"     ✅ Sent! (DM replies: {self.dm_reply_count}/{DM_MAX_REPLIES_PER_HOUR})")
            except Exception as e:
                print(f"     ❌ Send failed: {e}")

        time.sleep(2)

    def run(self):
        """Bot start karta hai — continuous mode."""
        if not self.login():
            return

        self.is_running = True
        print(f"\n{'='*50}")
        print(f"🤖 INSTAGRAM BOT v2 IS RUNNING!")
        print(f"{'='*50}")
        print(f"   DM Reply: {'ON' if REPLY_TO_DMS else 'OFF'}")
        print(f"   Group Reply: {'ON' if REPLY_TO_GROUPS else 'OFF'}")
        print(f"   Mention Only: {'YES' if REPLY_ONLY_WHEN_MENTIONED else 'NO'}")
        print(f"   Model: {'Ollama - ' + OLLAMA_MODEL if USE_OLLAMA else 'Keyword-Based'}")
        print(f"   Check interval: {DM_CHECK_INTERVAL}s")
        print(f"   Press Ctrl+C to stop\n")

        try:
            while self.is_running:
                now = datetime.now().strftime("%H:%M:%S")
                print(f"[{now}] 📥 Checking inbox...")
                self.process_inbox()
                time.sleep(DM_CHECK_INTERVAL)
        except KeyboardInterrupt:
            print(f"\n\n🛑 Bot stopped!")
            self.is_running = False

        print("👋 Bot is offline.")

    def run_once(self):
        """Ek baar check (testing ke liye)."""
        if not self.login():
            return
        print("\n📥 Checking inbox (one-time)...")
        self.process_inbox()
        print("✅ Done!")


# ╔══════════════════════════════════════════════════╗
# ║  TEST MODE — Bina Instagram ke test karo         ║
# ╚══════════════════════════════════════════════════╝

def test_mode():
    """Instagram ke bina bot test karo."""
    print("\n" + "=" * 50)
    print("🧪 TEST MODE — Bot Simulation")
    print("=" * 50)

    engine = SmartReplyEngine(use_ollama=USE_OLLAMA, model_name=OLLAMA_MODEL)
    group_logic = GroupChatLogic(INSTAGRAM_USERNAME)

    # DM Test
    print("\n📱 DM Simulation:")
    dm_messages = ["hi", "kaise ho?", "kya kar rahe ho?", "bore ho raha", "joke sunao", "bye"]
    for msg in dm_messages:
        reply = engine.get_reply(msg, "friend1", is_group=False)
        print(f"  👤 friend1: {msg}")
        print(f"  🤖 Bot: {reply}\n")

    # Group Test
    print("\n👥 GROUP Simulation:")
    group_messages = [
        ("user1", "koi hai yahan?"),
        ("user2", f"@{INSTAGRAM_USERNAME} kaise ho?"),
        ("user3", "aaj mausam accha hai"),
        ("user4", "koi movie suggest karo"),
        ("user1", "haha bahut funny"),
        ("user5", f"@{INSTAGRAM_USERNAME} joke sunao"),
        ("user2", "random message ignore hona chahiye"),
        ("user3", "kya plan hai weekend ka?"),
    ]

    for sender, msg in group_messages:
        should_reply, reason = group_logic.should_reply_in_group(msg, sender)
        if should_reply:
            reply = engine.get_reply(msg, sender, is_group=True)
            print(f"  👤 @{sender}: {msg}")
            print(f"  🤖 Bot [{reason}]: {reply}\n")
        else:
            print(f"  👤 @{sender}: {msg}")
            print(f"  ⏭️ Skipped [{reason}]\n")

    print("✅ Test complete!")


# ╔══════════════════════════════════════════════════╗
# ║  MAIN — Bot Start Karo                          ║
# ╚══════════════════════════════════════════════════╝

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║  🤖 Instagram Auto-Reply Bot v2              ║
║  DM + Group Chat Support                     ║
╠══════════════════════════════════════════════╣
║  1. Test Mode (Instagram ke bina)            ║
║  2. Run Once (ek baar check)                 ║
║  3. Run Continuous (24/7 auto-reply)         ║
╚══════════════════════════════════════════════╝
""")

    # Uncomment karo jo chahiye:

    # --- Option 1: Test (no Instagram needed) ---
    test_mode()

    # --- Option 2: Run Once ---
    # engine = SmartReplyEngine(use_ollama=USE_OLLAMA, model_name=OLLAMA_MODEL)
    # bot = InstagramBotV2(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, engine)
    # bot.run_once()

    # --- Option 3: Run Continuous ---
    # engine = SmartReplyEngine(use_ollama=USE_OLLAMA, model_name=OLLAMA_MODEL)
    # bot = InstagramBotV2(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, engine)
    # bot.run()
