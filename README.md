## 🧾 AI-Assisted PDF Invoice Sorter

This Python script automatically organizes PDF invoices from a specified folder into subfolders based on their **issue month and year**.  
It first attempts to extract the date from the filename. If that fails, it uses **OpenAI's GPT-4o** to extract the date from the **PDF content**.

---

### 🔧 Features

- ✅ Extracts `YYYY-MM` from the filename using regex
- 🧠 Uses GPT-4o to identify the invoice date from text inside the PDF
- 🗂️ Automatically moves files into folders like `Sorted/2023-01/`
- 📁 Falls back to `Sorted/Unsorted/` if no date is found
- 🔐 Loads your OpenAI API key securely from a `.env` file

---

### 📦 Requirements

- Python 3.8+
- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- `.env` file with:

```env
OPENAI_API_KEY=sk-...
```

- Install dependencies:

```bash
pip install openai pdfplumber python-dotenv
```

---

### 📁 Output Folder Structure

```
INVOICES /
├── invoice_sample.pdf
└── Sorted/
    ├── 2023-01/
    │   └── invoice_sample.pdf
    └── Unsorted/
        └── no_date_detected.pdf
```

---

### 🚀 Usage

1. Adjust the `SOURCE_FOLDER` variable in the script to point to your PDF directory.
2. Run the script:

```bash
python organize_invoices.py
```

---

### 💡 Notes

- Uses `pdfplumber` to extract text from PDFs
- GPT-4o is only queried when no date is found in the filename (efficient!)
- Ideal for bookkeeping, pre-accounting workflows, or automating document organization

---

Let me know if you'd like a `README.md` file version or a version with badges and GitHub Actions setup!
