from PIL import Image
import pytesseract

def extract_text_from_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)
