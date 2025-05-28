import cv2
import os

input_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"
processed_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\processed"

# Ensure output directory exists
os.makedirs(processed_folder, exist_ok=True)

def preprocess_image(image_path, processed_path):
    """Enhances image contrast, removes noise, and converts to grayscale for better OCR."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    image = cv2.GaussianBlur(image, (5,5), 0)  # Apply blur to remove noise
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarization

    cv2.imwrite(processed_path, image)
    print(f"Processed image saved: {processed_path}")

# Apply preprocessing to all images
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        processed_path = os.path.join(processed_folder, filename)
        preprocess_image(img_path, processed_path)

print("Image preprocessing completed!")
