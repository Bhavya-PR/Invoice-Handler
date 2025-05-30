import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0
)

# Define directories
TEXT_INPUT_FOLDER = "output/extracted_text"
JSON_OUTPUT_FOLDER = "output/parsed_json"

def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def preprocess_text(text):
    """
    Cleans OCR-extracted text and ensures correct alignment of item rows.
    - Standardizes date formats
    - Fixes broken invoice item structure
    - Enhances detection of quantity & unit price
    """
    text = re.sub(r"[^a-zA-Z0-9\s:/.,-]", "", text)  # Remove unwanted symbols
    text = re.sub(r"\s{2,}", " ", text)  # Reduce excessive spaces
    text = re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\1-\2-\3", text)  # Standardize dates

    # Ensure item rows follow structured format: `serial_number | description | hsn_sac | quantity | unit_price | total_amount`
    text = re.sub(r"(\d+)\s+([\w\s]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)", r"\1 | \2 | | \3 | \4 | \5", text)

    return text.strip()

# Improved prompt for extracting structured JSON output
prompt_template = PromptTemplate(
    input_variables=["ocr_text"],
    template="""
You are an expert at parsing invoice documents. Extract structured data from the OCR results into **valid JSON format**.

### **Required Fields**
- invoice_number
- invoice_date (format: DD-MM-YYYY)
- supplier_gst_number
- bill_to_gst_number
- po_number
- shipping_address
- seal_and_sign_present (true/false)
- no_items
- items: [{{serial_number, description, hsn_sac, quantity, unit_price, total_amount}}]

### **Important Instructions**
1️⃣ **Ensure ALL items are correctly extracted**—even if the text is unclear.
2️⃣ **If an item row is broken, intelligently infer missing values.**
3️⃣ **Verify unit prices match quantities properly to prevent mismatches.**
4️⃣ **Respond ONLY with valid JSON—no extra commentary.**

### **OCR Data for Parsing**
{ocr_text}
"""
)

# Combine prompt → LLM → output parser
chain = prompt_template | llm | StrOutputParser()

# Improved JSON extraction with validation
def extract_json_from_response(response_text):
    """
    Extracts and verifies JSON structure from AI response.
    - Removes extra non-JSON text
    - Ensures structured item formatting
    """
    try:
        parsed_json = json.loads(response_text)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\})", response_text, re.DOTALL)
        if match:
            try:
                parsed_json = json.loads(match.group(0))
            except json.JSONDecodeError:
                return {"error": "Failed to parse extracted JSON."}
        else:
            return {"error": "No valid JSON found in response."}

    # Validate item fields
    for item in parsed_json.get("items", []):
        if not item.get("quantity") or not item.get("unit_price"):
            item["error"] = "Quantity or unit price missing"

    return parsed_json

# Parse invoice details from extracted text files
def parse_invoice_text_files():
    """
    Reads text files from 'output/extracted_text/',
    extracts invoice fields using LLM, and saves structured JSON in 'output/parsed_json/'.
    """
    ensure_folder_exists(JSON_OUTPUT_FOLDER)

    for filename in os.listdir(TEXT_INPUT_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(TEXT_INPUT_FOLDER, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                ocr_text = f.read().strip()

            # Preprocess extracted text before sending to LLM
            cleaned_text = preprocess_text(ocr_text)

            # Skip empty OCR results
            if not cleaned_text or len(cleaned_text) < 30:
                parsed_data = {"error": "OCR text is too empty or unclear to parse."}
            else:
                try:
                    response_text = chain.invoke({"ocr_text": cleaned_text})
                    parsed_data = extract_json_from_response(response_text)
                except Exception as e:
                    parsed_data = {"error": f"Exception while invoking LLM: {str(e)}"}

            # Save extracted JSON
            json_filename = filename.replace(".txt", ".json")
            json_path = os.path.join(JSON_OUTPUT_FOLDER, json_filename)

            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(parsed_data, json_file, indent=4)

            print(f"✅ Extracted JSON saved: {json_path}")

# Example execution
if __name__ == "__main__":
    parse_invoice_text_files()