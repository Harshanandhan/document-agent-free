# Documind (free)

Upload PDFs, CSV, or Excel. The app extracts text/tables, then Groq (Llama 3.3 70B) returns structured markdown — vendor, dates, line items, totals.

Live-style deploy: FastAPI + static UI. Images are accepted but **not OCR’d** (upload PDF/CSV instead).

## Stack

- FastAPI + Uvicorn
- Groq API (`GROQ_API_KEY`), model `llama-3.3-70b-versatile`
- pdfplumber, pandas, openpyxl, Pillow

## Run locally

```bash
pip install -r requirements.txt
set GROQ_API_KEY=your_key
uvicorn app:app --reload
```

Open http://localhost:8000

On Linux/macOS use `export GROQ_API_KEY=your_key`.

## API

- `GET /` — web UI (`static/index.html`)
- `POST /process` — form fields `task` + `files`
- `GET /health` — reports whether `GROQ_API_KEY` is set

## Deploy

`Procfile` + `railway.toml` are set up for Railway. Set `GROQ_API_KEY` in the host’s environment.

## Author

Harsha Nandhan Reddy Gajulapalli  
https://github.com/Harshanandhan
