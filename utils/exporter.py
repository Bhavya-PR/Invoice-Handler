import os
import json
import pandas as pd

def combine_parsed_jsons(output_folder="output"):
    combined = []
    for filename in sorted(os.listdir(output_folder)):
        if filename.endswith("_parsed.json"):
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined.append(data)
    combined_path = os.path.join(output_folder, "extracted_data.json")
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=4)
    print(f"Combined JSON saved to {combined_path}")
    return combined

def json_to_excel(json_data, excel_path="output/extracted_data.xlsx"):
    rows = []
    for invoice in json_data:
        items = invoice.get("items", [])
        for item in items:
            row = {
                "invoice_number": invoice.get("invoice_number", ""),
                "invoice_date": invoice.get("invoice_date", ""),
                "supplier_gst_number": invoice.get("supplier_gst_number", ""),
                "bill_to_gst_number": invoice.get("bill_to_gst_number", ""),
                "po_number": invoice.get("po_number", ""),
                "shipping_address": invoice.get("shipping_address", ""),
                "seal_and_sign_present": invoice.get("seal_and_sign_present", ""),
                "serial_number": item.get("serial_number", ""),
                "description": item.get("description", ""),
                "hsn_sac": item.get("hsn_sac", ""),
                "quantity": item.get("quantity", ""),
                "unit_price": item.get("unit_price", ""),
                "total_amount": item.get("total_amount", "")
            }
            rows.append(row)
    df = pd.DataFrame(rows)
    df.to_excel(excel_path, index=False)
    print(f"Excel file saved to {excel_path}")

def generate_verifiability_report(parsed_data_list, validation_results, output_folder="output"):
    report = []
    for idx, (data, validation) in enumerate(zip(parsed_data_list, validation_results)):
        field_confidences = {field: 0.9 for field in data.keys() if field != 'items'}
        report.append({
            "page": idx + 1,
            "field_confidences": field_confidences,
            "validation_errors": validation.get("errors", []),
            "is_valid": validation.get("is_valid", False)
        })
    report_path = os.path.join(output_folder, "verifiability_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
    print(f"Verifiability report saved to {report_path}")
    return report
