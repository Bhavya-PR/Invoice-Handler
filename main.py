import os
import cv2
import json

from utils.ocr_utils import run_ocr  # Your OCR function
from utils.parser import parse_ocr_data  # Your parser function
from utils.validator import validate_invoice  # Your validator function
from utils.exporter import combine_parsed_jsons, json_to_excel, generate_verifiability_report
from utils.image_utils import crop_seal_signature  # Crop seal/sign function

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
        ocr_data = run_ocr(image)  # Your OCR function returning OCR results including bounding boxes and text
        parsed_json = parse_ocr_data(ocr_data)  # Parse OCR into structured JSON invoice data

        # Save per-page JSON
        json_path = os.path.join(output_folder, f"page_{page_num}_parsed.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=4)
        parsed_jsons.append(parsed_json)

        # Validate invoice data
        validation_result = validate_invoice(parsed_json)
        validation_results.append(validation_result)

        # Crop seal and signature
        crop_seal_signature(image, ocr_data, output_folder, page_num)

    # Combine all per-page JSONs into one file
    combined_json = combine_parsed_jsons(output_folder)

    # Generate verifiability report
    generate_verifiability_report(combined_json, validation_results, output_folder)

    # Export combined JSON to Excel
    json_to_excel(combined_json, os.path.join(output_folder, "extracted_data.xlsx"))

    print("All processing done successfully!")

if __name__ == "__main__":
    main()
