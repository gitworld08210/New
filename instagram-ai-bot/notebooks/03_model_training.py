# ============================================================
# 🧠 STEP 3: MODEL TRAINING (LoRA Fine-Tuning on Google Colab)
# ============================================================
# Yeh script tumhara apna chat model train karta hai
# Google Colab pe FREE GPU (T4) use karke
# 
# ⚠️ IMPORTANT: Colab mein Runtime → Change Runtime Type → GPU (T4) select karo
# 
# Pehle Step 1 aur Step 2 run karna zaruri hai
# ============================================================

# ============ CELL 1: Install Dependencies ============
# Yeh cell sirf ek baar run karo

# !pip install -q torch torchvision torchaudio
# !pip install -q transformers==4.44.0
# !pip install -q peft==0.12.0
# !pip install -q trl==0.9.6
# !pip install -q datasets==2.20.0
# !pip install -q accelerate==0.33.0
# !pip install -q bitsandbytes==0.43.1
# !pip install -q scipy

print("✅ All dependencies installed!")
print("⚠️ Agar 'Restart Runtime' ka message aaye toh restart karo aur CELL 2 se start karo")


# ============ CELL 2: Import Libraries ============

import torch
import json
import os
from datetime import datetime

# Check GPU
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_mem / 1e9
    print(f"✅ GPU Available: {gpu_name}")
    print(f"   Memory: {gpu_memory:.1f} GB")
else:
    print("❌ GPU not available! Runtime → Change Runtime Type → GPU select karo!")
    print("   CPU pe training bahut slow hogi")

print(f"\n🔥 PyTorch version: {torch.__version__}")
print(f"   CUDA available: {torch.cuda.is_available()}")


# ============ CELL 3: Load Training Data ============

# Agar Step 1 & 2 already run kiya hai toh yeh file hogi
# Agar nahi hai toh manually upload karo ya neeche ka sample data use karo

TRAINING_DATA_PATH = "training_data/train_alpaca.json"

# Check if training data exists, if not create sample
if not os.path.exists(TRAINING_DATA_PATH):
    print("⚠️ Training data not found! Creating sample data...")
    print("   (Best results ke liye Step 1 & 2 pehle run karo)")
    
    os.makedirs("training_data", exist_ok=True)
    
    # Sample training data (minimum viable)
    sample_data = [
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "hi", "output": "Hey! Kya haal hai? 😊 Bata kya chal raha hai?"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "kaise ho", "output": "Main mast hoon bhai! Tu bata kaisa hai? Sab theek?"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "kya kar rahe ho", "output": "Bas chill kar raha tha! Ab tera message aaya toh baat karte hain 😄"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "bore ho raha hoon", "output": "Chal kuch mast karte hain! Game khele? Movie dekh? Ya memes share kare? 😂"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "good morning", "output": "Good morning! ☀️ Aaj ka din accha jaaye tera! Chai pi?"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "good night", "output": "Good night! 🌙 Sweet dreams! Kal milte hain bro!"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "bahut sad hoon", "output": "Kya hua bhai? Mujhe bata, main hoon tere saath ❤️ Kuch bhi ho share kar"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "thank you", "output": "Arre koi baat nahi! Dost ke liye toh hamesha! 😊🤝"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "joke sunao", "output": "Teacher: Tum late kyu aaye? Student: Aapne kaha tha jaldi mat aana 😂😂"},
        {"instruction": "Tu ek friendly, caring dost hai. User ke message ka natural reply de.", "input": "i love you", "output": "Aww! That's so sweet! 😊❤️ You're really special to me too!"},
    ]
    
    with open(TRAINING_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

# Load data
with open(TRAINING_DATA_PATH, "r", encoding="utf-8") as f:
    training_data = json.load(f)

print(f"✅ Training data loaded: {len(training_data)} samples")
print(f"\n📝 Sample entry:")
print(f"   Input: {training_data[0]['input']}")
print(f"   Output: {training_data[0]['output']}")


# ============ CELL 4: Model Configuration ============

# ===== YAHAN CHANGE KARO APNE HISAAB SE =====

# Model selection (smaller = faster training, less RAM needed)
MODEL_NAME = "unsloth/Llama-3.2-1B-Instruct"  # 1B - Fast, works on free Colab T4
# MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct"  # 3B - Better quality, needs more RAM
# MODEL_NAME = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"  # 8B - Best quality, needs Colab Pro

# Training parameters
EPOCHS = 3                    # Kitni baar data pe train kare (3-5 best hai)
LEARNING_RATE = 2e-4          # Learning speed (2e-4 default, kam karo agar overfit ho)
BATCH_SIZE = 4                # Ek baar mein kitne samples (4 for T4, 8 for A100)
MAX_SEQ_LENGTH = 512          # Maximum text length
LORA_R = 16                   # LoRA rank (16 good balance)
LORA_ALPHA = 32               # LoRA alpha (usually 2x of r)
OUTPUT_DIR = "trained_model"  # Model save location

print("⚙️ Training Configuration:")
print(f"   Model: {MODEL_NAME}")
print(f"   Epochs: {EPOCHS}")
print(f"   Learning Rate: {LEARNING_RATE}")
print(f"   Batch Size: {BATCH_SIZE}")
print(f"   Max Sequence Length: {MAX_SEQ_LENGTH}")
print(f"   LoRA Rank: {LORA_R}")
print(f"   LoRA Alpha: {LORA_ALPHA}")
print(f"   Output: {OUTPUT_DIR}")


# ============ CELL 5: Load Model with Unsloth (FAST) ============
# Unsloth makes training 2x faster and uses 60% less memory

# !pip install -q unsloth

from unsloth import FastLanguageModel

print(f"🔄 Loading model: {MODEL_NAME}")
print("   (Pehli baar download hoga, 5-10 min lag sakta hai)...")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,  # Auto-detect
    load_in_4bit=True,  # 4-bit quantization for less memory
)

print(f"✅ Model loaded successfully!")
print(f"   Parameters: {model.num_parameters():,}")


# ============ CELL 6: Configure LoRA Adapters ============

model = FastLanguageModel.get_peft_model(
    model,
    r=LORA_R,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=LORA_ALPHA,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",  # Memory efficient
    random_state=42,
)

# Trainable parameters count
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"\n✅ LoRA configured!")
print(f"   Total parameters: {total_params:,}")
print(f"   Trainable parameters: {trainable_params:,} ({100*trainable_params/total_params:.2f}%)")
print(f"   (Sirf {100*trainable_params/total_params:.2f}% train ho raha — fast + efficient!)")


# ============ CELL 7: Prepare Dataset ============

from datasets import Dataset

# Format data for training
def format_prompt(sample):
    """Training prompt format banata hai."""
    instruction = sample.get("instruction", "Tu ek friendly dost hai. Natural reply de.")
    input_text = sample["input"]
    output_text = sample["output"]
    
    # Alpaca format
    prompt = f"""### Instruction:
{instruction}

### Input:
{input_text}

### Response:
{output_text}"""
    
    return {"text": prompt}

# Create HuggingFace dataset
dataset = Dataset.from_list(training_data)
dataset = dataset.map(format_prompt)

print(f"✅ Dataset prepared: {len(dataset)} samples")
print(f"\n📝 Formatted sample:")
print(dataset[0]["text"][:300] + "...")


# ============ CELL 8: Training Setup ============

from trl import SFTTrainer
from transformers import TrainingArguments

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=4,
    learning_rate=LEARNING_RATE,
    weight_decay=0.01,
    warmup_steps=10,
    logging_steps=10,
    save_steps=100,
    save_total_limit=2,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    optim="adamw_8bit",
    seed=42,
    report_to="none",  # Disable wandb
)

# Trainer setup
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    args=training_args,
    packing=True,  # Pack multiple samples together for efficiency
)

print("✅ Trainer configured!")
print(f"\n📊 Training Plan:")
print(f"   Samples: {len(dataset)}")
print(f"   Epochs: {EPOCHS}")
print(f"   Batch Size: {BATCH_SIZE} × 4 (gradient accumulation) = {BATCH_SIZE * 4} effective")
print(f"   Total Steps: ~{len(dataset) * EPOCHS // (BATCH_SIZE * 4)}")
print(f"\n⏱️ Estimated time: ~10-30 minutes (depends on data size)")


# ============ CELL 9: START TRAINING 🚀 ============

print("="*50)
print("🚀 TRAINING STARTED!")
print("="*50)
print(f"   Start time: {datetime.now().strftime('%H:%M:%S')}")
print(f"   Yeh 10-30 minutes le sakta hai...")
print(f"   Loss decrease hona chahiye har step pe\n")

# Train!
train_result = trainer.train()

print(f"\n{'='*50}")
print(f"🎉 TRAINING COMPLETE!")
print(f"{'='*50}")
print(f"   End time: {datetime.now().strftime('%H:%M:%S')}")
print(f"   Final Loss: {train_result.training_loss:.4f}")
print(f"   Total Steps: {train_result.global_step}")


# ============ CELL 10: Save Model ============

# Save LoRA adapters
print("\n💾 Saving model...")

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"✅ Model saved to: {OUTPUT_DIR}/")
print(f"   (Yeh sirf LoRA weights hain — ~50-100MB)")


# ============ CELL 11: Test the Model ============

print("\n" + "="*50)
print("🧪 TESTING YOUR MODEL")
print("="*50)

# Enable inference mode
FastLanguageModel.for_inference(model)

def chat(user_message):
    """Model se reply generate karta hai."""
    prompt = f"""### Instruction:
Tu ek friendly, caring dost hai. User ke message ka natural, conversational reply de. Hinglish ya English mein reply kar, emojis use kar.

### Input:
{user_message}

### Response:
"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the response part
    response = response.split("### Response:")[-1].strip()
    # Remove any trailing instruction/input if model generates them
    response = response.split("### Instruction:")[0].strip()
    response = response.split("### Input:")[0].strip()
    
    return response


# Test conversations
test_messages = [
    "hi",
    "kaise ho?",
    "kya kar rahe ho?",
    "bore ho raha hoon",
    "bahut sad hoon aaj",
    "good morning!",
    "koi movie suggest karo",
    "i love you",
    "joke sunao",
    "bye",
]

print("\n🤖 Model Responses:\n")
for msg in test_messages:
    response = chat(msg)
    print(f"  👤 User: {msg}")
    print(f"  🤖 Bot:  {response}")
    print()


# ============ CELL 12: Export Model for Deployment ============

print("\n" + "="*50)
print("📦 EXPORTING MODEL FOR DEPLOYMENT")
print("="*50)

# Option 1: Save merged model (larger but standalone)
print("\n📦 Option 1: Saving merged model (for Ollama/local use)...")

# Merge LoRA with base model
model.save_pretrained_merged(
    "merged_model",
    tokenizer,
    save_method="merged_16bit",  # Full precision merged model
)

print("✅ Merged model saved to: merged_model/")

# Option 2: Save as GGUF (for Ollama - RECOMMENDED)
print("\n📦 Option 2: Saving as GGUF (for Ollama)...")

model.save_pretrained_gguf(
    "model_gguf",
    tokenizer,
    quantization_method="q4_k_m",  # Good quality + small size
)

print("✅ GGUF model saved to: model_gguf/")
print("   (Yeh file directly Ollama mein load ho sakti hai!)")


# ============ CELL 13: Download Model ============

# Google Colab se download karo
print("\n" + "="*50)
print("⬇️ DOWNLOAD YOUR MODEL")
print("="*50)

print("""
📋 Download Options:

1. GGUF File (Ollama ke liye - RECOMMENDED):
   - Left panel mein 'model_gguf/' folder mein jaao
   - .gguf file pe right-click → Download
   - Size: ~500MB - 1GB

2. LoRA Adapters (lightweight):
   - 'trained_model/' folder download karo
   - Size: ~50-100MB
   - Baad mein base model ke saath merge karna padega

3. Google Drive mein save:
""")

# Save to Google Drive (optional)
try:
    from google.colab import drive
    drive.mount('/content/drive')
    
    import shutil
    drive_path = "/content/drive/MyDrive/instagram_bot_model"
    os.makedirs(drive_path, exist_ok=True)
    
    # Copy GGUF to Drive
    for f in os.listdir("model_gguf"):
        if f.endswith(".gguf"):
            shutil.copy2(f"model_gguf/{f}", drive_path)
            print(f"✅ Copied {f} to Google Drive!")
    
    # Copy LoRA to Drive
    shutil.copytree("trained_model", f"{drive_path}/lora_adapters", dirs_exist_ok=True)
    print(f"✅ LoRA adapters copied to Google Drive!")
    print(f"\n📁 Location: {drive_path}")
    
except:
    print("   Google Drive mount nahi hua. Manual download karo left panel se.")


print("""
\n🎉 MODEL TRAINING COMPLETE!
================================

Ab aage kya:
1. GGUF file download karo
2. Apne computer pe Ollama install karo: curl -fsSL https://ollama.com/install.sh | sh
3. Model load karo Ollama mein (Step 4 mein bataya hai)
4. Instagram bot connect karo (Step 4 notebook)

Ya directly Step 4 (Instagram Bot) notebook run karo! 🚀
""")
