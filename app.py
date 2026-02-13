import os
import uuid
import shutil
import pandas as pd

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse

from banks.detector import detect_bank
from banks.icici_parser import parse_icici
from banks.yes_parser import parse_yes
from banks.axis_parser import parse_axis
from banks.hdfc_parser import parse_hdfc
from banks.sbi_parser import parse_sbi


# ----------------------------------------
# FASTAPI INIT
# ----------------------------------------
app = FastAPI(title="Bank Statement Parser API")


# ----------------------------------------
# BANK PARSER MAP
# ----------------------------------------
BANK_PARSERS = {
    "ICICI": parse_icici,
    "YES": parse_yes,
    "AXIS": parse_axis,
    "HDFC": parse_hdfc,
    "SBI": parse_sbi,
}


# ----------------------------------------
# DIRECTORY SETUP
# ----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ----------------------------------------
# UPLOAD ENDPOINT
# ----------------------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # 1️⃣ Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    unique_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{unique_id}.pdf")

    # Save PDF
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect bank
    bank = detect_bank(pdf_path)

    if bank not in BANK_PARSERS:
        raise HTTPException(status_code=400, detail="Unsupported Bank")

    # Parse
    transactions = BANK_PARSERS[bank](pdf_path)

    if not transactions:
        raise HTTPException(status_code=400, detail="No transactions extracted")

    # Export Excel
    excel_filename = f"{unique_id}_transactions.xlsx"
    excel_path = os.path.join(OUTPUT_DIR, excel_filename)

    df = pd.DataFrame(transactions)
    df.to_excel(excel_path, index=False)

    return {
        "bank_detected": bank,
        "transactions_count": len(transactions),
        "download_url": f"/download/{excel_filename}"
    }



# ----------------------------------------
# DOWNLOAD ENDPOINT
# ----------------------------------------
@app.get("/download/{filename}")
def download_file(filename: str):

    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
