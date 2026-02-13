import os
import pandas as pd
from core.engine import process_pdf


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    PDF_NAME = "test.pdf"  # change for testing

    PDF_PATH = os.path.join(BASE_DIR, "test_pdfs", PDF_NAME)

    result = process_pdf(PDF_PATH)

    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(
        OUTPUT_DIR,
        PDF_NAME.replace(".pdf", "_transactions.xlsx")
    )

    df = pd.DataFrame(result["transactions"])
    df.to_excel(output_path, index=False)

    print("Detected Bank:", result["bank"])
    print("Transactions:", len(df))
    print("Saved to:", output_path)
