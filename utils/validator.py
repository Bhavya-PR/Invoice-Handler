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

    # Indian GSTIN pattern
    gst_pattern = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}$", re.IGNORECASE)
    # Generic relaxed GST-like pattern
    generic_gst_pattern = re.compile(r"^[A-Z0-9]{8,15}$", re.IGNORECASE)

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

    for field in required_fields:
        if field not in invoice_data:
            errors.append(f"Missing required field: {field}")

    # Validate invoice_number
    if "invoice_number" in invoice_data:
        val = invoice_data["invoice_number"]
        if not val or not isinstance(val, str):
            errors.append("Invalid invoice_number: should be a non-empty string")

    # Validate invoice_date
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
            errors.append(f"Invalid invoice_date: '{date_val}' does not match expected date formats")

    # Validate GST fields
    for gst_field in ["supplier_gst_number", "bill_to_gst_number"]:
        if gst_field in invoice_data:
            gst_val = invoice_data[gst_field].strip()
            if gst_val == "":
                errors.append(f"{gst_field} is empty")
            elif not gst_pattern.match(gst_val) and not generic_gst_pattern.match(gst_val):
                errors.append(f"{gst_field} '{gst_val}' is not a valid GST number")

    # Validate po_number
    if "po_number" in invoice_data:
        val = invoice_data["po_number"]
        if not val or not isinstance(val, str):
            errors.append("Invalid po_number: should be a non-empty string")

    # Validate shipping_address
    if "shipping_address" in invoice_data:
        val = invoice_data["shipping_address"]
        if not val or not isinstance(val, str):
            errors.append("Invalid shipping_address: should be a non-empty string")

    # Validate seal_and_sign_present
    if "seal_and_sign_present" in invoice_data:
        if not isinstance(invoice_data["seal_and_sign_present"], bool):
            errors.append("Invalid seal_and_sign_present: should be true or false")

    # Validate no_items
    if "no_items" in invoice_data:
        try:
            no_items = int(invoice_data["no_items"])
            if no_items < 0:
                errors.append("Invalid no_items: should be a non-negative integer")
        except:
            errors.append("Invalid no_items: should be an integer")

    # Validate items
    if "items" in invoice_data:
        if not isinstance(invoice_data["items"], list):
            errors.append("Invalid items: should be a list")
        else:
            items = invoice_data["items"]
            no_items = int(invoice_data.get("no_items", 0))

            # Skip validation if explicitly empty and matches no_items
            if no_items == 0 and len(items) == 0:
                pass
            else:
                for idx, item in enumerate(items, start=1):
                    required_item_fields = [
                        "serial_number", "description", "hsn_sac",
                        "quantity", "unit_price", "total_amount"
                    ]

                    for field in required_item_fields:
                        if field not in item:
                            errors.append(f"[Item {idx}] Missing field: {field}")
                            continue

                        if field in ["serial_number", "description", "hsn_sac"]:
                            if not isinstance(item[field], str) or not item[field].strip():
                                errors.append(f"[Item {idx}] Field '{field}' should be a non-empty string")

                        if field in ["quantity", "unit_price", "total_amount"]:
                            try:
                                val = float(item[field])
                                if val < 0:
                                    errors.append(f"[Item {idx}] Field '{field}' should be non-negative")
                            except:
                                errors.append(f"[Item {idx}] Field '{field}' should be numeric")

                    # Consistency check
                    try:
                        q = float(item.get("quantity", 0))
                        u = float(item.get("unit_price", 0))
                        t = float(item.get("total_amount", 0))
                        calculated = round(q * u, 2)
                        if abs(calculated - t) > 0.05:
                            errors.append(
                                f"[Item {idx}] total_amount {t} ≠ quantity * unit_price ({q} * {u} = {calculated})"
                            )
                    except:
                        pass  # Already handled above

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
