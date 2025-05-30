import json
import pandas as pd
import os

# Define paths
JSON_FILE = "output/extracted_data.json"
EXCEL_OUTPUT_FILE = "output/extracted_data.xlsx"

def json_to_excel():
    """Reads parsed JSON and converts it into an Excel file."""
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)  # Flatten JSON structure
    df.to_excel(EXCEL_OUTPUT_FILE, index=False)

    print(f"✅ Extracted data saved as {EXCEL_OUTPUT_FILE}")

if __name__ == "__main__":
    json_to_excel()
