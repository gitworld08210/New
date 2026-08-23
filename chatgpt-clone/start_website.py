import os,threading,time,random,re
from flask import Flask,request,jsonify,Response
from pyngrok import ngrok

BOT_NAME="MyAI"
responses={"hi":["Hey! Kya haal? 😊","Hello! Bata scene?","Hii! 😄"],"hello":["Hello! Kaise ho? 😊","Hey! Kya chal raha?"],"hey":["Hey! Badhiya? 😄","Heyy! Kya haal?"],"kaise ho":["Mast hoon! Tu bata? 😊","Badhiya! Tu suna?","Top pe! 😎"],"how are you":["Great! You? 😄","Doing good!","All good! 😊"],"kya kar rahe":["Chill! Tu bata? 😄","Tere liye wait! 😊"],"what are you doing":["Chilling! You? 😄","Talking to you! 😊"],"bore ho raha":["Game khelte! 🎮","Memes dekh! 😂","Baat kar! 😄"],"bored":["Let's chat! 😄","Game? 🎮"],"sad":["Kya hua? Bata ❤️","Main hoon na! 🤗","Theek hoga 💪"],"happy":["Yay! 🎉","Amazing! 😊","🥳🥳"],"good morning":["Good morning! ☀️","Morning! Chai pi? ☕","GM! 🌞"],"good night":["Good night! 🌙","Sweet dreams! 😴","GN! 💤"],"joke":["Teacher: Late kyu? Student: Aapne kaha jaldi mat aana 😂","Google: How to be happy? Delete social media 😂","Doctor: Problem? Patient: Log seriously nahi lete 😂"],"movie":["Genre bata! 🎬","Pushpa 2 dekhi? 🔥","Wednesday try kar! 📺"],"song":["Mood bata? 🎵","Arijit sun! 🎶"],"game":["Chalo! 🎮 Kaunsa?","BGMI? 🎯","Ready! 💪"],"thank":["Welcome! 🤝","No problem! 😊"],"sorry":["Cool! 😊","Maaf! 🤗"],"bye":["Bye! 👋","Take care! ❤️","Milte hain! 👋"],"love":["Aww! ❤️","Love! 🥰"],"miss":["Miss you too! 🥺","Jaldi milte! ❤️"],"khana":["Kya khaya? 🍕","Biryani? 😋"],"ok":["👍","Aur bata? 😊"],"haha":["😂😂","Haha! 🤣"],"lol":["😂😂😂","Funny! 🤣"],"kya chal raha":["Kuch nahi! Tu bata? 😊","Timepass! Tu? 😄"],"accha":["Haan! Aur? 😊","Phir? 😄"],"haan":["Phir? 😊","Mast! 👍"],"hmm":["Kya soch raha? 🤔","Bol na! 😊"],"cute":["Thanks! 😊","No u! 🥰"],"smart":["Haha thanks! 🧠","Tu bhi! 😄"],"photo":["Mast! 🔥","Bohot acchi! 😍"],"reel":["Mast reel! 🔥","Haha! 😂"]}
defaults=["Hmm batao? 😊","Accha! Phir? 🤔","Nice! 😄","Sahi hai! 😊","Aur bata? 🤗","Interesting! 😄","Mast! 🙌"]

def get_reply(msg):
    m=msg.lower().strip()
    for k,v in responses.items():
        if k in m:
            return random.choice(v)
    return random.choice(defaults)

HTML_PAGE='<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>'+BOT_NAME+'</title><style>:root{--bg:#0d0d0d;--bg2:#171717;--bg3:#212121;--text:#ececec;--text2:#b4b4b4;--muted:#6b6b6b;--border:#2f2f2f;--accent:#10a37f}*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;flex-direction:column}.header{padding:16px;border-bottom:1px solid var(--border);text-align:center}.header h1{font-size:20px}.chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}.welcome{text-align:center;padding:60px 20px}.welcome h2{font-size:24px;margin:16px 0}.welcome p{color:var(--text2);margin-bottom:24px}.suggestions{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:400px;margin:0 auto}.sug{padding:14px;background:var(--bg2);border:1px solid var(--border);border-radius:12px;cursor:pointer;font-size:13px;color:var(--text2);transition:all .2s}.sug:hover{background:var(--bg3);color:var(--text)}.msg{margin:12px 0;animation:fadeIn .3s}@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1}}.msg-row{display:flex;gap:12px;align-items:flex-start}.av{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}.msg.user .av{background:#5436da}.msg.bot .av{background:var(--accent)}.msg-text{line-height:1.6;font-size:15px;padding-top:4px;word-wrap:break-word;flex:1}.typing span{width:7px;height:7px;background:var(--muted);border-radius:50%;display:inline-block;animation:b 1.4s infinite;margin-right:4px}.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}@keyframes b{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}.input-area{padding:16px}.input-box{max-width:800px;margin:0 auto;display:flex;gap:10px;background:var(--bg3);border:1px solid var(--border);border-radius:24px;padding:12px 16px;align-items:center}.input-box textarea{flex:1;background:none;border:none;outline:none;color:var(--text);font-size:15px;font-family:inherit;resize:none;max-height:100px;line-height:1.4}.input-box textarea::placeholder{color:var(--muted)}.send{width:34px;height:34px;border-radius:50%;border:none;background:#676767;color:#0d0d0d;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px}.send:hover{background:var(--text)}.footer{text-align:center;font-size:11px;color:var(--muted);padding:8px}@media(max-width:600px){.suggestions{grid-template-columns:1fr}}</style></head><body><div class="header"><h1>&#129302; '+BOT_NAME+'</h1></div><div class="chat" id="chat"><div class="welcome" id="welcome"><div style="font-size:56px">&#129302;</div><h2>'+BOT_NAME+' - Tumhara AI Dost</h2><p>Kuch bhi pucho!</p><div class="suggestions"><div class="sug" onclick="send(\'Hi! Kaise ho?\')">&#128075; Hi! Kaise ho?</div><div class="sug" onclick="send(\'Bore ho raha hoon\')">&#128564; Bore ho raha</div><div class="sug" onclick="send(\'Joke sunao\')">&#128514; Joke sunao</div><div class="sug" onclick="send(\'Movie suggest karo\')">&#127916; Movie suggest</div></div></div></div><div class="input-area"><div class="input-box"><textarea id="inp" placeholder="Message..." rows="1" onkeydown="if(event.key===\'Enter\'&&!event.shiftKey){event.preventDefault();send()}"></textarea><button class="send" onclick="send()">&#9654;</button></div></div><div class="footer">'+BOT_NAME+' &#129302;</div><script>const chat=document.getElementById("chat"),inp=document.getElementById("inp"),welcome=document.getElementById("welcome");let busy=false;function send(t){if(busy)return;const m=t||inp.value.trim();if(!m)return;welcome.style.display="none";addMsg("user",m);inp.value="";busy=true;const ty=addTyping();fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:m})}).then(r=>r.json()).then(d=>{ty.remove();streamMsg(d.reply)}).catch(()=>{ty.remove();addMsg("bot","Error!");busy=false})}function addMsg(type,text){const d=document.createElement("div");d.className="msg "+type;d.innerHTML=\'<div class="msg-row"><div class="av">\'+(type==="user"?"&#128100;":"&#129302;")+\'</div><div class="msg-text">\'+text+"</div></div>";chat.appendChild(d);chat.scrollTop=chat.scrollHeight}function addTyping(){const d=document.createElement("div");d.className="msg bot";d.innerHTML=\'<div class="msg-row"><div class="av">&#129302;</div><div class="msg-text"><div class="typing"><span></span><span></span><span></span></div></div></div>\';chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}async function streamMsg(text){const d=document.createElement("div");d.className="msg bot";d.innerHTML=\'<div class="msg-row"><div class="av">&#129302;</div><div class="msg-text"></div></div>\';chat.appendChild(d);const el=d.querySelector(".msg-text");for(let i=0;i<text.length;i++){el.textContent+=text[i];chat.scrollTop=chat.scrollHeight;await new Promise(r=>setTimeout(r,25))}busy=false}</script></body></html>'

app=Flask(__name__)

@app.route("/")
def index():
    return Response(HTML_PAGE,content_type="text/html")

@app.route("/api/chat",methods=["POST"])
def chat_api():
    data=request.json
    reply=get_reply(data.get("message",""))
    return jsonify({"reply":reply})

try:
    ngrok.kill()
except:
    pass

threading.Thread(target=lambda:app.run(host="0.0.0.0",port=5001,use_reloader=False),daemon=True).start()
time.sleep(2)
url=ngrok.connect(5001)
print("\n"+"="*50)
print("🎉 WEBSITE LIVE!")
print("="*50)
print(f"\n🌐 URL: {url}")
print("\n📱 Phone mein bhi kholo!")
print("="*50)
