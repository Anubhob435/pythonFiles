import os
import cv2
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from tqdm import tqdm

# ================== CONFIG ==================
PDF_PATH = "input.pdf"
IMG_DIR = "output/images"
EXCEL_OUT = "output/tables.xlsx"
CSV_OUT = "output/tables.csv"
DPI = 300
ROW_Y_THRESHOLD = 25   # controls row grouping
# ============================================

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

print("🔹 Initializing OCR model (Hindi + English)...")
ocr = PaddleOCR(
    lang="hi",
    use_textline_orientation=True
)


# ---------------------------------------------------
# STEP 1: Convert PDF → Images
# ---------------------------------------------------
print("📄 Converting PDF to images...")
pages = convert_from_path(
    PDF_PATH,
    dpi=DPI,
    poppler_path=r"C:\poppler-25.12.0\Library\bin"
)


image_paths = []
for i, page in enumerate(pages):
    path = f"{IMG_DIR}/page_{i+1}.png"
    page.save(path, "PNG")
    image_paths.append(path)

print(f"✅ {len(image_paths)} pages converted")

# ---------------------------------------------------
# STEP 2: OCR + TABLE RECONSTRUCTION
# ---------------------------------------------------
all_rows = []

for img_path in tqdm(image_paths[1:], desc="🔍 OCR Processing"):
    result = ocr.predict(img_path)

    if not result:
        continue

    rows = {}

    for item in result:
        box = item["dt_polys"]
        text = item["rec_text"]

        x = int(box[0][0])
        y = int(box[0][1])

        row_key = y // ROW_Y_THRESHOLD
        rows.setdefault(row_key, []).append((x, text))

    for r in rows.values():
        r.sort(key=lambda x: x[0])
        row_text = [cell[1] for cell in r]

        if len(row_text) >= 4:
            all_rows.append(row_text)


# ---------------------------------------------------
# STEP 3: Normalize column count
# ---------------------------------------------------
max_cols = max(len(r) for r in all_rows)

normalized = []
for row in all_rows:
    row += [""] * (max_cols - len(row))
    normalized.append(row)

df = pd.DataFrame(normalized)

# ---------------------------------------------------
# STEP 4: Save Output
# ---------------------------------------------------
df.to_excel(EXCEL_OUT, index=False, header=False)
df.to_csv(CSV_OUT, index=False, header=False)

print("\n🎉 DONE!")
print(f"📊 Excel saved → {EXCEL_OUT}")
print(f"📄 CSV saved   → {CSV_OUT}")
