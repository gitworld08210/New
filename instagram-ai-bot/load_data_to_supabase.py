"""
📦 LOAD CONVERSATION DATA TO SUPABASE
======================================
Yeh script hinglish-conv-dataset se real conversations parse karke
Supabase database mein keyword-response pairs add karta hai.

Usage: python load_data_to_supabase.py
"""

import os, re, random, requests, json, time

SUPABASE_URL = "https://ijkxadnmeqfflfuwvmfz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlqa3hhZG5tZXFmZmxmdXd2bWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMTg0MTUsImV4cCI6MjEwMjc5NDQxNX0.i-fNXpFmLTGC635QUD33n7neNUarentevjyUxp4I4FA"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Keywords to detect from messages
KEYWORD_PATTERNS = {
    "greeting": ["hi", "hello", "hey", "kaise ho", "how are you", "kya haal", "namaste"],
    "activity": ["kya kar", "what are you doing", "kya chal raha", "busy", "free"],
    "bored": ["bore", "bored", "kuch karne ko", "timepass"],
    "emotion_sad": ["sad", "dukhi", "mood kharab", "feeling low", "ro raha", "akela"],
    "emotion_happy": ["khush", "happy", "mast", "amazing", "great news", "excited"],
    "food": ["khana", "food", "hungry", "biryani", "pizza", "chai", "coffee"],
    "entertainment": ["movie", "song", "music", "game", "netflix", "youtube"],
    "love": ["love", "miss", "pyaar", "cute", "beautiful", "handsome"],
    "time": ["morning", "night", "evening", "subah", "raat"],
    "goodbye": ["bye", "chalta", "baad mein", "good night"],
    "thanks": ["thank", "shukriya", "dhanyawad"],
    "sorry": ["sorry", "maaf", "galti"],
    "travel": ["trip", "goa", "travel", "ghumne", "beach", "mountain"],
    "study": ["padhai", "exam", "college", "school", "study"],
    "fun": ["joke", "funny", "haha", "lol", "maza"],
    "relationship": ["crush", "propose", "girlfriend", "boyfriend", "date"],
    "compliment": ["accha", "best", "amazing", "awesome", "zabardast"],
}

def detect_category(text):
    """Message ka category detect karta hai."""
    t = text.lower()
    for cat, keywords in KEYWORD_PATTERNS.items():
        for kw in keywords:
            if kw in t:
                return cat
    return "general"

def extract_keyword(text):
    """Message se main keyword extract karta hai."""
    t = text.lower().strip()
    # Remove punctuation
    t = re.sub(r'[^\w\s]', '', t)
    
    # Check known keywords
    all_keywords = []
    for kws in KEYWORD_PATTERNS.values():
        all_keywords.extend(kws)
    
    for kw in all_keywords:
        if kw in t:
            return kw
    
    # Use first 3-4 words as keyword
    words = t.split()[:4]
    return " ".join(words) if words else t[:30]

def parse_conversation_file(filepath):
    """Ek conversation file parse karke pairs banata hai."""
    pairs = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Parse [Name]: [Message] format
        messages = []
        for line in lines:
            line = line.strip()
            if ":" in line and len(line) > 3:
                parts = line.split(":", 1)
                if len(parts) == 2 and len(parts[1].strip()) > 2:
                    name = parts[0].strip()
                    msg = parts[1].strip()
                    messages.append({"name": name, "text": msg})
        
        # Make consecutive pairs (Q&A style)
        for i in range(0, len(messages) - 1, 2):
            q = messages[i]["text"]
            a = messages[i+1]["text"]
            
            # Filter: both should be reasonable length
            if 3 < len(q) < 200 and 3 < len(a) < 200:
                keyword = extract_keyword(q)
                category = detect_category(q)
                pairs.append({
                    "keyword": keyword,
                    "response": a,
                    "category": category
                })
    except Exception as e:
        pass
    
    return pairs

def upload_to_supabase(pairs, batch_size=50):
    """Pairs ko batches mein Supabase mein upload karta hai."""
    total = len(pairs)
    uploaded = 0
    
    for i in range(0, total, batch_size):
        batch = pairs[i:i+batch_size]
        try:
            r = requests.post(
                f"{SUPABASE_URL}/rest/v1/bot_responses",
                json=batch,
                headers=headers
            )
            if r.status_code == 201:
                uploaded += len(batch)
                print(f"  ✅ Uploaded {uploaded}/{total} responses")
            else:
                print(f"  ⚠️ Batch failed: {r.status_code}")
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
        time.sleep(0.5)  # Rate limit
    
    return uploaded

# === MAIN ===
print("="*50)
print("📦 LOADING CONVERSATION DATA TO SUPABASE")
print("="*50)

# Find conversation files
conv_dir = None
possible_paths = [
    "/projects/sandbox/hinglish-conv-dataset/conversations",
    "hinglish-conv-dataset/conversations",
    "../hinglish-conv-dataset/conversations",
    "conversations",
]

for path in possible_paths:
    if os.path.exists(path):
        conv_dir = path
        break

if not conv_dir:
    print("\n⚠️ Conversation files not found!")
    print("   Run: git clone https://github.com/skmanish/hinglish-conv-dataset.git")
    print("   Then run this script again.")
    exit()

# Parse all files
files = [f for f in os.listdir(conv_dir) if f.endswith(".txt")]
print(f"\n📁 Found {len(files)} conversation files")
print("   Parsing...")

all_pairs = []
for filename in files[:200]:  # First 200 files (enough data)
    filepath = os.path.join(conv_dir, filename)
    pairs = parse_conversation_file(filepath)
    all_pairs.extend(pairs)

print(f"\n✅ Parsed {len(all_pairs)} conversation pairs!")

# Deduplicate by response (avoid exact same responses)
seen_responses = set()
unique_pairs = []
for pair in all_pairs:
    if pair["response"] not in seen_responses:
        seen_responses.add(pair["response"])
        unique_pairs.append(pair)

print(f"   Unique: {len(unique_pairs)} (removed duplicates)")

# Limit to 500 best pairs (Supabase free tier friendly)
if len(unique_pairs) > 500:
    unique_pairs = random.sample(unique_pairs, 500)
    print(f"   Selected: 500 random pairs for upload")

# Category breakdown
from collections import Counter
cats = Counter(p["category"] for p in unique_pairs)
print(f"\n📊 Categories:")
for cat, count in cats.most_common():
    print(f"   {cat}: {count}")

# Upload
print(f"\n📤 Uploading to Supabase...")
uploaded = upload_to_supabase(unique_pairs)

print(f"\n🎉 DONE! Uploaded {uploaded} responses to Supabase!")
print(f"   Bot will automatically pick these up in 5 minutes.")
print(f"\n📋 Manage responses at:")
print(f"   https://supabase.com/dashboard/project/ijkxadnmeqfflfuwvmfz/editor")
