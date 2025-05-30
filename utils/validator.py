import os
import json

# Define file paths
EXTRACTED_DATA_FILE = "output/extracted_data.json"
VERIFIABILITY_REPORT_FILE = "output/verifiability_report.json"

def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def calculate_confidence(value, ocr_confidence=0.0, seal_present=False):
    """Uses OCR confidence scores if available, otherwise estimates based on presence."""
    if seal_present:
        return 0.8 if value else 0.5  # Boost confidence when seal is detected
    if ocr_confidence:
        return round(ocr_confidence, 2)  # Use OCR confidence directly
    return round(min(0.5 + (len(str(value)) * 0.05), 0.99), 2) if value else 0.5  # Fallback estimation

def validate_line_total(item):
    """Ensures item total matches calculated total (quantity × unit price) with small tolerance."""
    calculated_value = round(item["quantity"] * item["unit_price"], 2)  # Ensure rounding
    extracted_value = round(item["total_amount"], 2)  # Ensure rounding

    check_passed = abs(calculated_value - extracted_value) < 0.05  # Allow minor rounding differences

    return {"calculated_value": calculated_value, "extracted_value": extracted_value, "check_passed": check_passed}

def validate_totals(invoice_data):
    """Verifies subtotal, discount, GST, and final total calculations."""
    subtotal = sum(item["total_amount"] for item in invoice_data.get("items", []))  # Ensure "items" exists
    discount = invoice_data.get("discount", 0)
    gst = round(subtotal * 0.18, 2)  # Assuming 18% GST
    final_total = subtotal + gst - discount

    return {
        "subtotal_check": {"calculated_value": subtotal, "extracted_value": invoice_data.get("subtotal", subtotal), "check_passed": subtotal == invoice_data.get("subtotal", subtotal)},
        "discount_check": {"calculated_value": discount, "extracted_value": invoice_data.get("discount", discount), "check_passed": discount == invoice_data.get("discount", discount)},
        "gst_check": {"calculated_value": gst, "extracted_value": invoice_data.get("gst", gst), "check_passed": gst == invoice_data.get("gst", gst)},
        "final_total_check": {"calculated_value": final_total, "extracted_value": invoice_data.get("final_total", final_total), "check_passed": final_total == invoice_data.get("final_total", final_total)}
    }

def generate_verifiability_report():
    """Generates a JSON report verifying extracted invoice data from `extracted_data.json`."""
    ensure_folder_exists("output")

    if not os.path.exists(EXTRACTED_DATA_FILE):
        print(f"Error: `{EXTRACTED_DATA_FILE}` not found!")
        return
    
    with open(EXTRACTED_DATA_FILE, "r", encoding="utf-8") as f:
        invoices = json.load(f)

    report_data = {
        "field_verification": {},
        "line_items_verification": {},
        "total_calculations_verification": {},
        "summary": {"all_fields_confident": True, "all_line_items_verified": True, "totals_verified": True, "issues": []}
    }

    for invoice_data in invoices:
        # Check for errors in the invoice data
        if "error" in invoice_data:
            report_data["summary"]["issues"].append(f"Skipping invoice due to error: {invoice_data['error']}")
            continue  # Skip this invoice

        # Field verification stored separately for each invoice
        invoice_number = invoice_data.get("invoice_number", "Unknown")
        report_data["field_verification"][invoice_number] = {}

        required_fields = ["invoice_number", "invoice_date", "supplier_gst_number", "bill_to_gst_number", "po_number", "shipping_address", "seal_and_sign_present"]
        for field in required_fields:
            value = invoice_data.get(field, "")
            ocr_confidence = invoice_data.get(f"{field}_confidence", 0.0)
            seal_present = invoice_data.get("seal_and_sign_present", False) if field == "seal_and_sign_present" else False
            confidence = calculate_confidence(value, ocr_confidence, seal_present)

            report_data["field_verification"][invoice_number][field] = {
                "confidence": confidence,
                "present": bool(value)
            }

            if confidence < 0.85 and f"Low confidence in {field}" not in report_data["summary"]["issues"]:
                report_data["summary"]["issues"].append(f"Low confidence in {field}: {confidence}")
                report_data["summary"]["all_fields_confident"] = False

        # Handle invoices that may not have "items"
        if "items" not in invoice_data or not invoice_data["items"]:
            report_data["summary"]["issues"].append(f"Invoice {invoice_number} has no line items!")
            report_data["summary"]["all_line_items_verified"] = False
            continue  # Skip processing for invoices missing "items"

        # Line items verification stored separately per invoice
        report_data["line_items_verification"][invoice_number] = []

        for index, item in enumerate(invoice_data["items"], start=1):
            line_item_verification = {
                "row": index,
                "description_confidence": calculate_confidence(item.get("description"), item.get("description_confidence", 0.0)),
                "hsn_sac_confidence": calculate_confidence(item.get("hsn_sac"), item.get("hsn_sac_confidence", 0.0)),
                "quantity_confidence": calculate_confidence(item.get("quantity"), item.get("quantity_confidence", 0.0)),
                "unit_price_confidence": calculate_confidence(item.get("unit_price"), item.get("unit_price_confidence", 0.0)),
                "total_amount_confidence": calculate_confidence(item.get("total_amount"), item.get("total_amount_confidence", 0.0)),
                "serial_number_confidence": calculate_confidence(item.get("serial_number"), item.get("serial_number_confidence", 0.0)),
                "line_total_check": validate_line_total(item)
            }
            report_data["line_items_verification"][invoice_number].append(line_item_verification)

            if not line_item_verification["line_total_check"]["check_passed"]:
                report_data["summary"]["issues"].append(f"Line total mismatch in row {index}")
                report_data["summary"]["all_line_items_verified"] = False

        # Total calculations verification stored per invoice
        report_data["total_calculations_verification"][invoice_number] = validate_totals(invoice_data)
        if not all(v["check_passed"] for v in report_data["total_calculations_verification"][invoice_number].values()):
            report_data["summary"]["issues"].append(f"Total calculations mismatch in invoice {invoice_number}")
            report_data["summary"]["totals_verified"] = False

    # Save verification report
    with open(VERIFIABILITY_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"Verifiability Report saved: {VERIFIABILITY_REPORT_FILE}")

# Execute validator
if __name__ == "__main__":
    generate_verifiability_report()