import re
from datetime import datetime

def validate_invoice_data(invoice_data):
    """
    Validates extracted invoice fields from parsed JSON.
    
    Args:
        invoice_data (dict): Parsed JSON invoice data
    
    Returns:
        dict: Validation result with errors and status
    """
    errors = []

    # Updated GST pattern for Indian GST only
    gst_pattern = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}$", re.IGNORECASE)
    # Generic GST-like pattern to allow non-Indian GST (relaxed)
    generic_gst_pattern = re.compile(r"^[A-Z0-9]{8,15}$", re.IGNORECASE)

    # Support more date formats (including 2-digit year)
    date_formats = [
        "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y",
        "%d/%m/%y", "%m/%d/%y"
    ]  # Common date formats + 2-digit year

    required_fields = [
        "invoice_number", "invoice_date", "supplier_gst_number",
        "bill_to_gst_number", "po_number", "shipping_address",
        "seal_and_sign_present", "no_items", "items"
    ]

    for field in required_fields:
        if field not in invoice_data:
            errors.append(f"Missing required field: {field}")

    # Validate invoice_number: non-empty string
    if "invoice_number" in invoice_data:
        if not invoice_data["invoice_number"] or not isinstance(invoice_data["invoice_number"], str):
            errors.append("invoice_number should be a non-empty string")

    # Validate invoice_date: should match any allowed date format
    if "invoice_date" in invoice_data:
        valid_date = False
        date_val = invoice_data["invoice_date"]
        for fmt in date_formats:
            try:
                datetime.strptime(date_val, fmt)
                valid_date = True
                break
            except:
                pass
        if not valid_date:
            errors.append(f"invoice_date '{date_val}' does not match expected date formats")

    # Validate GST numbers - allow empty or generic pattern if non-Indian GST detected
    for gst_field in ["supplier_gst_number", "bill_to_gst_number"]:
        if gst_field in invoice_data:
            gst_val = invoice_data[gst_field].strip()
            if gst_val == "":
                errors.append(f"{gst_field} is empty")
            else:
                # Check Indian GST format first
                if not gst_pattern.match(gst_val):
                    # If not Indian GST, allow generic alphanumeric GST-like
                    if not generic_gst_pattern.match(gst_val):
                        errors.append(f"{gst_field} '{gst_val}' is not a valid GST number")

    # Validate po_number: non-empty string
    if "po_number" in invoice_data:
        if not invoice_data["po_number"] or not isinstance(invoice_data["po_number"], str):
            errors.append("po_number should be a non-empty string")

    # Validate shipping_address: non-empty string
    if "shipping_address" in invoice_data:
        if not invoice_data["shipping_address"] or not isinstance(invoice_data["shipping_address"], str):
            errors.append("shipping_address should be a non-empty string")

    # Validate seal_and_sign_present: should be boolean
    if "seal_and_sign_present" in invoice_data:
        if not isinstance(invoice_data["seal_and_sign_present"], bool):
            errors.append("seal_and_sign_present should be true or false")

    # Validate no_items: integer >= 0
    if "no_items" in invoice_data:
        try:
            no_items = int(invoice_data["no_items"])
            if no_items < 0:
                errors.append("no_items should be a non-negative integer")
        except:
            errors.append("no_items should be an integer")

    # Validate items: list with correct fields and amount check
    if "items" in invoice_data:
        if not isinstance(invoice_data["items"], list):
            errors.append("items should be a list")
        else:
            for idx, item in enumerate(invoice_data["items"], start=1):
                required_item_fields = ["serial_number", "description", "hsn_sac", "quantity", "unit_price", "total_amount"]
                for field in required_item_fields:
                    if field not in item:
                        errors.append(f"Item {idx} missing field: {field}")
                    else:
                        # Basic type checks
                        if field in ["serial_number", "description", "hsn_sac"]:
                            if not isinstance(item[field], str) or not item[field].strip():
                                errors.append(f"Item {idx} field '{field}' should be a non-empty string")
                        if field in ["quantity", "unit_price", "total_amount"]:
                            try:
                                val = float(item[field])
                                if val < 0:
                                    errors.append(f"Item {idx} field '{field}' should be non-negative")
                            except:
                                errors.append(f"Item {idx} field '{field}' should be numeric")

                # Amount consistency check: quantity * unit_price ≈ total_amount
                try:
                    q = float(item.get("quantity", 0))
                    u = float(item.get("unit_price", 0))
                    t = float(item.get("total_amount", 0))
                    calculated = round(q * u, 2)
                    # Allow small rounding difference (±0.05)
                    if abs(calculated - t) > 0.05:
                        errors.append(f"Item {idx} total_amount {t} does not match quantity * unit_price ({q} * {u} = {calculated})")
                except:
                    # If conversion fails, error already recorded above
                    pass

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
