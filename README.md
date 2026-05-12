# Document Processing Agent — Free & Open Source

An AI-powered document processing tool built with **Google Gemini 2.0 Flash** (free tier). Upload invoices, PDFs, spreadsheets, or scanned images — the AI extracts, validates, and structures your data instantly. No API costs.

## Features

- **Extract** structured data from invoices and bills (vendor, amounts, dates, line items)
- **Read** PDFs, CSV, Excel, and scanned images (vision)
- **Validate** invoice data — field checks and amount math
- **Compare** multiple documents side by side
- **Up to 5 files** per request
- **100% free** — powered by Gemini Flash free tier (1,500 requests/day)

## Tech Stack

- [Google Gemini 1.5 Flash](https://ai.google.dev) — multimodal AI (text + vision), free tier
- FastAPI — web server
- pdfplumber — PDF text & table extraction
- pandas — CSV/Excel processing
- Pillow — image handling

## Getting Started

```bash
pip install -r requirements.txt
```

Get a free API key at [aistudio.google.com](https://aistudio.google.com) — no credit card required.

```bash
export GOOGLE_API_KEY=your-key-here
uvicorn app:app --reload
```

Open `http://localhost:8000`

## Deploy on Railway

1. Push this repo to GitHub
2. Connect to [railway.app](https://railway.app)
3. Add environment variable: `GOOGLE_API_KEY=your-key`
4. Done — Railway gives you a public URL

## Author

**Harsha Nandhan Reddy**
- GitHub: [@Harshanandhan](https://github.com/Harshanandhan)
- Email: harshanandhan09@gmail.com
- Python developer · AI/ML Graduate · Blockchain & Web3 · Cybersecurity

## License

MIT
