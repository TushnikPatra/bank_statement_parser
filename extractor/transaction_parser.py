import re

DATE_PATTERNS = [
    r"\d{2}/[A-Za-z]{3}/\d{4}",
    r"\d{2}/\d{2}/\d{4}",
    r"\d{2}-\d{2}-\d{4}"
]

AMOUNT_PATTERN = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")


def extract_transaction_from_block(block_lines, bank_rules=None):
    if bank_rules is None:
        bank_rules = {}

    text = " ".join(block_lines)
    text = re.sub(r"\s+", " ", text).strip()

    # ================= DATE =================
    txn_date = ""
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            txn_date = match.group()
            break

    # ================= AMOUNTS =================
    amounts = [float(a.replace(",", "")) for a in AMOUNT_PATTERN.findall(text)]

    debit = 0.0
    credit = 0.0
    balance = 0.0

    if len(amounts) >= 2:
        balance = amounts[-1]

        # ICICI logic:
        # If narration contains deposit keywords → credit
        upper_text = text.upper()

        if any(k in upper_text for k in ["CASH DEP", "CAM/", "NEFT", "RTGS", "IMPS", "INF/", "INFT/"]):
            credit = amounts[-2]
        else:
            debit = amounts[-2]

    txn_amount = debit if debit > 0 else credit

    # ================= UTR =================
    utr = ""
    candidates = re.findall(r"\b\d{10,}\b", text)
    if candidates:
        utr = candidates[0]

    # ================= NARRATION CLEAN =================
    narration = text

    for p in DATE_PATTERNS:
        narration = re.sub(p, "", narration)

    narration = re.sub(r"\d{1,2}:\d{2}:\d{2}\s*(AM|PM)", "", narration)

    for amt in AMOUNT_PATTERN.findall(text):
        narration = narration.replace(amt, "")

    if utr:
        narration = narration.replace(utr, "")

    narration = narration.replace("/", " ").replace("-", " ")
    narration = re.sub(r"\s+", " ", narration).strip()

    return {
        "date": txn_date,
        "utr": utr,
        "debit": round(debit, 2),
        "credit": round(credit, 2),
        "txn_amount": round(txn_amount, 2),
        "balance": round(balance, 2),
        "narration": narration
    }
