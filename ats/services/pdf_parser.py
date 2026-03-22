import io

from pdfminer.high_level import extract_text


def extract_text_from_pdf(file):
    try:
        file.seek(0)
        pdf_bytes = file.read()
        if not pdf_bytes:
            return None
        text = extract_text(io.BytesIO(pdf_bytes))
        cleaned = (text or "").strip()
        if not cleaned:
            return None
        file.seek(0)
        return cleaned
    except Exception:
        return None
