import time
import random
import os
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, PeerFloodError
from dotenv import load_dotenv

# 🔄 Load credentials from .env file
load_dotenv()

# 🔐 Your Telegram credentials
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# ✅ Custom message to send
message = """👋 Hey! Hope you're doing awesome 😊  
Can you do me a solid and subscribe to my YouTube? 🙏  
👉 https://www.youtube.com/@PandaStories27 
Thanks a ton! 🎬🔥"""

# 📄 Track processed users
processed_file = 'processed_usernames.txt'
if os.path.exists(processed_file):
    with open(processed_file, 'r', encoding='utf-8') as file:
        processed_usernames = set(line.strip() for line in file)
else:
    processed_usernames = set()

# ✉️ Start Telegram client
with TelegramClient('user_session', api_id, api_hash) as client:
    with open('usernames.txt', 'r', encoding='utf-8') as file:
        usernames = [line.strip() for line in file if line.strip()]

    for username in usernames:
        if username in processed_usernames:
            print(f"✅ Skipping @{username} (already processed)")
            continue
        
        try:
            print(f"📨 Sending message to @{username}")
            user = client.get_entity(username)
            client.send_message(user, message)
            
            # 🕓 Randomized delay
            delay = random.uniform(8, 12)
            time.sleep(delay)

            # Save processed username
            processed_usernames.add(username)
            with open(processed_file, 'a', encoding='utf-8') as file:
                file.write(f"{username}\n")

        except UserPrivacyRestrictedError:
            print(f"🚫 @{username} has privacy settings that block messages.")
        except PeerFloodError:
            print("❗ Telegram thinks you're spamming. Stop the script for a while.")
            break
        except FloodWaitError as e:
            print(f"⏱️ Rate limited. Waiting for {e.seconds} seconds...")
            time.sleep(e.seconds)
        except Exception as e:
            print(f"❌ Error sending to @{username}: {e}")
