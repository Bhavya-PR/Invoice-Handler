import os

# Run all scripts sequentially
os.system("python src/pdf_to_image.py")    # Convert PDF to images
os.system("python src/preprocess_image.py") # Enhance images for better OCR
os.system("python src/extract_text.py")    # Extract text using OCR
os.system("python src/json_file_generator.py")   # Parse structured invoice data
os.system("python src/verify_invoice.py")  # Perform validation checks
os.system("python src/excel_file_generator.py") # Generate final Excel & JSON reports

print("✅ All tasks completed successfully! 🚀")
