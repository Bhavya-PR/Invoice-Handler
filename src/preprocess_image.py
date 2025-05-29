import cv2
import numpy as np
import os

input_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"
processed_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\processed"

# Ensure output directory exists
os.makedirs(processed_folder, exist_ok=True)

def preprocess_image(image_path, processed_path):
    """Enhances image contrast, removes noise, sharpens text, and applies adaptive thresholding."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  
    
    # Adaptive thresholding for better OCR clarity
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Sharpen the image to highlight text
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  # Sharpen filter
    image = cv2.filter2D(image, -1, kernel)

    cv2.imwrite(processed_path, image)
    print(f"Processed image saved: {processed_path}")

# Apply preprocessing to all images
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        processed_path = os.path.join(processed_folder, filename)
        preprocess_image(img_path, processed_path)

print("Image preprocessing completed!")
