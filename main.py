from utils import preprocess
from utils import parser
import cv2
import json
import os

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

images = preprocess.convert_pdf_to_images("input")

for i, img in enumerate(images):
    # Save preprocessed image
    output_path = f"output/page_{i+1}.png"
    cv2.imwrite(output_path, img)
    
    # Call parser on each image
    parsed_result_str = parser.parse_invoice_fields(img)
    
    # Try to parse the string result as JSON and save prettily
    try:
        parsed_result_json = json.loads(parsed_result_str)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON on page {i+1}. Saving raw text.")
        parsed_result_json = parsed_result_str  # fallback to raw text
    
    with open(f"output/page_{i+1}_parsed.json", "w", encoding="utf-8") as f:
        if isinstance(parsed_result_json, dict):
            json.dump(parsed_result_json, f, indent=4, ensure_ascii=False)
        else:
            f.write(parsed_result_json)
