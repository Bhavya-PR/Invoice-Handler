import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

input_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\processed"
output_text_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\text"

os.makedirs(output_text_folder, exist_ok=True)

def extract_text(image_path):
    """Extracts text from an invoice image using optimized OCR settings."""
    try:
        image = Image.open(image_path)
        
        custom_config = r'--psm 4 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/-'
        text = pytesseract.image_to_string(image, config=custom_config)

        return text.strip()
    except Exception as e:
        print(f"⚠️ Error processing {image_path}: {e}")
        return ""

# Process all images in the output folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        extracted_text = extract_text(img_path)
        
        text_file_path = os.path.join(output_text_folder, f"{filename}.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"✅ Extracted text saved to: {text_file_path}")

print("🎯 OCR process completed successfully!")
