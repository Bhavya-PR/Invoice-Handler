import os
import pytesseract
import cv2
import numpy as np

# Path to Tesseract executable (ensure it's installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define directories for input and output
PROCESSED_IMAGE_FOLDER = "output/images/processed"
TEXT_OUTPUT_FOLDER = "output/extracted_text"

def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def extract_text_from_images():
    """
    Extracts text from all processed images in 'output/images/processed/'
    and saves the results as text files in 'output/extracted_text/'.
    """
    ensure_folder_exists(TEXT_OUTPUT_FOLDER)

    for filename in os.listdir(PROCESSED_IMAGE_FOLDER):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(PROCESSED_IMAGE_FOLDER, filename)

            # Read the preprocessed image
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)

            # Save extracted text to a file
            text_filename = os.path.join(TEXT_OUTPUT_FOLDER, f"{filename}.txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(extracted_text)

            print(f"✅ Extracted text saved: {text_filename}")

# Example execution
if __name__ == "__main__":
    extract_text_from_images()