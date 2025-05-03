import re
import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
from paddleocr import PaddleOCR


def pytesseract_ocr(pdf_path):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path)

    # Loop through each page image
    for page_num, page_image in enumerate(pages, start=1):
        # Convert PIL image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

        # Optional: Resize image to improve OCR accuracy
        scale_percent = 150  # Scale up by 150%
        width = int(open_cv_image.shape[1] * scale_percent / 100)
        height = int(open_cv_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_img = cv2.resize(open_cv_image, dim, interpolation=cv2.INTER_LINEAR)

        # Convert to grayscale
        gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

        # Optional: Apply adaptive thresholding to enhance text regions
        thresh_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)

        # Use Tesseract OCR on the processed image
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh_img, config=custom_config)
        return text


# def paddleOCR(pdf_path):
#     # Convert PDF to images
#     pages = convert_from_path(pdf_path)
#     ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize OCR engine

#     # Process each page image and extract text
#     for page_num, page_image in enumerate(pages, start=1):
#         # Convert PIL Image to OpenCV format
#         img = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
        
#         # Perform OCR on the image
#         result = ocr_engine.ocr(img, cls=True)

#         for line in result[0]:
#             # Unpack the OCR result structure
#             box, (text, score) = line
#             print(text)
#             return text


def paddleOCR(pdf_path):
    # Convert PDF to images
    pages = convert_from_path(pdf_path)
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize OCR engine
    all_text = ""  # Initialize a string to collect all text

    # Process each page image and extract text
    for page_num, page_image in enumerate(pages, start=1):
        # Convert PIL Image to OpenCV format
        img = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
        
        # Perform OCR on the image
        result = ocr_engine.ocr(img, cls=True)

        # Collect text from each line on the page
        for line in result[0]:
            # Unpack the OCR result structure
            box, (text, score) = line
            all_text += text + "\n"  # Append each line to the all_text string

        # Print all text extracted from the current page
        print(f"\n--- Text for Page {page_num} ---")
        print(all_text)

    # Return the full text if you want to use it further
    return all_text


def identify_bank(pdf_text):
    """Identify bank from the PDF text based on keywords.
       Add more banks and keywords as needed based on over test cases"""
    bank_keywords = {
        "Axis Bank": ["axis", "Axis Bank"],
        "HDFC Bank": ["hdfc", "HDFC Bank"],
        "Canara Bank": ["Canara","Canara Bank"],
        "Induslnd Bank": ["Induslnd", "Induslnd Bank"],
        "Andhra Bank": ["Andhra Bank"],
        "Union Bank": ["union", "Union Bank"],
        "Bandhan Bank": ["bandhan", "Bandhan Bank"],
        "State Bank of India": ["OSBI","SBI", "SBI Card", "OSBI_LCArG", "State Bank of India", "sbi"]
    }

    for bank, keywords in bank_keywords.items():
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', pdf_text, re.IGNORECASE):
                return bank
    return "Bank not identified"


def main(pdf_path):
    # First, try to extract text using Tesseract OCR
    pdf_text = pytesseract_ocr(pdf_path)
    bank_name = identify_bank(pdf_text)
    
    # If no bank is identified, try to extract text using PaddleOCR
    if bank_name == "Bank not identified":
        print("Bank not identified using Tesseract. Trying PaddleOCR...")
        pdf_text = paddleOCR(pdf_path)
        bank_name = identify_bank(pdf_text)

    print(f"The bank statement is for: {bank_name}")


pdf_path = "/media/player/karna1/HYD/pdfplumber/sample_pdf/indusindaccountstatement-xxxxxxxx8783-6-12-2023-134949_compress.pdf"
main(pdf_path)


# import re
# import cv2
# import pytesseract
# from pdf2image import convert_from_path
# import numpy as np
# from paddleocr import PaddleOCR


# def extract_text_from_pdf(pdf_path):
#     # Convert PDF pages to images
#     pages = convert_from_path(pdf_path)

#     # Loop through each page image
#     extracted_text = ""
#     for page_num, page_image in enumerate(pages, start=1):
#         # Convert PIL image to OpenCV format
#         open_cv_image = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

#         # Optional: Resize image to improve OCR accuracy
#         scale_percent = 150
#         width = int(open_cv_image.shape[1] * scale_percent / 100)
#         height = int(open_cv_image.shape[0] * scale_percent / 100)
#         dim = (width, height)
#         resized_img = cv2.resize(open_cv_image, dim, interpolation=cv2.INTER_LINEAR)

#         # Convert to grayscale
#         gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

#         # Optional: Apply adaptive thresholding to enhance text regions
#         thresh_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                            cv2.THRESH_BINARY, 11, 2)

#         # Use Tesseract OCR on the processed image
#         custom_config = r'--oem 3 --psm 6'
#         text = pytesseract.image_to_string(thresh_img, config=custom_config)
#         extracted_text += text
#     return extracted_text


# def pdf_text_extract(pdf_path):
#     # Convert PDF to images
#     pages = convert_from_path(pdf_path)
#     ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')

#     extracted_text = ""
#     for page_num, page_image in enumerate(pages, start=1):
#         img = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
#         result = ocr_engine.ocr(img, cls=True)

#         for line in result[0]:
#             box, (text, score) = line
#             extracted_text += text + " "
#     return extracted_text

# # def identify_bank_details(pdf_text):
# #     """Identify bank, account number, and user name from the PDF text."""
# #     bank_keywords = {
# #         "Axis Bank": ["axis", "Axis Bank"],
# #         "HDFC Bank": ["hdfc", "HDFC Bank"],
# #         "Canara Bank": ["Canara","Canara Bank"],
# #         "Induslnd Bank": ["Induslnd", "Induslnd Bank"],
# #         "Andhra Bank": ["Andhra Bank"],
# #         "Union Bank": ["union", "Union Bank"],
# #         "Bandhan Bank": ["bandhan", "Bandhan Bank"],
# #         "State Bank of India": ["OSBI","SBI", "SBI Card", "OSBI_LCArG", "State Bank of India", "sbi"]
# #     }

# #     bank_name = "Bank not identified"
# #     account_number = "Account number not found"
# #     user_name = "User name not found"

# #     # Identify bank
# #     for bank, keywords in bank_keywords.items():
# #         for keyword in keywords:
# #             if re.search(rf'\b{keyword}\b', pdf_text, re.IGNORECASE):
# #                 bank_name = bank
# #                 break

# #     # Find account number (search for 'Account Number' or 'Account No', followed by digits)
# #     account_number_match = re.search(r"(Account (Number|No)[:\s]*)(\d{10,16})", pdf_text, re.IGNORECASE)
# #     if account_number_match:
# #         account_number = account_number_match.group(3)

# #     # Find user name in the format "Account Holder's Name"
# #     user_name_match = re.search(r"Account Holder(?:'s)? Name[:\s]+([A-Za-z\s]+)", pdf_text, re.IGNORECASE)
# #     if user_name_match:
# #         user_name = user_name_match.group(1).strip()

# #     return bank_name, account_number, user_name



# def identify_bank_details(pdf_text):
#     """Identify bank, account number, and user name from the PDF text."""
#     bank_keywords = {
#         "Axis Bank": ["axis", "Axis Bank"],
#         "HDFC Bank": ["hdfc", "HDFC Bank"],
#         "Canara Bank": ["Canara","Canara Bank"],
#         "Induslnd Bank": ["Induslnd", "Induslnd Bank"],
#         "Andhra Bank": ["Andhra Bank"],
#         "Union Bank": ["union", "Union Bank"],
#         "Bandhan Bank": ["bandhan", "Bandhan Bank"],
#         "State Bank of India": ["OSBI","SBI", "SBI Card", "OSBI_LCArG", "State Bank of India", "sbi"]
#     }

#     bank_name = "Bank not identified"
#     account_number = "Account number not found"
#     user_name = "User name not found"
    

#     # Identify bank
#     for bank, keywords in bank_keywords.items():
#         for keyword in keywords:
#             if re.search(rf'\b{keyword}\b', pdf_text, re.IGNORECASE):
#                 bank_name =  bank
#                 break

#     # Find account number (common pattern: 10-16 consecutive digits)
#     account_number_match = re.search(r'\b\d{10,16}\b', pdf_text)
#     if account_number_match:
#         account_number = account_number_match.group(0)

#     # Find user name (look for "Account Holder" or similar)
#     user_name_match = re.search(r"(Account Holder|Account Name):?\s+([A-Za-z\s]+)", pdf_text)
#     if user_name_match:
#         user_name = user_name_match.group(2).strip()

#     return bank_name, account_number, user_name


# def main(pdf_path):
#     # First, try to extract text using Tesseract OCR
#     pdf_text = extract_text_from_pdf(pdf_path)
#     bank_name, account_number, user_name = identify_bank_details(pdf_text)
    
#     # If bank is not identified, try using PaddleOCR
#     if bank_name == "Bank not identified":
#         print("Bank not identified using Tesseract. Trying PaddleOCR...")
#         pdf_text = pdf_text_extract(pdf_path)
#         bank_name, account_number, user_name = identify_bank_details(pdf_text)

#     print(f"Bank Name: {bank_name}")
#     print(f"Account Number: {account_number}")
#     print(f"User Name: {user_name}")


# # Usage example
# pdf_path = "/media/player/karna1/HYD/pdfplumber/sample_pdf/union-bank-of-india-1-account-statement-pdf_compress.pdf"
# main(pdf_path)
