from instagrapi import Client
import random, time, requests

# ===== INSTAGRAM DETAILS =====
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

# ===== SUPABASE DATABASE =====
SUPABASE_URL = "https://ijkxadnmeqfflfuwvmfz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlqa3hhZG5tZXFmZmxmdXd2bWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMTg0MTUsImV4cCI6MjEwMjc5NDQxNX0.i-fNXpFmLTGC635QUD33n7neNUarentevjyUxp4I4FA"

# ====================================

def load_responses():
    """Supabase se saari responses load karta hai."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/bot_responses?select=keyword,response"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            responses = {}
            for item in data:
                kw = item["keyword"]
                if kw not in responses:
                    responses[kw] = []
                responses[kw].append(item["response"])
            print(f"   ✅ Loaded {len(data)} responses from database")
            return responses
        else:
            print(f"   ⚠️ Database error: {r.status_code}")
            return {}
    except Exception as e:
        print(f"   ⚠️ Database connection error: {e}")
        return {}

def add_response(keyword, response, category="general"):
    """Naya response database mein add karta hai."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/bot_responses"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        data = {"keyword": keyword, "response": response, "category": category}
        r = requests.post(url, json=data, headers=headers)
        return r.status_code == 201
    except:
        return False

import re

defaults = ["Hmm batao? 😊", "Accha! Phir? 🤔", "Nice! 😄", "Sahi hai! 😊", "Aur bata? 🤗", "Interesting! 😄", "Mast! 🙌", "Haan bata? 😊", "Phir? 😄", "Okay! 👍"]

# Short keywords jo word boundary match honi chahiye (nahi toh "chhinra" mein "hi" match ho jaata hai)
SHORT_KEYWORDS = {"hi", "hey", "ok", "no", "ha", "na", "kya", "ho", "so", "tu"}

def get_reply(msg, responses):
    m = msg.lower().strip()

    # 1. Exact full message match
    for k, v in responses.items():
        if m == k:
            return random.choice(v)

    # 2. Multi-word keyword match (longer keywords first — more specific)
    sorted_keywords = sorted(responses.keys(), key=len, reverse=True)
    for k in sorted_keywords:
        if len(k) <= 3 or k in SHORT_KEYWORDS:
            # Short keywords: word boundary match only
            pattern = r'\b' + re.escape(k) + r'\b'
            if re.search(pattern, m):
                return random.choice(responses[k])
        else:
            # Longer keywords: substring match is fine
            if k in m:
                return random.choice(responses[k])

    return random.choice(defaults)

# === START ===
print("🔐 Logging in...")
cl = Client()
cl.login(USERNAME, PASSWORD)
print("✅ Logged in as @" + USERNAME)

print("\n📦 Loading responses from Supabase...")
responses = load_responses()

if not responses:
    print("   ⚠️ No responses in database! Using defaults.")

my_id = str(cl.user_id)
replied = set()

print("\n🤖 Instagram Auto-Reply Bot RUNNING!")
print("   ✅ DM reply: ON")
print("   ✅ Group reply: ON")
print(f"   📦 Database: {len(responses)} keywords loaded")
print("   ⏱️ Checking every 30 seconds")
print("   🔄 Refreshes data every 5 minutes")
print("   🛑 Stop: Ctrl+C\n")

refresh_counter = 0

while True:
    try:
        # Refresh responses from DB every 5 minutes (10 cycles)
        refresh_counter += 1
        if refresh_counter >= 10:
            responses = load_responses()
            refresh_counter = 0

        threads = cl.direct_threads(amount=10)
        for thread in threads:
            msgs = cl.direct_messages(thread.id, amount=3)
            for msg in msgs:
                if msg.id in replied:
                    continue
                if str(msg.user_id) == my_id:
                    continue
                if not msg.text:
                    continue
                reply = get_reply(msg.text, responses)
                delay = random.randint(3, 10)
                time.sleep(delay)
                cl.direct_send(reply, thread_ids=[thread.id])
                replied.add(msg.id)
                sender = "unknown"
                try:
                    sender = cl.user_info(msg.user_id).username
                except:
                    pass
                print(f"  💬 @{sender}: {msg.text}")
                print(f"  🤖 Reply: {reply}\n")
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    time.sleep(30)
