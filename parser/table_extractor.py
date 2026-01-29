def extract_tables_from_page(page):
    """
    Extracts all tables from a single PDF page.
    Returns a list of rows.
    """
    rows = []
    tables = page.extract_tables()

    if not tables:
        return rows

    for table in tables:
        for row in table:
            if row and any(cell for cell in row):
                cleaned_row = [
                    cell.strip() if cell else "" for cell in row
                ]
                rows.append(cleaned_row)

    return rows
