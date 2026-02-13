BANK_RULES = {
    "ICICI": {
        "utr_prefixes": ["IMPS", "NEFT", "RTGS", "ICICN", "YESBN"],
        "ignore_number_lengths": [15, 16]  # account numbers
    },
    "HDFC": {
        "utr_prefixes": ["IMPS", "NEFT", "UTR"],
        "ignore_number_lengths": [14, 16]
    },
    "SBI": {
        "utr_prefixes": ["IMPS", "NEFT", "UTR"],
        "ignore_number_lengths": [11, 17]
    },
    "AXIS": {
        "utr_prefixes": ["IMPS", "NEFT", "AXIS"],
        "ignore_number_lengths": [15]
    },
    "YES": {
        "utr_prefixes": ["IMPS", "NEFT", "YESBN"],
        "ignore_number_lengths": [16]
    },
     "UNKNOWN": {
        "utr_prefixes": ["IMPS", "NEFT", "RTGS"],
        "ignore_number_lengths": [],
    }

}

