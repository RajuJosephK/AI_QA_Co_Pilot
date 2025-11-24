from bs4 import BeautifulSoup

def read_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.get_text(separator="\n").strip()
