import pdfplumber

def parse_sbi(pdf_path):

    final_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                for row in table:

                    if not row or len(row) < 7:
                        continue

                    # Skip header rows
                    if row[0] and "VALUE DATE" in row[0].upper():
                        continue

                    try:
                        date = row[0].strip() if row[0] else ""
                        narration = row[2].strip() if row[2] else ""

                        debit_raw = row[4].strip() if row[4] else ""
                        credit_raw = row[5].strip() if row[5] else ""
                        balance_raw = row[6].strip() if row[6] else ""

                        # Remove commas
                        debit_raw = debit_raw.replace(",", "")
                        credit_raw = credit_raw.replace(",", "")
                        balance_raw = balance_raw.replace(",", "")

                        debit_val = float(debit_raw) if debit_raw and debit_raw != "-" else 0.0
                        credit_val = float(credit_raw) if credit_raw and credit_raw != "-" else 0.0
                        balance_val = float(balance_raw) if balance_raw else 0.0

                        if date and balance_raw:
                            final_rows.append({
                                "Date": date,
                                "Narration": narration,
                                "Debit": debit_val,
                                "Credit": credit_val,
                                "Balance": balance_val
                            })

                    except:
                        continue

    return final_rows
