from pdf2image import convert_from_path

# Set the correct Poppler binary path
poppler_path = r"C:\Users\HP\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pdf_path = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\input\sample_invoice.pdf"
output_folder = r"C:\Users\HP\OneDrive\Desktop\FRONT END COURSE\Portfolio\Portfolio-master\Yavar.AI-Hackathon-PS-1\output"

def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    for i, img in enumerate(images):
        img.save(f"{output_folder}/invoice_page_{i+1}.jpg", "JPEG")
    print(f"Extracted {len(images)} pages from {pdf_path}")

pdf_to_images(pdf_path, output_folder)
