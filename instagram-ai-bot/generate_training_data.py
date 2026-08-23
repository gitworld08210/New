"""
🧠 GENERATE 10,000 TRAINING CONVERSATIONS USING GROQ (FREE)
=============================================================
Yeh script Groq API se Hinglish conversations generate karta hai
Jo baad mein APNA model train karne ke liye use honge.

Usage: python generate_training_data.py
"""

import requests
import json
import time
import random
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_KEY_HERE")
# Colab mein run karo: !GROQ_API_KEY="gsk_xxx" python generate_training_data.py
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

os.makedirs("training_output", exist_ok=True)

# Categories aur topics jinpe conversations generate karni hain
TOPICS = [
    # Greetings & Status
    "greeting someone casually in Hinglish",
    "asking how are you and replying in Hinglish",
    "saying good morning/good night in Hinglish",
    
    # Daily life
    "asking what are you doing and replying casually in Hinglish",
    "talking about being bored and suggesting fun activities in Hinglish",
    "discussing food and what to eat in Hinglish",
    "talking about weather in Hinglish",
    "discussing sleep schedule in Hinglish",
    
    # Emotions
    "comforting someone who is sad in Hinglish",
    "celebrating happy moments together in Hinglish",
    "dealing with anger and calming someone in Hinglish",
    "motivating someone who is feeling low in Hinglish",
    "expressing excitement about something in Hinglish",
    
    # Entertainment
    "recommending movies in Hinglish",
    "discussing songs and music in Hinglish",
    "talking about gaming in Hinglish",
    "discussing Netflix/web series in Hinglish",
    "sharing memes and jokes in Hinglish",
    
    # Relationships
    "casual flirting in Hinglish",
    "expressing love and affection in Hinglish",
    "missing someone in Hinglish",
    "giving compliments in Hinglish",
    "talking about crush in Hinglish",
    
    # Studies & Work
    "discussing exams and study tips in Hinglish",
    "talking about job and career in Hinglish",
    "motivating for interviews in Hinglish",
    "discussing college life in Hinglish",
    
    # Fun
    "telling jokes in Hinglish",
    "playing truth or dare in Hinglish",
    "sharing interesting facts in Hinglish",
    "shayari and poetry in Hinglish",
    
    # Sports & Fitness
    "discussing cricket matches in Hinglish",
    "talking about gym and fitness in Hinglish",
    "discussing IPL in Hinglish",
    
    # Travel
    "planning a trip in Hinglish",
    "discussing travel destinations in Hinglish",
    
    # Tech
    "discussing phones and gadgets in Hinglish",
    "talking about social media in Hinglish",
    
    # Thanks/Sorry/Bye
    "saying thank you and responding in Hinglish",
    "apologizing and forgiving in Hinglish",
    "saying goodbye casually in Hinglish",
    
    # Random
    "random fun banter between friends in Hinglish",
    "giving life advice in Hinglish",
    "discussing health tips in Hinglish",
    "talking about birthdays and celebrations in Hinglish",
    "discussing shopping in Hinglish",
]

SYSTEM_PROMPT = """You are a training data generator. Generate exactly 20 short conversation pairs in JSON format.
Each pair should be a casual Instagram DM style message and its reply.
Messages should be in Hinglish (Hindi + English mix using English script).
Replies should be short (1-2 lines max), friendly, use emojis, and feel natural.

Output ONLY valid JSON array in this format:
[
  {"input": "user message", "output": "bot reply"},
  {"input": "user message", "output": "bot reply"}
]

Rules:
- Keep replies SHORT (max 2 lines)
- Use emojis naturally
- Make it sound like real Indian youth chatting on Instagram
- Vary the responses (don't repeat same style)
- Use Hinglish (mix of Hindi and English in Roman script)
- No explicit/inappropriate content"""

all_data = []
total_target = 10000
batch_size = 20  # 20 pairs per API call
calls_needed = total_target // batch_size  # 500 calls

print("=" * 50)
print("🧠 GENERATING TRAINING DATA WITH GROQ")
print("=" * 50)
print(f"   Target: {total_target} conversations")
print(f"   API calls needed: ~{calls_needed}")
print(f"   Topics: {len(TOPICS)}")
print(f"   Estimated time: 30-45 minutes")
print(f"   (Groq free = 30 requests/min limit)")
print("=" * 50)

calls_made = 0
errors = 0
save_every = 100  # Save after every 100 pairs

for i in range(calls_needed + 50):  # Extra buffer
    if len(all_data) >= total_target:
        break
    
    topic = random.choice(TOPICS)
    
    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Generate 20 conversation pairs about: {topic}"}
                ],
                "temperature": 0.9,
                "max_tokens": 2000,
            },
            timeout=30
        )
        
        calls_made += 1
        
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            
            # Parse JSON from response
            try:
                # Find JSON array in response
                start = content.find("[")
                end = content.rfind("]") + 1
                if start >= 0 and end > start:
                    pairs = json.loads(content[start:end])
                    for pair in pairs:
                        if "input" in pair and "output" in pair:
                            if len(pair["input"]) > 2 and len(pair["output"]) > 2:
                                all_data.append(pair)
            except json.JSONDecodeError:
                errors += 1
        
        elif response.status_code == 429:
            # Rate limit - wait
            print(f"  ⏳ Rate limit hit. Waiting 60s... ({len(all_data)}/{total_target})")
            time.sleep(60)
            continue
        else:
            errors += 1
        
        # Progress
        if calls_made % 10 == 0:
            print(f"  📊 Progress: {len(all_data)}/{total_target} | Calls: {calls_made} | Errors: {errors}")
        
        # Save periodically
        if len(all_data) % save_every == 0 and len(all_data) > 0:
            with open("training_output/training_data_partial.json", "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        # Rate limit: 30/min = 1 every 2 seconds
        time.sleep(2.1)
        
    except Exception as e:
        errors += 1
        time.sleep(5)

# Final save
print(f"\n✅ Generation complete!")
print(f"   Total conversations: {len(all_data)}")
print(f"   API calls made: {calls_made}")
print(f"   Errors: {errors}")

# Save final data
with open("training_output/training_data_full.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

# Also save in Alpaca format (ready for training)
alpaca_data = []
system = "Tu ek friendly, caring dost hai. Hinglish mein short reply de. Emojis use kar. Natural aur varied reply de."
for item in all_data:
    alpaca_data.append({
        "instruction": system,
        "input": item["input"],
        "output": item["output"]
    })

with open("training_output/train_alpaca.json", "w", encoding="utf-8") as f:
    json.dump(alpaca_data, f, ensure_ascii=False, indent=2)

# Also save to Supabase for immediate bot use
print(f"\n📤 Uploading to Supabase for immediate use...")
SUPABASE_URL = "https://ijkxadnmeqfflfuwvmfz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlqa3hhZG5tZXFmZmxmdXd2bWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMTg0MTUsImV4cCI6MjEwMjc5NDQxNX0.i-fNXpFmLTGC635QUD33n7neNUarentevjyUxp4I4FA"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Upload first 2000 to Supabase (for keyword bot until model is ready)
upload_data = []
for item in all_data[:2000]:
    keyword = item["input"].lower().strip()[:50]
    upload_data.append({
        "keyword": keyword,
        "response": item["output"],
        "category": "ai_generated"
    })

uploaded = 0
for i in range(0, len(upload_data), 50):
    batch = upload_data[i:i+50]
    try:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/bot_responses", json=batch, headers=headers)
        if r.status_code == 201:
            uploaded += len(batch)
    except:
        pass
    time.sleep(0.5)

print(f"   ✅ Uploaded {uploaded} to Supabase!")

print(f"""
{'='*50}
🎉 ALL DONE!
{'='*50}

📁 Files saved:
   1. training_output/training_data_full.json  ({len(all_data)} pairs)
   2. training_output/train_alpaca.json        (training ready)

📦 Supabase: {uploaded} responses uploaded (bot will use immediately)

🚀 Next step: Train your model on Colab!
   Upload train_alpaca.json to Colab
   Run the training script (03_model_training.py)
   Your own AI model ready!
""")
