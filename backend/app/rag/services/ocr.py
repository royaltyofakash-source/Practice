from io import BytesIO
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes))
    extracted = pytesseract.image_to_string(image)

    print(f"DEBUG: OCR extracted {len(extracted)} characters from image")
    print(f"DEBUG: OCR preview: {extracted[:200]}...")

    return extracted

def extract_text_from_scanned_pdf(pdf_bytes: bytes) -> str:
    pages = convert_from_bytes(pdf_bytes)

    page_texts = []
    for idx, page_image in enumerate(pages):
        page_text = pytesseract.image_to_string(page_image)
        page_texts.append(page_text)
        print(f"DEBUG: OCR page {idx + 1}/{len(pages)}: {len(page_text)} characters")

    full_text = "\n".join(page_texts)

    print(f"DEBUG: OCR extracted {len(full_text)} characters from {len(pages)} pages")
    print(f"DEBUG: OCR preview: {full_text[:200]}...")

    return full_text
