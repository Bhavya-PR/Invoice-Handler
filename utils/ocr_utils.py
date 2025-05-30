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

def preprocess_image(image_path):
    """
    Enhances image before OCR using:
    - Grayscale conversion
    - Adaptive thresholding
    - Noise reduction
    - Edge sharpening
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian Blur to reduce noise
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Adaptive thresholding for better text isolation
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)

    # Edge sharpening using kernel filter
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    image = cv2.filter2D(image, -1, kernel)

    return image

def extract_text_from_images():
    """
    Extracts text from all processed images in 'output/images/processed/'
    using Tesseract with enhanced preprocessing.
    """
    ensure_folder_exists(TEXT_OUTPUT_FOLDER)

    for filename in os.listdir(PROCESSED_IMAGE_FOLDER):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(PROCESSED_IMAGE_FOLDER, filename)

            # Preprocess the image for better OCR accuracy
            processed_image = preprocess_image(image_path)

            # Extract text using Tesseract with `"--psm 6"` for structured text blocks
            extracted_text = pytesseract.image_to_string(processed_image, config="--psm 6")

            # Save extracted text to a file
            text_filename = os.path.join(TEXT_OUTPUT_FOLDER, f"{filename}.txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(extracted_text.strip())

            print(f"✅ Extracted text saved: {text_filename}")

# Example execution
if __name__ == "__main__":
    extract_text_from_images()