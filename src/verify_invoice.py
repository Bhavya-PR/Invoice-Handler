import json
import os
import random  # Simulating confidence scores

# Input/output directories
input_json_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"
verification_report_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output\verification"

# Ensure output directory exists
os.makedirs(verification_report_folder, exist_ok=True)

def generate_confidence_score():
    """Simulate confidence score (Range: 0–1)"""
    return round(random.uniform(0.7, 1.0), 2)  # Simulated confidence between 70% and 100%

def clean_number(value):
    """Removes unwanted characters and converts to a proper float."""
    try:
        return round(float(value.replace(",", "").strip()), 2)  # Removes commas and extra spaces
    except ValueError:
        return None  # Returns None for invalid values

def verify_invoice(invoice_data):
    """Verifies invoice calculations, flags errors, and assigns confidence scores."""
    verification_report = {
        "invoice_number": invoice_data["invoice_number"],
        "invoice_date": invoice_data["invoice_date"],
        "checks": {},
        "confidence_scores": {},
        "warnings": []
    }
    
    # ✅ Confidence Scores for Key Fields
    for key in ["invoice_number", "invoice_date", "supplier_gst_number", "bill_to_gst_number", "po_number"]:
        verification_report["confidence_scores"][key] = generate_confidence_score()
        verification_report["checks"][key] = invoice_data[key] is not None

    # ✅ Line Item Validation (unit_price × quantity = total_amount)
    for item in invoice_data["items"]:
        item["quantity"] = clean_number(item["quantity"])
        item["unit_price"] = clean_number(item["unit_price"])
        item["total_amount"] = clean_number(item["total_amount"])

        if item["quantity"] is None or item["unit_price"] is None or item["total_amount"] is None:
            verification_report["warnings"].append(f"⚠️ Invalid numeric data detected in item: {item['description']}")
            continue

        expected_total = round(float(item["quantity"]) * float(item["unit_price"]), 2)
        extracted_total = round(float(item["total_amount"]), 2)
        check_passed = expected_total == extracted_total

        verification_report["checks"][item["description"]] = check_passed
        verification_report["confidence_scores"][item["description"]] = generate_confidence_score()

        if not check_passed:
            verification_report["warnings"].append(f"Calculation mismatch in item: {item['description']}")

    # ✅ Total Calculation Checks
    subtotal = sum(float(item["total_amount"]) for item in invoice_data["items"] if item["total_amount"] is not None)
    final_total_calculated = round(subtotal - float(invoice_data.get("discount", 0)) + float(invoice_data.get("gst", 0)), 2)

    verification_report["checks"]["subtotal_valid"] = invoice_data.get("subtotal") == subtotal
    verification_report["checks"]["final_total_valid"] = invoice_data.get("final_total") == final_total_calculated

    if not verification_report["checks"]["subtotal_valid"]:
        verification_report["warnings"].append("Subtotal calculation mismatch.")
    if not verification_report["checks"]["final_total_valid"]:
        verification_report["warnings"].append("Final total calculation mismatch.")

    return verification_report

# Process all JSON invoice files
for filename in os.listdir(input_json_folder):
    if filename.endswith(".json"):
        json_file_path = os.path.join(input_json_folder, filename)
        
        # Load invoice data
        with open(json_file_path, "r", encoding="utf-8") as f:
            invoice_data = json.load(f)
        
        verification_results = verify_invoice(invoice_data)

        # Save verification report
        report_path = os.path.join(verification_report_folder, f"{filename}_verification.json")
        with open(report_path, "w", encoding="utf-8") as report_file:
            json.dump(verification_results, report_file, indent=4)

        print(f"Verification report saved: {report_path}")

print("Invoice verification & confidence scoring completed successfully!")
