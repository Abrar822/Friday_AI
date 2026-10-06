import os
from groq import Groq
# from dotenv import load_dotenv
from ..persistent_memory.db import get_conn_obj
from fastapi import HTTPException, status

# load_dotenv("backend/.env")
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def fetchKey():
    conn, cur = None, None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """SELECT value FROM keyval WHERE key = ?
        """
        cur.execute(query, ("api_key",))
        api_key = cur.fetchone()
        print('inside function: ', api_key)

        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Groq Api Key not found."
            )
        return api_key[0]
    except HTTPException:
        raise
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Some error occurred.",
        )
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def transcribe(file):
    api_key = fetchKey()
    client = Groq(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        file=(file.filename, file.file, file.content_type),
        model="whisper-large-v3-turbo",
        language="en",
        response_format="json",
        temperature=0,
    )
    return transcription.text


