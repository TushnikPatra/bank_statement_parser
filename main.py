from parser.pdf_reader import read_pdf_pages
from parser.table_extractor import extract_tables_from_page
from parser.transaction_parser import rows_to_transactions
from parser.analyzer import analyze_transactions

PDF_PATH = "uploads/test.pdf"

if __name__ == "__main__":
    all_rows = []

    for page_no, page in read_pdf_pages(PDF_PATH):
        rows = extract_tables_from_page(page)
        all_rows.extend(rows)

    transactions = rows_to_transactions(all_rows)
    result = analyze_transactions(transactions)

    print("\n--- SUMMARY ---")
    print(result["summary"])

    print("\n--- FIRST 3 CREDIT TRANSACTIONS ---")
    for txn in result["credit_transactions"][:3]:
        print(txn)

    print("\n--- FIRST 3 DEBIT TRANSACTIONS ---")
    for txn in result["debit_transactions"][:3]:
        print(txn)
