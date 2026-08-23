# 🤖 AI Projects — Personal ChatGPT + Instagram Bot

## Yeh Repository Kya Hai?

Ismein 2 projects hain:

1. **ChatGPT Clone** — Apni khud ki ChatGPT jaisi website (trained model ke saath)
2. **Instagram AI Bot** — Instagram auto-reply bot (smart, varied replies)

---

## 📁 Project Structure

```
New/
├── chatgpt-clone/           ← ChatGPT jaisi website
│   ├── colab_fixed.py       ← ⭐ ALL-IN-ONE (Colab mein paste karo, sab ho jaayega!)
│   ├── app.py               ← Backend server (local use)
│   ├── requirements.txt     ← Dependencies
│   ├── Dockerfile           ← Docker deployment
│   ├── DEPLOY_GUIDE.md      ← Deployment instructions
│   ├── templates/
│   │   └── index.html       ← Main page
│   └── static/
│       ├── style.css        ← Dark/Light theme
│       └── script.js        ← Chat logic
│
├── instagram-ai-bot/        ← Instagram Auto-Reply Bot
│   ├── README.md            ← Full instructions
│   └── notebooks/
│       ├── 01_data_collection.py  ← Data collect
│       ├── 02_data_cleaning.py    ← Data clean
│       ├── 03_model_training.py   ← Model train
│       └── 04_instagram_bot.py    ← Bot run
│
└── README.md                ← Yeh file
```

---

## 🚀 Quick Start — ChatGPT Website (5 min mein live!)

### Google Colab pe:

1. [Google Colab](https://colab.research.google.com) open karo
2. **Runtime → Change Runtime Type → GPU (T4)**
3. Pehle ek cell mein run karo:
```python
!pip install -q unsloth flask flask-cors pyngrok requests datasets transformers trl peft accelerate bitsandbytes scipy
```
4. Restart Runtime (agar popup aaye)
5. Naye cell mein `chatgpt-clone/colab_fixed.py` ka code paste karo
6. Run karo → **Public URL milega!** 🎉

### Ya Direct GitHub se Colab mein:
```python
!git clone https://github.com/gitworld08210/New.git
%run New/chatgpt-clone/colab_fixed.py
```

---

## 🤖 Instagram Bot Setup

Full instructions: [instagram-ai-bot/README.md](instagram-ai-bot/README.md)

---

## 💰 Cost: ₹0 (Everything FREE!)

| Item | Cost |
|------|------|
| Google Colab GPU | Free |
| Model Training | Free |
| Hosting (ngrok) | Free |
| Ollama | Free |
| **Total** | **₹0** |

---

## ⚠️ Disclaimer

- ChatGPT clone: Educational purpose, personal use
- Instagram bot: Test account use karo, ban risk hai
- Model training: Free tier GPUs limited hain

---

**Made with ❤️**
