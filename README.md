# secondBrain

Personal knowledge capture assistant that ingests text, URLs, PDFs, images, audio, and YouTube metadata, then stores searchable embeddings. Includes a Flask API and a Telegram bot client.

## Features

- Ingests text, PDFs, images (captioned), audio, URLs, and YouTube links
- Summarizes text before storage (where configured)
- Embeds and stores documents for later retrieval
- Telegram bot for quick capture

## Project structure

- app.py: Flask API entry point
- services/: ingestion and conversion helpers
- embeddings/: embedding and storage helpers
- telegram_bot/: Telegram bot client
- temp/, output/, db/: runtime artifacts

## Requirements

- Python 3.10+ recommended
- A virtual environment (venv, conda, etc.)
- FFmpeg installed (required by pydub for audio handling)
- Environment variables in .env (see below)

## Environment variables

Create a .env file in the repo root:

```env
TELEGRAM_TOKEN=your_bot_token_here
```

If your embedding or summarization services require API keys, add them here as well.

## Setup

```bash
python -m venv venv-secondbrain
venv-secondbrain\Scripts\activate
pip install -r requirements.txt
```

Install FFmpeg and ensure it is on your PATH.

## Run the Flask API

```bash
python app.py
```

The API listens on http://127.0.0.1:5000 by default.

## Run the Telegram bot

In another terminal:

```bash
python telegram_bot/bot-runner.py
```

## API endpoints

All endpoints are POST requests and accept form data.

- /store_text: text
- /store_pdf: pdf_path, file_name
- /store_image: image_path, caption, file_name
- /store_audio: audio_path, file_name
- /store_youtube_info: url
- /store_url: url
- /ask_question: question

## Notes

- Audio handling expects local files. When using the Telegram bot, files are downloaded into telegram_bot/temp before being sent to the API.
- The project writes temporary and output files into temp/ and output/.

## Troubleshooting

- If audio ingestion fails, verify FFmpeg is installed and the file path is correct.
- If you see file path errors on Windows, run the Flask API from the repo root.
