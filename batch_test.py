import os
import subprocess
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FOLDER = os.path.join(BASE_DIR, "test_pdfs")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

REPORT_PATH = os.path.join(OUTPUT_FOLDER, "batch_report.csv")

python_exe = "python"  # change if needed

pdf_files = [ f for f in os.listdir(TEST_FOLDER)
    if f.lower().endswith(".pdf")]

report_rows = []

for pdf in pdf_files:
    print("\n==============================")
    print("TESTING:", pdf)
    print("==============================")

    env = os.environ.copy()
    env["PDF_NAME"] = pdf

    result = subprocess.run(
        [python_exe, "main.py"],
        cwd=BASE_DIR,
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("SUCCESS", pdf)
        status = "SUCCESS"
        output_file = f"{os.path.splitext(pdf)[0]}_transactions.xlsx"
        log = ""
    else:
        print("FAILED", pdf)
        print(result.stderr)
        status = "FAILED"
        output_file = ""
        log = result.stderr.strip()

    report_rows.append([pdf, status, output_file, log])


# Write CSV report
with open(REPORT_PATH, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["PDF", "Status", "Output", "Log"])
    writer.writerows(report_rows)

print("\nBatch report saved to:", REPORT_PATH)
