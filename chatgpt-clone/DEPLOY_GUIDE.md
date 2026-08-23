# 🚀 DEPLOYMENT GUIDE — MyAI ChatGPT Clone

## Apni ChatGPT website ko live kaise karo (FREE!)

---

## 📋 3 Ways to Deploy:

| Method | Cost | Difficulty | Best For |
|--------|------|-----------|----------|
| 🟢 **Google Colab** | ₹0 | Easiest | Testing, temporary use |
| 🔵 **Local Machine** | ₹0 | Medium | Personal use, always-on |
| 🟣 **Cloud (Render/Railway)** | ₹0 | Medium | Share with others, 24/7 |

---

## 🟢 Method 1: Google Colab (EASIEST — Recommended for Start)

### Steps:
1. **Google Colab** open karo: [colab.research.google.com](https://colab.research.google.com)
2. **New Notebook** create karo
3. **Runtime → Change Runtime Type → GPU (T4)** select karo
4. **`colab_train_and_deploy.py`** ka code paste karo
5. **Cell by cell run karo** (Cell 1 → Cell 2 → ... → Cell 6)
6. **Public URL milega** (ngrok) — kisi ko bhi share kar sakte ho! 🎉

### Ngrok Setup (Optional but Recommended):
1. [ngrok.com](https://ngrok.com) pe free account banao
2. Dashboard se **Auth Token** copy karo
3. Code mein `NGROK_AUTH_TOKEN = "your_token"` mein paste karo
4. Ab URL stable rahega!

### Limitations:
- Colab **90 min idle** ke baad disconnect ho jaata hai
- Free GPU **12 hours** max per session
- URL har baar naya milega (ngrok free tier)

### Tips:
- Tab active rakho (koi video chala do background mein)
- Colab Pro (₹750/month) loge toh zyada stable rehta hai

---

## 🔵 Method 2: Local Machine (PERMANENT — Always Available)

### Requirements:
- Computer with **8GB+ RAM**
- Windows / Mac / Linux
- Internet connection (sirf setup ke liye)

### Step-by-Step Setup:

#### 1. Ollama Install Karo

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
- [ollama.com/download](https://ollama.com/download) se download karo
- Install karo (next → next → finish)

#### 2. Model Download Karo

```bash
# Base model (agar trained model nahi hai):
ollama pull llama3.2:1b

# Ya trained model load karo (agar Colab se GGUF export kiya):
# Pehle Modelfile banao:
cat > Modelfile << 'EOF'
FROM ./your_model.gguf

SYSTEM "Tu ek friendly, caring aur fun dost hai. Tu Hinglish mein baat karta hai. Tu emojis use karta hai. Tu short natural replies deta hai."

PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER num_predict 150
PARAMETER repeat_penalty 1.2
EOF

# Model create karo:
ollama create mybot -f Modelfile
```

#### 3. Website Files Setup Karo

```bash
# Folder create karo
mkdir myai-website
cd myai-website

# Files copy karo (jo maine banai hain):
# - app.py
# - requirements.txt
# - templates/index.html
# - static/style.css
# - static/script.js

# Dependencies install karo
pip install -r requirements.txt
```

#### 4. Server Start Karo

```bash
# Terminal 1: Ollama (agar already nahi chal raha)
ollama serve

# Terminal 2: Website
python app.py
```

#### 5. Browser Open Karo

```
http://localhost:5000
```

🎉 **Done! Tumhari ChatGPT website local pe chal rahi hai!**

### Auto-Start (Computer on hote hi chale):

**Linux (systemd):**
```bash
# /etc/systemd/system/myai.service
[Unit]
Description=MyAI Chat Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/myai-website
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable myai
sudo systemctl start myai
```

**Windows (Task Scheduler):**
1. Task Scheduler open karo
2. Create Basic Task → "MyAI Server"
3. Trigger: "When the computer starts"
4. Action: Start a program → `python app.py`
5. Working directory set karo

---

## 🟣 Method 3: Cloud Deployment (24/7 FREE Hosting)

### Option A: Render.com (RECOMMENDED — Easiest Cloud)

1. [render.com](https://render.com) pe free account banao
2. GitHub pe apna code push karo
3. Render pe "New Web Service" create karo
4. Settings:

```
Build Command:    pip install -r requirements.txt
Start Command:    gunicorn app:app --bind 0.0.0.0:$PORT
Environment:      Python 3
Plan:             Free
```

5. Environment Variables:
```
OLLAMA_URL = https://your-ollama-server.com  (ya keyword mode use karo)
MODEL_NAME = mybot
```

⚠️ **Note:** Render free tier pe Ollama nahi chal sakta (GPU nahi hai). 
**Solution:** Keyword-based mode use karo (app.py mein built-in hai) ya:
- Groq API (free, fast) use karo as alternative
- Ya separately GPU server pe Ollama chala ke connect karo

#### Render with Keyword Mode (Simplest):
App automatically keyword-based fallback use karega agar Ollama connect nahi hota.
Yeh bilkul free mein 24/7 chalega!

---

### Option B: Railway.app

1. [railway.app](https://railway.app) pe account banao
2. "New Project" → "Deploy from GitHub"
3. Apna repo select karo
4. Railway automatically detect karega Python app

```
# railway.toml (optional)
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn app:app --bind 0.0.0.0:$PORT"
```

Free tier: $5 credit/month (enough for a chat bot!)

---

### Option C: Hugging Face Spaces (FREE + GPU!)

Best option agar model ko bhi cloud pe chalana hai:

1. [huggingface.co/spaces](https://huggingface.co/spaces) pe jaao
2. "Create Space" → Gradio/Docker
3. Files upload karo
4. Free GPU available hai! 🎉

```dockerfile
# Dockerfile for HF Spaces
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["python", "app.py"]
```

Change `app.py` mein port to 7860:
```python
app.run(host='0.0.0.0', port=7860)
```

---

### Option D: Vercel (Frontend only + API)

Sirf frontend deploy karo, backend separately:

1. Frontend (HTML/CSS/JS) → Vercel pe deploy
2. Backend (Flask) → Render pe deploy
3. Frontend ko backend API URL se connect karo

```javascript
// script.js mein change:
const API_URL = "https://your-render-backend.onrender.com";

// fetch call:
const response = await fetch(`${API_URL}/api/chat`, {...});
```

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `MODEL_NAME` | `mybot` | Tumhara model name |
| `PORT` | `5000` | Server port |

---

## 📱 Mobile Access (Same WiFi)

Agar local machine pe chal raha hai aur phone se access karna hai:

1. Computer ka IP address find karo:
   - Windows: `ipconfig` (IPv4 address dekho)
   - Mac/Linux: `ifconfig` ya `ip addr`
   
2. Phone ke browser mein type karo:
   ```
   http://192.168.1.XX:5000
   ```
   (XX = tumhara IP)

3. Done! Phone pe ChatGPT jaisi website! 📱

---

## 🌐 Custom Domain (Optional)

Free domain options:
- **Freenom**: `.tk`, `.ml`, `.ga` domains (free)
- **DuckDNS**: `yourname.duckdns.org` (free dynamic DNS)
- **Cloudflare Tunnel**: Free, secure, custom domain

### Cloudflare Tunnel (Best Free Option):

```bash
# Install cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared

# Login
./cloudflared tunnel login

# Create tunnel
./cloudflared tunnel create myai

# Run
./cloudflared tunnel run --url http://localhost:5000 myai
```

Ab tumhari website `myai.your-domain.com` pe live! 🎉

---

## 📊 Comparison Table

| Feature | Colab | Local | Render | HF Spaces |
|---------|-------|-------|--------|-----------|
| Cost | ₹0 | ₹0 | ₹0 | ₹0 |
| GPU | ✅ T4 | ❌ (CPU) | ❌ | ✅ |
| 24/7 Uptime | ❌ | ✅ (if PC on) | ✅ | ✅ |
| Custom Domain | ❌ | ✅ | ✅ | ❌ |
| AI Model | ✅ Full | ✅ Ollama | ⚠️ Keyword only | ✅ Full |
| Share URL | ✅ ngrok | ⚠️ Same WiFi | ✅ Public | ✅ Public |
| Setup Time | 5 min | 15 min | 10 min | 10 min |

---

## 🎯 Meri Recommendation:

1. **Start:** Google Colab (testing ke liye)
2. **Daily use:** Local machine + Ollama
3. **Share with others:** Render.com (keyword mode) ya HF Spaces (with model)

---

## ❓ Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| Colab disconnect | Tab active rakho, Colab Pro consider karo |
| Ollama not responding | `ollama serve` run karo pehle |
| Port already in use | `lsof -i :5000` se check karo, kill karo |
| Ngrok URL not working | Auth token add karo, free tier limit check karo |
| Model slow on CPU | Smaller model use karo (`llama3.2:1b`) |
| Render sleeping | Free tier 15 min inactivity pe sleep hota hai (normal) |
| Phone se access nahi ho raha | Same WiFi check karo, firewall check karo |

---

## 🚀 Quick Start Summary

### Sabse Fast Way (5 minutes):
```
1. Google Colab open karo
2. GPU enable karo (Runtime → GPU)
3. colab_train_and_deploy.py paste karo
4. Run karo
5. URL copy karo → DONE! 🎉
```

### Permanent Way (15 minutes):
```
1. Ollama install karo
2. ollama pull llama3.2:1b
3. Website files download karo
4. pip install -r requirements.txt
5. python app.py
6. http://localhost:5000 → DONE! 🎉
```

---

**Made with ❤️ — Tumhari apni ChatGPT, bilkul FREE!**
