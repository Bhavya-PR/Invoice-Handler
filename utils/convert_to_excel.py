import json
import pandas as pd
import os

# Define paths
JSON_FILE = "output/extracted_data.json"
EXCEL_OUTPUT_FILE = "output/extracted_data.xlsx"

def json_to_excel():
    """Reads parsed JSON and converts it into a structured Excel file."""
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten structure and ensure all required fields are included
    structured_data = []

    for invoice in data:
        for item in invoice.get("items", []):
            structured_data.append({
                "Invoice Number": invoice.get("invoice_number", ""),
                "Invoice Date": invoice.get("invoice_date", ""),
                "Supplier GST": invoice.get("supplier_gst_number", ""),
                "Bill-To GST": invoice.get("bill_to_gst_number", ""),
                "PO Number": invoice.get("po_number", ""),
                "Shipping Address": invoice.get("shipping_address", ""),
                "Seal & Sign": invoice.get("seal_and_sign_present", ""),
                "No. of Items": invoice.get("no_items", ""),
                "Serial Number": item.get("serial_number", ""),
                "Description": item.get("description", ""),
                "HSN/SAC": item.get("hsn_sac", ""),
                "Quantity": item.get("quantity", ""),
                "Unit Price": item.get("unit_price", ""),
                "Total Amount": item.get("total_amount", "")
            })

    # Convert structured data to DataFrame
    df = pd.DataFrame(structured_data)

    # Save to Excel
    df.to_excel(EXCEL_OUTPUT_FILE, index=False)

    print(f"✅ Structured invoice data saved as {EXCEL_OUTPUT_FILE}")

if __name__ == "__main__":
    json_to_excel()