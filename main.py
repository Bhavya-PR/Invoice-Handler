import os
import subprocess

# Define script paths
PREPROCESS_SCRIPT = "utils/preprocess.py"
OCR_SCRIPT = "utils/ocr_utils.py"
IMAGE_UTILS_SCRIPT = "utils/image_utils.py"
PARSER_SCRIPT = "utils/parser.py"
VALIDATOR_SCRIPT = "utils/validator.py"
EXCEL_SCRIPT = "utils/convert_to_excel.py"

def run_script(script_path):
    """Executes a Python script as a subprocess and captures the output."""
    if os.path.exists(script_path):
        print(f"Running {script_path}...")
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error in {script_path}: {result.stderr}")
    else:
        print(f"Script {script_path} not found!")

def main():
    """Runs the full invoice processing pipeline."""
    print("🔄 Starting Invoice Processing Pipeline...")

    # Step 1: Preprocess Images
    run_script(PREPROCESS_SCRIPT)

    # Step 2: Perform OCR on Invoices
    run_script(OCR_SCRIPT)

    # Step 3: Handle Image Processing (Seal Detection, Cropping)
    run_script(IMAGE_UTILS_SCRIPT)

    # Step 4: Parse Extracted Data into Structured Format
    run_script(PARSER_SCRIPT)

    # Step 5: Validate Extracted Invoice Data
    run_script(VALIDATOR_SCRIPT)

    # Step 6: Convert JSON to Excel Report
    run_script(EXCEL_SCRIPT)

    print("Invoice Processing Completed!")

if __name__ == "__main__":
    main()
