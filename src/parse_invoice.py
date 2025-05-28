import re
import json
import os

# Directory where extracted text files are stored
input_text_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\text"
output_json_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"

# Ensure output directory exists
os.makedirs(output_json_folder, exist_ok=True)

def extract_field(text, field_names):
    """Search multiple possible field names to extract data."""
    for field in field_names:
        for line in text.split("\n"):
            if field.lower() in line.lower():
                return line.split(":")[-1].strip()
    return None

def parse_invoice(text_file):
    """Parse invoice details from extracted text."""
    with open(text_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Structured invoice parsing
    parsed_data = {
        "invoice_number": extract_field(raw_text, ["Invoice No", "Bill No", "Invoice ID"]),
        "invoice_date": extract_field(raw_text, ["Date", "Invoice Date", "Billing Date"]),
        "supplier_gst_number": extract_field(raw_text, ["Supplier GST", "GSTIN"]),
        "bill_to_gst_number": extract_field(raw_text, ["Bill To GST", "Client GST"]),
        "po_number": extract_field(raw_text, ["PO Number", "Purchase Order"]),
        "shipping_address": extract_field(raw_text, ["Shipping Address", "Delivery Address"]),
        "seal_and_sign_present": "Seal/Signature Detected" in raw_text,
        "items": []  # Will store line items dynamically
    }

    # Extract line items dynamically (quantity, unit price, total)
    line_item_pattern = re.compile(r"(\d+)\s+([\w\s]+)\s+(\d+)\s+([\d\.]+)\s+([\d\.]+)")
    for match in line_item_pattern.findall(raw_text):
        item = {
            "serial_number": match[0],
            "description": match[1].strip(),
            "quantity": match[2],
            "unit_price": match[3],
            "total_amount": match[4]
        }
        parsed_data["items"].append(item)

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

print("Invoice parsing completed successfully!")
