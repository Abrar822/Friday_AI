import requests
import json
from .system_prompt import system_prompt


def route_task(prompt: str):
    response = requests.post(
        "http://127.0.0.1:8080/chat/completions",
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
    route = response.json()
    print(route)
    data = route["choices"][0]["message"]["content"]
    if data.endswith('"'):
        data = data[:-1]
    print('llm', repr(data))
    data = json.loads(data)
    return data
