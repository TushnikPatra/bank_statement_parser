import os
import pandas as pd

from banks.detector import detect_bank
from banks.icici_parser import parse_icici
from banks.yes_parser import parse_yes
from banks.axis_parser import parse_axis
from banks.hdfc_parser import parse_hdfc
from banks.sbi_parser import parse_sbi
from validator import validate_transactions


BANK_PARSERS = {
    "ICICI": parse_icici,
    "YES": parse_yes,
    "AXIS": parse_axis,
    "HDFC": parse_hdfc,
    "SBI": parse_sbi,
}


def process_pdf(pdf_path):

    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    if not os.path.exists(pdf_path):
        raise ValueError("File not found")

    bank = detect_bank(pdf_path)

    if bank not in BANK_PARSERS:
        raise ValueError("Unsupported Bank")

    final_rows = BANK_PARSERS[bank](pdf_path)

    if not final_rows:
        raise ValueError("No transactions extracted")

    if bank != "ICICI":
        validate_transactions(final_rows)

    return {
        "bank": bank,
        "transactions": final_rows
    }
