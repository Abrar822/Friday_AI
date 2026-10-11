# import os
from groq import Groq

# from dotenv import load_dotenv
from fastapi import HTTPException, status
from ...core.api_key_handling import get_api_key

# load_dotenv("backend/.env")
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def fetchKey():
    try:
        api_key = get_api_key() or ""
        return api_key
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Some error occurred.",
        )


def transcribe(file):
    api_key = fetchKey()
    if not api_key.strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please provide a Groq Api Key')
    client = Groq(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        file=(file.filename, file.file, file.content_type),
        model="whisper-large-v3-turbo",
        language="en",
        response_format="json",
        temperature=0,
    )
    return transcription.text
