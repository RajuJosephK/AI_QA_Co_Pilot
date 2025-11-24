import os
from src.readers.pdf_reader import read_pdf
from src.readers.docx_reader import read_docx
from src.readers.txt_reader import read_txt
from src.readers.pptx_reader import read_pptx
from src.readers.html_reader import read_html
from src.readers.excel_reader import read_xlsx

EXTENSION_READERS = {
    ".pdf": read_pdf,
    ".docx": read_docx,
    ".txt": read_txt,
    ".pptx": read_pptx,
    ".xlsx": read_xlsx,
    ".xls": read_xlsx,
    ".html": read_html,
    ".htm": read_html,
}

def load_all_documents(directory="sample_docs"):
    documents = []
    for file in os.listdir(directory):
        ext = os.path.splitext(file)[1].lower()
        reader = EXTENSION_READERS.get(ext)
        if reader:
            documents.append(reader(os.path.join(directory, file)))
    return documents