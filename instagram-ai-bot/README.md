# 🤖 Instagram AI Auto-Reply Bot — Complete Pipeline

## Apna AI Model Train Karo + Instagram Bot Banao (₹0 Cost!)

---

## 🎯 Yeh Kya Hai?

Ek complete system jo:
1. Social media se **real conversations collect** karta hai (log kaise baat karte hain)
2. Us data se **apna AI model train** karta hai (free, local)
3. Trained model ko **Instagram bot** se connect karta hai
4. Bot **smart, varied replies** deta hai — har baar alag!

---

## 📋 4 Steps — Sab Google Colab Pe (FREE)

| Step | File | Kya Karta Hai | Time |
|------|------|---------------|------|
| 1️⃣ | `01_data_collection.py` | Twitter/Reddit/Instagram se conversations collect | 10-15 min |
| 2️⃣ | `02_data_cleaning.py` | Data clean + training format mein convert | 2-3 min |
| 3️⃣ | `03_model_training.py` | Apna AI model train (LoRA fine-tuning) | 15-30 min |
| 4️⃣ | `04_instagram_bot.py` | Instagram auto-reply bot | Local pe run |

---

## 🚀 Quick Start

### Step 1: Google Colab Open Karo
1. [Google Colab](https://colab.research.google.com) jaao
2. New Notebook create karo
3. Runtime → Change Runtime Type → **GPU (T4)** select karo

### Step 2: Scripts Paste Karo
1. `01_data_collection.py` ka code paste karo → Run karo
2. `02_data_cleaning.py` ka code paste karo → Run karo  
3. `03_model_training.py` ka code paste karo → Run karo
4. Model download karo (GGUF file)

### Step 3: Local Machine Pe Bot Chalao
1. [Ollama](https://ollama.com) install karo
2. Trained model load karo Ollama mein
3. `04_instagram_bot.py` run karo
4. Bot auto-reply shuru kar dega! 🎉

---

## 📊 Data Collection Details

### Kahan Se Data Aata Hai:

| Source | Type | Quantity |
|--------|------|----------|
| **Twitter** | Public replies & threads | ~100-500 pairs |
| **Reddit** | Comment conversations | ~200-1000 pairs |
| **Manual** | Hand-written quality data | 90+ pairs (built-in) |
| **Augmented** | Variations of manual data | 150+ pairs |

### Categories Covered:
- ✅ Greetings (hi, hello, kaise ho)
- ✅ Status (kya kar rahe, how are you)
- ✅ Emotions (happy, sad, bored, angry)
- ✅ Time-based (good morning, good night)
- ✅ Food (khana khaya, hungry)
- ✅ Entertainment (movies, songs, games)
- ✅ Love/Romance (I love you, miss you)
- ✅ Compliments (cute, smart, amazing)
- ✅ Thanks/Sorry
- ✅ Goodbye
- ✅ Fun (jokes, facts, riddles)
- ✅ Health/Advice/Study

---

## 🧠 Model Training Details

| Setting | Value |
|---------|-------|
| Base Model | Llama 3.2 1B (or 3B/8B) |
| Method | LoRA Fine-tuning |
| Training Time | ~15-30 min (Colab T4) |
| Output Size | ~500MB (GGUF) |
| Cost | ₹0 (Colab Free Tier) |
| Quality | Very Good for casual chat |

---

## 🤖 Bot Features

- ✅ **Smart replies** — Context-aware, varied responses
- ✅ **Hinglish support** — Hindi + English mixed conversations
- ✅ **Emoji support** — Natural emojis in replies
- ✅ **Rate limiting** — Ban se bachne ke liye
- ✅ **Natural delays** — Human jaisa reply timing
- ✅ **Per-user history** — Yaad rakhta hai pichli baatein
- ✅ **Keyword fallback** — Agar AI fail ho toh bhi reply aayega
- ✅ **Ignore list** — Specific users ko ignore karo
- ✅ **Session persistence** — Restart pe re-login nahi karna padta

---

## ⚠️ Important Warnings

### 🚨 Instagram Ban Risk:
- **SIRF TEST/DUMMY ACCOUNT USE KARO**
- Main account pe mat chalao — ban ho sakta hai
- Rate limits follow karo (20 replies/hour max)
- Natural delays rakho (3-15 seconds)

### 🔒 Security:
- Password code mein directly mat rakho (environment variables use karo)
- Session file (.json) ko git mein mat daalo
- 2FA temporarily off karna padega

### ⚖️ Legal/Ethical:
- Automation Instagram ToS ke against hai
- Educational purpose ke liye hai
- Commercial use mat karo without proper API access
- Dusre logo ko batao ki bot se baat ho rahi hai

---

## 📁 Project Structure

```
instagram-ai-bot/
├── notebooks/
│   ├── 01_data_collection.py    ← Step 1: Data collect
│   ├── 02_data_cleaning.py      ← Step 2: Data clean
│   ├── 03_model_training.py     ← Step 3: Model train
│   └── 04_instagram_bot.py      ← Step 4: Bot run
├── data/                         ← Collected raw data
├── models/                       ← Trained model files
├── bot/                          ← Bot configuration
└── README.md                     ← Yeh file
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Colab GPU nahi mil raha | Runtime → Change Runtime → GPU. Agar nahi mila toh kuch der baad try karo |
| Ollama install nahi ho raha | Windows pe: ollama.com se download karo |
| Instagram login fail | 2FA off karo, VPN try karo, naya account try karo |
| Bot ban ho gaya | Naya account banao, delays badha do, replies kam karo |
| Model acche replies nahi de raha | Zyada data add karo (2000+ pairs), epochs badha do |
| Out of memory (Colab) | Batch size kam karo (2), ya smaller model use karo |

---

## 🚀 Future Improvements

- [ ] Multi-language support (pure Hindi, pure English)
- [ ] Image/Reel response support
- [ ] Sentiment analysis (mood detect karke reply)
- [ ] Scheduled messages (good morning auto)
- [ ] Analytics dashboard (kitne replies, response time)
- [ ] WhatsApp integration (same model)
- [ ] Telegram bot (safest platform)

---

## 💡 Tips for Better Results

1. **Zyada data = Better model** — 2000+ pairs try karo
2. **Quality > Quantity** — Spam data se model kharab hota hai
3. **Apni chats use karo** — WhatsApp export karke training mein daalo (best quality!)
4. **Regular update** — Naya data add karke retrain karo
5. **Test pehle** — Bot start karne se pehle test mode mein check karo

---

## 📞 Need Help?

Agar koi step mein problem aaye toh:
1. Error message copy karo
2. Google Colab ka screenshot lo
3. Issue describe karo

---

**Made with ❤️ for learning purposes**

⚠️ Disclaimer: Yeh project educational purpose ke liye hai. Instagram automation unki Terms of Service ke against hai. Apni responsibility pe use karo.
