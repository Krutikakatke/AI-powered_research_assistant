from pdfminer.high_level import extract_text
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract raw text from PDF using PDFMiner
    """
    text = extract_text(pdf_path)
    return text


def remove_references(text):
    """
    Remove references section to reduce noise
    """
    patterns = [
        r"\nreferences\b",
        r"\nbibliography\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = text[:match.start()]
            break

    return text


def extract_title_abstract_body(text):
    """
    Split extracted text into title, abstract, and body
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = lines[0] if lines else ""

    abstract = ""
    body = ""

    abstract_start = False
    body_start = False

    for line in lines[1:]:
        if re.fullmatch(r"abstract", line.lower()):
            abstract_start = True
            continue

        if abstract_start and not body_start:
            if re.search(r"\b(introduction|keywords)\b", line.lower()):
                body_start = True
                continue
            abstract += line + " "

        elif body_start:
            body += line + " "

    return {
        "title": title,
        "abstract": abstract.strip(),
        "body": body.strip()
    }


def process_pdf(pdf_path):
    """
    Complete pipeline for one PDF
    """
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = remove_references(raw_text)
    structured_text = extract_title_abstract_body(cleaned_text)

    return structured_text