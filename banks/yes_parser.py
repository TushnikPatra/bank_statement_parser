import pdfplumber
import pandas as pd


def parse_yes(pdf_path):

    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)

                # Remove empty rows
                df = df.dropna(how="all")

                # Skip header rows
                df = df[df.apply(lambda row: not str(row[0]).startswith("Report"), axis=1)]
                df = df[df.apply(lambda row: not str(row[0]).startswith("Transaction Date"), axis=1)]

                for _, row in df.iterrows():
                    row_values = [str(x).strip() if x else "" for x in row.tolist()]

                    # Must contain date pattern
                    if "-" not in row_values[0]:
                        continue

                    try:
                        date = row_values[0]

                        narration = row_values[2]

                        debit = 0.0
                        credit = 0.0

                        # Debit column usually index 4
                        if row_values[4]:
                            debit = float(row_values[4].replace(",", ""))

                        # Credit column usually index 5
                        if row_values[5]:
                            credit = float(row_values[5].replace(",", ""))

                        balance = float(row_values[6].replace(",", ""))

                        transactions.append({
                            "Date": date,
                            "UTR": "",
                            "Debit": debit,
                            "Credit": credit,
                            "Balance": balance,
                            "Narration": narration
                        })

                    except:
                        continue

    return transactions
