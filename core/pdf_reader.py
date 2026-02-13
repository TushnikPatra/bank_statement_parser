import pdfplumber


def read_pdf_text(pdf_path):
    """
    Reads text from all pages of a PDF.
    Returns a list of page texts.
    """
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            pages.append({
                "page": page_number,
                "text": text or ""
            })

    return pages
def split_pages_into_lines(pages):
    """
    Takes output of read_pdf_text()
    Returns a flat list of clean text lines.
    """
    lines = []

    for page in pages:
        text = page["text"]
        if not text:
            continue

        for line in text.splitlines():
            clean_line = line.strip()
            if clean_line:
                lines.append(clean_line)

    return lines


