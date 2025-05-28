import json
import pandas as pd
import os

# Directories for input JSON and output Excel files
input_json_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"
output_excel_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"

# Ensure output directory exists
os.makedirs(output_excel_folder, exist_ok=True)

def json_to_excel(json_file):
    """Converts parsed JSON invoice data into an Excel file."""
    with open(json_file, "r", encoding="utf-8") as f:
        invoice_data = json.load(f)

    # Convert invoice details to DataFrame
    invoice_details = {
        "Invoice Number": [invoice_data["invoice_number"]],
        "Invoice Date": [invoice_data["invoice_date"]],
        "Supplier GST": [invoice_data["supplier_gst_number"]],
        "Bill To GST": [invoice_data["bill_to_gst_number"]],
        "PO Number": [invoice_data["po_number"]],
        "Shipping Address": [invoice_data["shipping_address"]],
        "Seal & Signature Present": [invoice_data["seal_and_sign_present"]]
    }
    df_invoice = pd.DataFrame(invoice_details)

    # Convert line items to DataFrame
    df_items = pd.DataFrame(invoice_data["items"])

    # Save to Excel (multiple sheets)
    excel_file_path = os.path.join(output_excel_folder, f"{os.path.basename(json_file).replace('.json', '.xlsx')}")
    with pd.ExcelWriter(excel_file_path) as writer:
        df_invoice.to_excel(writer, sheet_name="Invoice Details", index=False)
        df_items.to_excel(writer, sheet_name="Line Items", index=False)

    print(f"Excel report saved: {excel_file_path}")

# Process all JSON invoice files
for filename in os.listdir(input_json_folder):
    if filename.endswith(".json"):
        json_file_path = os.path.join(input_json_folder, filename)
        json_to_excel(json_file_path)

print("Excel generation completed successfully!")
