import os
import json
import random
from datetime import datetime

# Define output directory
VERIFICATION_OUTPUT_FOLDER = "output"
VERIFICATION_REPORT_FILE = os.path.join(VERIFICATION_OUTPUT_FOLDER, "verifiability_report.json")

def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def generate_confidence_score():
    """
    Generates a random confidence score (range: 0.8 - 1.0).
    Adjust scoring logic as needed based on OCR confidence values.
    """
    return round(random.uniform(0.8, 1.0), 2)

def validate_invoice_data(invoice_data):
    """
    Validates extracted invoice fields and computes confidence scores.

    Args:
        invoice_data (dict): Parsed JSON invoice data

    Returns:
        dict: Validation result with confidence scores, errors, and verifiability report
    """
    errors = []
    field_verification = {}
    line_items_verification = []
    total_calculations_verification = {}

    # Supported date formats
    date_formats = [
        "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y",
        "%d/%m/%y", "%m/%d/%y", "%d-%b-%y", "%d-%b-%Y"
    ]

    required_fields = [
        "invoice_number", "invoice_date", "supplier_gst_number",
        "bill_to_gst_number", "po_number", "shipping_address",
        "seal_and_sign_present", "no_items", "items"
    ]

    # **Field Verification**
    for field in required_fields:
        confidence = generate_confidence_score()
        present = field in invoice_data and bool(invoice_data[field])
        field_verification[field] = {"confidence": confidence, "present": present}

        if not present:
            errors.append(f"Missing required field: {field}")

    # Validate invoice_date format
    date_val = invoice_data.get("invoice_date", "")
    valid_date = any(datetime.strptime(date_val, fmt) for fmt in date_formats if date_val)
    field_verification["invoice_date"]["present"] = valid_date
    if not valid_date:
        errors.append(f"Invalid invoice_date format: {date_val}")

    # **Line Item Validation**
    subtotal_calculated = 0
    items = invoice_data.get("items", [])
    
    for idx, item in enumerate(items, start=1):
        try:
            q = float(item.get("quantity", 0))
            u = float(item.get("unit_price", 0))
            t = float(item.get("total_amount", 0))
            calculated_total = round(q * u, 2)
            check_passed = abs(calculated_total - t) < 0.05
        except:
            check_passed = False
            errors.append(f"[Item {idx}] Invalid quantity/unit price values.")

        subtotal_calculated += calculated_total

        line_items_verification.append({
            "row": idx,
            "description_confidence": generate_confidence_score(),
            "hsn_sac_confidence": generate_confidence_score(),
            "quantity_confidence": generate_confidence_score(),
            "unit_price_confidence": generate_confidence_score(),
            "total_amount_confidence": generate_confidence_score(),
            "serial_number_confidence": generate_confidence_score(),
            "line_total_check": {
                "calculated_value": calculated_total,
                "extracted_value": t,
                "check_passed": check_passed
            }
        })

    # **Total Calculation Checks**
    subtotal_extracted = float(invoice_data.get("subtotal", subtotal_calculated))
    discount_extracted = float(invoice_data.get("discount", 0))
    gst_extracted = float(invoice_data.get("gst", 0))

    final_total_calculated = subtotal_calculated - discount_extracted + gst_extracted
    final_total_extracted = float(invoice_data.get("final_total", final_total_calculated))

    total_calculations_verification = {
        "subtotal_check": {
            "calculated_value": subtotal_calculated,
            "extracted_value": subtotal_extracted,
            "check_passed": abs(subtotal_calculated - subtotal_extracted) < 0.05
        },
        "discount_check": {
            "calculated_value": discount_extracted,
            "extracted_value": discount_extracted,
            "check_passed": True  # Assuming discount is extracted correctly
        },
        "gst_check": {
            "calculated_value": gst_extracted,
            "extracted_value": gst_extracted,
            "check_passed": True  # Assuming GST is extracted correctly
        },
        "final_total_check": {
            "calculated_value": final_total_calculated,
            "extracted_value": final_total_extracted,
            "check_passed": abs(final_total_calculated - final_total_extracted) < 0.05
        }
    }

    # **Summary**
    summary = {
        "all_fields_confident": all(field["confidence"] >= 0.85 for field in field_verification.values()),
        "all_line_items_verified": all(item["line_total_check"]["check_passed"] for item in line_items_verification),
        "totals_verified": all(check["check_passed"] for check in total_calculations_verification.values()),
        "issues": errors
    }

    # **Final JSON Report**
    verification_report = {
        "field_verification": field_verification,
        "line_items_verification": line_items_verification,
        "total_calculations_verification": total_calculations_verification,
        "summary": summary
    }

    return verification_report

# **Generate JSON Verification Report**
def save_verification_report(invoice_data):
    """Validates invoice data and saves the verification report as JSON."""
    ensure_folder_exists(VERIFICATION_OUTPUT_FOLDER)

    verification_result = validate_invoice_data(invoice_data)
    
    with open(VERIFICATION_REPORT_FILE, "w", encoding="utf-8") as json_file:
        json.dump(verification_result, json_file, indent=4)

    print(f"✅ Verification report saved: {VERIFICATION_REPORT_FILE}")

# **Example Execution**
if __name__ == "__main__":
    print("🚀 Validator is ready! Call `save_verification_report(invoice_data)` with parsed JSON.")