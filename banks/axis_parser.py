import pdfplumber
import re


def clean_amount(val):
    if not val:
        return 0.0
    return float(val.replace(",", "").strip())


def parse_axis(pdf_path):

    final_rows = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                header_row_index = None
                col_map = {}

                # --- Step 1: Find header row dynamically ---
                for i, row in enumerate(table):
                    row_text = " ".join([str(x).upper() for x in row if x])

                    if "TRANSACTION" in row_text and "BALANCE" in row_text:
                        header_row_index = i
                        break

                if header_row_index is None:
                    continue

                header = table[header_row_index]

                # --- Step 2: Map columns ---
                for idx, col in enumerate(header):
                    if not col:
                        continue

                    col_upper = col.upper()

                    if "TRANSACTION" in col_upper and "DATE" in col_upper:
                        col_map["date"] = idx
                    elif "PARTICULAR" in col_upper:
                        col_map["narration"] = idx
                    elif "AMOUNT" in col_upper:
                        col_map["amount"] = idx
                    elif "DEBIT/CREDIT" in col_upper:
                        col_map["drcr"] = idx
                    elif "BALANCE" in col_upper:
                        col_map["balance"] = idx

                if not col_map:
                    continue

                # --- Step 3: Read data rows ---
                for row in table[header_row_index + 1:]:

                    if not row:
                        continue

                    row = [str(x).strip() if x else "" for x in row]

                    try:
                        txn_date = row[col_map["date"]]
                        narration = row[col_map["narration"]]
                        amount = clean_amount(row[col_map["amount"]])
                        drcr = row[col_map["drcr"]].upper()
                        balance = clean_amount(row[col_map["balance"]])

                    except:
                        continue

                    if not txn_date:
                        continue

                    debit = 0.0
                    credit = 0.0

                    if drcr == "DR":
                        debit = amount
                    elif drcr == "CR":
                        credit = amount

                    final_rows.append({
                        "Date": txn_date,
                        "UTR": "",
                        "Debit": debit,
                        "Credit": credit,
                        "Balance": balance,
                        "Narration": narration
                    })

    return final_rows
