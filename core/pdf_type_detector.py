def detect_pdf_type(full_text, lines):
    """
    Detect PDF type:
    - TEXT: readable text
    - TABLE: table-like structure
    - SCANNED: almost no text
    """

    # Very little text → scanned PDF
    if len(full_text.strip()) < 300:
        return "SCANNED"

    # Table indicators (common in bank statements)
    table_markers = ["|", "----", "____", "Sl No", "Debit", "Credit", "Balance"]
    for line in lines:
        if any(marker in line for marker in table_markers):
            return "TABLE"

    return "TEXT"
