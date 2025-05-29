import re
import json
import os
from langchain_groq import ChatGroq  # Correct GroqCloud AI import

API_KEY = "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"  # Replace with your actual API key
llm = ChatGroq(api_key=API_KEY, model="llama3-70b-8192")

input_text_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\text"
output_json_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"

os.makedirs(output_json_folder, exist_ok=True)

def extract_field(text, patterns):
    """Extract fields using regex patterns."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extract_with_groqcloud_api(ocr_text):
    """Uses GroqCloud AI to extract structured invoice data."""
    prompt = f"""
You are an intelligent invoice parser.

Extract ONLY the fields present in the scanned invoice text.
Ignore missing fields and return structured JSON.

Fields to extract:
- invoice_number
- invoice_date
- supplier_gst_number
- bill_to_gst_number
- po_number
- shipping_address
- seal_and_sign_present (true/false)
- line_items: list containing:
    - serial_number
    - description
    - quantity
    - unit_price
    - total_amount

Text:
{ocr_text}

Format response as valid JSON.
"""

    try:
        response = llm.invoke(input=prompt)
        response_text = response.content.strip()

        # Ensure response is in JSON format before parsing
        json_start = response_text.find("{")  # Locate start of JSON
        if json_start == -1:
            raise ValueError("AI response does not contain valid JSON.")

        structured_data = json.loads(response_text[json_start:])  # Convert to dict
        return structured_data

    except Exception as e:
        print(f"⚠️ AI Parsing Failed: {e}")
        return {}  # Return empty dict if AI parsing fails

def parse_invoice(text_file):
    """Parses invoice details from extracted text."""
    with open(text_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    parsed_data = {
        "invoice_number": extract_field(raw_text, [r"Invoice\s*No\.*\s*([\w-]+)", r"Bill\s*No\.*\s*([\w-]+)"]),
        "invoice_date": extract_field(raw_text, [r"Date\.*\s*([\d\-\/]+)", r"Invoice Date\.*\s*([\d\-\/]+)"]),
        "supplier_gst_number": extract_field(raw_text, [r"Supplier GST\.*\s*([\w\d]+)", r"GSTIN\s*([\w\d]+)"]),
    }

    # If Invoice Number is missing, use AI-powered parsing
    if not parsed_data["invoice_number"]:
        print("\n⚠️ Invoice number missing! Using AI-powered parsing...\n")
        structured_data = extract_with_groqcloud_api(raw_text)

        # Ensure AI response is valid before merging
        if isinstance(structured_data, dict) and structured_data:
            parsed_data.update(structured_data)  # Merge AI extracted fields
        else:
            print("⚠️ AI extraction returned an invalid response.")

    return parsed_data

# Process all text files
for filename in os.listdir(input_text_folder):
    if filename.endswith(".txt"):
        text_file_path = os.path.join(input_text_folder, filename)
        parsed_invoice = parse_invoice(text_file_path)

        json_output_path = os.path.join(output_json_folder, f"{filename}.json")
        with open(json_output_path, "w", encoding="utf-8") as json_file:
            json.dump(parsed_invoice, json_file, indent=4)

        print(f"✅ Parsed invoice saved to: {json_output_path}")

print("🎯 Hybrid invoice parsing completed successfully!")
