"""
Document Processing Agent (Free) — Web Server
Uses Google Gemini Flash (free tier). No API costs.
"""

import os
import uuid
import shutil
import asyncio
import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from processor import process_documents

app = FastAPI(title="Document Processing Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=10)

UPLOAD_DIR = Path(tempfile.gettempdir()) / "doc_agent_free"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/process")
async def process(
    task: str = Form(...),
    files: list[UploadFile] = File(default=[]),
):
    session_dir = UPLOAD_DIR / str(uuid.uuid4())
    session_dir.mkdir(parents=True)

    try:
        saved = []
        for file in files:
            if file and file.filename:
                dest = session_dir / Path(file.filename).name
                with open(dest, "wb") as f:
                    shutil.copyfileobj(file.file, f)
                saved.append(dest)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            lambda: process_documents(saved, task)
        )

        return JSONResponse({"status": "ok", "result": result})

    except Exception as e:
        return JSONResponse({"status": "error", "result": str(e)}, status_code=500)

    finally:
        shutil.rmtree(session_dir, ignore_errors=True)


@app.get("/health")
async def health():
    return {"status": "ok", "model": "gemini-2.0-flash", "api_key_set": bool(os.environ.get("GOOGLE_API_KEY"))}


static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
