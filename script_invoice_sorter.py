import os
import shutil
import pdfplumber
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file (for the API key)
load_dotenv()

# Initialize OpenAI client and load API key
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# Folder containing incoming invoices (PDFs)
SOURCE_FOLDER = Path("<replace>")

# Target folder where sorted files will be placed
DESTINATION_BASE = SOURCE_FOLDER / "Sorted"

# Regex to detect a date in the format YYYY-MM from the filename
FILENAME_DATE_REGEX = re.compile(r"(\d{4})[-_\.]?(\d{2})")

def extract_from_filename(filename: str):
    """
    Try to extract year and month from the filename.
    Supports formats like 2023-01, 202301, 2023_01, etc.
    """
    match = FILENAME_DATE_REGEX.search(filename)
    if match:
        return match.group(1), match.group(2)
    return None, None

def extract_text_from_pdf(pdf_path: Path):
    """
    Extract visible text content from all pages of the given PDF.
    Returns the combined text or an empty string if extraction fails.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        print(f"❌ Error reading {pdf_path.name}: {e}")
        return ""

def extract_date_from_text(text: str):
    """
    Ask GPT-4o to find the invoice issue date from the PDF text.
    Expects a result in the format YYYY-MM. Returns (year, month).
    """
    try:
        prompt = f"""
        Here is the text of an invoice. Please identify the month and year in which the invoice was issued.
        Return the result **only in the format YYYY-MM**. If no date can be found, just respond with "NONE".

        Text:
        {text[:4000]}
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        answer = response.choices[0].message.content.strip()
        match = re.search(r"(\d{4})-(\d{2})", answer)
        if match:
            return match.group(1), match.group(2)
    except Exception as e:
        print(f"🧠 AI error: {e}")
    return None, None

def organize_invoices():
    """
    Main function:
    - Scans all PDF files in the source folder
    - Tries to extract invoice date from the filename
    - If not found, extracts text and uses GPT to detect the date
    - Sorts PDFs into folders named by YYYY-MM or into 'Unsorted'
    """
    for file in SOURCE_FOLDER.iterdir():
        if file.is_file() and file.suffix.lower() == ".pdf":
            print(f"🔍 Processing file: {file.name}")

            # Step 1: Try extracting date from the filename
            year, month = extract_from_filename(file.name)

            # Step 2: If not found, extract from text using GPT
            if not (year and month):
                text = extract_text_from_pdf(file)
                year, month = extract_date_from_text(text)

            # Step 3: Define the destination folder
            if year and month:
                target_dir = DESTINATION_BASE / f"{year}-{month}"
            else:
                target_dir = DESTINATION_BASE / "Unsorted"

            # Create target folder if needed, and copy the file
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target_dir / file.name)
            print(f"✅ Saved: {file.name} → {target_dir}")

if __name__ == "__main__":
    organize_invoices()
