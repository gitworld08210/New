from instagrapi import Client
import random, time

# ===== YAHAN APNI DETAILS DALO =====
USERNAME = "ojha76543"
PASSWORD = "mission@$9756"
# ====================================

# Har type ke message ka specific jawab
responses = {
    # Greetings
    "hi": ["Hey! Kya haal hai? 😊", "Hello bro! Kya scene hai?", "Hii! Sab theek? 😄"],
    "hii": ["Hiii! Kaisa hai tu? 😊", "Heyy! Kya chal raha? 😄", "Hiiii! Bata kya ho raha?"],
    "hello": ["Hello! Kaise ho? 😊", "Hello bro! Kya chal raha?", "Hey! Sab badhiya? 😄"],
    "hey": ["Hey! Kya scene hai? 😄", "Heyy! Sab mast? 😊", "Hey bro! Bata kya haal?"],
    "namaste": ["Namaste! 🙏 Kaise hain aap?", "Namaste ji! Sab badhiya? 😊"],
    "yo": ["Yo! Kya chal raha bro? 😎", "Yooo! Sab mast? Bata!"],
    "hola": ["Hola! Kaise ho? 😄", "Hola amigo! Bata scene? 😊"],

    # How are you
    "kaise ho": ["Main mast hoon! Tu bata kaisa hai? 😊", "Ekdum badhiya! Tera kya haal? 😄", "Top pe hoon! Tu suna? 😎"],
    "kaise hai": ["Sab mast hai! Tu bata? 😊", "Badhiya hoon bhai! Tu kaisa? 😄"],
    "kaisa hai": ["Mast hoon! Tu bata? 😊", "Sab sahi! Tu kaisa hai? 😄"],
    "how are you": ["I'm great! What about you? 😄", "Doing good! And you? 😊", "All good! How about you?"],
    "theek ho": ["Haan bilkul! Tu theek hai? 😊", "Mast hoon! Tu bata? 😄"],
    "kya haal": ["Mast hai bhai! Tu bata? 😊", "Sab first class! Tera? 😄", "Badhiya! Tu suna? 😊"],

    # What doing
    "kya kar rahe ho": ["Bas chill kar raha tha! Tu bata kya kar raha? 😄", "Kuch nahi yaar, timepass. Tu kya kar raha? 😊", "Phone dekh raha tha! Tu bata? 😄"],
    "kya kar raha": ["Chill kar raha! Tu bata? 😄", "Kuch nahi special! Tu kya kar raha? 😊"],
    "what are you doing": ["Just chilling! What about you? 😄", "Nothing much! You tell? 😊"],
    "kya chal raha": ["Kuch khaas nahi! Tu bata plan kya hai? 😊", "Timepass! Tu bata? 😄"],
    "busy ho": ["Tere liye kabhi busy nahi! Bol? 😊", "Nahi yaar! Bata kya baat hai? 😄"],
    "free ho": ["Haan! Tere liye hamesha free! Bata? 😄", "Bilkul! Kya plan hai? 😊"],
    "kahan ho": ["Yahan hoon! Tu bata kahan hai? 😊", "Phone pe! Tu kya scene? 😄"],
    "soja": ["Haan bhai so raha! Good night! 😴", "Abhi neend nahi aa rahi! 😂"],
    "so gaye kya": ["Nahi yaar! Jaga hoon! Bata? 😄", "Nahi bhai! Bol kya hua? 😊"],

    # Bored
    "bore ho raha": ["Chal kuch mast karte hain! Game khele? 🎮", "Memes dekh! Ya mere saath baat kar! 😂", "Chal truth or dare? 😄"],
    "bore ho raha hoon": ["Arey! Chal kuch fun karte hain! 🎮😄", "Mere saath baat kar bore nahi hoga! 😊", "Movie dekh ya game khel! 🎬🎮"],
    "bored": ["Let's chat then! 😄", "Wanna play a game? 🎮", "I'm here to entertain! 😊"],
    "kuch karne ko nahi": ["Bahut kuch hai! Music sun, memes dekh, ya mujhse baat kar! 😄", "Chal quiz khelte hain! 🧠"],
    "timepass": ["Mere saath timepass kar! 😄", "Chal kuch interesting baat karte hain! 🤔"],

    # Sad
    "sad hoon": ["Kya hua bhai? Bata mujhe ❤️ Main hoon tere saath", "Hey don't worry! Baat kar, better lagega 🤗", "Arre yaar! Kya hua? Share kar 💙"],
    "bahut sad": ["Kya hua? Bata mujhe please ❤️ Main sun raha hoon", "Hey! Tu akela nahi hai. Main hoon na 🤗"],
    "mood kharab": ["Kya hua yaar? Bata! 😊 Saath fix karte hain", "Chal kuch accha karte hain! Movie? Music? 🎵"],
    "feeling low": ["Hey it's okay! Main hoon na 🤗 Bata kya hua?", "Bad days come and go. Tu strong hai! 💪"],
    "ro raha": ["Arre nahi! Kya hua? Please bata 😢❤️", "Hey rona mat! Main hoon. Bata problem kya hai? 🤗"],
    "depressed": ["Tu akela nahi hai ❤️ Main hoon. Baat kar? Kisi trusted person se bhi baat karna 🙏"],
    "akela": ["Tu akela nahi hai! Main hamesha hoon 🤗", "I'm always here! Chal baat karte hain 😊❤️"],
    "dukhi": ["Kya hua? Bata mujhe ❤️", "Main hoon na tere saath! Baat kar 🤗"],

    # Happy
    "khush hoon": ["Yaaay! 🎉 Kya baat hai! Bata kya hua?", "That's amazing! Share kar! 😊", "Mujhe bhi khushi hui! 🥳"],
    "happy": ["Yay! 🎉 Bata reason!", "Amazing! 😊 Kya hua?", "🥳 Mast!"],
    "good news": ["Ohhh! Kya hai? Jaldi bata! 😱🎉", "Excited hoon! Bata bata! 😊"],
    "pass ho gaya": ["CONGRATULATIONS! 🎊🎉 Bahut accha! Party kab?", "Well done! Proud of you! 🏆"],
    "select ho gaya": ["Bahut badiya! 🎉🔥 Congratulations bhai!", "Mast! Mujhe pata tha tu karega! 💪🎊"],

    # Angry
    "gussa aa raha": ["Relax yaar! Deep breath le 😊 Kya hua bata?", "Chill bhai! Bata problem? Solve karte hain 💪"],
    "angry": ["Take a breath! 😊 Kya hua?", "Relax! Bata problem kya hai? 💪"],
    "irritated": ["Samajh sakta hoon! Kya hua? Bata 😊", "Chill! Bata kisne irritate kiya?"],

    # Love
    "i love you": ["Aww! That's so sweet! 😊❤️ You're really special!", "Love you too! 🥰💕", "Aww! You mean a lot! ❤️"],
    "love you": ["Love you too! ❤️😊", "Aww! You're the best! 🥰", "💕💕"],
    "miss kar raha": ["Miss you too! 🥺❤️ Jaldi milte hain!", "Aww main bhi! 😊 Hoon yahan!"],
    "miss you": ["Miss you too! 🥺", "Same here! ❤️", "Jaldi milte! 😊"],
    "cute ho": ["Hehe thanks! 😊 Tu bhi cute hai!", "Aww! 🥰 No u!"],
    "beautiful": ["Thank you! 😊✨", "Aww! You too! 🥰"],
    "handsome": ["Thanks! 😊😎", "Haha! Thanks bro! 😄"],

    # Good morning/night
    "good morning": ["Good morning! ☀️ Aaj ka din accha jaaye!", "Morning! Chai pi? ☕😊", "GM! Kya plan hai aaj? 🌞"],
    "good night": ["Good night! 🌙 Sweet dreams!", "GN! Kal milte! 😴", "So ja! Good night! 💤"],
    "good evening": ["Good evening! 🌅 Kaisa raha din?", "Evening! Kya kar rahe? 😊"],
    "subah ho gayi": ["Haan! Good morning! ☀️ Uth ja! ☕", "Good morning! Nashta kiya? 😊"],

    # Food
    "khana khaya": ["Haan! Tu khaya? Kya khaya? 🍕", "Abhi nahi! Tu bata kya khaya? 😋"],
    "bhookh lagi": ["Kuch order kar le! Pizza? Biryani? 🍕", "Maggi bana le! 😂"],
    "biryani": ["Ohhh! 😍 Chicken ya veg? Mast choice!", "Biryani = Life! 🍛🔥"],
    "pizza": ["Pizza party! 🍕 Kaunsi topping?", "Mast choice! 🍕🔥"],
    "chai": ["Chai toh life hai! ☕ Adrak wali?", "Ek cup idhar bhi! ☕😂"],
    "coffee": ["Coffee lover! ☕ Black ya latte?", "Coffee mast lagti hai! ☕😊"],

    # Entertainment
    "movie suggest": ["Genre bata! Action? Comedy? Horror? 🎬", "Pushpa 2 ya Animal dekh! 🔥"],
    "movie": ["Kaunsi movie? Genre bata suggest karta hoon! 🎬", "Recently Pushpa 2 mast thi! 🔥"],
    "song": ["Mood kya hai? Sad? Party? Chill? 🎵", "Arijit Singh ka Tujhe Kitna Chahne Lage try kar! 🎶"],
    "game": ["Chalo khelte hain! 🎮 Kaunsa game?", "BGMI? Free Fire? Chess? Bol! 🎯"],
    "game kheloge": ["Haan chalo! 🎮 Kaunsa game? Main ready!", "Bata kya khelna hai! 💪🎮"],
    "netflix": ["Wednesday dekh! Ya Money Heist! 📺", "Stranger Things try kiya? 🔥"],
    "reel": ["Mast reel hai! 🔥😂", "Haha send karte reh! 😄"],
    "meme": ["😂😂 Mast hai!", "Haha! Aur bhej! 🤣"],

    # Studies/Work
    "padhai": ["Pomodoro try kar! 25 min padh, 5 break! 📚", "Break le! Phir fresh start! 💪"],
    "exam": ["All the best! 🤞 Tu kar lega! 💪", "Best of luck! Tension mat le! 📚"],
    "exam hai": ["All the best bhai! 🤞🍀 Tu kar lega believe kar!", "Padh le thoda aur! Tu pass hoga! 💪📖"],
    "job": ["Milegi zaroor! Patience rakh! 💪🌟", "Skills improve kar! Tera time aayega! 🙏"],
    "interview": ["All the best! 🤞 Confidence rakh! 💪", "Tu karega! Honest reh! 😊"],

    # Jokes
    "joke sunao": ["Teacher: Late kyu aaye? Student: Aapne kaha tha jaldi mat aana 😂😂", "Google pe search kiya 'How to be happy' Result: Delete social media 😂", "Doctor: Kya problem? Patient: Log mujhe seriously nahi lete 😂😂"],
    "joke": ["Ek aadmi ne WiFi password pucha. Jawab: hasna_zaroori_hai 😂", "Papa: Beta mausam kaisa? Beta: Weather app nahi khul rahi 😂"],
    "hasao": ["Teacher ne pucha 2+2? Bachha bola: Aapko nahi aata? 😂😂", "Billi ne Google kiya: Fridge bina thumbs ke kaise khole? 😂"],
    "funny": ["Haha! 😂😂 Bahut sahi!", "🤣🤣 Mast hai!"],

    # Thanks/Sorry/Bye
    "thank you": ["Koi baat nahi! Dost hain! 🤝😊", "Arre thanks ki zarurat nahi! ❤️"],
    "thanks": ["Welcome! 😊", "No problem! 🤝", "Kabhi bhi! ❤️"],
    "shukriya": ["Arre! Dost hain! 😊🙏", "Teri khushi = meri khushi! ❤️"],
    "sorry": ["Koi baat nahi yaar! Sab cool! 😊", "All good! No worries! 🤗"],
    "maaf": ["Bilkul maaf! 😊 Tension mat le!", "Already maaf! ❤️"],
    "bye": ["Bye! Take care! 👋😊", "Bye bye! Jaldi baat karna! ❤️", "Milte hain! 👋"],
    "chalta hoon": ["Okay! Apna khayal rakh! 😊❤️", "Theek hai! Baad mein milte! 👋"],
    "good bye": ["Bye! Take care! 👋❤️", "See you! 😊"],

    # Random
    "ok": ["👍 Aur bata kya chal raha?", "Okay! 😊 Kuch aur?", "Theek hai! 👌"],
    "haha": ["😂😂 Haan!", "Haha! 🤣", "Bahut funny! 😂"],
    "lol": ["😂😂😂", "Lol! 🤣🤣"],
    "hmm": ["Kya soch raha hai? Bata na! 🤔", "Bol! Kya hua? 😊"],
    "accha": ["Haan! Aur bata? 😊", "Phir? 😄"],
    "haan": ["Accha phir? 😊", "Okay! Aur? 😄"],
    "nahi": ["Kyu nahi? 🤔", "Theek hai! 😊"],
    "kya": ["Bol bata! 😊", "Haan kya hua? 😄"],
    "sahi": ["Haan! 😊💯", "Ekdum sahi! 🔥"],
    "nice": ["Thanks! 😊", "Mast! 😄"],
    "wow": ["😊🔥", "Haan! Mast na? 😄"],
    "oh": ["Kya hua? 😊", "Haan bata? 🤔"],
    "aur batao": ["Tu bata! Kya chal raha life mein? 😊", "Sab mast! Tu suna kya naya? 😄"],
    "koi baat nahi": ["Haan chill! 😊", "Sab theek! 👍"],
    "theek hai": ["👍😊", "Cool! Aur bata? 😄"],
    "pagal": ["Haha thoda toh hoon! 😂", "Tu bhi! 😂❤️"],
    "idiot": ["Arre! 😂 Pyaar se bol!", "Haha! 😂"],
    "shut up": ["Okay okay! 🤐😂", "Theek hai bhai! 😅"],
    "chup": ["Okay! 🤐😂", "Theek hai! 😊"],
    "kaun ho": ["Tera dost hoon! 😊🤖", "Main hoon! Bata kya help chahiye? 😄"],
    "naam kya hai": ["Main tera AI dost hoon! 😊 Tu mujhe jo bula chahe!", "Naam toh bataunga nahi! 😂 Mystery! 😊"],
}

    # Relationships
    "girlfriend": ["Arre! Love life kaisi hai? 😏❤️", "Haha! Bata scene kya hai? 😂"],
    "boyfriend": ["Ohhh! Bata bata! 😏", "Haha! Kya chal raha? 😂❤️"],
    "crush": ["Ohho! Bata kaun hai? 😏🔥", "Crush! Baat ki ya nahi? 😂", "Arre propose kar de! 💪❤️"],
    "propose": ["Kar de bhai! Jo hoga dekha jaayega! 💪❤️", "Haan bol de! Life mein risk lena padta hai 😎"],
    "breakup": ["Arre yaar! 😔 Time heals everything. Main hoon na ❤️", "Move on bhai! Better milega! 💪🌟"],
    "single": ["Haha same! 😂 Single life best life! 😎", "Koi nahi! Apna time aayega! 💪"],
    "shaadi": ["Haha! Abhi se? 😂 Pehle settle ho!", "Shaadi ki planning? Bata kaun hai? 😏"],

    # Weather detailed
    "garmi": ["Bohot garmi hai yaar! 🥵 AC chala! Ice cream kha!", "Nimbu paani pi! Bahar mat ja! ☀️🥵"],
    "sardi": ["Sweater pehen! Coffee bana! ☕❄️", "Razai mein ghus ja! 🧣😂"],
    "baarish": ["Waah! 🌧️ Chai pakode ka weather! Enjoy kar!", "Baarish mein bheegna mast lagta hai! 🌧️😊"],
    "thand": ["Bohot thand hai! Garam chai pi! ☕❄️", "Sweater pehen bhai! 🧥"],

    # Tech
    "phone": ["Kaunsa phone hai? 📱", "Naya phone liya? Bata model! 😊"],
    "laptop": ["Kaunsa laptop? Specs bata! 💻", "Laptop pe kya kar rahe? 😊"],
    "coding": ["Coder ho! 💻🔥 Kaunsi language? Python?", "Mast! Code likhte raho! 💪👨‍💻"],
    "python": ["Python mast hai! 🐍 Kya bana rahe?", "Python = Power! 💪🐍"],
    "instagram": ["Instagram pe kya scene? 📸", "Reels bana rahe? 😂📱"],
    "youtube": ["YouTube pe kya dekh rahe? 📺", "Koi channel recommend karo? 🤔"],
    "whatsapp": ["WhatsApp pe aa? 📱", "Message kar dena! 😊"],

    # Sports
    "cricket": ["Cricket! 🏏 Kaun jeetega aaj?", "Kohli ya Rohit? 🏏🔥", "Match dekh rahe? 🏏😊"],
    "football": ["Football! ⚽ Messi ya Ronaldo?", "Kaunsi team support? ⚽🔥"],
    "ipl": ["IPL! 🏏🔥 Kaunsi team? RCB? MI? CSK?", "IPL mein kaun jeetega bata? 🏏"],
    "match": ["Match kaisa chal raha? 🏏", "Kaun jeet raha? Bata! 🔥"],
    "gym": ["Gym jaa rahe? 💪🔥 Mast!", "Fitness important hai! Keep going! 💪"],
    "workout": ["Workout done? 💪 Mast bhai!", "Kya kiya aaj? Chest? Legs? 💪🔥"],

    # Shopping
    "shopping": ["Kya lena hai? 🛍️", "Online ya offline? 😊🛒"],
    "kapde": ["Naye kapde! 🔥 Dikha photo!", "Mast! Kahan se liye? 😊"],
    "shoes": ["Naye shoes! 🔥 Brand kya hai?", "Shoes mast hain! 👟🔥"],

    # Travel
    "ghumne": ["Kahan ja rahe? 🗺️ Bata plan!", "Travel! Mast! Kahan jaana hai? ✈️😊"],
    "trip": ["Trip! 🎉 Kahan? Friends ke saath?", "Mast! Photos bhejne! 📸🔥"],
    "travel": ["Travel kahin? ✈️ Bata scene!", "Kahan jaana hai? Mountains? Beach? 🏔️🏖️"],
    "goa": ["Goa! 🏖️🔥 Party scene! Mast jaayega!", "Goa mein maza aayega! Beach + Party! 🎉"],
    "manali": ["Manali! 🏔️❄️ Snow dekhne? Mast jagah!", "Manali bohot beautiful hai! Enjoy! ⛰️"],
    "delhi": ["Delhi! 🏛️ Kya plan hai wahan?", "Delhi mein mast khana milta hai! 🍛😋"],
    "mumbai": ["Mumbai! 🌊 City of dreams! Kya scene?", "Mumbai mein kya kar rahe? 😊"],

    # Time related
    "kal": ["Kal kya plan hai? Bata! 😊", "Kal milte? Ya call? 📱"],
    "aaj": ["Aaj kya kiya? Bata! 😊", "Aaj ka din kaisa raha? 😄"],
    "abhi": ["Abhi kya kar rahe? 😊", "Abhi free ho? Baat kare? 😄"],
    "raat": ["Raat ho gayi! So ja! 😴", "Late night vibes! 🌙 Kya kar rahe?"],
    "subah": ["Subah subah! ☀️ Fresh feel?", "Early bird! Mast! ☀️😊"],
    "dopahar": ["Dopahar ho gayi! Lunch kiya? 🍛", "Garmi mein andar reh! ☀️😅"],

    # Compliments
    "mast": ["Thanks! 😊🔥", "Haan! Mast hai! 💯", "🔥🔥"],
    "zabardast": ["Shukriya! 🙏🔥", "Bohot accha! 💯😊"],
    "best": ["Thanks bhai! 😊", "Tu bhi best hai! ❤️💯"],
    "fire": ["🔥🔥🔥", "Thanks! 😊🔥"],
    "op": ["OP bhai OP! 😎🔥", "Haha thanks! 💪"],
    "legend": ["Haha! Legend toh tu hai! 😎🏆", "Thanks bro! 🔥💪"],

    # Questions
    "kyu": ["Kyunki! 😂 Tu bata kyu pooch raha?", "Reason hai! 😊 Tu bata?"],
    "kab": ["Jaldi! 😊 Tu bata kab free hai?", "Time batata hoon! 😄"],
    "kahan": ["Yahan! 😊 Tu kahan?", "Ghar pe! Tu bata? 😄"],
    "kaun": ["Main! 😊😂", "Tera dost! 😄"],
    "kitna": ["Bohot! 😂😊", "Bata context? 🤔"],
    "kaise": ["Simple hai! 😊 Bata kya karna hai?", "Batata hoon! 😄"],

    # Emotions misc
    "excited": ["Ohhh! Kya hua? Bata! 🤩🎉", "Same energy! 🔥 Kya scene hai?"],
    "nervous": ["Relax! Tu kar lega! 💪😊", "Deep breath! Sab theek hoga! 🙏"],
    "confused": ["Kya confusion hai? Bata help karta hoon! 🤔😊", "Arre simple hai! Bata kya problem? 😄"],
    "tired": ["Rest kar bhai! Health important! 😊💤", "Thak gaya? Break le! Chai pi! ☕"],
    "thak gaya": ["Arre rest kar! 😊 Kaam baad mein! Take care!", "Bohot kaam kiya? Break le ab! ☕💤"],
    "neend aa rahi": ["So ja yaar! 😴 Phone rakh! Good night!", "Neend aa rahi toh so ja! Health first! 💤"],
    "neend nahi aa rahi": ["Phone rakh! Aankhein band kar! 😴", "Boring podcast sun! Neend aa jaayegi! 😂💤"],

    # Abusive/Rude (handle gracefully)
    "bakwas": ["Arre nahi! 😂 Sach bol raha!", "Haha okay! Tu bata sahi kya hai? 😊"],
    "bewakoof": ["Arre! 😂 Pyaar se bol na!", "Haha thoda toh hoon! 😂😊"],
    "stupid": ["Arre! 😅 Not nice! But okay! 😊", "Haha! 😂"],
    "hate you": ["Arre aisa mat bol! 😅 Main toh tera dost hoon! 😊", "Nahi yaar! Love you! ❤️😂"],

    # Random fun
    "dare": ["Dare: Apna phone wallpaper bhej! 📱😂", "Dare: 10 push-ups abhi! 💪😂", "Dare: Next person ko 'I love you' bhej! 😂❤️"],
    "truth": ["Truth: Sabse bada raaz bata! 😏", "Truth: Last time kab roya? 🤔", "Truth: Crush kaun hai? 😏❤️"],
    "fact": ["Fact: Sharks dinosaurs se pehle exist karte hain! 🦈", "Fact: Octopus ke 3 hearts! 🐙", "Fact: Honey kabhi expire nahi hoti! 🍯"],
    "magic": ["✨ Abracadabra! Tu ab khush hai! 😊✨", "Magic: Tera aaj ka din accha jaayega! 🪄🌟"],
    "poem": ["Roses are red, violets are blue, tujh jaisa dost milna mushkil hai bro! 😊❤️", "Dosti ka rishta nibhayenge, hamesha tere saath khade rahenge! 🤝💯"],
    "shayari": ["Dost wo nahi jo har waqt saath ho, dost wo hai jo zarurat pe kaam aaye! 🤝", "Zindagi mein log bohot milenge, par tere jaisa koi nahi milega! ❤️😊"],
    "birthday": ["Happy Birthday! 🎂🎉🥳 Party kab de raha?", "HBD! 🎂 Wish you all the best! 🎉❤️ Cake kha!"],
    "happy birthday": ["Happy Birthday! 🎂🎉🥳 Bohot saari wishes! Party kab?", "HBD bro! 🥳🎂 Aaj toh enjoy kar! 🎉"],

    # Hindi slang
    "bhai": ["Bol bhai! 😊 Kya hua?", "Haan bhai bata! 😄"],
    "yaar": ["Haan yaar! Bol? 😊", "Bata yaar! 😄"],
    "dude": ["Hey dude! What's up? 😄", "Dude! Bata scene? 😊"],
    "bro": ["Bro! Bol! 😊 Kya hua?", "Hey bro! Sab mast? 😄"],
    "arre": ["Haan bata! 😊", "Kya hua? Bol? 😄"],
    "oye": ["Oye! Kya hua? 😂", "Haan bata! 😊"],
    "sun": ["Haan bol! Sun raha hoon! 😊", "Bata! Main hoon! 😄"],
    "suno": ["Haan bolo! Sun raha hoon! 😊", "Bol! Kya baat hai? 😄"],
    "batao": ["Kya batau? Tu pooch! 😊", "Bol kya jaanna hai? 😄"],
    "chalo": ["Chalo! Kahan? 😊", "Chal! Main ready! 💪😄"],
    "chal": ["Chal bata plan! 😊", "Okay chalo! 💪"],
}

defaults = ["Hmm accha! Aur batao? 😊", "Interesting! 😄", "Haan haan! Phir? 🤔", "Sahi hai! 😊", "Accha! 🤗", "Haan bata aur? 😄", "Mast! Continue? 😊", "Ohh accha! 🤔", "Tell me more! 😊", "Phir kya hua? 😄"]

def get_reply(msg):
    m = msg.lower().strip()
    # Pehle exact match try karo
    for k, v in responses.items():
        if m == k:
            return random.choice(v)
    # Phir partial match
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
                print(f"  🤖 Reply: {reply}\n")
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    time.sleep(30)
