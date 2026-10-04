import requests
import os
from groq import Groq
from dotenv import load_dotenv


def to_llm(augmented_prompt: str):
    system_prompt = """
    Answer using ONLY the provided PDF context.
    Do not use outside knowledge or hallucinate.
    If the context is insufficient, say so.
    Use only plain paragraphs or numbered points.
    Never use tables, headings, bullets, markdown formatting, or other structured formats.
    If the user asks for detail, provide more detail while following the same format.
    """
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

load_dotenv("backend/.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def to_llm_by_groq(augmented_prompt: str):
    system_prompt = """
    Answer ONLY from the provided PDF context.
    Do not use outside knowledge or hallucinate.
    If the context is insufficient, say so.
    Use only plain paragraphs or numbered points.
    Never use tables, headings, bullets, markdown, or other structured formats.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": augmented_prompt},
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    data = response.choices[0].message.content
    return data
