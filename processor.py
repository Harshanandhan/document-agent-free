"""
Document processor using Google Gemini Flash (free tier).
Extracts content from PDFs, images, CSV, Excel then sends to Gemini.
"""

import os
import base64
import mimetypes
from pathlib import Path

import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))

MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = """You are an expert document processing assistant. You analyze documents and extract structured information clearly and professionally.

When processing invoices or bills, always extract:
- Vendor / Company name
- Invoice number
- Invoice date & due date
- Line items (description, quantity, unit price, total)
- Subtotal, tax, and total amount
- Currency
- Billing address
- Payment terms

Format your response cleanly using markdown:
- Use tables for structured data
- Use headings to organize sections
- Use bold for important values
- Be concise and professional — no filler phrases

If multiple documents are provided, process each one and clearly separate the results."""

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def extract_pdf(path: Path) -> str:
    if not HAS_PDFPLUMBER:
        return f"[PDF: {path.name} — install pdfplumber to extract text]"
    lines = []
    with pdfplumber.open(str(path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            tables = page.extract_tables() or []
            if text:
                lines.append(f"--- Page {i+1} ---\n{text}")
            for table in tables:
                rows = [" | ".join(str(c or "") for c in row) for row in table]
                lines.append("\n".join(rows))
    return "\n\n".join(lines) or f"[No text found in {path.name}]"


def extract_csv_excel(path: Path) -> str:
    if not HAS_PANDAS:
        return f"[{path.name} — install pandas to extract data]"
    ext = path.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(str(path))
        return df.to_markdown(index=False)
    else:
        result = []
        xf = pd.ExcelFile(str(path))
        for sheet in xf.sheet_names:
            df = xf.parse(sheet)
            result.append(f"**Sheet: {sheet}**\n{df.to_markdown(index=False)}")
        return "\n\n".join(result)


def build_parts(files: list[Path], task: str) -> list:
    """Build Gemini content parts from files + task."""
    import google.generativeai.types as genai_types

    parts = []
    img_exts = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp"}

    for path in files:
        ext = path.suffix.lower()
        parts.append(f"\n### Document: {path.name}\n")

        if ext in img_exts:
            raw = path.read_bytes()
            mime, _ = mimetypes.guess_type(str(path))
            parts.append({"mime_type": mime or "image/jpeg", "data": raw})

        elif ext == ".pdf":
            text = extract_pdf(path)
            parts.append(text)

        elif ext in {".csv", ".xlsx", ".xls", ".xlsm"}:
            text = extract_csv_excel(path)
            parts.append(text)

        else:
            try:
                parts.append(path.read_text(encoding="utf-8", errors="replace")[:4000])
            except Exception:
                parts.append(f"[Could not read {path.name}]")

    parts.append(f"\n---\n**Task:** {task}")
    return parts


def process_documents(files: list[Path], task: str) -> str:
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=SYSTEM_PROMPT,
    )

    parts = build_parts(files, task)

    # Convert dicts (images) to Gemini Part objects
    content = []
    for part in parts:
        if isinstance(part, dict):
            content.append(genai.types.Part.from_data(
                data=part["data"],
                mime_type=part["mime_type"]
            ))
        else:
            content.append(str(part))

    response = model.generate_content(content)
    return response.text
