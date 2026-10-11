import os
import socket
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"
BACKEND_PYTHON = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
FRONTEND_DIR = ROOT / "frontend"


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_backend(url, process, timeout=120):
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Backend exited before becoming ready.")

        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except Exception:
            pass

        time.sleep(0.25)

    raise TimeoutError("Backend did not become ready in time.")


port = get_free_port()
backend_url = f"http://127.0.0.1:{port}"
backend = None

try:
    backend = subprocess.Popen(
        [
            str(BACKEND_PYTHON),
            str(BACKEND_DIR / "launcher.py"),
            "--port",
            str(port),
        ],
        cwd=ROOT,
    )

    print(f"Waiting for backend at {backend_url}...")
    wait_for_backend(f"{backend_url}/health", backend)
    print("Backend ready. Starting Tauri...")

    env = os.environ.copy()
    env["VITE_BACKEND_URL"] = backend_url

    subprocess.run(
        ["cmd", "/c", "npm", "run", "tauri", "dev"],
        cwd=FRONTEND_DIR,
        env=env,
        check=True,
    )

finally:
    if backend and backend.poll() is None:
        backend.terminate()
        try:
            backend.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend.kill()
