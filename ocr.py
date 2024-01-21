from PIL import Image
import pytesseract

def ocr_detect():
    return pytesseract.image_to_string( Image.open('ocr.png'), config = "--psm 9") 