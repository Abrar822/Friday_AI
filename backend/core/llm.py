import requests
import json
from .system_prompt import system_prompt

FRIDAY_GRAMMAR = r"""
# Allow structural spaces anywhere between tokens safely
root ::= ws "{" ws "\"response\"" ws ":" ws string ws "," ws "\"tasks\"" ws ":" ws task-list ws "}" ws
task-list ::= "[" ws (task (ws "," ws task)*)? ws "]"

task ::= "{" ws "\"id\"" ws ":" ws integer ws "," ws "\"module\"" ws ":" ws module-types ws "," ws "\"action\"" ws ":" ws action-types ws "," ws "\"parameters\"" ws ":" ws parameters-object ws "}"

module-types ::= "\"email\"" | "\"browser\"" | "\"desktop\""

action-types ::= "\"compose_email\"" | "\"search_specific_website\"" | "\"open_website\"" | "\"set_volume\"" | "\"set_brightness\"" | "\"perform_shutdown\"" | "\"perform_restart\"" | "\"perform_locking\"" | "\"perform_sleep\"" | "\"perform_hibernation\"" | "\"take_screenshot\"" | "\"create_folder\"" | "\"create_file\"" | "\"open_file\"" | "\"open_folder\"" | "\"delete_file\"" | "\"delete_folder\"" | "\"rename_file\"" | "\"rename_folder\"" | "\"close_file\"" | "\"open_local_app\"" | "\"search_folder\"" | "\"search_file\"" | "\"move_folder\"" | "\"move_file\"" | "\"conversation\""

# Flexible object for parameters
parameters-object ::= "{" ws (string ws ":" ws value (ws "," ws string ws ":" ws value)*)? ws "}"

# Primitive types
value ::= string | number | "true" | "false" | "null" | parameters-object | "[]"
string ::= "\"" ([^"\\] | "\\" ["\\/bfnrt] | "\\u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])* "\""
number ::= ("-")? ([0-9])+ ("." ([0-9])+)? ([eE] [+-]? ([0-9])+)?
integer ::= [0-9]+
ws ::= [ \t\n\r]*
"""



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
            "grammar": FRIDAY_GRAMMAR,
        },
        timeout=60,
    )
    route = response.json()
    data = route["choices"][0]["message"]["content"]
    if data.endswith('"'):
        data = data[:-1]
    data = json.loads(data)
    print(data)
    return data
