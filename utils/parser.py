import os
import re
from dotenv import load_dotenv
from utils.ocr_utils import extract_text_with_layout, extract_text
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192"
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

# Use the new pipe syntax: prompt | llm
chain = prompt_template | llm

# Function to extract JSON block from text
def extract_json_from_response(response_text):
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        return match.group(0)
    return "{}"

# Main parser function
def parse_invoice_fields(image, use_layout=True):
    # OCR extraction
    if use_layout:
        ocr_data = extract_text_with_layout(image)
        text_blocks = "\n".join([f"{item['text']} (pos: {item['top']},{item['left']})" for item in ocr_data])
    else:
        text_blocks = extract_text(image)

    # Run the LLM chain
    response = chain.invoke({"ocr_text": text_blocks})

    # Extract just the JSON string
    response_text = response.content
    json_only = extract_json_from_response(response_text)

    return json_only
