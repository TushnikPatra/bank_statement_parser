import re

# ---------------- DATE REGEX ----------------
ICICI_DATE_RE = re.compile(
    r"\d{2}/[A-Za-z]{3}/\d{2,4}"
    r"|\d{2}/\d{2}/\d{4}"
    r"|\d{2}-\d{2}-\d{4}"
)

SBI_DATE_COL_RE = re.compile(r"\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}")

AXIS_DATE_RE = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
AXIS_AMOUNT_RE = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")


# ---------------- ICICI ----------------
def build_icici_blocks(df):
    blocks = []
    current_block = []

    for _, row in df.iterrows():
        row_text = " ".join(str(c) for c in row if str(c).strip())

        if ICICI_DATE_RE.search(row_text):
            if current_block:
                blocks.append(current_block)
                current_block = []
            current_block.append(row_text)
        else:
            if current_block:
                current_block.append(row_text)

    if current_block:
        blocks.append(current_block)

    return blocks


# ---------------- SBI ----------------
def build_sbi_blocks(df):
    blocks = []
    current_block = []

    for _, row in df.iterrows():
        col0 = str(row.iloc[0]).strip()
        row_text = " ".join(str(c) for c in row if str(c).strip())

        if SBI_DATE_COL_RE.search(col0):
            if current_block:
                blocks.append(current_block)
                current_block = []
            current_block.append(row_text)
        else:
            if current_block:
                current_block.append(row_text)

    if current_block:
        blocks.append(current_block)

    return blocks


# ---------------- AXIS (FIXED) ----------------
def build_axis_blocks(df):
    blocks = []
    current_block = []
    date_seen = False

    for _, row in df.iterrows():
        row_text = " ".join(str(c) for c in row if str(c).strip())

        # Date row
        if AXIS_DATE_RE.search(row_text):
            if current_block:
                blocks.append(current_block)
                current_block = []

            current_block.append(row_text)
            date_seen = True
            continue

        # Narration row
        if date_seen and not AXIS_AMOUNT_RE.search(row_text):
            current_block.append(row_text)
            continue

        # Amount row (ends transaction)
        if date_seen and AXIS_AMOUNT_RE.search(row_text):
            current_block.append(row_text)
            blocks.append(current_block)
            current_block = []
            date_seen = False

    return blocks


# ---------------- HDFC ----------------
def build_hdfc_blocks(df):
    return build_icici_blocks(df)


# ---------------- KOTAK ----------------
def build_kotak_blocks(df):
    return build_sbi_blocks(df)


# ---------------- YES BANK ----------------
def build_yes_blocks(df):
    return build_icici_blocks(df)
