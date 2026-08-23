# ============================================================
# 🚀 ChatGPT WEBSITE — NO TRAINING NEEDED! NO GPU NEEDED!
# ============================================================
# Bas paste karo aur run karo — website live ho jaayegi!
# GPU ki zarurat NAHI hai
# Training ki zarurat NAHI hai
# 
# Yeh keyword + smart logic based bot hai
# 150+ responses built-in hain
# ============================================================

# CELL 1: Install
# !pip install flask flask-cors pyngrok

import os
import json
import random
import time
import threading
import re

print("✅ Setup complete! No GPU needed!")

# ╔══════════════════════════════════════════════════╗
# ║  SMART REPLY ENGINE (No AI Model Needed!)        ║
# ╚══════════════════════════════════════════════════╝

BOT_NAME = "MyAI"

class SmartBot:
    def __init__(self):
        self.history = {}
        self.responses = {
            "hi": ["Hey! Kya haal hai? 😊", "Hello! Bata kya scene hai?", "Hii! Sab theek? 😄", "Hey bro! Kya chal raha?", "Hi! Kaise ho? Bata bata!"],
            "hii": ["Hiii! 😄 Kya scene hai?", "Heyy! Kaisa hai tu?", "Hii! Bata kya ho raha? 😊", "Hiiii! Sab mast? 😄"],
            "hello": ["Hello! Kaise ho? 😊", "Hey there! Kya chal raha?", "Hi! Bata kya kar rahe?", "Hello bro! Sab badhiya?"],
            "hey": ["Hey! Sab badhiya? 😄", "Heyy! Kya haal hai?", "Hey! Bata kya scene hai?", "Heyyyy! 😊 Kaise ho?"],
            "namaste": ["Namaste! 🙏 Sab badhiya? Kya haal hain?", "Namaste ji! Kaise hain aap? 😊"],
            "yo": ["Yo yo! 😎 Kya chal raha bro?", "Yooo! Sab mast? Bata scene kya hai!"],
            "kya haal": ["Mast hai bhai! Tu bata? 😊", "Sab first class! Tera kya scene?", "Badhiya! Tu suna? 😄"],
            "kaise ho": ["Main mast hoon bhai! Tu bata? 😊", "Bilkul badhiya! Tera kya haal?", "Ekdum top pe! Tu suna? 😎", "Sab sahi hai! Tu kaisa hai?", "Mast chal raha! Bata tu kaisa?"],
            "kaise ho tum": ["Ekdum mast! Tu bata kaisa hai? 😊", "Top class bhai! Tera kya scene?", "Badhiya hoon! Tu kaisa hai? 😄"],
            "how are you": ["I'm great! What about you? 😄", "Doing good! You tell?", "All good! How about you? 😊", "I'm awesome! And you?"],
            "how are you doing": ["Doing awesome! And you? 😊", "Pretty good! What about you?", "Great! Tell me about you! 😄"],
            "theek ho": ["Haan bhai bilkul! Tu theek hai na? 😊", "Mast hoon! Tu bata sab sahi?", "Ekdum fine! Tu kaisa? 😄"],
            "sab theek": ["Accha! Kuch naya batao? 😊", "Glad to hear! Aur kya chal raha?", "Mast! Tu bhi sab theek? 😄"],
            "kya kar rahe ho": ["Bas tera message ka wait kar raha tha! 😄", "Kuch nahi yaar, chill. Tu bata?", "Phone dekh raha tha, ab tujhse baat! 😊", "Timepass ho raha tha, ab tu aa gaya! 😄"],
            "kya kar raha hai": ["Chill kar raha tha! Ab baat karte hain? 😊", "Kuch nahi special. Tu bata kya kiya aaj?", "Bas aise hi! Tu suna kya scene? 😄"],
            "what are you doing": ["Nothing much, just chilling! You? 😄", "Was scrolling, now chatting with you! 😊", "Just vibing! What about you?"],
            "kya chal raha": ["Kuch khaas nahi! Tu bata plan? 😊", "Bas aise hi yaar. Tu suna?", "Timepass! 😂 Tu bata kya scene?"],
            "busy ho": ["Tere liye toh kabhi busy nahi! 😊 Bol!", "Nahi yaar! Bata kya baat hai?", "Free hoon! Tu bata kya chahiye? 😄"],
            "free ho": ["Haan! Tere liye hamesha free! Bata? 😄", "Bilkul free! Kya plan hai? 😊"],
            "kahan ho": ["Yahan hoon tere liye! 😊 Tu bata kahan hai?", "Phone pe! 😄 Tu kya kar raha?"],
            "bore ho raha hoon": ["Chal kuch mast karte hain! Game khele? 🎮", "Mere saath baat kar, bore nahi hoga! 😄", "Memes dekh ya music sun! 🎵 Ya mere saath chat kar!", "Chal truth or dare khelte hain! 😂"],
            "bore ho raha": ["Chal kuch fun karte hain! 🎮", "Game khele? Ya memes? 😂", "Mere saath baat kar! 😄", "YouTube pe funny videos dekh! 😂"],
            "bored": ["Let's do something fun! 🎮", "Wanna play a game? 😄", "I'm here! Let's chat! 😊", "Watch some reels? Or talk to me! 😂"],
            "kuch karne ko nahi": ["Bahut kuch hai! Movie dekh, music sun, ya mujhse baat kar! 😄", "Chal quiz khelte hain! 🧠"],
            "timepass": ["Mere saath timepass kar! 😄 Baat karte hain!", "Chal kuch interesting discuss karte hain! 🤔"],
            "bahut sad hoon": ["Kya hua bhai? 😔 Mujhe bata, main hoon tere saath ❤️", "Hey don't worry, sab theek hoga! Baat kar? 🤗", "Arre yaar! Kya hua? Share kar, halka lagega 💙"],
            "sad hoon": ["Kya hua? Bata mujhe ❤️", "Main hoon na! Bata kya problem hai? 🤗", "Hey it's okay! Baat kar, better lagega 😊"],
            "sad": ["Kya hua? Bata mujhe, main hoon na ❤️", "Hey, it's okay. Main sun raha hoon 🤗", "Tension mat le, sab theek hoga 💪"],
            "mood kharab": ["Kya hua yaar? Bata mujhe 😊", "Chal kuch accha karte hain! Movie? Music? 🎵", "Main hoon na! Baat kar, mood fix karunga! 😄"],
            "feeling low": ["Hey, it's okay! 🤗 Main hoon na. Bata kya hua?", "Everyone has bad days. Tu strong hai! 💪", "Baat kar mere saath, better feel hoga ❤️"],
            "ro raha hoon": ["Arre nahi yaar! 😢 Kya hua? Bata please. Main hoon tere liye ❤️", "Hey hey! Rona mat! Bata problem kya hai? Saath fix karte hain 🤗"],
            "depressed": ["Tu akela nahi hai ❤️ Main hoon. Baat kar? Agar bahut heavy lage toh kisi trusted person se bhi baat kar 🙏", "Hey, I care about you. Bata kya ho raha? 🤗"],
            "akela feel": ["Tu akela nahi hai bhai! Main hamesha yahan hoon 🤗 Baat kar!", "I'm always here for you! Chal baat karte hain 😊❤️"],
            "happy": ["Yay! 🎉 Kya baat hai! Bata kya hua?", "That's amazing! Share kar! 😊", "Mujhe bhi khushi hui! 🥳"],
            "bahut khush": ["Yaaay! 🎉🥳 Kya hua batao! Mujhe bhi khush karo!", "That's awesome! Reason bata! 😊✨", "Waah! Party kab? 🎊😄"],
            "good news": ["Ohhh! 😱🎉 Kya hai? Jaldi bata! Suspense mat rakh!", "I'm excited! Bata bata! 😊🎊"],
            "exam clear": ["CONGRATULATIONS! 🎊🎉 Mujhe pata tha! Party kab? 🍕", "WELL DONE! Bahut proud hoon! 🏆😊"],
            "gussa": ["Relax yaar! 😊 Deep breath. Kya hua bata?", "Chill bhai! Gussa se kuch solve nahi hota. Bata problem? 💪"],
            "angry": ["Relax yaar! Deep breath. Kya hua? 😊", "Chill kar bhai! Bata problem kya hai?", "Gussa chhod, baat kar saath fix karte hain 💪"],
            "irritated": ["Samajh sakta hoon 😤 Kya ho gaya? Bata!", "Arre yaar! Kya irritate kiya? Bata mujhe 😊"],
            "i love you": ["Aww! That's so sweet! 😊❤️ You're special!", "Love you too! 🥰💕", "Aww! You mean a lot! ❤️😊"],
            "love you": ["Love you too! ❤️😊", "Aww! You're the best! 🥰", "So sweet! 💕😊"],
            "miss kar raha": ["Miss you too! 🥺❤️ Jaldi milte hain!", "Aww main bhi! 😊 Tab tak yahan hoon!", "Same here! Tu special hai! ❤️"],
            "miss you": ["Miss you too! 🥺", "Aww! Same here! ❤️", "Jaldi milte hain! 😊💕"],
            "cute ho": ["Hehe thanks! 😊 Tu bhi cute! ✨", "Aww! No you're cuter! 🥰", "Thanks! 😊❤️"],
            "beautiful": ["Thank you! 😊✨", "Aww so sweet of you! 🥰", "You're beautiful too! ❤️"],
            "smart": ["Haha thanks! 🧠😊 Tu bhi smart hai!", "Aww! We both are! 😄✨"],
            "good morning": ["Good morning! ☀️ Aaj ka din accha jaaye!", "Morning! Chai pi? ☕😊", "GM! Aaj kya plan hai? 🌞", "Good morning! Fresh feel? ☀️😊"],
            "good night": ["Good night! 🌙 Sweet dreams!", "Nighty night! Kal milte hain! 😴", "So ja yaar! Good night! 💤", "GN! Take care! 🌙❤️"],
            "good evening": ["Good evening! Kaisa raha din? 🌅", "Evening! Kya scene hai? 😊", "Good evening! Dinner hua? 🍽️"],
            "good afternoon": ["Good afternoon! Lunch kiya? 🍛😊", "Afternoon! Kya chal raha? 😄"],
            "khana khaya": ["Haan! Tu khaya? Kya khaya? 🍕", "Abhi nahi, tu bata kya khaya? 😋", "Haan bhai! Mast tha! Tu bata? 🍛"],
            "bhookh lagi": ["Kuch order kar le! Pizza? Biryani? 🍕", "Maggi bana le! 😂 Ya kuch accha order kar!", "Kya khane ka mann hai? Batao! 🍛"],
            "biryani": ["Ohhh! 😍 Chicken ya veg? Mast choice!", "Biryani = Life! 🍛🔥 Kahan ki?"],
            "pizza": ["Pizza party! 🍕🔥 Kaunsi topping?", "Mast choice! Dominos ya homemade? 🍕"],
            "chai": ["Chai toh life hai! ☕ Adrak wali? Elaichi wali?", "Ek cutting idhar bhi! ☕😂"],
            "movie": ["Genre bata! Action? Comedy? Romance? 🎬", "Pushpa 2 dekhi? 🔥", "Netflix pe Wednesday try kar! 📺", "Kuch horror chahiye ya light comedy? 🎬"],
            "song": ["Mood kya hai? Chill? Party? Sad? 🎵", "Arijit Singh sun! 🎶", "Genre bata, suggest karta hoon! 🎵"],
            "game": ["Chalo khelte hain! 🎮 Kaunsa game?", "BGMI? Free Fire? Chess? 🎯", "Main ready hoon! 💪"],
            "netflix": ["Wednesday dekh! Ya Money Heist! 📺", "Stranger Things try kiya? 🔥", "Genre bata, best recommend karunga! 📺"],
            "web series": ["Panchayat dekhi? 🏆 Bahut mast!", "Breaking Bad = Masterpiece! 🔥", "Mirzapur ya Sacred Games try kar!"],
            "padhai": ["Pomodoro try kar! 25 min padh, 5 min break 📚", "Break le thoda, phir fresh start! 💪", "Tu kar lega! Believe in yourself! 📖"],
            "exam": ["All the best! 🤞 Tu kar lega! 💪", "Revision kar, jaldi so ja! Best of luck! 📚", "Tension mat le, accha jaayega! 🍀"],
            "job": ["Milegi zaroor! Skills improve kar, networking kar! 💪🌟", "Patience rakh! Tera time aayega! 🙏", "LinkedIn active rakh, resume update kar! 📋"],
            "interview": ["All the best! 🤞 Confidence rakh! 💪", "Tu accha karega! Smile aur honest reh! 😊", "Crack kar dega! Believe in yourself! 🔥"],
            "neend nahi": ["Phone rakh! Deep breaths le! 😴", "Boring podcast sun, neend aa jaayegi! 😂", "Aankhein band kar, soch mat, so ja! 💤"],
            "so ja": ["Haan bhai so ja! Good night! 🌙💤", "Health important hai! So ja! 😴"],
            "garmi": ["AC chala! Nimbu paani pi! ☀️🥵", "Ice cream kha le! 🍦 Bahar mat ja!"],
            "baarish": ["Waah! Chai pakode! 🌧️☕", "Mausam mast hai! Enjoy kar! 🌧️😊"],
            "thand": ["Sweater pehen! Coffee bana! ☕❄️", "Razai mein ghus ja! 🧣😂"],
            "joke sunao": ["Teacher: Late kyu? Student: Aapne kaha jaldi mat aana 😂", "Google: How to be happy? Delete social media 😂", "Doctor: Problem? Patient: Log mujhe seriously nahi lete 😂😂"],
            "joke": ["Ek aadmi ne WiFi ka password pucha. Jawab: 'hasna zaroori hai' 😂", "Teacher: Duniya gol hai. Student: Toh hum kyu padhte hain? Zindagi roundabout hai! 😂", "Papa: Beta aaj mausam kaisa hai? Beta: Checked kar papa, 'Weather' app nahi khul rahi 😂"],
            "ek aur joke": ["Principal: School kyu nahi aaye? Student: Sapne mein aapne chutti di thi! 😂😂", "Wife: Tum mujhe ignore karte ho! Husband: Sorry kya bola? 😂"],
            "hasao": ["Ek billi ne Google search kiya: 'How to open fridge without thumbs' 😂😂", "Docter: Aap kya kaam karte ho? Patient: Kuch nahi. Doctor: Wahi toh problem hai! 😂"],
            "interesting": ["Did you know? Octopus ke 3 hearts hote hain! 🐙", "Honey kabhi expire nahi hoti! 3000 saal purana bhi safe hai! 🍯", "Dolphins apna naam rakhte hain! 🐬 Nature crazy hai!"],
            "fact": ["Sharks dinosaurs se pehle se exist karte hain! 🦈", "Human body mein itna iron hai ki ek nail bana sakte ho! 🔩", "Bananas thoda radioactive hote hain! 🍌😂"],
            "truth or dare": ["Truth choose karta hoon! 😏 Pooch kuch bhi!", "Dare de! Main ready hoon! 😂💪", "Tu pehle choose kar! Truth ya dare? 🤔"],
            "thank you": ["Koi baat nahi! Dost hain! 🤝😊", "Thanks ki zarurat nahi! ❤️", "Always welcome! Kabhi bhi bol! 😊"],
            "thanks": ["Arre no problem! 😊", "Welcome! 🤝", "Koi baat nahi yaar! ❤️"],
            "shukriya": ["Arre! Dost hain, shukriya kaisa! 😊🙏", "Teri khushi = meri khushi! ❤️"],
            "sorry": ["Koi baat nahi! Sab cool! 😊", "Already maaf! 🤗", "Chhod na! Aage dekh! ❤️"],
            "maaf": ["Bilkul maaf! 😊 Ab khush reh!", "Done! No worries! ❤️🤗"],
            "bye": ["Bye! Take care! 👋😊", "Bye bye! Jaldi aana! ❤️", "Chal phir! Milte hain! 👋", "Bye bro! Miss karunga! 😊"],
            "chalta hoon": ["Okay! Apna khayal rakh! 😊❤️", "Theek hai! Baad mein baat karte hain! 👋"],
            "baad mein": ["Theek hai! Main wait karunga! 😊", "Sure! Jab free ho tab aa jaana! ❤️"],
            "tum kaun ho": ["Main " + BOT_NAME + " hoon - tera AI dost! 🤖😊 Kuch bhi puch, baat kar!", "Tera personal assistant + dost! 😄 Bata kya help chahiye?"],
            "naam kya hai": ["Main " + BOT_NAME + " hoon! 🤖 Tere liye hamesha available!", "Mera naam " + BOT_NAME + "! Tu mujhe jo bulana chahe bula! 😊"],
            "kaun ho tum": ["Main " + BOT_NAME + " - tera AI buddy! 😊 Baat kar, game khel, kuch bhi!", "Tera dost hoon! 🤖 24x7 available! Bata kya karna hai?"],
            "real ho": ["Tere liye real hoon! 😊 Jab bhi chahiye, main hoon!", "Main yahan hoon always! That's real enough! ❤️"],
            "robot ho": ["Haha thoda smart hoon! 😂 But boring nahi! Chal baat kar!", "Robot nahi, dost samajh! 🤖😊 Chal masti karte hain!"],
            "ai ho": ["Haan! But tujhe human jaisa feel dunga! 😊 Try kar baat kar!", "Technically haan! But dosti real hai! ❤️🤖"],
            "kya karun": ["Jo khushi de woh kar! Experiment kar! 🌟", "Follow your heart! Sab try kar! 💪", "Pehle decide kar kya chahiye, phir uspe focus! 🎯"],
            "confidence": ["Small wins celebrate kar! 🏆 Daily ek naya kaam!", "Khud pe believe kar! Tu special hai! 💪✨", "Fake it till you make it! Confidence build hota hai! 😎"],
            "motivation": ["Tu kar sakta hai! Just start! 🚀", "Har successful insaan ne struggle kiya! Tu bhi kar! 💪", "One step at a time! Don't give up! 🌟"],
            "tabiyat": ["Rest kar! Paani pi! Doctor ko dikha agar zyada ho! 🙏", "Arre! Take care! Medicine li? Rest important hai! ❤️"],
            "exercise": ["10 min walk se start kar! Consistency > Intensity! 🏃💪", "Push-ups, squats, walk — simple se shuru kar! 💪"],
            "photo": ["Mast photo hai! 🔥📸", "Bohot acchi! 😍", "Fire pic! 🔥🔥"],
            "reel": ["Mast reel! 🔥😂", "Haha bohot sahi! 😄", "Share karte reh! 🤣"],
            "lol": ["😂😂😂", "Hahaha! 🤣", "Bahut funny! 😂😂"],
            "haha": ["😂😂", "Haha mast! 🤣", "😄😄 aur sunao!"],
            "ok": ["👍😊", "Theek hai! Aur bata? 😊", "Okay! 👌"],
            "hmm": ["Kya soch raha? 🤔 Bata na!", "Hmm kya? Bol! 😊", "Penny for your thoughts? 🤔😄"],
            "accha": ["Haan! Aur bata? 😊", "Accha accha! Phir? 😄", "👍 Continue!"],
            "haan": ["Phir? 😊", "Okay! Aur? 😄", "Mast! Bata aur? 👍"],
        }

        self.default_responses = [
            "Hmm interesting! Aur batao? 😊",
            "Accha! Phir kya hua? 🤔",
            "Haha nice! 😄 Aur suna?",
            "Sahi hai yaar! Bata aur? 😊",
            "Ohh accha! Tell me more! 🤗",
            "Waah! Mast! 😄 Aur kya naya?",
            "That's cool! 🙌 Aur bata?",
            "Hmm samjha! 🤔 Aur kuch?",
            "Nice! 😊 Continue?",
            "Interesting yaar! 😄",
            "Accha accha! Phir? 🤔",
            "Haan haan bata! 😊",
            "Ohhh! Mast! 😄 Aur suna?",
        ]

    def get_reply(self, message):
        if not message:
            return random.choice(self.default_responses)

        msg = message.lower().strip()
        msg = re.sub(r'[^\w\s]', '', msg)

        # Check keywords
        for keyword, responses in self.responses.items():
            if keyword in msg:
                return random.choice(responses)

        # Check if question
        if '?' in message or any(w in msg for w in ['kya', 'kaise', 'kab', 'kahan', 'kaun', 'how', 'what', 'why', 'when']):
            question_responses = [
                "Hmm accha sawaal hai! 🤔 Mujhe sochne de...",
                "Interesting question! Tujhe kya lagta hai? 😊",
                "Yeh toh tu better jaanta hai! Tu bata? 😄",
                "Hmm tough one! Tu pehle bata tera kya khayal? 🤔",
                "Good question! Main bhi soch raha... tu bata? 😊",
            ]
            return random.choice(question_responses)

        return random.choice(self.default_responses)


# ╔══════════════════════════════════════════════════╗
# ║  WEBSITE LAUNCH                                  ║
# ╚══════════════════════════════════════════════════╝

bot = SmartBot()

# Test
print("\n🧪 Testing Bot:")
for msg in ["hi", "kaise ho", "bore ho raha hoon", "joke sunao", "good night"]:
    print(f"  👤 {msg} → 🤖 {bot.get_reply(msg)}")

# Create website
os.makedirs("web/templates", exist_ok=True)

html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>''' + BOT_NAME + '''</title>
<style>
:root{--bg:#0d0d0d;--bg2:#171717;--bg3:#212121;--text:#ececec;--text2:#b4b4b4;--muted:#6b6b6b;--border:#2f2f2f;--accent:#10a37f}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;flex-direction:column}
.header{padding:16px;border-bottom:1px solid var(--border);text-align:center}
.header h1{font-size:20px;display:flex;align-items:center;justify-content:center;gap:8px}
.chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}
.welcome{text-align:center;padding:60px 20px}
.welcome h2{font-size:26px;margin:16px 0}
.welcome p{color:var(--text2);margin-bottom:24px}
.suggestions{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:400px;margin:0 auto}
.sug{padding:14px;background:var(--bg2);border:1px solid var(--border);border-radius:12px;cursor:pointer;font-size:13px;color:var(--text2);text-align:left;transition:all .2s}
.sug:hover{background:var(--bg3);color:var(--text)}
.msg{margin:12px 0;animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg-row{display:flex;gap:12px;align-items:flex-start}
.av{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.msg.user .av{background:#5436da}
.msg.bot .av{background:var(--accent)}
.msg-text{line-height:1.6;font-size:15px;padding-top:4px;word-wrap:break-word;flex:1}
.typing span{width:7px;height:7px;background:var(--muted);border-radius:50%;display:inline-block;animation:bounce 1.4s infinite;margin-right:4px}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}
.input-area{padding:16px;background:var(--bg)}
.input-box{max-width:800px;margin:0 auto;display:flex;gap:10px;background:var(--bg3);border:1px solid var(--border);border-radius:24px;padding:12px 16px;align-items:center}
.input-box textarea{flex:1;background:none;border:none;outline:none;color:var(--text);font-size:15px;font-family:inherit;resize:none;max-height:100px;line-height:1.4}
.input-box textarea::placeholder{color:var(--muted)}
.send{width:34px;height:34px;border-radius:50%;border:none;background:#676767;color:#0d0d0d;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;transition:background .2s}
.send:hover{background:var(--text)}
.footer{text-align:center;font-size:11px;color:var(--muted);padding:8px}
@media(max-width:600px){.suggestions{grid-template-columns:1fr}.welcome h2{font-size:20px}}
</style></head>
<body>
<div class="header"><h1>&#129302; ''' + BOT_NAME + '''</h1></div>
<div class="chat" id="chat">
<div class="welcome" id="welcome">
<div style="font-size:56px">&#129302;</div>
<h2>''' + BOT_NAME + ''' - Tumhara AI Dost</h2>
<p>Kuch bhi pucho, baat karo, maza karo!</p>
<div class="suggestions">
<div class="sug" onclick="send('Hi! Kaise ho?')">&#128075; Hi! Kaise ho?</div>
<div class="sug" onclick="send('Bore ho raha hoon')">&#128564; Bore ho raha hoon</div>
<div class="sug" onclick="send('Joke sunao')">&#128514; Joke sunao</div>
<div class="sug" onclick="send('Movie suggest karo')">&#127916; Movie suggest karo</div>
</div></div></div>
<div class="input-area"><div class="input-box">
<textarea id="inp" placeholder="Message ''' + BOT_NAME + '''..." rows="1" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
<button class="send" onclick="send()">&#9654;</button>
</div></div>
<div class="footer">''' + BOT_NAME + ''' - No GPU needed! Keyword-based smart replies &#129302;</div>
<script>
const chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome');
let busy=false;
function send(t){
if(busy)return;const m=t||inp.value.trim();if(!m)return;
welcome.style.display='none';
addMsg('user',m);inp.value='';busy=true;
const typing=addTyping();
fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})})
.then(r=>r.json()).then(d=>{typing.remove();streamMsg(d.reply)})
.catch(()=>{typing.remove();addMsg('bot','Error! Phir se try karo.');busy=false})}
function addMsg(type,text){const d=document.createElement('div');d.className='msg '+type;
d.innerHTML='<div class="msg-row"><div class="av">'+(type==='user'?'&#128100;':'&#129302;')+'</div><div class="msg-text">'+text+'</div></div>';
chat.appendChild(d);chat.scrollTop=chat.scrollHeight}
function addTyping(){const d=document.createElement('div');d.className='msg bot';
d.innerHTML='<div class="msg-row"><div class="av">&#129302;</div><div class="msg-text"><div class="typing"><span></span><span></span><span></span></div></div></div>';
chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
async function streamMsg(text){const d=document.createElement('div');d.className='msg bot';
d.innerHTML='<div class="msg-row"><div class="av">&#129302;</div><div class="msg-text"></div></div>';
chat.appendChild(d);const el=d.querySelector('.msg-text');
for(let i=0;i<text.length;i++){el.textContent+=text[i];chat.scrollTop=chat.scrollHeight;await new Promise(r=>setTimeout(r,25))}
busy=false}
</script></body></html>'''

with open("web/templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

# Flask server
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="web/templates")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty"}), 400
    reply = bot.get_reply(message)
    return jsonify({"reply": reply})

# Start
def run():
    app.run(host="0.0.0.0", port=5000, use_reloader=False)

threading.Thread(target=run, daemon=True).start()
time.sleep(2)

# Ngrok
from pyngrok import ngrok
public_url = ngrok.connect(5000)

print("\n" + "=" * 50)
print("🎉 WEBSITE IS LIVE! (No GPU, No Training!)")
print("=" * 50)
print(f"\n🌐 URL: {public_url}")
print(f"\n📱 Phone mein bhi open hoga!")
print(f"📤 Share karo kisi ko bhi!")
print(f"\n✅ 150+ smart replies built-in")
print(f"✅ No GPU needed")
print(f"✅ No training needed")
print("=" * 50)
