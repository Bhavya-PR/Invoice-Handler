
# 📄 Yavar.AI Hackathon – Invoice Extraction & Verification System

An AI-Powered Invoice Processing System designed for automated, accurate, and scalable financial document handling. It uses **OCR**, **Computer Vision**, and **LLM-based parsing** to extract, validate, and structure invoice data from scanned PDFs into **JSON** and **Excel reports**, with intelligent verification using **seal/signature detection** and **missing detail inference**.

![Workflow](workflow.jpg)

---

## 🚀 Overview

This system performs the following:
- Converts **PDFs to images**
- Applies **preprocessing** to enhance OCR clarity
- Extracts **invoice text** using **Tesseract OCR**
- Detects **seals and signatures** using **YOLOv8**
- Parses text into **structured JSON** using **Groq's Llama3**
- Validates & assigns **confidence scores**
- Outputs **Excel reports** using **Pandas**

---

## 🛠 Technologies Used

| Technology                 | Description                                           |
|----------------------------|-------------------------------------------------------|
| **Python**                 | Main programming language                             |
| **Tesseract OCR**          | Extracts text from invoice images                     |
| **PDF2Image**              | Converts PDFs into images                             |
| **OpenCV**                 | Image preprocessing (grayscale, thresholding, etc.)   |
| **YOLOv8**                 | Detects seals/signatures                              |
| **Pandas**                 | Converts structured JSON to Excel                     |
| **LangChain + Llama3**     | LLM-based intelligent parsing and correction          |
| **Regex**                  | Refines extracted text                                |
| **dotenv**                 | Manages environment variables                         |
| **Subprocess**             | Dynamically runs OCR & model commands                 |
| **NumPy**                  | Image and array operations                            |

---

## 🔧 Preprocessing Steps for OCR Optimization

- 🎨 **Grayscale conversion** to eliminate background noise
- 🖤 **Adaptive thresholding** to improve text contrast
- 🌪 **Denoising** using Gaussian & Non-Local Means (NLM)
- 🛠 **Morphological operations** to clean broken characters
- 🧾 **Regex formatting** for standardizing invoice content

---

## 🧠 LLM Parsing & Optimization

- 🧠 Engineered prompts to guide **Groq’s Llama3** for clean structured output
- 🧪 Confidence scoring to evaluate data reliability
- ⚙️ Refined invoice field extraction using pattern rules
- 🔍 Corrects missing or unclear data intelligently

---

## 📈 Fine-Tuning Summary

| Component         | Optimization Done                                  |
|------------------|-----------------------------------------------------|
| **Tesseract OCR**| Used `--psm 6 --oem 3` for layout-aware accuracy     |
| **YOLOv8**       | Adjusted IoU & confidence thresholds for seals      |
| **Llama3**       | Prompt engineering for precise JSON formatting      |
| **Regex**        | Cleaned and formatted key fields                    |

---

## 📁 File Structure

```
invoice_extractor/
├── input/                  # Input PDF files
├── output/                 # JSON/Excel output
├── utils/                  
│   ├── ocr_utils.py        # OCR and preprocessing logic
│   ├── parser.py           # LLM-based text parsing
│   ├── validator.py        # Field validation & confidence scores
│   ├── exporter.py         # Export to Excel
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

![File Structure](file_structure.png)

---

## 🧪 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Bhavya-PR/Yavar.AI-Hackathon-Invoice-Handler
cd invoice-processing-system
```

### 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Install & Configure Tesseract OCR

📥 [Download Tesseract for Windows](https://github.com/tesseract-ocr/tesseract)

Default install path:
```bash
C:\Program Files\Tesseract-OCR\
```

Add this to your script:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

### 4️⃣ Install & Configure Poppler

📥 [Download Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)

Extract and move to:
```bash
C:\Program Files\poppler-24.08.0\
```

Update your script:
```python
from pdf2image import convert_from_path
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
```

---

### 5️⃣ Run the Project

```bash
python main.py
```

---

## 🎥 Demo Video

🔗 [Click here to view the demo](https://drive.google.com/drive/folders/11QP1McS6u0orVLN1PsFPv4WMIqK5LtCI?usp=sharing)

> 🎥 *Ensure HD quality for the best viewing experience.*

---

## 🤝 Contributing

If you'd like to improve or extend the system, feel free to fork, make changes, and open a pull request!

---

## 📩 Contact

For any questions or feedback, reach out via GitHub or email 📬.

---

> ⚡ Powered by AI, Automation & Creativity – Built with ❤️ for the Yavar.AI Hackathon
