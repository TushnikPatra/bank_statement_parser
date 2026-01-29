import re
from dateutil.parser import parse


def is_valid_date(value):
    if not value:
        return False

    value = str(value).strip()

    # Reject serial numbers like '1', '2'
    if value.isdigit():
        return False

    try:
        parse(value, fuzzy=False)
        return True
    except Exception:
        return False


def clean_amount(value):
    if not value:
        return 0.0

    value = str(value)
    value = value.replace(",", "").replace("₹", "").strip()

    try:
        return float(value)
    except Exception:
        return 0.0


def rows_to_transactions(rows):
    """
    Parser for YOUR bank statement structure
    """
    transactions = []

    for row in rows:
        # Safety: your table has 10 columns
        if len(row) < 9:
            continue

        txn_date = row[3]          # Transaction Date
        narration = row[6]         # Transaction Remarks
        debit_raw = row[7]         # Withdrawal (Dr)
        credit_raw = row[8]        # Deposit (Cr)

        # Validate date
        if not is_valid_date(txn_date):
            continue

        debit = clean_amount(debit_raw)
        credit = clean_amount(credit_raw)

        if credit > 0:
            txn_type = "CREDIT"
            amount = credit
        elif debit > 0:
            txn_type = "DEBIT"
            amount = debit
        else:
            continue  # skip zero rows

        transactions.append({
            "date": txn_date,
            "narration": narration.replace("\n", " ").strip(),
            "amount": round(amount, 2),
            "type": txn_type
        })

    return transactions
