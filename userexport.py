from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# 🧩 Replace with your credentials
api_id = 26969028  # your api_id (integer)
api_hash = 'b7ee890512bb3ed73ed6c0d093a82a21'  # your api_hash string
group_username = '@POGOENCODERJOBHIRING'  # group's @username (e.g., 'mygroup123')

# 🔐 Start client
client = TelegramClient('session_name', api_id, api_hash)
client.start()

# 📥 Get group entity
group = client.get_entity(group_username)

# 👤 Get participants
all_participants = []
offset = 0
limit = 100

while True:
    participants = client(GetParticipantsRequest(
        group, ChannelParticipantsSearch(''), offset, limit, hash=0
    ))
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)

# 📝 Save usernames
with open('usernames.txt', 'w', encoding='utf-8') as f:
    for user in all_participants:
        if user.username:
            f.write(f"{user.username}\n")

print(f"✅ Done! {len(all_participants)} users extracted.")
client.disconnect()
