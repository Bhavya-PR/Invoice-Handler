import os
import cv2
import json

from utils.parser import parse_invoice_fields  # Your parser function that takes an image
from utils.validator import validate_invoice_data
from utils.exporter import combine_parsed_jsons, json_to_excel, generate_verifiability_report
from utils.image_utils import crop_seal_signature
from utils.ocr_utils import extract_text_with_layout  # For cropping seal/sign

def main():
    input_folder = "input"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    images = sorted([f for f in os.listdir(input_folder) if f.endswith(".png") or f.endswith(".jpg")])
    parsed_jsons = []
    validation_results = []

    for idx, image_file in enumerate(images):
        page_num = idx + 1
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        print(f"Processing page {page_num}: {image_file}")

        # Run OCR separately to get bounding boxes for seal/sign cropping
        ocr_data = extract_text_with_layout(image)

        # Parse invoice fields (this runs OCR internally on the image)
        parsed_json_str = parse_invoice_fields(image)
        try:
            parsed_json = json.loads(parsed_json_str)
        except json.JSONDecodeError:
            parsed_json = {"error": "Failed to decode JSON from parser output."}

        # Save per-page JSON
        json_path = os.path.join(output_folder, f"page_{page_num}_parsed.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=4)
        parsed_jsons.append(parsed_json)

        # Validate invoice data
        validation_result = validate_invoice_data(parsed_json)
        validation_results.append(validation_result)

        # Crop seal and signature using OCR layout data
        crop_seal_signature(image, ocr_data, output_folder, page_num)

    # Combine all per-page JSONs into one list
    combined_json = combine_parsed_jsons(output_folder)

    # Safety check: lengths must match to generate report correctly
    if len(combined_json) != len(validation_results):
        print("❌ Warning: Number of parsed JSON entries and validation results do not match!")
        print(f"Parsed JSON count: {len(combined_json)}")
        print(f"Validation results count: {len(validation_results)}")
        print("Verifiability report generation skipped to avoid empty or mismatched report.")
    else:
        # Generate verifiability report with combined JSON and validation results
        generate_verifiability_report(combined_json, validation_results, output_folder)

    # Export combined JSON to Excel
    json_to_excel(combined_json, os.path.join(output_folder, "extracted_data.xlsx"))

    print("All processing done successfully!")

if __name__ == "__main__":
    main()
