# ============================================================
# 🧹 STEP 2: DATA CLEANING & FORMAT CONVERSION
# ============================================================
# Yeh script raw data ko clean karke training format mein convert karta hai
# 
# Google Colab pe paste karo aur run karo
# (Pehle Step 1 run karna zaruri hai)
# ============================================================

# ============ CELL 1: Setup ============
import json
import re
import os
from collections import Counter

print("🧹 Data Cleaning & Conversion Script")
print("="*50)

# ============ CELL 2: Load Raw Data ============

with open("collected_data/all_conversations.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

print(f"📊 Loaded {len(raw_data)} conversation pairs")
print(f"\nSources breakdown:")
source_counts = Counter(item.get("source", "unknown") for item in raw_data)
for source, count in source_counts.most_common():
    print(f"  {source}: {count}")


# ============ CELL 3: Cleaning Functions ============

def clean_text(text):
    """Text ko clean karta hai — spam, links, special chars hatata hai."""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    
    # Remove Reddit markdown
    text = re.sub(r'\[deleted\]', '', text)
    text = re.sub(r'\[removed\]', '', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&#x200B;', '', text)
    
    # Remove excessive special characters
    text = re.sub(r'[#*_~`|]', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def is_valid_pair(input_text, output_text):
    """Check karta hai ki conversation pair valid hai ya nahi."""
    
    # Too short
    if len(input_text) < 2 or len(output_text) < 2:
        return False
    
    # Too long (model ke liye)
    if len(input_text) > 300 or len(output_text) > 500:
        return False
    
    # Spam patterns
    spam_patterns = [
        r'follow me',
        r'check my profile',
        r'subscribe',
        r'free money',
        r'click here',
        r'bit\.ly',
        r'onlyfans',
        r'crypto',
        r'nft',
        r'\$\d+',
        r'dm me for',
        r'join my',
        r'promo code',
    ]
    
    combined = (input_text + " " + output_text).lower()
    for pattern in spam_patterns:
        if re.search(pattern, combined):
            return False
    
    # Only emojis/special chars
    alpha_ratio_input = len(re.findall(r'[a-zA-Z\u0900-\u097F]', input_text)) / max(len(input_text), 1)
    alpha_ratio_output = len(re.findall(r'[a-zA-Z\u0900-\u097F]', output_text)) / max(len(output_text), 1)
    
    if alpha_ratio_input < 0.3 or alpha_ratio_output < 0.3:
        return False
    
    # Same input and output
    if input_text.lower().strip() == output_text.lower().strip():
        return False
    
    return True


def categorize_conversation(input_text):
    """Conversation ko automatically categorize karta hai."""
    text = input_text.lower()
    
    # Greeting patterns
    if any(w in text for w in ["hi", "hello", "hey", "namaste", "hola"]):
        return "greeting"
    
    # How are you
    if any(w in text for w in ["kaise ho", "kaise hai", "how are", "kaisa hai", "kya haal", "haal"]):
        return "status"
    
    # What doing
    if any(w in text for w in ["kya kar", "what are you", "what doing", "kya chal"]):
        return "activity"
    
    # Emotions
    if any(w in text for w in ["sad", "dukhi", "ro raha", "crying", "upset", "depressed"]):
        return "emotion_sad"
    if any(w in text for w in ["happy", "khush", "mast", "amazing", "great"]):
        return "emotion_happy"
    if any(w in text for w in ["bore", "bored", "boring", "timepass"]):
        return "emotion_bored"
    if any(w in text for w in ["angry", "gussa", "irritate", "annoyed"]):
        return "emotion_angry"
    
    # Time-based
    if any(w in text for w in ["morning", "subah", "suprabhat"]):
        return "morning"
    if any(w in text for w in ["night", "raat", "sone ja", "good night"]):
        return "night"
    
    # Food
    if any(w in text for w in ["khana", "food", "hungry", "bhookh", "eat", "dinner", "lunch"]):
        return "food"
    
    # Entertainment
    if any(w in text for w in ["movie", "song", "music", "game", "netflix", "youtube"]):
        return "entertainment"
    
    # Goodbye
    if any(w in text for w in ["bye", "alvida", "chalta", "baad mein", "later"]):
        return "goodbye"
    
    # Thanks
    if any(w in text for w in ["thank", "shukriya", "dhanyawad", "thanks"]):
        return "thanks"
    
    # Love
    if any(w in text for w in ["love", "pyaar", "miss", "special", "cute"]):
        return "romantic"
    
    return "general"


# ============ CELL 4: Clean All Data ============

print("\n🧹 Cleaning data...")

cleaned_data = []
removed_count = 0

for item in raw_data:
    input_clean = clean_text(item.get("input", ""))
    output_clean = clean_text(item.get("output", ""))
    
    if is_valid_pair(input_clean, output_clean):
        cleaned_item = {
            "input": input_clean,
            "output": output_clean,
            "source": item.get("source", "unknown"),
            "category": item.get("category", categorize_conversation(input_clean))
        }
        cleaned_data.append(cleaned_item)
    else:
        removed_count += 1

print(f"✅ Cleaned: {len(cleaned_data)} valid pairs")
print(f"🗑️ Removed: {removed_count} invalid pairs")

# Category breakdown
print(f"\nCategory breakdown:")
cat_counts = Counter(item["category"] for item in cleaned_data)
for cat, count in cat_counts.most_common():
    print(f"  {cat}: {count}")


# ============ CELL 5: Convert to Training Formats ============

os.makedirs("training_data", exist_ok=True)

# --- FORMAT 1: Alpaca Format (for LoRA fine-tuning) ---
print("\n📝 Converting to Alpaca format...")

alpaca_data = []
for item in cleaned_data:
    alpaca_item = {
        "instruction": "Tu ek friendly, caring dost hai. User ke message ka natural, conversational reply de. Hinglish ya English mein reply kar, emojis use kar, aur har baar thoda alag reply de.",
        "input": item["input"],
        "output": item["output"]
    }
    alpaca_data.append(alpaca_item)

with open("training_data/train_alpaca.json", "w", encoding="utf-8") as f:
    json.dump(alpaca_data, f, ensure_ascii=False, indent=2)

print(f"  ✅ Saved: training_data/train_alpaca.json ({len(alpaca_data)} samples)")


# --- FORMAT 2: ChatML Format (for chat models) ---
print("\n📝 Converting to ChatML format...")

chatml_data = []
system_prompt = "Tu ek friendly, caring aur fun dost hai. Tu Hinglish (Hindi + English mix) mein baat karta hai. Tu hamesha caring, supportive aur entertaining hai. Tu emojis use karta hai. Tu har baar thoda alag reply deta hai taaki boring na lage."

for item in cleaned_data:
    chatml_item = {
        "conversations": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": item["input"]},
            {"role": "assistant", "content": item["output"]}
        ]
    }
    chatml_data.append(chatml_item)

with open("training_data/train_chatml.json", "w", encoding="utf-8") as f:
    json.dump(chatml_data, f, ensure_ascii=False, indent=2)

print(f"  ✅ Saved: training_data/train_chatml.json ({len(chatml_data)} samples)")


# --- FORMAT 3: ShareGPT Format (compatible with many trainers) ---
print("\n📝 Converting to ShareGPT format...")

sharegpt_data = []
for item in cleaned_data:
    sharegpt_item = {
        "conversations": [
            {"from": "system", "value": system_prompt},
            {"from": "human", "value": item["input"]},
            {"from": "gpt", "value": item["output"]}
        ]
    }
    sharegpt_data.append(sharegpt_item)

with open("training_data/train_sharegpt.json", "w", encoding="utf-8") as f:
    json.dump(sharegpt_data, f, ensure_ascii=False, indent=2)

print(f"  ✅ Saved: training_data/train_sharegpt.json ({len(sharegpt_data)} samples)")


# --- FORMAT 4: Simple Pairs (for keyword-based fallback) ---
print("\n📝 Converting to Simple Pairs format...")

simple_pairs = {}
for item in cleaned_data:
    key = item["input"].lower().strip()
    if key not in simple_pairs:
        simple_pairs[key] = []
    simple_pairs[key].append(item["output"])

with open("training_data/keyword_pairs.json", "w", encoding="utf-8") as f:
    json.dump(simple_pairs, f, ensure_ascii=False, indent=2)

print(f"  ✅ Saved: training_data/keyword_pairs.json ({len(simple_pairs)} unique inputs)")


# ============ CELL 6: Train/Validation Split ============

import random
random.seed(42)

# Shuffle
random.shuffle(alpaca_data)

# 90% train, 10% validation
split_idx = int(len(alpaca_data) * 0.9)
train_data = alpaca_data[:split_idx]
val_data = alpaca_data[split_idx:]

with open("training_data/train.json", "w", encoding="utf-8") as f:
    json.dump(train_data, f, ensure_ascii=False, indent=2)

with open("training_data/val.json", "w", encoding="utf-8") as f:
    json.dump(val_data, f, ensure_ascii=False, indent=2)

print(f"\n📊 Train/Val Split:")
print(f"  Train: {len(train_data)} samples")
print(f"  Validation: {len(val_data)} samples")


# ============ CELL 7: Data Quality Report ============

print("\n" + "="*50)
print("📊 FINAL DATA QUALITY REPORT")
print("="*50)

print(f"\n✅ Total clean pairs: {len(cleaned_data)}")
print(f"📁 Files generated:")
print(f"  1. training_data/train_alpaca.json - Alpaca format (LoRA training)")
print(f"  2. training_data/train_chatml.json - ChatML format (chat models)")
print(f"  3. training_data/train_sharegpt.json - ShareGPT format (various trainers)")
print(f"  4. training_data/keyword_pairs.json - Keyword lookup (fallback bot)")
print(f"  5. training_data/train.json - Training split (90%)")
print(f"  6. training_data/val.json - Validation split (10%)")

# Average lengths
avg_input = sum(len(item["input"]) for item in cleaned_data) / len(cleaned_data)
avg_output = sum(len(item["output"]) for item in cleaned_data) / len(cleaned_data)

print(f"\n📏 Average lengths:")
print(f"  Input: {avg_input:.1f} characters")
print(f"  Output: {avg_output:.1f} characters")

print(f"\n🎉 DATA CLEANING COMPLETE!")
print(f"   Ab Step 3 (Model Training) mein jaao! 🚀")
