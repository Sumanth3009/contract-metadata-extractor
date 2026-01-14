from .ocr import extract_text_from_image
from .docx_reader import extract_text_from_docx
from .extractor import extract_fields

def run(file_path):
    if file_path.endswith(".png"):
        text = extract_text_from_image(file_path)
    else:
        text = extract_text_from_docx(file_path)

    return extract_fields(text)
