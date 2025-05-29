from utils import preprocess
from utils import parser
from utils import validator
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
    
    # Validate only if parsed JSON is a dict (structured data)
    if isinstance(parsed_result_json, dict):
        validation_result = validator.validate_invoice_data(parsed_result_json)
        if not validation_result["is_valid"]:
            print(f"Validation errors on page {i+1}:")
            for err in validation_result["errors"]:
                print(f" - {err}")
        else:
            print(f"Page {i+1} validation passed.")
    else:
        print(f"Page {i+1} parsing output is raw text, skipping validation.")
    
    # Save parsed result to JSON or raw text file
    with open(f"output/page_{i+1}_parsed.json", "w", encoding="utf-8") as f:
        if isinstance(parsed_result_json, dict):
            json.dump(parsed_result_json, f, indent=4, ensure_ascii=False)
        else:
            f.write(parsed_result_json)
