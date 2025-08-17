import os
import docx2txt
import PyPDF2

def extract_text(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ' '.join(page.extract_text() for page in reader.pages if page.extract_text())
    elif ext == '.docx':
        text = docx2txt.process(file_path)
    else:
        text = ''
    return text
