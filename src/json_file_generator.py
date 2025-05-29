import re
import json
import os
from langchain_groq import extract_with_groqcloud_api  # GroqCloud AI integration

input_text_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\text"
output_json_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"

os.makedirs(output_json_folder, exist_ok=True)

def extract_field(text, patterns):
    """Extract fields using multiple regex patterns."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def parse_invoice(text_file):
    """Parses invoice details from extracted text."""
    with open(text_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Try regex-based extraction first
    parsed_data = {
        "invoice_number": extract_field(raw_text, [
            r"Invoice\s*No\.*\s*([\w-]+)",  
            r"Bill\s*No\.*\s*([\w-]+)",  
            r"Invoice ID\s*([\w-]+)",  
            r"Tax\s*Invoice\s*([\w-]+)"
        ]),
        "invoice_date": extract_field(raw_text, [
            r"Date\.*\s*([\d\-\/]+)",  
            r"Invoice Date\.*\s*([\d\-\/]+)"
        ]),
        "supplier_gst_number": extract_field(raw_text, [
            r"Supplier GST\.*\s*([\w\d]+)",  
            r"GSTIN\s*([\w\d]+)"
        ]),
        "bill_to_gst_number": extract_field(raw_text, [
            r"Bill To GST\.*\s*([\w\d]+)",  
            r"Client GST\.*\s*([\w\d]+)"
        ]),
        "po_number": extract_field(raw_text, [
            r"PO Number\.*\s*([\w\d]+)",  
            r"Purchase Order\.*\s*([\w\d]+)"
        ]),
        "shipping_address": extract_field(raw_text, [
            r"Shipping Address\.*\s*(.*)",  
            r"Delivery Address\.*\s*(.*)"
        ]),
        "seal_and_sign_present": "Seal/Signature Detected" in raw_text,
        "items": []
    }

    # If Invoice Number is missing, use AI-powered parsing
    if not parsed_data["invoice_number"]:
        print("\n⚠️ Invoice number missing! Using AI-powered parsing...\n")
        structured_data = extract_with_groqcloud_api(raw_text)
        parsed_data["invoice_number"] = structured_data.get("invoice_number", None)
        parsed_data.update(structured_data)  # Merge extracted fields

    return parsed_data

# Process all text files and save parsed data
for filename in os.listdir(input_text_folder):
    if filename.endswith(".txt"):
        text_file_path = os.path.join(input_text_folder, filename)
        parsed_invoice = parse_invoice(text_file_path)

        # Save JSON output
        json_output_path = os.path.join(output_json_folder, f"{filename}.json")
        with open(json_output_path, "w", encoding="utf-8") as json_file:
            json.dump(parsed_invoice, json_file, indent=4)

        print(f"Parsed invoice saved to: {json_output_path}")

print("✅ Hybrid invoice parsing completed successfully!")
