from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
import requests


def load_model(chroma_db_client, collection, model):
    path = Path.home() / "Friday_AI" / "chromadb.db"
    chroma_db_client = chromadb.PersistentClient(path=str(path))
    collection = chroma_db_client.get_or_create_collection(
        name="Friday_documents_collection"
    )
    model = SentenceTransformer(
        str(Path("backend/friday_modules/pdf_assistant_module/model/all-MiniLM-L6-v2"))
    )
    return model, collection, chroma_db_client


def to_llm(augmented_prompt: str):
    system_prompt = """Answer the user's question using only the provided PDF context. Do not hallucinate or use outside knowledge. If the context is insufficient, say about it. If user asks in detail then provide detailing."""
    response = requests.post(
        "http://127.0.0.1:8080/chat/completions",
        json={
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": augmented_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 2048,
        },
        timeout=100,
    )
    res = response.json()
    data = res["choices"][0]["message"]["content"]
    return data