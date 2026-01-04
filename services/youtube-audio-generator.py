# if needed install required libraries
# pip install yt-dlp moviepy

import yt_dlp
from moviepy import AudioFileClip
import os

def download_youtube_audio(youtube_url, output_path):
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    
    # Download and convert to MP3
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    # Rename the output file
    if os.path.exists('../temp/temp_audio.wav'):
        os.rename('../temp/temp_audio.wav', output_path)

youtube_url = "https://youtube.com/watch?si=_SXsFI8fqcwngzXm&v=j1lTvjmOJbQ"

# In case you want to enter the video to use directly:
# youtube_url = str(input("Enter the URL of the video you want to 
#               download: \n>>"))

output_path = '../temp/temp_audio.wav'
download_youtube_audio(youtube_url, output_path)