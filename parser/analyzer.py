def analyze_transactions(transactions):
    """
    Analyzes transactions and prepares summary
    exactly in the structure required by the UI.
    """

    credit_transactions = []
    debit_transactions = []

    total_credits = 0.0
    total_debits = 0.0

    for txn in transactions:
        if txn["type"] == "CREDIT":
            credit_transactions.append(txn)
            total_credits += txn["amount"]

        elif txn["type"] == "DEBIT":
            debit_transactions.append(txn)
            total_debits += txn["amount"]

    summary = {
        "total_credits": round(total_credits, 2),
        "total_debits": round(total_debits, 2),
        "net_amount": round(total_credits - total_debits, 2)
    }

    return {
        "summary": summary,
        "credit_transactions": credit_transactions,
        "debit_transactions": debit_transactions
    }
