from fastapi import APIRouter, HTTPException, status, UploadFile, File
from .speech_to_text import transcribe

stt_endpoints = APIRouter()


@stt_endpoints.post("/stt")
async def stt(file: UploadFile = File(...)):
    try:
        text = transcribe(file)
        return {"text": text}
    except HTTPException:
        raise
    except Exception as err:
        print(str(err))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot perform transcription.",
        )