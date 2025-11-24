from .pdf_reader import read_pdf
from .docx_reader import read_docx
from .txt_reader import read_txt
from .html_reader import read_html
from .pptx_reader import read_pptx
from .excel_reader import read_xlsx

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

def read_file(path: str) -> str:
    ext = path.lower().split(".")[-1]
    ext = "." + ext

    if ext not in EXTENSION_READERS:
        raise ValueError(f"Unsupported file extension: {ext}")

    reader = EXTENSION_READERS[ext]
    return reader(path)
