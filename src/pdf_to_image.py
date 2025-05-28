from pdf2image import convert_from_path


def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    for i, img in enumerate(images):
        img.save(f"{output_folder}/invoice_page_{i+1}.jpg", "JPEG")
    print(f"Extracted {len(images)} pages from {pdf_path}")

pdf_to_images("input/sample_invoice.pdf", "output")
