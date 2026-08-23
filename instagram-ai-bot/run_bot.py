from instagrapi import Client
import random, time

# ===== YAHAN APNI DETAILS DALO =====
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
# ====================================

responses = {"hi":["Hey! 😊","Hello!","Hii! 😄"],"hello":["Hello! Kaise ho? 😊","Hey! 😄","Hi bro!"],"hey":["Hey! 😊","Heyy! 😄"],"kaise ho":["Mast! Tu bata? 😊","Badhiya! 😄","Top pe! Tu suna?"],"how are you":["Great! You? 😄","Good! 😊","Doing well!"],"kya kar rahe":["Chill! Tu bata? 😄","Tere liye wait! 😊","Timepass! Tu?"],"what are you doing":["Chilling! You? 😄","Talking to you! 😊"],"bore":["Game khele! 🎮","Memes dekh! 😂","Mere saath baat kar! 😄"],"bored":["Let's chat! 😄","Game? 🎮","I'm here! 😊"],"sad":["Kya hua? ❤️","Main hoon na! 🤗","Theek hoga 💪"],"happy":["Yay! 🎉","Amazing! 😊","🥳"],"angry":["Relax! 😊","Chill bhai! 💪","Kya hua bata?"],"good morning":["Good morning! ☀️","Morning! Chai pi? ☕","GM! 🌞"],"good night":["Good night! 🌙","Sweet dreams! 😴","GN! 💤"],"good evening":["Good evening! 🌅","Evening! 😊"],"joke":["Teacher: Late kyu? Student: Jaldi mat aana kaha tha 😂","Google: How to be happy? Delete social media 😂","Doctor: Problem? Patient: Log seriously nahi lete 😂"],"movie":["Genre bata! 🎬","Pushpa 2 dekhi? 🔥","Wednesday try kar! 📺"],"song":["Mood bata? 🎵","Arijit sun! 🎶"],"game":["Chalo! 🎮","BGMI? 🎯","Ready! 💪"],"thank":["Welcome! 🤝","No problem! 😊","Kabhi bhi! ❤️"],"sorry":["Cool! 😊","Koi baat nahi! 🤗","Maaf! ❤️"],"bye":["Bye! 👋","Take care! 😊❤️","Milte hain! 👋"],"love":["Aww! ❤️","Love! 🥰","You're special! 💕"],"miss":["Miss you too! 🥺","Jaldi milte! ❤️"],"cute":["Thanks! 😊","No u! 🥰"],"khana":["Kya khaya? 🍕","Biryani? 😋","Bhookh lagi? 🍛"],"photo":["Mast! 🔥","Bohot acchi! 😍"],"reel":["Mast reel! 🔥","Haha! 😂"],"ok":["👍","Aur bata? 😊"],"haha":["😂😂","Haha! 🤣"],"lol":["😂😂😂","Funny! 🤣"],"hmm":["Kya soch raha? 🤔","Bol na! 😊"],"kya chal raha":["Kuch nahi! Tu bata? 😊","Timepass! 😄"],"accha":["Haan! Aur? 😊","Phir? 😄"],"haan":["Phir? 😊","Mast! 👍"],"nahi":["Kyu nahi? 🤔","Theek hai! 😊"],"kya":["Bol bata! 😊","Kya hua?"],"kaun":["Main hoon! 😊","Tera dost! 😄"],"kahan":["Yahan! 😊","Tere paas! 😄"],"pagal":["Haha thoda! 😂","Tu bhi! 😂"],"bakwas":["Arre nahi! 😂","Sach bol raha! 😄"],"chup":["Okay okay! 🤐😂","Theek hai! 😊"],"aur batao":["Tu bata! 😊","Kya batau? 😄","Sab mast! Tu suna?"],"koi baat nahi":["Haan! Chill! 😊","Sab theek! 👍"],"theek hai":["👍😊","Cool!","Mast!"]}
defaults = ["Hmm batao? 😊","Nice! 😄","Accha! 🤔","Sahi hai! 😊","Aur bata? 🤗","Interesting! 😄","Mast! 🙌","Haha! 😂","Phir? 😊","Okay! 👍"]

def get_reply(msg):
    m = msg.lower()
    for k, v in responses.items():
        if k in m:
            return random.choice(v)
    return random.choice(defaults)

cl = Client()
print("🔐 Logging in...")
cl.login(USERNAME, PASSWORD)
print("✅ Logged in as @" + USERNAME)

my_id = str(cl.user_id)
replied = set()

print("\n🤖 Instagram Auto-Reply Bot RUNNING!")
print("   ✅ DM reply: ON")
print("   ✅ Group reply: ON")
print("   ⏱️ Checking every 30 seconds")
print("   🛑 Stop: Ctrl+C or Stop button\n")

while True:
    try:
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
                reply = get_reply(msg.text)
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
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    time.sleep(30)
