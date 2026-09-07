import subprocess
import json


def create_registry():
    command = (
        'Get-StartApps | ConvertTo-Json'
    )
    result = subprocess.run(
        ["powershell.exe", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout.strip():
       result = json.loads(result.stdout.strip())
    else:
        result = []

    return result
