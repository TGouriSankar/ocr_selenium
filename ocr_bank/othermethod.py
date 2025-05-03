# from google.cloud import vision
# from PIL import Image
# import fitz  # PyMuPDF
# import pandas as pd
# import os


# def detect_text_google_vision(image_path):
#     """Detects text in an image using Google Cloud Vision."""
#     client = vision.ImageAnnotatorClient()

#     with open(image_path, "rb") as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)
#     response = client.text_detection(image=image)
#     annotations = response.text_annotations

#     if response.error.message:
#         raise Exception(f"Error from Vision API: {response.error.message}")

#     # Extract text and bounding boxes
#     if annotations:
#         detected_text = annotations[0].description  # Full detected text
#         return detected_text
#     else:
#         return ""


# def extract_tables_to_files_google_vision(pdf_file_path, output_folder):
#     """Extract tables from a PDF using Google Cloud Vision and save to CSV/Excel."""
#     os.makedirs(output_folder, exist_ok=True)

#     # Convert PDF pages to images
#     images = []
#     with fitz.open(pdf_file_path) as pdf:
#         for pg in range(pdf.page_count):
#             page = pdf[pg]
#             mat = fitz.Matrix(2, 2)
#             pm = page.get_pixmap(matrix=mat, alpha=False)

#             # Ensure the image isn't too large
#             if pm.width > 2000 or pm.height > 2000:
#                 pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

#             img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
#             image_path = os.path.join(output_folder, f"page_{pg + 1}.png")
#             img.save(image_path)
#             images.append(image_path)

#     # Process each image with Google Cloud Vision
#     for idx, image_path in enumerate(images):
#         detected_text = detect_text_google_vision(image_path)

#         # Process detected text into rows and columns
#         rows = detected_text.strip().split("\n")
#         data = [row.split() for row in rows]  # Adjust splitting based on actual layout

#         # Save to CSV and Excel
#         page_number = idx + 1
#         csv_file_path = os.path.join(output_folder, f"page_{page_number}.csv")
#         excel_file_path = os.path.join(output_folder, f"page_{page_number}.xlsx")
        
#         # Convert to DataFrame
#         df = pd.DataFrame(data)
        
#         # Save as CSV
#         df.to_csv(csv_file_path, index=False, header=False)
#         print(f"Extracted data for page {page_number} saved to {csv_file_path}")

#         # Save as Excel
#         df.to_excel(excel_file_path, index=False, header=False)
#         print(f"Extracted data for page {page_number} saved to {excel_file_path}")


# def main(pdf_path):
#     output_folder = f'/media/nesru/karna/HYD/{os.path.splitext(os.path.basename(pdf_path))[0]}'
#     extract_tables_to_files_google_vision(pdf_path, output_folder)


# if __name__ == "__main__":
#     pdf_path = "/media/nesru/karna/HYD/pdfplumber/pdf-sample/union-bank-of-india-1-account-statement-pdf_compress.pdf"
#     main(pdf_path)


import pytesseract
import pandas as pd
from PIL import Image
import fitz  # PyMuPDF
import os
import cv2
import numpy as np
import re

def extract_tables_to_files_tesseract(pdf_file_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open PDF and convert pages to images
    imgs = []
    with fitz.open(pdf_file_path) as pdf:
        for pg in range(pdf.page_count):
            page = pdf[pg]
            mat = fitz.Matrix(2, 2)
            pm = page.get_pixmap(matrix=mat, alpha=False)

            if pm.width > 2000 or pm.height > 2000:
                pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

            img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            imgs.append(img)

    # Process each image
    for index, img in enumerate(imgs):
        # Use Tesseract to extract data
        extracted_text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')  # PSM 6 for uniform blocks

        # Convert extracted text into a table format
        rows = extracted_text.strip().split("\n")
        data = [re.split(r'\s{2,}', row) for row in rows]  # Split by two or more spaces
        df = pd.DataFrame(data)

        # Save the data to a CSV or Excel file
        page_number = index + 1
        csv_file_path = os.path.join(output_folder, f"page_{page_number}.csv")
        excel_file_path = os.path.join(output_folder, f"page_{page_number}.xlsx")
        
        # Save as CSV
        df.to_csv(csv_file_path, index=False, header=False)
        print(f"Extracted data for page {page_number} saved to {csv_file_path}")

        # Save as Excel
        df.to_excel(excel_file_path, index=False, header=False)
        print(f"Extracted data for page {page_number} saved to {excel_file_path}")


# Main function to coordinate steps
def main(pdf_path):
    output_folder = f'/media/nesru/karna/HYD/{os.path.splitext(os.path.basename(pdf_path))[0]}'
    extract_tables_to_files_tesseract(pdf_path, output_folder)


# Run the main function with the specified PDF path
if __name__ == "__main__":
    pdf_path = "/media/nesru/karna/HYD/pdfplumber/pdf-sample/union-bank-of-india-1-account-statement-pdf_compress.pdf"
    main(pdf_path)