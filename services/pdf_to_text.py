# importing required modules
from pypdf import PdfReader

def extract_pdf_to_text(pdf_path: str) -> str:
    # creating a pdf reader object
    reader = PdfReader(pdf_path)

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