import pdfplumber
import re
from datetime import datetime


def clean_amount(val):
    return float(val.replace(",", "").strip())


def parse_hdfc(pdf_path):

    final_rows = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")

            for line in lines:

                # Match HDFC transaction pattern
                # Date ... Debit Credit Balance
                match = re.search(
                    r"(\d{2}/\d{2}/\d{2}).*?(\d{1,3}(?:,\d{3})*\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})$",
                    line
                )

                if not match:
                    continue

                date_val = match.group(1)
                amount1 = clean_amount(match.group(2))
                amount2 = clean_amount(match.group(3))

                # Last amount is balance
                balance = amount2

                # Determine debit or credit from balance change later
                final_rows.append({
                    "Date": date_val,
                    "UTR": "",
                    "Debit": 0.0,
                    "Credit": 0.0,
                    "Balance": balance,
                    "Narration": line
                })

    # Sort by date
    final_rows.sort(
        key=lambda x: datetime.strptime(x["Date"], "%d/%m/%y")
    )

    # Compute debit/credit from balance difference
    previous_balance = None

    for txn in final_rows:

        if previous_balance is None:
            previous_balance = txn["Balance"]
            continue

        diff = txn["Balance"] - previous_balance

        if diff > 0:
            txn["Credit"] = round(diff, 2)
        else:
            txn["Debit"] = round(abs(diff), 2)

        previous_balance = txn["Balance"]

    return final_rows
