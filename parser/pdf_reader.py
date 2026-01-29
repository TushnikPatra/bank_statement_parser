import pdfplumber


def read_pdf_pages(pdf_path):
    """
    Generator that yields (page_number, page_object)
    This is memory-safe and works for large PDFs.
    """
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF opened successfully. Total pages: {total_pages}")

        for page_number, page in enumerate(pdf.pages, start=1):
            yield page_number, page
