from pyrogram import Client, filters
import json
import os

api_id = ''
api_hash = ''
session_name = ''

app = Client(session_name, api_id=api_id, api_hash=api_hash)

photos_folder = 'photos'
if not os.path.exists(photos_folder):
    os.makedirs(photos_folder)

def save_message(message):
    message_data = {
        "message_id": message.id,
        "from_user": message.from_user.username if message.from_user else None,
        "chat_id": message.chat.id,
        "chat_title": message.chat.title if message.chat.title else 'Private',
        "date": str(message.date),
        "text": message.text if message.text else None
    }
    
    if message.photo:
        file_path = os.path.join(photos_folder, f"{message.id}.jpg")
        message.download(file_path)
        message_data["photo"] = file_path

    with open('messages.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(message_data, ensure_ascii=False) + '\n')

@app.on_message(filters.all)
def handle_new_message(client, message):
    print(f"New message from {message.chat.title if message.chat.title else 'Private'}: {message.text}")
    save_message(message)

if __name__ == '__main__':
    print("Starting the client...")
    app.run()
