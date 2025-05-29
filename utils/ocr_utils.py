import pytesseract
from pytesseract import Output
import cv2

def extract_text(image):
    """
    Extract raw text from a preprocessed image using Tesseract.
    """
    text = pytesseract.image_to_string(image)
    return text

def extract_text_with_layout(image):
    """
    Extract text along with positional information (bounding boxes).
    Returns a list of dicts with keys: text, left, top, width, height, conf.
    """
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    results = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 50 and data['text'][i].strip() != '':
            results.append({
                "text": data['text'][i],
                "left": data['left'][i],
                "top": data['top'][i],
                "width": data['width'][i],
                "height": data['height'][i],
                "conf": data['conf'][i]
            })
    return results
