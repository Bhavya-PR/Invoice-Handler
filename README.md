# Yavar.AI Hackathon Invoice Handler
 
# Invoice Extraction & Verification System
## 🚀 Overview
An Automated Invoice Processing System utilizes **OCR (Tesseract)** and **YOLOv8** to extract, validate, and process invoice data efficiently. It converts PDFs into structured **JSON and Excel reports**, ensuring accurate financial document handling while detecting seals/signatures for verification. Additionally, **Groq's Llama3 model** enhances text parsing, intelligently correcting and inferring missing invoice details.

## 🛠 Technologies Used
- **Python** → Main programming language for processing

- **Tesseract OCR** → Optical character recognition for text extraction

- **PDF2Image** → Converts PDFs into images for better OCR accuracy

- **OpenCV** → Preprocesses images (grayscale, sharpening, noise removal)

- **YOLOv8** → Deep learning model for seal/signature detection

- **Pandas** → Handles structured data, converts JSON to Excel output

- **LangChain & Groq's Llama3** → LLM-based intelligent text parsing & correction

- **dotenv** → Manages environment variables for API security

- **JSON** → Stores extracted invoice data in a structured format

- **Regex** → Cleans and refines OCR-extracted text

- **Subprocess** → Executes pipeline components dynamically

- **cv2 (OpenCV)** → Image transformations & noise reduction

- **NumPy** → Efficient array handling for image and text processing

## 🔧 Installation Guide
```bash
pip install -r requirements.txt
