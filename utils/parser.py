import os
import re
import json
from dotenv import load_dotenv
from utils.ocr_utils import extract_text_with_layout, extract_text
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0
)

# Define the prompt
prompt_template = PromptTemplate(
    input_variables=["ocr_text"],
    template="""
You are an expert at parsing invoice documents. Based on the following OCR output from an invoice, extract and return the information in valid JSON format.

Fields to extract:
- invoice_number
- invoice_date
- supplier_gst_number
- bill_to_gst_number
- po_number
- shipping_address
- seal_and_sign_present (true/false)
- no_items
- items: [{{serial_number, description, hsn_sac, quantity, unit_price, total_amount}}]

OCR Result:
{ocr_text}

Respond only with the JSON output.
"""
)

# Combine prompt → LLM → output parser
chain = prompt_template | llm | StrOutputParser()

# Function to extract JSON from response text
def extract_json_from_response(response_text):
    try:
        return json.dumps(json.loads(response_text), indent=2)
    except:
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            try:
                return json.dumps(json.loads(match.group(0)), indent=2)
            except:
                return json.dumps({"error": "Failed to parse extracted JSON."})
        return json.dumps({"error": "No valid JSON found in response."})


# Main parser function
def parse_invoice_fields(image, use_layout=True):
    # OCR Extraction
    if use_layout:
        ocr_data = extract_text_with_layout(image)
        text_blocks = "\n".join(
            [f"{item['text']} (pos: {item['top']},{item['left']})" for item in ocr_data]
        )
    else:
        text_blocks = extract_text(image)

    # Check for empty OCR text
    if not text_blocks.strip() or len(text_blocks.strip()) < 30:
        return json.dumps({
            "error": "OCR result is too empty or unclear to parse."
        }, indent=2)

    try:
        # Run LLM chain
        response_text = chain.invoke({"ocr_text": text_blocks})
        json_only = extract_json_from_response(response_text)
        return json_only
    except Exception as e:
        return json.dumps({
            "error": f"Exception while invoking LLM: {str(e)}"
        }, indent=2)
