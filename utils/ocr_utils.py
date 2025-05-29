import pytesseract
from pytesseract import Output
import cv2
from pdf2image import convert_from_path  # pip install pdf2image
import numpy as np

# Tesseract path (your existing line)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    """Extract raw text from a preprocessed image using Tesseract."""
    text = pytesseract.image_to_string(image)
    return text

def extract_text_with_layout(image):
    """Extract text with bounding boxes."""
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

def extract_text_from_pdf(pdf_path):
    """
    Convert each page of PDF to image and extract text from each page.
    Returns a list of text strings, one per page.
    """
    pages_text = []
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path)
    for page in pages:
        # Convert PIL image to OpenCV image
        open_cv_image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        text = extract_text(open_cv_image)
        pages_text.append(text)
    return pages_text
