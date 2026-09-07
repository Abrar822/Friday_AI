# Run Qwen:=> .\backend\core\llama_cpp\llama-server.exe -m ".\backend\core\model\qwen2.5-1.5b-instruct-q4_k_m.gguf" -c 4096

# new: .\backend\core\llama_cpp\llama-server.exe -m ".\backend\core\model\Qwen3-1.7B-Q4_K_M.gguf" -c 4096

# data = {
#     "response": "Email is being generated, pls dont press any key sir",
#     "tasks": [
#         {
#             "id": 1,
#             "module": "browser",
#             "action": "search_specific_website",
#             "parameters": {"website_name": "youtube", "query": "Abrar Shekh"},
#         }
#     ],
# }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.llm_prompt_endpoint import llm_prompt_router
from .friday_modules.persistent_memory.memory_endpoints import memory_endpoints
from .friday_modules.persistent_memory.db import db, get_conn_obj
from contextlib import asynccontextmanager
from .core.TaskRouter import TaskRouter
from .friday_modules.text_to_speech_module.Piper_TTS import tts
from .friday_modules.persistent_memory.memory_operations import fetch_locations
from .friday_modules.desktop_module.app_registry.create_registry import create_registry
from .friday_modules.desktop_module.app_registry import registry


@asynccontextmanager
async def lifespan(app: FastAPI):
    db()

    conn = get_conn_obj()
    app.state.locations = fetch_locations(conn)
    conn.close()

    registry.registry = create_registry()

    app.state.ai = TaskRouter()
    app.state.speaker = tts.TextToSpeechModule()
    # app.state.speaker.tts('Hi, I am Friday. How can I help you')
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Call endpoints
app.include_router(llm_prompt_router)
app.include_router(memory_endpoints)
