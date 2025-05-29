import os
import json
import fitz  # PyMuPDF
import cv2
import numpy as np
from utils.parser import parse_invoice_fields
from utils.validator import validate_invoice_data
from utils.exporter import json_to_excel

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]

parsed_jsons = []
validation_results = []

def pdf_to_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        images.append(img)
    return images

for pdf_file in pdf_files:
    file_path = os.path.join(INPUT_FOLDER, pdf_file)
    print(f"\n📄 Processing {pdf_file}...")

    try:
        # Step 1: Convert PDF to images
        images = pdf_to_images(file_path)

        for page_num, image in enumerate(images, start=1):
            print(f"\n🔍 Page {page_num}: Running LLM parser...")

            # Step 2: Parse with LLM
            parsed_json_str = parse_invoice_fields(image, use_layout=True)

            try:
                parsed_json = json.loads(parsed_json_str)
            except json.JSONDecodeError:
                parsed_json = {"error": "Failed to decode JSON from parser output."}

            # Save parsed JSON
            json_path = os.path.join(OUTPUT_FOLDER, f"{pdf_file}_page_{page_num}_parsed.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(parsed_json, f, indent=4)
            parsed_jsons.append(parsed_json)

            # Step 3: Validation
            if "error" in parsed_json:
                validation_result = {
                    "is_valid": False,
                    "errors": [parsed_json["error"]]
                }
            else:
                validation_result = validate_invoice_data(parsed_json)

            print(f"✅ Validation result for page {page_num}: {validation_result}")
            validation_results.append(validation_result)

    except Exception as e:
        print(f"❌ Error processing {pdf_file}: {str(e)}")

# Step 4: Save combined JSON
combined_path = os.path.join(OUTPUT_FOLDER, "extracted_data.json")
with open(combined_path, "w", encoding="utf-8") as f:
    json.dump(parsed_jsons, f, indent=4)
print("\n✅ Combined JSON saved to output\\extracted_data.json")

# Step 5: Summary and Export
print("\n📊 Summary:")
print(f"🔢 Parsed JSON count: {len(parsed_jsons)}")
print(f"🛡️ Validation results count: {len(validation_results)}")

if len(parsed_jsons) == len(validation_results):
    json_to_excel(parsed_jsons, validation_results, os.path.join(OUTPUT_FOLDER, "extracted_data.xlsx"))
    print("📈 Excel file saved to output\\extracted_data.xlsx")
    print("✅ Verifiability report generated!")
else:
    print("❌ Mismatch between parsed JSON and validation results.")
    print("🛑 Verifiability report skipped.")

print("\n🎉 All processing done successfully!")
