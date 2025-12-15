from pdf2image import convert_from_path

pages = convert_from_path(
    "input.pdf",
    dpi=200,
    poppler_path=r"C:\poppler-25.12.0\Library\bin"
)

print(f"Converted {len(pages)} pages")
