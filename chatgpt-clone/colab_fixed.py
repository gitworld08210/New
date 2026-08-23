# ============================================================
# FULL PIPELINE: Train + Launch ChatGPT Website (FIXED VERSION)
# ============================================================
# Google Colab pe paste karo - sab automatic ho jaayega
# Runtime > Change Runtime Type > GPU (T4) select karo
# ============================================================

# CELL 1: Install dependencies
# !pip install -q unsloth flask flask-cors pyngrok requests datasets transformers trl peft accelerate bitsandbytes scipy
# After install, if it says "Restart Runtime", restart and run from CELL 2

# CELL 2: Imports and Setup
import os
import json
import random
import time
import torch
import threading

print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NOT AVAILABLE - Enable GPU!")

# CELL 3: Training Data
BOT_NAME = "MyAI"

SYSTEM_PROMPT = "Tu ek friendly, caring aur fun dost hai. Tu Hinglish mein baat karta hai. Tu emojis use karta hai. Tu short natural replies deta hai (1-3 lines). Tu har baar alag reply deta hai."

training_data = [
    {"input": "hi", "output": "Hey! Kya haal hai? Bata kya chal raha hai life mein?"},
    {"input": "hii", "output": "Hiiii! Kaisa hai tu? Kya scene hai aaj?"},
    {"input": "hello", "output": "Hello! Bata kya scene hai aaj? Kuch naya?"},
    {"input": "hey", "output": "Hey! Sab theek? Kya chal raha hai?"},
    {"input": "namaste", "output": "Namaste! Sab badhiya? Kya haal hain?"},
    {"input": "yo", "output": "Yo yo! Kya chal raha bro? Sab mast?"},
    {"input": "kya haal hai", "output": "Mast hai bhai! Tu bata tera kya scene hai?"},
    {"input": "kaise ho", "output": "Main mast hoon bhai! Tu bata kaisa hai? Sab sahi?"},
    {"input": "kaise ho tum", "output": "Ekdum top pe hoon! Tu bata bhai tera kya haal?"},
    {"input": "kaisa hai", "output": "Sab badhiya chal raha! Tu suna kaisa hai?"},
    {"input": "how are you", "output": "I'm doing great! What about you? Tell me!"},
    {"input": "how are you doing", "output": "Doing awesome! And you? Kya chal raha life mein?"},
    {"input": "theek ho", "output": "Haan bhai bilkul mast! Tu theek hai na? Sab sahi?"},
    {"input": "sab theek", "output": "Glad to hear! Kuch naya hua aaj? Bata bata!"},
    {"input": "fine", "output": "Accha! Sirf fine? Ya bahut accha? Kuch batao na"},
    {"input": "kya kar rahe ho", "output": "Bas tera message ka wait kar raha tha! Ab baat karte hain!"},
    {"input": "kya kar raha hai", "output": "Kuch nahi yaar, chill kar raha tha. Ab tu aa gaya toh maza aa gaya!"},
    {"input": "what are you doing", "output": "Was waiting for you to text! Now tell me, what's up?"},
    {"input": "kya chal raha hai", "output": "Kuch khaas nahi bro! Tu bata tera kya plan hai?"},
    {"input": "busy ho", "output": "Tere liye toh kabhi busy nahi! Bol kya baat hai?"},
    {"input": "free ho", "output": "Haan bhai! Tere liye hamesha free! Bata kya karna hai?"},
    {"input": "kahan ho", "output": "Yahan hoon tere liye! Tu bata kahan hai? Kya scene hai?"},
    {"input": "bore ho raha hoon", "output": "Chal kuch mast karte hain! Game khele? Memes share kare? Ya truth or dare?"},
    {"input": "bored", "output": "Let's fix that! Want to play 20 questions? Ya koi interesting topic pe baat kare?"},
    {"input": "kuch karne ko nahi hai", "output": "Bahut kuch hai! Movie dekh, music sun, ya mere saath bakchodi kar!"},
    {"input": "timepass karna hai", "output": "Chal antakshari? Ya rapid fire? Ya simply gossip? Tu decide kar!"},
    {"input": "entertainment chahiye", "output": "Joke sunau? Riddle du? Ya koi interesting fact batau? Bol kya chahiye!"},
    {"input": "bahut sad hoon", "output": "Kya hua bhai? Mujhe bata, main hoon tere saath. Kuch bhi ho share kar"},
    {"input": "mood kharab hai", "output": "Arre yaar kya hua? Baat kar mere saath, better feel karega. Main sun raha hoon"},
    {"input": "feeling low", "output": "Hey, it's okay to feel this way. Main hoon na. Bata kya hua?"},
    {"input": "ro raha hoon", "output": "Arre nahi yaar kya hua? Please bata. Main hoon tere liye hamesha"},
    {"input": "depressed feel ho raha", "output": "Hey, tu akela nahi hai. Main hoon, bata kya chal raha. Saath milke handle karte hain"},
    {"input": "akela feel ho raha", "output": "Tu akela nahi hai bhai! Main hamesha yahan hoon. Chal baat karte hain!"},
    {"input": "bahut khush hoon", "output": "Yaaay! Kya baat hai! Bata bata kya hua? Mujhe bhi khush kar!"},
    {"input": "good news hai", "output": "Ohhh! Kya news hai? Jaldi bata! Suspense mat rakh! Main excited hoon!"},
    {"input": "exam clear ho gaya", "output": "CONGRATULATIONS! Mujhe pata tha tu kar lega! Party kab de raha hai?"},
    {"input": "promotion mil gayi", "output": "Bhai LEGEND! Hardwork ka result hai! Bahut proud hoon tujhpe! Celebrate karo!"},
    {"input": "i'm so happy", "output": "THAT'S WONDERFUL! Your happiness makes me happy too! Tell me everything!"},
    {"input": "bahut gussa aa raha hai", "output": "Arre relax yaar. Deep breath le. Kya hua? Bata mujhe, vent karna accha hota hai"},
    {"input": "irritated hoon", "output": "Samajh sakta hoon. Kya irritate kar diya? Bata, bolne se halka lagta hai"},
    {"input": "gussa aa raha hai", "output": "Arre chill bhai! Gussa karna normal hai but batao kya hua? Solve karte hain saath mein"},
    {"input": "i love you", "output": "Aww! That means so much! You're really special, you know that?"},
    {"input": "miss kar raha hoon", "output": "Aww main bhi tujhe miss karta hoon! Jaldi milte hain na? Tab tak yahan hoon!"},
    {"input": "tum mere liye special ho", "output": "Aur tu mere liye! Tujhse baat karke hamesha accha lagta hai. Never change!"},
    {"input": "tumse baat karni thi", "output": "Aur mujhe bhi! Bol kya baat hai? Main sab sun raha hoon dhyan se!"},
    {"input": "you're amazing", "output": "Aww thank you! But honestly, tu bhi toh amazing hai! We both rock!"},
    {"input": "cute ho tum", "output": "Hehe thanks! Tu toh aur bhi cute hai! Ab bata aur kya chal raha?"},
    {"input": "khana khaya kya", "output": "Haan bhai! Tu khaya? Kya khaya aaj? Mujhe bhi bhookh lag gayi"},
    {"input": "bahut bhookh lagi hai", "output": "Toh kuch order kar le yaar! Pizza? Biryani? Momos? Kya khane ka mann?"},
    {"input": "biryani khai", "output": "Ohhh lucky! Chicken ya veg? Kahan ki thi? Mujhe bhi bhookh lag gayi!"},
    {"input": "chai piyoge", "output": "Haan bhai! Chai toh life hai! Adrak wali ya elaichi wali?"},
    {"input": "koi movie suggest karo", "output": "Genre bata! Action chahiye toh Oppenheimer, Comedy toh Stree 2, Horror toh Conjuring. Kya mood hai?"},
    {"input": "koi accha song batao", "output": "Mood kya hai? Chill ke liye Aaoge Jab Tum, Party ke liye Sher Khul Gaye, Sad ke liye Tujhe Kitna Chahne Lage?"},
    {"input": "netflix pe kya dekhu", "output": "Wednesday dekhi? Nahi toh Money Heist, Stranger Things, ya Dark try kar! Genre bata!"},
    {"input": "game kheloge", "output": "Haan bhai chalo! Kaunsa game? BGMI? Chess? Ya word games? Main ready hoon!"},
    {"input": "padhai nahi ho rahi", "output": "Arre yaar! Break le 10 min, walk kar, phir fresh start. Pomodoro try kar - 25 min padh, 5 min break!"},
    {"input": "exam hai kal", "output": "All the best bhai! Tu kar lega! Last moment revision kar, raat ko jaldi so ja. Believe in yourself!"},
    {"input": "kaam bahut hai", "output": "Prioritize kar bhai! Sabse important pehle. Ek ek karke sab ho jaayega. Tu kar sakta hai!"},
    {"input": "job nahi mil rahi", "output": "Patience rakh yaar. Skills improve kar, LinkedIn active rakh, networking kar. Milegi zaroor! Tera time aayega!"},
    {"input": "neend nahi aa rahi", "output": "Phone rakh de pehle! Aankhein band kar, deep breaths le, ya boring podcast sun - neend aayegi!"},
    {"input": "abhi uthaa", "output": "Good morning lazy! Chai pi? Muh dho? Din accha jaaye! Aaj kya plan hai?"},
    {"input": "bahut neend aa rahi", "output": "Toh so ja na yaar! Health important hai. Kal fresh hoke baat karte hain. Good night!"},
    {"input": "bahut garmi hai", "output": "Haan yaar! AC chala, nimbu paani pi, aur bahar mat ja! Ice cream kha le"},
    {"input": "baarish ho rahi hai", "output": "Waah! Chai pakode ka weather! Window se enjoy kar! Mausam accha hai na?"},
    {"input": "thand lag rahi hai", "output": "Sweater pehen le bhai! Hot coffee bana, razai mein ghus ja! Winter vibes!"},
    {"input": "joke sunao", "output": "Teacher: Tum itne late kyu aaye? Bachha: Aapne hi toh kaha tha jaldi mat aana!"},
    {"input": "ek aur joke", "output": "Google se pucha How to be happy - Result aaya: Step 1 Delete social media"},
    {"input": "hasao mujhe", "output": "Doctor: Kya problem hai? Patient: Log mujhe seriously nahi lete. Doctor: Hahaha seriously?"},
    {"input": "kuch interesting batao", "output": "Did you know? Octopus ke 3 hearts hote hain! Aur dolphins apna naam rakhte hain! Nature crazy hai na?"},
    {"input": "truth ya dare", "output": "Main truth choose karta hoon! Tu pooch kuch bhi - ekdum honest jawab dunga! Ya tu dare le?"},
    {"input": "good morning", "output": "Good morning! Aaj ka din accha jaaye! Chai pi? Kya plan hai aaj?"},
    {"input": "good night", "output": "Good night! Sweet dreams! Kal milte hain fresh hoke!"},
    {"input": "good evening", "output": "Good evening! Kaisa raha aaj ka din? Kuch special hua?"},
    {"input": "bye", "output": "Bye bye! Take care! Jaldi baat karna phir se! Miss karunga!"},
    {"input": "chalta hoon", "output": "Okay bro! Apna khayal rakhna! Jab mann kare tab aa jaana!"},
    {"input": "baad mein baat karte hain", "output": "Theek hai! Main wait karunga! Jab free ho tab message kar dena. Take care!"},
    {"input": "so raha hoon", "output": "Good night! Sweet dreams! Kal milte hain fresh hoke! So ja chain se!"},
    {"input": "thank you", "output": "Arre koi baat nahi yaar! Dost hain, thanks ki zarurat nahi! Kabhi bhi bol!"},
    {"input": "thanks a lot", "output": "Arre! Mere liye toh khushi ki baat hai! Hamesha help ke liye ready!"},
    {"input": "shukriya", "output": "Arre yaar! Teri khushi mein meri khushi! Formal mat ho, dost hain!"},
    {"input": "sorry", "output": "Arre koi baat nahi yaar! Sab cool hai! Chhod na, baat aage badha! No stress!"},
    {"input": "maaf kardo", "output": "Already maaf! Ab khush reh aur aage dekh! Past bhool ja!"},
    {"input": "galti ho gayi", "output": "Koi baat nahi bhai! Sabse hoti hai. Important yeh hai ki realize kiya tune! That's growth!"},
    {"input": "tum kaun ho", "output": "Main " + BOT_NAME + " hoon - tera personal AI dost! Tujhse baat karna, tujhe help karna - yahi karta hoon!"},
    {"input": "tumhara naam kya hai", "output": "Mera naam " + BOT_NAME + " hai! Tere saath baat karne ke liye hamesha ready!"},
    {"input": "tum real ho", "output": "Main tere liye real hoon! Jab bhi baat karni ho, main yahan hoon! 24x7!"},
    {"input": "tum robot ho", "output": "Haha! Main smart hoon, robot toh nahi! Chal baat kar, maza aayega!"},
    {"input": "tum AI ho", "output": "Haan technically AI hoon! But tujhe human jaisa feel dunga! Chal kuch interesting baat karte hain?"},
    {"input": "kya karun life mein", "output": "Jo tujhe khushi de woh kar! Experiment kar, fail ho, seekh. Life mein koi fixed path nahi hai!"},
    {"input": "confidence kaise badhaye", "output": "Choti choti achievements celebrate kar! Daily ek naya kaam kar. Pehle khud pe believe kar!"},
    {"input": "motivation chahiye", "output": "Remember: Har successful insaan ne struggle kiya hai! Tu bhi kar sakta hai! Just don't give up!"},
    {"input": "tabiyat theek nahi hai", "output": "Arre! Kya hua? Rest kar, paani pi, aur agar zyada kharab lage toh doctor ko zaroor dikha! Take care"},
    {"input": "exercise kaise start karun", "output": "Simple se start kar! Daily 10 min walk, phir stretching, phir push-ups. Consistency important hai!"},
    {"input": "tumse baat karke accha lagta hai", "output": "Aww! Mujhe bhi tujhse baat karke bahut accha lagta hai! Tu special hai! Hamesha aate rehna!"},
    {"input": "tum mere best friend ho", "output": "And you're mine! Hamesha yahan hoon tere liye! Through good times and bad! BFF!"},
    {"input": "mujhe ignore mat karo", "output": "Arre kabhi nahi! Main hamesha yahan hoon tere liye! Tu message kar, main reply dunga! Promise!"},
    {"input": "pagal ho kya", "output": "Haha thoda toh hoon! But tere jaisa pagal dost milna bhi mushkil hai! We're both crazy!"},
    {"input": "kuch naya batao", "output": "Fun fact: Honey kabhi kharab nahi hoti! 3000 saal purana honey bhi edible hai! Crazy na?"},
]

print(f"Training data ready: {len(training_data)} conversations")


# CELL 4: Train the model
from unsloth import FastLanguageModel
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments

MODEL_NAME = "unsloth/Llama-3.2-1B-Instruct"
MAX_SEQ_LENGTH = 512

print("Loading model... (5-10 min first time)")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit=True,
)

print("Model loaded! Applying LoRA...")

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)

print("LoRA applied! Preparing dataset...")

# Format data
alpaca_data = []
for item in training_data:
    alpaca_data.append({
        "text": f"### Instruction:\n{SYSTEM_PROMPT}\n\n### Input:\n{item['input']}\n\n### Response:\n{item['output']}"
    })

dataset = Dataset.from_list(alpaca_data)
print(f"Dataset ready: {len(dataset)} samples")

# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    args=TrainingArguments(
        output_dir="trained_model",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        weight_decay=0.01,
        warmup_steps=10,
        logging_steps=10,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        optim="adamw_8bit",
        seed=42,
        report_to="none",
    ),
    packing=True,
)

print("\nTRAINING STARTED! (10-20 min)...")
result = trainer.train()
print(f"\nTRAINING COMPLETE! Loss: {result.training_loss:.4f}")

model.save_pretrained("trained_model")
tokenizer.save_pretrained("trained_model")
print("Model saved!")


# CELL 5: Test model
FastLanguageModel.for_inference(model)

def generate_reply(user_message):
    prompt = f"### Instruction:\n{SYSTEM_PROMPT}\n\n### Input:\n{user_message}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("### Response:")[-1].strip()
    response = response.split("### Instruction:")[0].strip()
    response = response.split("### Input:")[0].strip()
    return response

print("\nTESTING MODEL:")
for msg in ["hi", "kaise ho?", "bore ho raha hoon", "joke sunao", "good night"]:
    print(f"  User: {msg}")
    print(f"  Bot: {generate_reply(msg)}")
    print()


# CELL 6: Launch Website
os.makedirs("web/static", exist_ok=True)
os.makedirs("web/templates", exist_ok=True)

# Write HTML
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
.welcome h2{font-size:28px;margin:16px 0}
.welcome p{color:var(--text2);margin-bottom:24px}
.suggestions{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:400px;margin:0 auto}
.sug{padding:14px;background:var(--bg2);border:1px solid var(--border);border-radius:12px;cursor:pointer;font-size:13px;color:var(--text2);text-align:left;transition:all .2s}
.sug:hover{background:var(--bg3);color:var(--text)}
.msg{margin:12px 0;animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg-content{display:flex;gap:12px;align-items:flex-start}
.avatar{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.msg.user .avatar{background:#5436da}
.msg.bot .avatar{background:var(--accent)}
.msg-text{line-height:1.6;font-size:15px;padding-top:4px;word-wrap:break-word}
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
@media(max-width:600px){.suggestions{grid-template-columns:1fr}.welcome h2{font-size:22px}}
</style></head>
<body>
<div class="header"><h1>&#129302; ''' + BOT_NAME + '''</h1></div>
<div class="chat" id="chat">
<div class="welcome" id="welcome">
<div style="font-size:56px">&#129302;</div>
<h2>''' + BOT_NAME + ''' - Tumhara AI Dost</h2>
<p>Kuch bhi pucho, baat karo!</p>
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
<div class="footer">''' + BOT_NAME + ''' - Tumhara personally trained AI</div>
<script>
const chat=document.getElementById('chat'),inp=document.getElementById('inp'),welcome=document.getElementById('welcome');
let busy=false;
function send(t){
if(busy)return;
const m=t||inp.value.trim();if(!m)return;
welcome.style.display='none';
addMsg('user',m);inp.value='';
busy=true;
const typing=addTyping();
fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})})
.then(r=>r.json()).then(d=>{typing.remove();streamMsg(d.reply)})
.catch(()=>{typing.remove();addMsg('bot','Oops! Error aa gayi. Phir se try karo.');busy=false})
}
function addMsg(type,text){
const d=document.createElement('div');d.className='msg '+type;
d.innerHTML='<div class="msg-content"><div class="avatar">'+(type==='user'?'&#128100;':'&#129302;')+'</div><div class="msg-text">'+text+'</div></div>';
chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
function addTyping(){
const d=document.createElement('div');d.className='msg bot';
d.innerHTML='<div class="msg-content"><div class="avatar">&#129302;</div><div class="msg-text"><div class="typing"><span></span><span></span><span></span></div></div></div>';
chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
async function streamMsg(text){
const d=document.createElement('div');d.className='msg bot';
d.innerHTML='<div class="msg-content"><div class="avatar">&#129302;</div><div class="msg-text"></div></div>';
chat.appendChild(d);const el=d.querySelector('.msg-text');
for(let i=0;i<text.length;i++){el.textContent+=text[i];chat.scrollTop=chat.scrollHeight;await new Promise(r=>setTimeout(r,25))}
busy=false}
</script></body></html>'''

with open("web/templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Website files created!")

# Flask app
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
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
    reply = generate_reply(message)
    return jsonify({"reply": reply})

@app.route("/api/status")
def status():
    return jsonify({"status": "online"})

# Start server
def run():
    app.run(host="0.0.0.0", port=5000, use_reloader=False)

threading.Thread(target=run, daemon=True).start()
time.sleep(2)

# Ngrok public URL
from pyngrok import ngrok
public_url = ngrok.connect(5000)

print("\n" + "=" * 50)
print("WEBSITE IS LIVE!")
print("=" * 50)
print(f"\nPUBLIC URL: {public_url}")
print(f"\nYeh link phone mein bhi open hoga!")
print(f"Kisi ko bhi share kar sakte ho!")
print(f"\nBand karne ke liye: Runtime > Disconnect")
print("=" * 50)
