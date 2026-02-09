# importing required modules
from pypdf import PdfReader
import os

def extract_pdf_to_text(pdf_path: str) -> str:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(repo_root, "telegram_bot", "temp", "telegram_docs")
    if os.path.isabs(pdf_path) and os.path.exists(pdf_path):
        PDF_IN = pdf_path
    else:
        PDF_IN = os.path.join(docs_dir, pdf_path)

    # creating a pdf reader object
    reader = PdfReader(PDF_IN)

    # printing number of pages in pdf file
    print(len(reader.pages))

    # getting a specific page from the pdf file
    page = reader.pages

    # extracting text from page
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    # print(text)
    # with open("../output/pdf_extracted_text.txt", "w", encoding="utf-8") as f:
    #     f.write(text)
    return text