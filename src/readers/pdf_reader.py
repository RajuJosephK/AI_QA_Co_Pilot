
def read_pdf(path):
   
   import pdfplumber
  

   with pdfplumber.open(path) as pdf:
       text = ""
       for page in pdf.pages:
           text += page.extract_text() or ""
   return text 