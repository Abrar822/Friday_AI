# Friday - AI Desktop Assistant

Friday is an AI-powered desktop productivity assistant that enables users to interact with their computer using voice or text. It combines desktop automation, browser automation, persistent memory, and a PDF assistant in a unified application.

Friday understands user intent, converts requests into structured tasks, and executes them through dedicated modules using an object-oriented architecture. It supports both text and voice input, with responses delivered in text and voice.

## Features

- **Voice and Text Interaction:** Interact with Friday through voice commands or text input, with text and voice responses.
- **Desktop Automation:** Control volume and brightness, manage files and folders, capture screenshots, open applications, and execute system power commands.
- **Browser Automation:** Open websites, search supported platforms, summarize webpage content, and compose emails.
- **Persistent Memory:** Store user preferences and saved folder locations locally, with secure API key storage through Windows Credential Manager.
- **PDF Assistant:** Upload PDFs and ask questions about their contents using Retrieval-Augmented Generation (RAG).
- **Screen and Content Analysis:** Analyze screenshots and explain, rewrite, or verify selected content.
- **Multi-Task Execution:** Handle multiple independent actions from a single request.
- **Structured Task Validation:** Validate task-router responses using Pydantic models before execution.

## Operating Modes

### 1. General Mode

Handles conversational queries and supports desktop and browser automation.

### 2. PDF Retrieval Mode

Uses the PDF assistant to retrieve relevant information from uploaded PDF documents and answer questions based on their contents.

The assistant uses a local embedding model and a RAG pipeline to retrieve relevant document content for answering queries.

## Architecture and Execution Flow

Friday follows a modular, object-oriented architecture.

```text
          User Input
        (Voice or Text)
                |
                v
       Speech-to-Text (Voice)
                |
                v
           TaskRouter
       (Intent Recognition)
                |
                v
     Structured JSON Response
                |
                v
       Pydantic Validation
                |
                v
          TaskRouter
       (Task Execution)
                |
          +-----+-----+
          |           |
          v           v
     DesktopModule  BrowserModule
          |           |
          v           v
     Desktop Actions Browser Actions
          |           |
          +-----+-----+
                |
                v
       Text-to-Speech / Text
```

The PDF assistant operates through the dedicated PDF Retrieval mode.

### Task Routing

Friday uses `openai/gpt-oss-20b` through Groq to interpret user requests and generate structured JSON containing an acknowledgement and an array of tasks.

Example:

```json
{
  "acknowledgement_before_task": "Searching YouTube for Abrar Shekh.",
  "tasks": [
    {
      "id": 1,
      "module": "browser",
      "action": "search_specific_website",
      "parameters": {
        "website_name": "youtube",
        "query": "Abrar Shekh"
      }
    }
  ]
}
```

A request can generate multiple independent tasks. Each task specifies its module, action, and parameters.

Pydantic validates the response using module- and action-specific schemas. The TaskRouter then dispatches each validated task to the corresponding module for execution.

This separates intent recognition, validation, and execution into distinct responsibilities.

## Modules

| Module | Responsibilities |
|---|---|
| Desktop Module | System controls, file and folder operations, application launching, screenshots, clipboard actions, and screen/content analysis |
| Browser Module | Website navigation, supported website searches, webpage summarization, and email composition |
| Persistent Memory | Local storage of user preferences and saved folder locations, with API keys stored separately using the operating system's credential manager |
| PDF Assistant | PDF retrieval and question answering using RAG |

## Persistent Memory

Friday stores user-specific configuration and folder information locally on the user's machine.

Stored information includes:

- Username and preferred nickname.
- User preferences.
- Saved folder names and their locations.

### Secure API Key Storage

Friday uses Python's `keyring` library to store the Groq API key in Windows Credential Manager rather than storing it as ordinary plaintext in the application's database.

This separates sensitive credentials from general application settings and uses the operating system's credential storage mechanism.

### Folder Management

Users can select folder paths through the Tauri folder picker and save them using the interface.

The memory interface supports:

- Viewing saved folder names and paths in a table.
- Searching saved folders.
- Deleting saved entries.
- Preventing duplicate folder names using case-insensitive matching.

For example, `DSA`, `dsa`, and `Dsa` are treated as the same folder name for memory purposes.

Friday also maintains saved paths when parent folders are renamed or moved, and removes affected entries when folders are deleted, according to its folder-management logic.

This allows users to refer to saved folders by name without repeatedly providing their full paths.

## PDF Assistant and RAG

Friday's PDF assistant uses Retrieval-Augmented Generation to answer questions using relevant content retrieved from uploaded PDF documents.

The pipeline uses:

- **PyMuPDF:** PDF text extraction.
- **all-MiniLM-L6-v2:** Local text embedding generation.
- **Vector retrieval:** Finding relevant document content for a query.
- **LLM:** Generating answers using retrieved context.

The embedding model runs locally on the user's machine. Users can upload multiple PDFs without a predefined application-level file-count or file-size limit.

Actual processing capacity depends on available system resources and the implementation's memory, storage, and processing constraints.

## Technology Stack

| Component | Technology |
|---|---|
| Desktop Application | Tauri |
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| Task Routing | Groq API - `openai/gpt-oss-20b` |
| Speech-to-Text | Groq API - `whisper-large-v3-turbo` |
| Text-to-Speech | Piper TTS |
| PDF Text Extraction | PyMuPDF |
| Embeddings | all-MiniLM-L6-v2 |
| Browser Automation | Playwright, Python `webbrowser` |
| Desktop Automation | PyAutoGUI and dedicated Python libraries |
| Response Validation | Pydantic |
| Credential Storage | Python `keyring`, Windows Credential Manager |

## Data and Privacy

Friday is designed to keep user-specific application data on the user's machine wherever practical.

- **User preferences and folder locations:** Stored locally.
- **API credentials:** Stored through Python `keyring`, using Windows Credential Manager on Windows.
- **PDF documents:** Stored locally on the user's machine.
- **Embedding generation:** Performed locally using `all-MiniLM-L6-v2`.

Some AI operations rely on hosted Groq models. Audio sent for transcription, prompts sent for task routing, and screenshots sent for vision analysis may be transmitted to the external API when those features are used.

Therefore, Friday is not entirely offline. Users should avoid submitting sensitive information to cloud services unless they are comfortable with the applicable provider's data-handling policies.

Using Windows Credential Manager also does not eliminate every security risk. The application must still protect credentials in memory, avoid exposing them through logs, and handle API errors safely.

## Building Friday

### 1. Build the Backend Executable

Run the following command from the project root in PowerShell:

```powershell
.\backend\.venv\Scripts\python.exe -m PyInstaller `
  --clean `
  --onedir `
  --name FridayBackend `
  --paths . `
  --collect-submodules backend `
  --collect-all chromadb `
  --collect-all chromadb_rust_bindings `
  --collect-all posthog `
  --collect-all rfc3987_syntax `
  --hidden-import backend.main `
  --hidden-import chromadb.api.rust `
  --hidden-import chromadb.telemetry.product.posthog `
  backend\launcher.py
```

The generated executable and its supporting files will be located in:

```text
dist/
└── FridayBackend/
    ├── FridayBackend.exe
    └── ...
```

The entire `FridayBackend` directory must be packaged with the application because PyInstaller is configured to use `--onedir`.

### 2. Build the Tauri Installer

Run the following command from the frontend directory containing `package.json`:

```powershell
npm run tauri build
```

Tauri will build the desktop application and generate the installer according to the bundle configuration in `tauri.conf.json`.

The installer is typically generated under:

```text
src-tauri/target/release/bundle/
```

The exact installer format and output location depend on the Tauri bundle configuration.

Ensure that the build configuration includes the packaged backend executable and its supporting files.

## Project Goals

Friday aims to simplify everyday computer interaction by combining conversational AI, structured task execution, desktop and browser automation, persistent memory, and document retrieval in one desktop assistant.

Its modular architecture makes it easier to maintain existing functionality and extend the system with additional actions and capabilities.

---

**Friday - Your AI-powered desktop productivity assistant.**
