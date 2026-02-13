import camelot


def extract_tables(pdf_path):
    """
    Extract tables from a bank statement PDF using Camelot.
    Returns a list of pandas DataFrames.
    """
    tables = camelot.read_pdf(
        pdf_path,
        pages="all",
        flavor="stream"   # safest for bank statements
    )

    print(f"Tables detected: {len(tables)}")

    dataframes = []
    for i, table in enumerate(tables):
        df = table.df
        print(f"\n--- TABLE {i+1} (first 5 rows) ---")
        print(df.head())
        dataframes.append(df)

    return dataframes
