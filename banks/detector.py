import pdfplumber


def detect_bank(pdf_path):
    header_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for i in range(min(2, len(pdf.pages))):
            text = pdf.pages[i].extract_text()
            if text:
                header_text += text.upper()

    header_text = header_text[:2500]

    
    
    

    # ---- STRICT ORDER ----

    # 1️⃣ SBI (most specific first)
    if "STATE BANK OF INDIA" in header_text:
        return "SBI"

    # 2️⃣ ICICI
    if "ICICI BANK" in header_text:
        return "ICICI"

    # 3️⃣ YES (IFSC prefix YESB only)
    if "IFSC" in header_text and "YESB" in header_text:
        return "YES"

    # 4️⃣ HDFC (IFSC prefix HDFC)
    if "IFSC" in header_text and "HDFC" in header_text:
        return "HDFC"

    # 5️⃣ AXIS
    if "AXIS BANK" in header_text:
        return "AXIS"

    return "UNKNOWN"
