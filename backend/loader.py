import os
import re
import docx
import pdfplumber
import fitz
#import easyocr
import numpy as np
from PIL import Image
from pypdf import PdfReader


#reader = easyocr.Reader(['ar', 'en'], gpu=False)


def looks_like_broken_arabic(text: str) -> bool:

    if not text or not text.strip():
        return True

    strange_patterns = ['ٮ', '⸻', 'ڡ', 'ةدم', 'تاعاس لمعلا']
    score = sum(1 for p in strange_patterns if p in text)

    if score >= 2:
        return True

    if len(text.strip()) < 30:
        return True

    return False


def extract_text_with_pdfplumber(file_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass

    return text.strip()


def extract_text_with_pypdf(file_path: str) -> str:
    text = ""
    try:
        reader_pdf = PdfReader(file_path)
        for page in reader_pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        pass

    return text.strip()


def extract_page_image_for_ocr(pdf_path: str, page_index: int):
    doc = fitz.open(pdf_path)
    page = doc[page_index]
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def extract_text_with_ocr(pdf_path: str) -> str:
    # OCR disabled in deployment (Render Free plan memory limit)
    return ""

def clean_extracted_text(text: str) -> str:
    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    text = "\n".join(lines)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def read_pdf(file_path: str) -> str:
    text = extract_text_with_pdfplumber(file_path)
    if not text.strip():
        text = extract_text_with_pypdf(file_path)

    text = clean_extracted_text(text)

    if looks_like_broken_arabic(text):
        print("Broken Arabic PDF detected, but OCR is disabled in deployment.")

        return text


def read_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    return clean_extracted_text(text)


def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return clean_extracted_text(f.read())


def load_document(file_path: str) -> str:
    lower_path = file_path.lower()

    if lower_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif lower_path.endswith(".docx"):
        return read_docx(file_path)
    elif lower_path.endswith(".txt"):
        return read_txt(file_path)
    else:
        raise ValueError("Unsupported file format")