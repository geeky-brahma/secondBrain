import os
import math
import speech_recognition as sr
from pydub import AudioSegment  # pip install pydub


AUDIO_IN = "temp_audio.wav"
WAV_MONO = "temp_audio_mono.wav"
CHUNK_LEN_MS = 55_000  # under 60s

# Ensure correct format: mono, 16 kHz, 16-bit PCM
audio = AudioSegment.from_file(AUDIO_IN)
audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
audio.export(WAV_MONO, format="wav")

r = sr.Recognizer()
transcripts = []

with sr.AudioFile(WAV_MONO) as source:
    duration_ms = len(audio)
    for i in range(0, duration_ms, CHUNK_LEN_MS):
        source.DURATION = min(CHUNK_LEN_MS / 1000, duration_ms / 1000 - i / 1000)
        source.SEEK = i / 1000
        data = r.record(source, duration=source.DURATION, offset=source.SEEK)
        try:
            transcripts.append(r.recognize_google(data))
        except sr.RequestError as e:
            print(f"Chunk {i//CHUNK_LEN_MS} failed: {e}")
        except sr.UnknownValueError:
            print(f"Chunk {i//CHUNK_LEN_MS} not understood")

print("\nThe resultant text from video is:\n")
print("\n".join(transcripts))