from groq import Groq
import requests


def llm_request(prompt: str, system_prompt: str, llm_mode: str, api_key: str):
    if llm_mode == "qwen":
        response = requests.post(
            "http://127.0.0.1:8000/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 2048,
            },
            timeout=60,
        )
        return response.json()["choices"][0]["message"]["content"]
    elif llm_mode == "groq":
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2048,
            response_format={"type": "text"},
        )
        return response.choices[0].message.content
