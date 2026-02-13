from core.table_extractor import extract_tables


def parse_icici(pdf_path):

    tables = extract_tables(pdf_path)
    final_rows = []

    for df in tables:

        df = df.astype(str)
        current_txn = None

        for _, row in df.iterrows():

            row_values = [str(x).strip() for x in row.tolist()]

            if not row_values:
                continue

            first_col = row_values[0]

            # NEW TRANSACTION ROW
            if first_col.isdigit():

                if current_txn:
                    final_rows.append(current_txn)

                total_cols = len(row_values)

                # ICICI structure: last = balance, second last = credit, third last = debit
                balance_index = total_cols - 1
                credit_index = total_cols - 2
                debit_index = total_cols - 3

                current_txn = {
                    "Date": row_values[3] if len(row_values) > 3 else "",
                    "UTR": row_values[1] if len(row_values) > 1 else "",
                    "Debit": 0.0,
                    "Credit": 0.0,
                    "Balance": 0.0,
                    "Narration": row_values[6] if len(row_values) > 6 else ""
                }

                # Extract Debit
                debit_val = row_values[debit_index].replace(",", "").strip()
                if debit_val and debit_val.replace(".", "").isdigit():
                    current_txn["Debit"] = float(debit_val)

                # Extract Credit
                credit_val = row_values[credit_index].replace(",", "").strip()
                if credit_val and credit_val.replace(".", "").isdigit():
                    current_txn["Credit"] = float(credit_val)

                # Extract Balance
                balance_val = row_values[balance_index].replace(",", "").strip()
                if balance_val and balance_val.replace(".", "").isdigit():
                    current_txn["Balance"] = float(balance_val)

            # CONTINUATION ROW
            else:
                if current_txn:
                    # Only append text columns (ignore numeric columns)
                    text_parts = []
                    for val in row_values:
                        if not val.replace(",", "").replace(".", "").isdigit():
                            text_parts.append(val)

                    current_txn["Narration"] += " " + " ".join(text_parts)

        if current_txn:
            final_rows.append(current_txn)

    return final_rows
