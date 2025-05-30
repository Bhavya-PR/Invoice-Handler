from ultralytics import YOLO
import cv2
import os

ORIGINAL_IMAGE_FOLDER = "output/images/original"
SEAL_SIGNATURE_FOLDER = "output/seal_signatures"

def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Load YOLO model
model = YOLO("yolov8n.pt")  # Replace with trained model for seals/signatures

def detect_seal_signature(image_path):
    """Detects seal/signature in an invoice using YOLO."""
    image = cv2.imread(image_path)
    results = model(image)  # Run YOLO detection

    ensure_folder_exists(SEAL_SIGNATURE_FOLDER)
    
    for i, box in enumerate(results[0].boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        cropped_seal = image[y1:y2, x1:x2]
        filename = os.path.join(SEAL_SIGNATURE_FOLDER, f"seal_signature_{i+1}.png")
        cv2.imwrite(filename, cropped_seal)
        print(f"✅ Saved cropped seal/signature: {filename}")

def process_images_for_seals():
    """Scans all original images and applies YOLO seal detection."""
    ensure_folder_exists(SEAL_SIGNATURE_FOLDER)

    for filename in os.listdir(ORIGINAL_IMAGE_FOLDER):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(ORIGINAL_IMAGE_FOLDER, filename)
            detect_seal_signature(image_path)

if __name__ == "__main__":
    process_images_for_seals()