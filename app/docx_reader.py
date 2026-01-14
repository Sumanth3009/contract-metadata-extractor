import docx2txt

def extract_text_from_docx(path):
    return docx2txt.process(path)
