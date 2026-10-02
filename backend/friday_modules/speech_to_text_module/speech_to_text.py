import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv('backend/.env')

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def transcribe(file):
    transcription = client.audio.transcriptions.create(file=(file.filename, file.file, file.content_type), model='whisper-large-v3-turbo', language='en', response_format='json', temperature=0)
    return transcription.text