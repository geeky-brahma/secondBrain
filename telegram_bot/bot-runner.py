import os
import logging
from time import sleep
from object_store import upload_file, download_file
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

import requests
URL = 'http://127.0.0.1:5000'
CONNECT_TIMEOUT_SECONDS = 30.0
READ_TIMEOUT_SECONDS = 300.0
WRITE_TIMEOUT_SECONDS = 300.0
POOL_TIMEOUT_SECONDS = 30.0

TOKEN = os.getenv("TELEGRAM_TOKEN")
# print("Your TELEGRAM_TOKEN is:", TOKEN)

from telegram import Update
from telegram import InputFile
from telegram.request import HTTPXRequest
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
                if "youtube.com" in url or "youtu.be" in url:
                    print(f"YOUTUBE LINK RECEIVED: {url}")
                    response = requests.post(f"{URL}/store_youtube_info", data={"url": url})
                    print("Response from backend:", response.text)
                    await message.reply_text(f'YouTube link received and info extracted: {url}')
                else:
                    print(f"LINK RECEIVED: {url}")
                    response = requests.post(f"{URL}/store_url", data={"url": url})
                    print("Response from backend:", response.text)
                    await message.reply_text(f'Link received: {url}')
                
    
    # Handle text
    if message.text:
        print(f"TEXT MESSAGE: {message.text}")
        response = requests.post(f"{URL}/store_text", data={"text": message.text})
        print("Response from backend:", response.text)
        await message.reply_text(f'Your response is saved: {message.text}')
    
    # Handle photos
    elif message.photo:
        if message.caption:
            os.makedirs(os.path.join("temp", "telegram_photos"), exist_ok=True)
            photo = message.photo[-1]
            telegram_file = await photo.get_file()
            telegram_uid = telegram_file.file_unique_id
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            local_path = os.path.join("temp", "telegram_photos", f"{telegram_uid}_{user_id}_{timestamp}.jpg")
            await telegram_file.download_to_drive(local_path)
            upload_file(local_path, f"{telegram_uid}_{user_id}_{timestamp}.jpg")
            file_name = f"{telegram_uid}_{user_id}_{timestamp}.jpg"
            try:
                response = requests.post(
                    f"{URL}/store_image",
                    data={
                        "image_path": local_path,
                        "caption": message.caption,
                        "file_name": file_name,
                    },
                )
            except requests.RequestException as exc:
                print("Backend request failed:", exc)
                await message.reply_text("Backend error. File kept locally.")
                return
            print(
                f"PHOTO WITH CAPTION RECEIVED: {len(message.photo)} photo(s) with caption: {message.caption}"
            )
            print("Saved photo to:", local_path)
            print("Response from backend:", response.text)
            if response.ok:
                os.remove(local_path)
                await message.reply_text('Photo received and saved!')
            else:
                await message.reply_text("Backend error. File kept locally.")
        else:
            await message.reply_text('Send photo with caption to save it.')
        
        
    
    # Handle audio
    elif message.audio:
        os.makedirs(os.path.join("temp", "telegram_audio"), exist_ok=True)
        telegram_file = await message.audio.get_file()
        telegram_uid = telegram_file.file_unique_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = message.audio.file_name or f"audio_{telegram_uid}.mp3"
        # _, ext = os.path.splitext(original_name)
        # ext = ext or ".mp3"
        local_path = os.path.join("temp", "telegram_audio", f"{telegram_uid}_{user_id}_{timestamp}.mp3")
        await telegram_file.download_to_drive(local_path)
        upload_file(local_path, f"{telegram_uid}_{user_id}_{timestamp}.mp3")
        sleep(5)
        print(f"AUDIO RECEIVED: {original_name}")
        try:
            response = requests.post(
                f"{URL}/store_audio",
                data={
                    "audio_path": local_path,
                    "file_name": f"{telegram_uid}_{user_id}_{timestamp}.mp3",
                },
            )
        except requests.RequestException as exc:
            print("Backend request failed:", exc)
            await message.reply_text("Backend error. File kept locally.")
            return
        print("Response from backend:", response.text)
        if response.ok:
            os.remove(local_path)
            await message.reply_text(f'Audio received: {original_name}')
        else:
            await message.reply_text("Backend error. File kept locally.")
    
    # Handle files/documents
    elif message.document:
        os.makedirs(os.path.join("temp", "telegram_docs"), exist_ok=True)
        telegram_file = await message.document.get_file()
        telegram_uid = telegram_file.file_unique_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = message.document.file_name or f"document_{telegram_uid}"
        _, ext = os.path.splitext(original_name)
        ext = ext or ".bin"
        local_path = os.path.join("temp", "telegram_docs", f"{telegram_uid}_{user_id}_{timestamp}{ext}")
        await telegram_file.download_to_drive(local_path)
        upload_file(local_path, f"{telegram_uid}_{user_id}_{timestamp}{ext}")

        try:
            response = requests.post(
                f"{URL}/store_pdf",
                data={
                    "pdf_path": local_path,
                    "file_name": f"{telegram_uid}_{user_id}_{timestamp}{ext}",
                },
            )
        except requests.RequestException as exc:
            print("Backend request failed:", exc)
            await message.reply_text("Backend error. File kept locally.")
            return
        print(f"FILE RECEIVED: {original_name}")
        print("Response from backend:", response.text)
        if response.ok:
            os.remove(local_path)
            await message.reply_text(f'File received: {original_name}')
        else:
            await message.reply_text("Backend error. File kept locally.")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args)
    print(f"Received question: {question}")
    response = requests.post(f"{URL}/ask_question", data={"question": question})
    print("Response from backend:", response.text)
    extensions = [
        ".txt", ".pdf", ".doc", ".docx", ".md",
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
        ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"
    ]
    if any(ext in response.text for ext in extensions):
        os.makedirs(os.path.join("temp", "telegram_response"), exist_ok=True)
        local_path = os.path.join("temp", "telegram_response", os.path.basename(response.text))
        download_file(response.text, local_path)
        await update.message.reply_text('Relevant information for your question:')
        with open(local_path, "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename=os.path.basename(local_path)))
        os.remove(local_path)
    else:
        await update.message.reply_text(f'Relevant information for your question: \n{response.text}')
    

request = HTTPXRequest(
    connect_timeout=CONNECT_TIMEOUT_SECONDS,
    read_timeout=READ_TIMEOUT_SECONDS,
    write_timeout=WRITE_TIMEOUT_SECONDS,
    pool_timeout=POOL_TIMEOUT_SECONDS,
)
app = ApplicationBuilder().token(TOKEN).request(request).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.AUDIO | filters.Document.ALL, handle_message))

print("Bot is running... waiting for messages")
app.run_polling()