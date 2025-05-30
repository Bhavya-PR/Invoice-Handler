import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

# Manually specify Poppler path if needed
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"

# Define directories for output images
OUTPUT_IMAGE_FOLDER = "output/images"
ORIGINAL_FOLDER = os.path.join(OUTPUT_IMAGE_FOLDER, "original")
PROCESSED_FOLDER = os.path.join(OUTPUT_IMAGE_FOLDER, "processed")

def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def convert_pdf_to_images(input_dir):
    """
    Converts all PDFs in the input folder to images (one per page).
    Saves both original and preprocessed images separately.
    Returns a list of file paths.
    """
    ensure_folder_exists(ORIGINAL_FOLDER)
    ensure_folder_exists(PROCESSED_FOLDER)

    image_paths = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)

            try:
                pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
            except Exception as e:
                print(f"Error converting {filename}: {e}")
                continue

            for page_num, page in enumerate(pages):
                # Save original image
                original_image_path = os.path.join(ORIGINAL_FOLDER, f"{filename}_page_{page_num+1}_original.jpg")
                page.save(original_image_path, "JPEG")

                # Convert to OpenCV format
                image = np.array(page)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Apply preprocessing
                preprocessed = preprocess_image(image)

                # Save preprocessed image
                processed_image_path = os.path.join(PROCESSED_FOLDER, f"{filename}_page_{page_num+1}_processed.jpg")
                cv2.imwrite(processed_image_path, preprocessed)

                # Store paths
                image_paths.append((original_image_path, processed_image_path))

    return image_paths

def preprocess_image(image):
    """
    Apply grayscale, sharpening, denoise, adaptive thresholding, and morphological transformations.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply sharpening to enhance text edges
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)

    # Stronger denoising
    denoised = cv2.fastNlMeansDenoising(sharpened, h=40)  

    # Adaptive threshold for better text separation
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    # Morphological opening to remove small artifacts
    kernel = np.ones((2,2), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return morph

# Example execution (if needed)
if __name__ == "__main__":
    convert_pdf_to_images("input")