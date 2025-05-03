import re
import cv2
from pdf2image import convert_from_path
import numpy as np
from paddleocr import PaddleOCR


def paddle_ocr(pdf_path):
    # Convert the first page of the PDF to an image
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)
    if not pages:
        print("Failed to convert PDF to image.")
        return

    # Initialize OCR engine
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')
    # Use the first page image for OCR
    img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)  
    result = ocr_engine.ocr(img, cls=True)  
    # Concatenate the text results from PaddleOCR into a single string
    full_text = ""
    for line in result[0]:
        _, (text, _) = line
        full_text += text + " "
    return full_text.strip()  

def extract_account_number(pdf_text):
    """Extract the account number based on keywords like 'Account Number', 'Account No', 'Account ID'."""
    account_patterns = [
        r"(?:Account Number|Account No\.?|Account ID|AccountNumber)[\s:]*([A-Za-z0-9]+)",  
        r"\b([A-Za-z0-9]{10,20})\b"  
    ]
    for pattern in account_patterns:
        match = re.search(pattern, pdf_text)
        if match:
            return match.group(1)  
    return "Account number not found"

# def extract_account_holder_name(pdf_text):
#     """Extract the account holder's name based on keywords like 'Account Holder's Name', 'Account Name', 'Name'."""
#     name_patterns = [
#         r"(?:Account Holder's Name|Account Name|Name)[:\s]*([A-Za-z\s]+)",  # Match name after keywords
#         r"(?<=Name[:\s])([A-Za-z\s]+)",  
#     ]
#     for pattern in name_patterns:
#         match = re.search(pattern, pdf_text, re.IGNORECASE)
#         if match:
#             return match.group(1).strip()  
#     return "Account holder's name not found"

def identify_bank(pdf_text):
    """Identify bank from the PDF text based on keywords."""
    bank_keywords = {
        "Axis Bank": ["axis", "Axis Bank"],
        "HDFC Bank": ["hdfc", "HDFC Bank"],
        "Canara Bank": ["Canara", "Canara Bank"],
        "Induslnd Bank": ["Induslnd", "Induslnd Bank"],
        "Andhra Bank": ["andhra", "Andhra Bank"],
        "Union Bank": ["union", "Union Bank"],
        "Bandhan Bank": ["bandhan", "Bandhan Bank"],
        "State Bank of India": ["OSBI", "SBI", "State Bank of India", "sbi"]
    }

    for bank, keywords in bank_keywords.items():
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', pdf_text, re.IGNORECASE):
                return bank
    return "Bank not identified"

def main(pdf_path):
    # First, try to extract text using Tesseract OCR
    pdf_text = paddle_ocr(pdf_path)
    bank_name = identify_bank(pdf_text)
    account_number = extract_account_number(pdf_text)
    # account_holder_name = extract_account_holder_name(pdf_text)

    print(f"The bank statement is for: {bank_name}")
    print(f"Extracted account number: {account_number}")
    # print(f"Extracted account holder's name: {account_holder_name}")


pdf_path = input("Please enter the pdf path:- ")
main(pdf_path)
