"""Read PDF files into the internal document model (best-effort).

Supports both text-based and image-based (scanned) PDFs.
For image-based pages, falls back to OCR via Tesseract if available.
"""

import os

# ---------------------------------------------------------------------------
# OCR availability check (done once at import time)
# ---------------------------------------------------------------------------

_OCR_AVAILABLE = False
_OCR_UNAVAILABLE_REASON = ""

try:
    import pytesseract
    from PIL import Image

    # On Windows, Tesseract is often installed but not on PATH.
    # Check common install locations.
    import shutil
    if not shutil.which("tesseract"):
        _common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
        ]
        for path in _common_paths:
            if os.path.isfile(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break

    pytesseract.get_tesseract_version()
    _OCR_AVAILABLE = True
except ImportError:
    _OCR_UNAVAILABLE_REASON = (
        "pytesseract or Pillow not installed. "
        "Install with: pip install pytesseract Pillow"
    )
except Exception as e:
    _OCR_UNAVAILABLE_REASON = (
        f"Tesseract binary not found or not working: {e}. "
        "Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki"
    )


def _ocr_page_pdfplumber(page):
    """Render a pdfplumber page to image and run OCR on it.

    Returns extracted text string, or empty string on failure.
    """
    if not _OCR_AVAILABLE:
        return ""

    try:
        # Render page to a PIL Image at 300 DPI for good OCR quality
        page_image = page.to_image(resolution=300)
        pil_image = page_image.original

        # Run Tesseract OCR
        text = pytesseract.image_to_string(pil_image)
        return text.strip() if text else ""
    except Exception:
        return ""


def _ocr_page_pymupdf(filepath, page_num):
    """Fallback: use PyMuPDF to render page to image for OCR.

    Used when pdfplumber's to_image isn't available or fails.
    """
    if not _OCR_AVAILABLE:
        return ""

    try:
        import fitz  # PyMuPDF
        from PIL import Image
        import io

        doc = fitz.open(filepath)
        page = doc[page_num]
        # Render at 300 DPI (default is 72, so matrix scale = 300/72)
        mat = fitz.Matrix(300 / 72, 300 / 72)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        pil_image = Image.open(io.BytesIO(img_bytes))
        doc.close()

        text = pytesseract.image_to_string(pil_image)
        return text.strip() if text else ""
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Main reader
# ---------------------------------------------------------------------------

def read_pdf(filepath):
    """Extract text from a PDF and structure it as paragraphs.

    PDF extraction is inherently lossy — we do our best to preserve
    paragraph breaks but headings, tables, and formatting are approximate.

    For pages with no extractable text (image-based/scanned PDFs), falls
    back to OCR via Tesseract if available.
    """
    blocks = []
    title = os.path.splitext(os.path.basename(filepath))[0]
    ocr_used = False
    ocr_failed_pages = []

    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()

                # If no text extracted, attempt OCR
                if not text or not text.strip():
                    # Try pdfplumber's built-in image rendering first
                    text = _ocr_page_pdfplumber(page)

                    # If that failed, try PyMuPDF rendering
                    if not text:
                        text = _ocr_page_pymupdf(filepath, page_num)

                    if text:
                        ocr_used = True
                    else:
                        ocr_failed_pages.append(page_num + 1)
                        continue

                # Parse extracted text into blocks
                paragraphs = text.split("\n\n")
                for para in paragraphs:
                    cleaned = para.strip()
                    if cleaned:
                        # Heuristic: short all-caps or bold-looking lines might be headings
                        if len(cleaned) < 80 and cleaned.isupper():
                            blocks.append({"type": "heading", "level": 2, "text": cleaned.title()})
                        else:
                            # Rejoin soft-wrapped lines within a paragraph
                            lines = cleaned.split("\n")
                            joined = " ".join(l.strip() for l in lines)
                            blocks.append({"type": "paragraph", "text": joined})

                # Try to extract tables (only works on text-based pages)
                try:
                    tables = page.extract_tables()
                    for table in tables:
                        rows = []
                        for row in table:
                            cells = [str(cell).strip() if cell else "" for cell in row]
                            rows.append(cells)
                        if rows:
                            blocks.append({"type": "table", "rows": rows})
                except Exception:
                    pass

    except Exception as e:
        blocks.append({"type": "paragraph", "text": f"[PDF extraction error: {e}]"})

    # Add informational notes about OCR usage
    if ocr_used:
        blocks.insert(0, {
            "type": "paragraph",
            "text": "[Note: This document was converted using OCR. Please review for accuracy.]"
        })

    if ocr_failed_pages:
        if not _OCR_AVAILABLE:
            msg = (
                f"[Warning: Pages {', '.join(str(p) for p in ocr_failed_pages)} "
                f"appear to be image-based but OCR is not available. "
                f"{_OCR_UNAVAILABLE_REASON}]"
            )
        else:
            msg = (
                f"[Warning: OCR could not extract text from pages "
                f"{', '.join(str(p) for p in ocr_failed_pages)}.]"
            )
        blocks.append({"type": "paragraph", "text": msg})

    return {
        "title": title,
        "blocks": blocks,
    }
