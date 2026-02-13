def validate_transactions(rows):
    if not rows or len(rows) < 2:
        return True  # nothing to validate

    for i in range(1, len(rows)):
        prev = rows[i - 1]
        curr = rows[i]

        expected_balance = (
            prev["Balance"]
            - curr["Debit"]
            + curr["Credit"]
        )

        if round(expected_balance, 2) != round(curr["Balance"], 2):
            raise ValueError(
                f"Balance mismatch at row {i}: "
                f"Expected {round(expected_balance,2)}, "
                f"got {curr['Balance']}"
            )

    return True
