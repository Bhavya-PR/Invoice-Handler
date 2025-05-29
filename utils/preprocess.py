import os
import cv2
from pdf2image import convert_from_path
import numpy as np
from PIL import Image

def convert_pdf_to_images(input_dir):
    """
    Converts all PDFs in the input folder to images (one per page).
    Returns a list of preprocessed OpenCV image arrays.
    """
    images = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            pages = convert_from_path(pdf_path, dpi=300)
            for page_num, page in enumerate(pages):
                # Save as PIL image and convert to OpenCV format
                image = np.array(page)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                processed = preprocess_image(image)
                images.append(processed)
    return images

def preprocess_image(image):
    """
    Apply grayscale + denoise + adaptive thresholding
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresh
