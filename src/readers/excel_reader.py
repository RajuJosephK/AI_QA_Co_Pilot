import pandas as pd

def read_xlsx(path: str) -> str:
    df = pd.read_excel(path, dtype=str)
    return "\n".join(df.fillna("").astype(str).apply(lambda row: " ".join(row), axis=1)).strip()
