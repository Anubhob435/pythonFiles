# 📄 OCR PDF Table Extractor (Hindi + English)

A **production-ready Python tool** to extract **tables from scanned PDFs** (image-based, no text layer) using **PaddleOCR + Tesseract**, and export them into **Excel / CSV** for further analysis or database ingestion.

Designed specifically for **government-style multi-page tabular PDFs** written in **Hindi (Devanagari) with English mix**.

---

## ✨ Features

* ✅ Handles **scanned PDFs** (image-only, no embedded text)
* ✅ Supports **Hindi + English OCR**
* ✅ Works on **multi-page tables**
* ✅ Automatically **reconstructs rows using visual layout**
* ✅ Skips title/cover pages (e.g. first page)
* ✅ Exports to **Excel (.xlsx)** and **CSV**
* ✅ Windows-safe (works with `uv`, `venv`, PowerShell)

---

## 🧠 Tech Stack

* **Python 3.11+**
* **PaddleOCR (PP-OCRv5 – Devanagari)**
* **Tesseract OCR**
* **Poppler (pdf2image backend)**
* **OpenCV**
* **Pandas**

---

## 📁 Project Structure

```
ocr_pdf_extractor/
│
├── main.py
├── input.pdf
├── README.md
├── output/
│   ├── images/
│   ├── tables.xlsx
│   └── tables.csv
└── .venv/
```

---

## 🔧 System Requirements (Windows)

### 1️⃣ Install Tesseract OCR

Download from:
👉 [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

During installation:

* ✔ Enable **Hindi (hin)** language
* ✔ Add to **PATH**

Verify:

```powershell
tesseract --version
tesseract --list-langs
```

You should see:

```
eng
hin
```

---

### 2️⃣ Install Poppler (Required for pdf2image)

Download:
👉 [https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)

Extract to:

```
C:\poppler
```

Verify:

```powershell
pdftoppm -h
pdfinfo -h
```

---

## 🐍 Python Environment Setup (Using uv)

Create and activate environment:

```powershell
uv venv
```

Install dependencies:

```powershell
uv add pdf2image pytesseract paddleocr paddlepaddle opencv-python pandas numpy tqdm
```

---

## ▶️ How to Run

1️⃣ Place your scanned PDF as:

```
input.pdf
```

2️⃣ Run the extractor:

```powershell
uv run python main.py
```

---

## 📤 Output

After successful execution:

```
output/
├── tables.xlsx   # Excel-ready tables
└── tables.csv    # Database / MySQL import
```

* Tables are reconstructed **row-wise**
* First page is automatically skipped
* Hindi text preserved

---

## ⚙️ Important Implementation Details

### Explicit Windows Paths (Mandatory)

To avoid PATH issues on Windows, the script explicitly sets:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\poppler\Library\bin"
```

This ensures compatibility with:

* `uv`
* `venv`
* PowerShell
* VS Code

---

## 🧪 Troubleshooting

### ❌ `PDFInfoNotInstalledError`

✔ Ensure `pdfinfo.exe` exists
✔ Ensure `poppler_path` is explicitly passed

---

### ❌ `TesseractNotFoundError`

✔ Set `pytesseract.pytesseract.tesseract_cmd`
✔ Restart PowerShell

---

### ❌ PaddleOCR KeyErrors / API issues

✔ This project uses **PP-OCRv5 compatible APIs**
✔ Uses `ocr.predict()` (not deprecated methods)

---

## 🚀 Future Enhancements

* Column header detection
* Duplicate row removal
* Hindi spelling normalization
* Direct MySQL/PostgreSQL export
* Streamlit dashboard
* Page auto-classification

---

## 📜 License

MIT License — free to use, modify, and distribute.


