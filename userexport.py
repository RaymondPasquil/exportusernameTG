from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 26969028
api_hash = 'b7ee890512bb3ed73ed6c0d093a82a21'
group_name = '@POGOENCODERJOBHIRING'

client = TelegramClient('session', api_id, api_hash)
client.start()

for dialog in client.iter_dialogs():
    if dialog.name == group_name:
        for user in client.iter_participants(dialog.id):
            print(user.username)

client.disconnect()
