# For use with PrivateGPT to weed out problematic PDFs
# python fitz_validate.py /path/to/source/directory

import fitz
import sys
import shutil
import os

def read_pdf(path: str) -> str:
    try:
        doc = fitz.open(path)
    except fitz.fitz.FileDataError:
        print(f"Error: Unable to open or read the document '{path}'. It may be broken.")
        quarantine_file(path)
        return ""

    txt = ""
    for page in doc:
        txt += page.get_text("text")
    return txt

def quarantine_file(file_path: str, quarantine_dir: str = './quarantine/') -> None:
    """Moves the problematic file to a quarantine directory."""
    if not os.path.exists(quarantine_dir):
        os.makedirs(quarantine_dir)

    shutil.move(file_path, os.path.join(quarantine_dir, os.path.basename(file_path)))
    print(f"Moved '{file_path}' to the quarantine directory.")

if len(sys.argv) < 2:
    print("Please provide a path to the source directory as an argument.")
    sys.exit(1)

source_dir = sys.argv[1]
if not os.path.exists(source_dir):
    print(f"The directory '{source_dir}' does not exist.")
    sys.exit(1)

# Loop through all files in the source directory
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            txt = read_pdf(pdf_path)
            if txt:
                print(txt)

