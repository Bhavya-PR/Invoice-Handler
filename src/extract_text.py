import pytesseract
from PIL import Image
import os

# Set Tesseract path manually
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Directories for input images and output text
input_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"
output_text_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\text"

# Ensure output directory exists
os.makedirs(output_text_folder, exist_ok=True)

def extract_text(image_path):
    """Extracts text from an invoice image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

# Process all images in the output folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        extracted_text = extract_text(img_path)
        
        # Save extracted text to a file
        text_file_path = os.path.join(output_text_folder, f"{filename}.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"Extracted text saved to: {text_file_path}")

print("OCR process completed successfully!")
