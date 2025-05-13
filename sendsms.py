import time
import random
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, PeerFloodError
import os

# 🔐 Your Telegram credentials (consider storing these in environment variables or a secure file)
api_id = os.getenv('26969028')  # Replace with your real api_id
api_hash = os.getenv('b7ee890512bb3ed73ed6c0d093a82a21')  # Replace with your real api_hash

# ✅ Custom message to send
message = """👋 Hey! Hope you're doing awesome 😊  
Can you do me a solid and subscribe to my YouTube? 🙏  
👉 https://www.youtube.com/@PandaStories27 
Thanks a ton! 🎬🔥"""

# Path to a file that stores processed usernames
processed_file = 'processed_usernames.txt'

# Load already processed usernames into a set for fast lookup
if os.path.exists(processed_file):
    with open(processed_file, 'r', encoding='utf-8') as file:
        processed_usernames = set(line.strip() for line in file)
else:
    processed_usernames = set()

# ✉️ Start the client using your phone number
with TelegramClient('user_session', api_id, api_hash) as client:
    # 🔓 Login prompt will ask for your number (e.g., +639667701072) and then code from Telegram

    # 📁 Load usernames
    with open('usernames.txt', 'r', encoding='utf-8') as file:
        usernames = [line.strip() for line in file if line.strip()]

    for username in usernames:
        if username in processed_usernames:
            print(f"✅ Skipping @{username} (already processed)")
            continue  # Skip users that have already received the message
        
        try:
            print(f"📨 Sending message to @{username}")
            user = client.get_entity(username)
            client.send_message(user, message)

            # 🕓 Randomized delay to avoid spam detection
            delay_time = random.uniform(8, 12)  # Randomize sleep time between 8 and 12 seconds
            time.sleep(delay_time)

            # After sending, add the username to the processed set and save it to the file
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
