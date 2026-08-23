from instagrapi import Client
import random, time, requests, re, os, subprocess

# ===== INSTAGRAM DETAILS =====
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

# ===== SUPABASE DATABASE =====
SUPABASE_URL = "https://ijkxadnmeqfflfuwvmfz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlqa3hhZG5tZXFmZmxmdXd2bWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMTg0MTUsImV4cCI6MjEwMjc5NDQxNX0.i-fNXpFmLTGC635QUD33n7neNUarentevjyUxp4I4FA"

# ====================================

SHORT_KEYWORDS = {"hi", "hey", "ok", "no", "ha", "na", "kya", "ho", "so", "tu", "hii", "bye", "gm", "gn"}
defaults = ["Hmm batao? 😊", "Accha! Phir? 🤔", "Nice! 😄", "Sahi hai! 😊", "Aur bata? 🤗", "Interesting! 😄", "Mast! 🙌", "Haan bata? 😊", "Phir? 😄", "Okay! 👍"]

def load_responses():
    """Supabase se LIVE responses load karta hai. Har call pe fresh data."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/bot_responses?select=keyword,response"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            responses = {}
            for item in data:
                kw = item["keyword"].lower().strip()
                if kw not in responses:
                    responses[kw] = []
                responses[kw].append(item["response"])
            return responses, len(data)
        else:
            return None, 0
    except:
        return None, 0

def get_reply(msg, responses):
    m = msg.lower().strip()
    # 1. Exact match
    for k, v in responses.items():
        if m == k:
            return random.choice(v)
    # 2. Smart match (longer keywords first)
    sorted_keywords = sorted(responses.keys(), key=len, reverse=True)
    for k in sorted_keywords:
        if len(k) <= 3 or k in SHORT_KEYWORDS:
            pattern = r'\b' + re.escape(k) + r'\b'
            if re.search(pattern, m):
                return random.choice(responses[k])
        else:
            if k in m:
                return random.choice(responses[k])
    return random.choice(defaults)

def auto_update_code():
    """Git se latest code pull karta hai (silent)."""
    try:
        subprocess.run(["git", "pull"], capture_output=True, timeout=30)
    except:
        pass

# ===== MAIN BOT =====
print("🔐 Logging in...")
cl = Client()
cl.login(USERNAME, PASSWORD)
print("✅ Logged in as @" + USERNAME)

# First load
print("📦 Loading responses from Supabase...")
responses, count = load_responses()
if responses:
    print(f"   ✅ Loaded {count} responses from database!")
else:
    print("   ⚠️ Database connect nahi hua. Defaults use honge.")
    responses = {}

my_id = str(cl.user_id)
replied = set()
cycle = 0

print(f"\n🤖 Instagram Auto-Reply Bot RUNNING!")
print(f"   ✅ DM reply: ON")
print(f"   ✅ Group reply: ON")
print(f"   📦 Responses: {count}")
print(f"   🔄 Auto-refresh: Every 5 min (database)")
print(f"   🔄 Auto-update: Every 30 min (code)")
print(f"   ⏱️ Checking DMs every 30 sec")
print(f"   🛑 Stop: Ctrl+C\n")

while True:
    try:
        cycle += 1

        # === AUTO REFRESH DATABASE (every 5 min = 10 cycles) ===
        if cycle % 10 == 0:
            new_responses, new_count = load_responses()
            if new_responses:
                responses = new_responses
                if new_count != count:
                    print(f"  🔄 Database refreshed! {count} → {new_count} responses")
                    count = new_count

        # === AUTO UPDATE CODE (every 30 min = 60 cycles) ===
        if cycle % 60 == 0:
            auto_update_code()

        # === CHECK INBOX ===
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
                print(f"  🤖 Reply ({delay}s): {reply}\n")

        # Clean old replied IDs (memory save)
        if len(replied) > 1000:
            replied = set(list(replied)[-500:])

    except KeyboardInterrupt:
        print("\n🛑 Bot stopped!")
        break
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        time.sleep(10)

    time.sleep(30)
