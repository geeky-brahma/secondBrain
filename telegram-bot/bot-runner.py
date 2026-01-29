import os
import logging
from dotenv import load_dotenv
load_dotenv()

import requests
URL = 'http://127.0.0.1:5000'

TOKEN = os.getenv("TELEGRAM_TOKEN")
print("Your TELEGRAM_TOKEN is:", TOKEN)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    print(f"CHAT ID: {chat_id} | USER ID: {user_id}")
    print(f"Received /hello command from {update.effective_user.first_name}")
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username or "No username"
    
    print(f"CHAT ID: {chat_id} | USER ID: {user_id} | USERNAME: {username}")
    
    # Handle links/URLs
    if message.entities:
        for entity in message.entities:
            if entity.type == "url":
                url = message.text[entity.offset:entity.offset + entity.length]
                print(f"LINK RECEIVED: {url}")
                await message.reply_text(f'Link received: {url}')
                return
    
    # Handle text
    if message.text:
        print(f"TEXT MESSAGE: {message.text}")
        response = requests.post(f"{URL}/store_text", data={"text": message.text})
        print("Response from backend:", response.text)
        await message.reply_text(f'Your response is saved: {message.text}')
    
    # Handle photos
    elif message.photo:
        if message.caption:
            print(f"PHOTO WITH CAPTION RECEIVED: {len(message.photo)} photo(s) with caption: {message.caption}")
            await message.reply_text('Photo received and saved!')
        else:
            await message.reply_text('Send photo with caption to save it.')
        
        
    
    # Handle audio
    elif message.audio:
        print(f"AUDIO RECEIVED: {message.audio.file_name}")
        await message.reply_text(f'Audio received: {message.audio.file_name}')
    
    # Handle files/documents
    elif message.document:
        print(f"FILE RECEIVED: {message.document.file_name}")
        await message.reply_text(f'File received: {message.document.file_name}')


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.AUDIO | filters.Document.ALL, handle_message))

print("Bot is running... waiting for messages")
app.run_polling()