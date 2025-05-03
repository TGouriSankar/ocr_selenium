import os
from pdf2image import convert_from_path
from ultralyticsplus import YOLO
import cv2
import re
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from paddleocr import PPStructure, save_structure_res, PaddleOCR
import pandas as pd

""" Bank Name & Account ID """
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

def identify_bank(pdf_text):
    """Identify bank from the PDF text based on keywords."""
    bank_keywords = {
        "Axis Bank": ["axis", "Axis Bank"],
        "HDFC Bank": ["hdfc", "HDFC Bank"],
        # "Canara Bank": ["Canara", "Canara Bank"],
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

""" PDF TO EXCEL """
# Step 1: Detect tables and create PDF
def detect_tables_and_create_pdf(pdf_path, output_folder):
    # Load YOLO model
    model = YOLO('foduucom/table-detection-and-extraction')

    # Set model parameters
    model.overrides['conf'] = 0.25
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1000

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Buffer size in pixels for each side
    buffer_size = 20

    # Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Process each page
    for page_num, page_image in enumerate(pages, start=1):
        # Convert PIL image to OpenCV format
        page_image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

        # Perform inference
        results = model.predict(page_image_cv)

        last_cropped_img = None

        # Loop through detected boxes and keep the last table with a score > 0.7
        for idx, box in enumerate(results[0].boxes):
            score = box.conf[0].item()
            if score > 0.7:
                x_min = max(0, int(box.xyxy[0][0]) - buffer_size)
                y_min = max(0, int(box.xyxy[0][1]) - buffer_size)
                x_max = min(page_image_cv.shape[1], int(box.xyxy[0][2]) + buffer_size)
                y_max = min(page_image_cv.shape[0], int(box.xyxy[0][3]) + buffer_size)

                # Crop the bounding box with buffer
                last_cropped_img = page_image_cv[y_min:y_max, x_min:x_max]

        # Save the last cropped image if found, else save the full page image
        if last_cropped_img is not None:
            last_cropped_img_pil = Image.fromarray(cv2.cvtColor(last_cropped_img, cv2.COLOR_BGR2RGB))
            # last_cropped_image_path = os.path.join(output_folder, f'page_{page_num}.png')
            last_cropped_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_{page_num}.png')
            last_cropped_img_pil.save(last_cropped_image_path)
            print(f"Saved last detected table on page {page_num} at {last_cropped_image_path}")
        else:
            # full_page_image_path = os.path.join(output_folder, f'page_{page_num}.png')
            full_page_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_{page_num}.png')
            page_image.save(full_page_image_path)
            print(f"No tables detected on page {page_num}. Saved full page image at {full_page_image_path}")

    # Create a PDF from all images in the output folder
    image_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
    image_files.sort()

    if image_files:
        image_paths = [os.path.join(output_folder, img_file) for img_file in image_files]
        first_image = Image.open(image_paths[0])
        pdf_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.pdf")
        first_image.save(pdf_file_path, save_all=True, append_images=[Image.open(img) for img in image_paths[1:]])
        print(f"All images saved into PDF at {pdf_file_path}")
        return pdf_file_path
    else:
        print("No images were found in the output folder, so no PDF was created.")
        return None

def detect_tables_and_create_pdf_hdfc(pdf_path, output_folder):
    # Load YOLO model
    model = YOLO('foduucom/table-detection-and-extraction')

    # Set model parameters
    model.overrides['conf'] = 0.25
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1000

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Buffer size in pixels for each side
    buffer_size = 20

    # Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Process each page
    for page_num, page_image in enumerate(pages, start=1):
        # Convert PIL image to OpenCV format
        page_image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

        # Perform inference
        results = model.predict(page_image_cv)

        last_cropped_img = None

        # Loop through detected boxes and keep the last table with a score > 0.7
        for idx, box in enumerate(results[0].boxes):
            score = box.conf[0].item()
            if score > 0.8:
                x_min = max(0, int(box.xyxy[0][0]) - buffer_size)
                y_min = max(0, int(box.xyxy[0][1]) - buffer_size)
                x_max = min(page_image_cv.shape[1], int(box.xyxy[0][2]) + buffer_size)
                y_max = min(page_image_cv.shape[0], int(box.xyxy[0][3]) + buffer_size)

                # Crop the bounding box with buffer
                last_cropped_img = page_image_cv[y_min:y_max, x_min:x_max]

        # Save the last cropped image if found, else save the full page image
        if last_cropped_img is not None:
            last_cropped_img_pil = Image.fromarray(cv2.cvtColor(last_cropped_img, cv2.COLOR_BGR2RGB))
            # last_cropped_image_path = os.path.join(output_folder, f'page_{page_num}.png')
            last_cropped_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_{page_num}.png')
            last_cropped_img_pil.save(last_cropped_image_path)
            print(f"Saved last detected table on page {page_num} at {last_cropped_image_path}")
        else:
            # full_page_image_path = os.path.join(output_folder, f'page_{page_num}.png')
            full_page_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_{page_num}.png')
            page_image.save(full_page_image_path)
            print(f"No tables detected on page {page_num}. Saved full page image at {full_page_image_path}")

    # Create a PDF from all images in the output folder
    image_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
    image_files.sort()

    if image_files:
        image_paths = [os.path.join(output_folder, img_file) for img_file in image_files]
        first_image = Image.open(image_paths[0])
        pdf_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.pdf")
        first_image.save(pdf_file_path, save_all=True, append_images=[Image.open(img) for img in image_paths[1:]])
        print(f"All images saved into PDF at {pdf_file_path}")
        return pdf_file_path
    else:
        print("No images were found in the output folder, so no PDF was created.")
        return None

def detect_tables_and_create_pdf_canara(pdf_path, output_folder):
    # Load YOLO model
    model = YOLO('foduucom/table-detection-and-extraction')

    # Set model parameters
    model.overrides['conf'] = 0.25
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1000

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Buffer size in pixels for each side
    buffer_size = 20

    # Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Process each page
    for page_num, page_image in enumerate(pages, start=1):
        if page_num == 1:
            # Always save the full image for the first page
            first_page_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_page_1.png')
            page_image.save(first_page_image_path)
            print(f"Saved full image of first page at {first_page_image_path}")
        else:
            # Convert PIL image to OpenCV format
            page_image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

            # Perform inference
            results = model.predict(page_image_cv)

            # Flag to track if a table has been detected
            table_detected = False

            # Loop through detected boxes and save the first table with a score > 0.7
            for idx, box in enumerate(results[0].boxes):
                score = box.conf[0].item()
                if score > 0.7:
                    # Crop the bounding box with buffer
                    x_min = max(0, int(box.xyxy[0][0]) - buffer_size)
                    y_min = max(0, int(box.xyxy[0][1]) - buffer_size)
                    x_max = min(page_image_cv.shape[1], int(box.xyxy[0][2]) + buffer_size)
                    y_max = min(page_image_cv.shape[0], int(box.xyxy[0][3]) + buffer_size)

                    cropped_img = page_image_cv[y_min:y_max, x_min:x_max]
                    
                    # Save the first detected table and break the loop
                    if not table_detected:
                        cropped_img_pil = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
                        cropped_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_page_{page_num}_1.png')
                        cropped_img_pil.save(cropped_image_path)
                        print(f"Saved first detected table on page {page_num} at {cropped_image_path}")
                        table_detected = True
                        break  # Move on to the next page after saving the first table

            # If no table is detected, save the full page image
            if not table_detected:
                full_page_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_page_{page_num}.png')
                page_image.save(full_page_image_path)
                print(f"No tables detected on page {page_num}. Saved full page image at {full_page_image_path}")

    # Create a PDF from all images in the output folder
    image_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
    image_files.sort()

    if image_files:
        image_paths = [os.path.join(output_folder, img_file) for img_file in image_files]
        first_image = Image.open(image_paths[0])
        pdf_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.pdf")
        first_image.save(pdf_file_path, save_all=True, append_images=[Image.open(img) for img in image_paths[1:]])
        print(f"All images saved into PDF at {pdf_file_path}")
        return pdf_file_path
    else:
        print("No images were found in the output folder, so no PDF was created.")
        return None

def detect_tables_and_create_pdf_axis(pdf_path, output_folder):
    """
    Detects tables in a PDF using YOLO, extracts the second-to-last table per page, and creates a new PDF.

    Parameters:
        pdf_path (str): Path to the input PDF.
        output_folder (str): Folder to save the output images and final PDF.

    Returns:
        str: Path to the final merged PDF or None if no tables were found.
    """
    # Load YOLO model
    model = YOLO('foduucom/table-detection-and-extraction')

    # Set model parameters
    model.overrides['conf'] = 0.25
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1000

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Buffer size in pixels for each side
    buffer_size = 20

    # Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Process each page
    for page_num, page_image in enumerate(pages, start=1):
        # Convert PIL image to OpenCV format
        page_image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

        # Perform inference
        results = model.predict(page_image_cv)

        # List to store cropped table images
        cropped_images = []

        # Loop through detected boxes and save cropped table images
        for idx, box in enumerate(results[0].boxes):
            score = box.conf[0].item()
            if score > 0.7:
                x_min = max(0, int(box.xyxy[0][0]) - buffer_size)
                y_min = max(0, int(box.xyxy[0][1]) - buffer_size)
                x_max = min(page_image_cv.shape[1], int(box.xyxy[0][2]) + buffer_size)
                y_max = min(page_image_cv.shape[0], int(box.xyxy[0][3]) + buffer_size)

                # Crop the bounding box with buffer
                cropped_img = page_image_cv[y_min:y_max, x_min:x_max]
                cropped_images.append(cropped_img)

        # Save the second-to-last cropped image if available
        if len(cropped_images) > 1:
            second_last_img = cropped_images[-2]
            second_last_img_pil = Image.fromarray(cv2.cvtColor(second_last_img, cv2.COLOR_BGR2RGB))
            second_last_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_{page_num}.png')
            second_last_img_pil.save(second_last_image_path)
            print(f"Saved second-to-last detected table on page {page_num} at {second_last_image_path}")
        else:
            # Save the full page image if no second-to-last table is found
            full_page_image_path = os.path.join(output_folder, f'{os.path.basename(output_folder)}_{page_num}.png')
            page_image.save(full_page_image_path)
            print(f"No second-to-last table detected on page {page_num}. Saved full page image at {full_page_image_path}")

    # Create a PDF from all images in the output folder
    image_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
    image_files.sort()

    if image_files:
        image_paths = [os.path.join(output_folder, img_file) for img_file in image_files]
        first_image = Image.open(image_paths[0])
        pdf_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.pdf")
        first_image.save(pdf_file_path, save_all=True, append_images=[Image.open(img) for img in image_paths[1:]])
        print(f"All images saved into PDF at {pdf_file_path}")
        return pdf_file_path
    else:
        print("No images were found in the output folder, so no PDF was created.")
        return None


# Step 2: Extract tables from images and save to Excel files
def extract_tables_to_files(pdf_file_path, output_folder):
    # Initialize OCR engine
    ocr_engine = PPStructure(table=True, ocr=True, show_log=False, use_gpu=True)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open PDF and convert pages to images
    imgs = []
    with fitz.open(pdf_file_path) as pdf:
        for pg in range(pdf.page_count):
            page = pdf[pg]
            mat = fitz.Matrix(2, 2)
            pm = page.get_pixmap(matrix=mat, alpha=False)

            # Limit image size to prevent enlargement
            if pm.width > 2000 or pm.height > 2000:
                pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

            # Convert pixmap to OpenCV image format
            img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            imgs.append(img)

    # Process each image and save results as individual Excel files
    for index, img in enumerate(imgs):
        print("index_check",index)
        result = ocr_engine(img)

        # Save results with page number in the filename
        page_number = index + 1  # Adjust for 1-based page numbering
        excel_file_path = os.path.join(output_folder, f"page_{page_number}.xlsx")

        # Save OCR result as Excel directly in the output folder
        # save_structure_res(result, output_folder, f"page_{page_number}", index)  # Save without subfolder
        save_structure_res(result, output_folder, f"page_{page_number}", None)

        print(f"Extracted data for page {page_number} saved to {excel_file_path}")

        # Display OCR result structure for debugging
        for line in result:
            line.pop('img', None)  # Remove image data for readability
            print(line, "Good Luck")


""" Final Merge Excel """
def merge_excel_files(folder_path, output_file_name=None):
    """
    Merges all Excel files in the given folder into a single Excel file.
    
    Parameters:
        folder_path (str): The path to the folder containing Excel files.
        output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
    Returns:
        str: Path to the merged Excel file.
    """
    is_first_file = True
    all_data = []
    for root, dirs, files in sorted(os.walk(folder_path)):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_excel(file_path, dtype=str, engine='openpyxl')
                    if len(df.columns) > 3:
                        if not is_first_file:
                            df.columns = all_data[0].columns  
                        all_data.append(df)
                        is_first_file = False
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    merged_data = pd.concat(all_data, ignore_index=True)
    if not output_file_name:
        output_file_name = f"{os.path.basename(folder_path)}.xlsx"
    output_file = os.path.join(folder_path, output_file_name)
    try:
        merged_data.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Merged Excel file saved at: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving merged file: {e}")
        return None


import os
import numpy as np
import pandas as pd

def merge_excel_files_axis(folder_path, output_file_name=None):
    """
    Merges all Excel files in the given folder into a single Excel file, 
    processing specific columns if certain conditions are met.
    
    Parameters:
        folder_path (str): The path to the folder containing Excel files.
        output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
    Returns:
        str: Path to the merged Excel file.
    """
    is_first_file = True
    all_data = []
    column_names = None  # To store column names from the first file

    excluded_header = [
        np.nan, "Period RecoverDate", "Charge Type", "Total(RS).", "Char"
    ]

    for root, dirs, files in sorted(os.walk(folder_path)):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                try:
                    if is_first_file:
                        # Read the first file with headers
                        df = pd.read_excel(file_path, dtype=str, engine='openpyxl')
                        column_names = df.columns  # Store the column names
                        is_first_file = False
                    else:
                        # Read subsequent files without headers
                        df = pd.read_excel(file_path, dtype=str, engine='openpyxl', header=None)
                        
                        # If the file has exactly 5 columns
                        if df.shape[1] == 5:
                            # Check if the first row matches the excluded header
                            first_row = df.iloc[0].tolist()  # Get the first row as a list
                            print(first_row, "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                            if first_row == excluded_header:
                                print(f"Skipping {file} due to matching excluded header.")
                                continue
                            
                            # Process the column at index 4
                            df['New Column'] = None  # Add a new column
                            for i, value in df[4].items():
                                if isinstance(value, str):  # Ensure the value is a string
                                    # Split at the first space
                                    parts = value.split(' ', 1)
                                    if len(parts) > 1:  # Ensure there is a space to split
                                        df.at[i, 4] = parts[0]  # Keep the part before the space in column 4
                                        df.at[i, 'New Column'] = parts[1]  # Move the part after the space to 'New Column'
                        
                        elif df.shape[1] == 6:
                            # Skip processing if there are 6 columns
                            print(f"Skipping processing for {file} as it has 6 columns.")

                        # Assign stored column names to maintain consistency
                        df.columns = column_names

                    all_data.append(df)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if not all_data:
        print("No valid data to merge.")
        return None

    # Concatenate all dataframes
    merged_data = pd.concat(all_data, ignore_index=True)

    # Remove rows where all columns are empty
    merged_data.dropna(how='all', inplace=True)

    # Define output file name if not provided
    if not output_file_name:
        output_file_name = f"{os.path.basename(folder_path)}.xlsx"
    
    output_file = os.path.join(folder_path, output_file_name)
    
    try:
        # Save the merged data back to an Excel file
        merged_data.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Merged Excel file saved at: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving merged file: {e}")
        return None


#### This is Working Function But it will not remove the empty Rows in the excel

# def merge_excel_files_axis(folder_path, output_file_name=None):
#     """
#     Merges all Excel files in the given folder into a single Excel file, 
#     processing specific columns if certain conditions are met.
    
#     Parameters:
#         folder_path (str): The path to the folder containing Excel files.
#         output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
#     Returns:
#         str: Path to the merged Excel file.
#     """
#     is_first_file = True
#     all_data = []
#     column_names = None  # To store column names from the first file

#     excluded_header = [
#         np.nan, "Period RecoverDate", "Charge Type", "Total(RS).", "Char"
#     ]

#     for root, dirs, files in sorted(os.walk(folder_path)):
#         for file in files:
#             if file.endswith('.xlsx') or file.endswith('.xls'):
#                 file_path = os.path.join(root, file)
#                 try:
#                     if is_first_file:
#                         # Read the first file with headers
#                         df = pd.read_excel(file_path, dtype=str, engine='openpyxl')
#                         column_names = df.columns  # Store the column names
#                         is_first_file = False
#                     else:
#                         # Read subsequent files without headers
#                         df = pd.read_excel(file_path, dtype=str, engine='openpyxl', header=None)
                        
#                         # If the file has exactly 5 columns
#                         if df.shape[1] == 5:
#                             # Check if the first row matches the excluded header
#                             first_row = df.iloc[0].tolist()  # Get the first row as a list
#                             print(first_row,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
#                             if first_row == excluded_header:
#                                 print(f"Skipping {file} due to matching excluded header.")
#                                 continue
                            
#                             # Process the column at index 4
#                             df['New Column'] = None  # Add a new column
#                             for i, value in df[4].items():
#                                 if isinstance(value, str):  # Ensure the value is a string
#                                     # Split at the first space
#                                     parts = value.split(' ', 1)
#                                     if len(parts) > 1:  # Ensure there is a space to split
#                                         df.at[i, 4] = parts[0]  # Keep the part before the space in column 4
#                                         df.at[i, 'New Column'] = parts[1]  # Move the part after the space to 'New Column'
                        
#                         elif df.shape[1] == 6:
#                             # Skip processing if there are 6 columns
#                             print(f"Skipping processing for {file} as it has 6 columns.")

#                         # Assign stored column names to maintain consistency
#                         df.columns = column_names

#                     all_data.append(df)
#                 except Exception as e:
#                     print(f"Error reading {file_path}: {e}")

#     if not all_data:
#         print("No valid data to merge.")
#         return None

#     # Concatenate all dataframes
#     merged_data = pd.concat(all_data, ignore_index=True)
    
#     # Define output file name if not provided
#     if not output_file_name:
#         output_file_name = f"{os.path.basename(folder_path)}.xlsx"
    
#     output_file = os.path.join(folder_path, output_file_name)
    
#     try:
#         # Save the merged data back to an Excel file
#         merged_data.to_excel(output_file, index=False, engine='openpyxl')
#         print(f"Merged Excel file saved at: {output_file}")
#         return output_file
#     except Exception as e:
#         print(f"Error saving merged file: {e}")
#         return None

    
def process_excel_file(file_path):
    """
    Processes an Excel file by performing the specified steps: 
    - Insert an empty column between the 3rd and 4th columns.
    - Create a new column for conditions.
    - Modify and clean columns based on specific conditions.
    
    Parameters:
        file_path (str): The path to the Excel file to be processed.
        
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Read the Excel file without headers, treating all rows as data
    df = pd.read_excel(file_path, header=None)

    # Insert an empty column between the 3rd and 4th columns (index 3 and 4)
    df.insert(4, ' ', None)

    # Insert a new column for the condition (at the end of the DataFrame)
    df['New Column'] = None

    # Loop through the DataFrame rows
    for index, row in df.iterrows():
        # Check if the value in the 2nd column (index 1) is non-NaN
        if pd.notna(row[1]):
            # Prepend the non-NaN value to the value in the 3rd column (index 2) with a space between them
            df.at[index, 2] = str(row[1]) + str(row[2])
            # Empty the value in the 2nd column (index 1)
            df.at[index, 1] = None  # Or use np.nan if you prefer

        # Use regex to find decimal numbers in the 3rd column (index 2)
        if pd.notna(row[2]) and isinstance(row[2], str):
            # Find decimal numbers in the 3rd column (index 2)
            match = re.search(r'\d+\.\d+', row[2])  # Match decimal numbers
            if match:
                # Copy the decimal number to the 4th column (index 3)
                df.at[index, 3] = match.group(0)  # Extract the matched decimal number

        # Compare the value in the last column with the previous row's value
        if index > 0:  # Ensure there's a previous row to compare with
            previous_balance = df.iloc[index - 1, -2]  # Second-to-last column of the previous row
            current_balance = df.iloc[index, -2]      # Second-to-last column of the current row

            # Ensure the values are strings, clean them, and convert to float
            if pd.notna(previous_balance) and pd.notna(current_balance):
                previous_balance = float(str(previous_balance).replace(',', ''))
                current_balance = float(str(current_balance).replace(',', ''))
                
                # Check if the current balance is greater than the previous balance
                if current_balance > previous_balance:
                    # Move the data from the 4th column to the new column
                    df.at[index, 'New Column'] = df.at[index, 3]
                    
                    # Remove the value from the 4th column (index 3) after moving to New Column
                    df.at[index, 3] = None

    # Remove the 5th column (currently index 4)
    df.drop(df.columns[4], axis=1, inplace=True)

    # Move the 'New Column' to the 5th column (index 4)
    df.insert(4, 'New Column', df.pop('New Column'))

    # Remove column names by setting the column labels to None
    df.columns = [None] * df.shape[1]

    return df


def merge_excel_files_andhra(folder_path, output_file_name=None):
    """
    Merges all Excel files in the given folder into a single Excel file, applying processing steps
    to each file except the first one.
    
    Parameters:
        folder_path (str): The path to the folder containing Excel files.
        output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
    Returns:
        str: Path to the merged Excel file.
    """
    is_first_file = True
    all_data = []
    
    # Walk through the folder and process each Excel file
    for root, dirs, files in sorted(os.walk(folder_path)):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                
                try:
                    # Read the first file without any processing
                    if is_first_file:
                        df = pd.read_excel(file_path, dtype=str, engine='openpyxl')
                        is_first_file = False  # Set the flag to False after processing the first file
                    else:
                        # Process subsequent files
                        df = process_excel_file(file_path)
                    
                    # Adjust column names of subsequent files to match the first file's columns
                    if len(all_data) > 0:
                        df.columns = all_data[0].columns  # Align columns with the first file's columns
                    
                    # Append the DataFrame to the list
                    all_data.append(df)
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Concatenate all the data into a single DataFrame
    merged_data = pd.concat(all_data, ignore_index=True)
    
    # Define the output file name if not provided
    if not output_file_name:
        output_file_name = f"{os.path.basename(folder_path)}.xlsx"
        
    # Construct the output file path
    output_file = os.path.join(folder_path, output_file_name)
    
    try:
        # Save the merged DataFrame to the output file
        merged_data.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Merged Excel file saved at: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving merged file: {e}")
        return None

# Main function to coordinate steps
def main(pdf_path):
    """ Step:1 """
    pdf_text = paddle_ocr(pdf_path)
    bank_name = identify_bank(pdf_text)
    account_number = extract_account_number(pdf_text)
    print(f"The bank statement is for: {bank_name}")
    print(f"Extracted account number: {account_number}")

    """ Step:2 """
    output_folder = f'/media/nesru/karna/HYD/{os.path.splitext(os.path.basename(pdf_path))[0]}'
    if bank_name in ["Bandhan Bank", "Union Bank", "State Bank of India", "Andhra Bank", "Bank not identified"]:
        pdf_file_path = detect_tables_and_create_pdf(pdf_path, output_folder)
    elif bank_name in ["Canara Bank"]:
        pdf_file_path = detect_tables_and_create_pdf_canara(pdf_path, output_folder)
    elif bank_name in ["Axis Bank"]:
        pdf_file_path = detect_tables_and_create_pdf_axis(pdf_path, output_folder)
    elif bank_name in ["HDFC Bank"]:
        pdf_file_path = detect_tables_and_create_pdf_hdfc(pdf_path, output_folder)
    else:
        print("Bank not supported.")
        return

    print(f"PDF processing completed. Output file: {pdf_file_path}")

    
    if pdf_file_path:
        if bank_name in ["HDFC Bank","Bandhan Bank","Canara Bank","Union Bank","Bank not identified"]:
            extract_tables_to_files(pdf_file_path, output_folder)
            merge_excel_files(output_folder)
        elif bank_name in ["Axis Bank"]:
            extract_tables_to_files(pdf_file_path, output_folder)
            merge_excel_files_axis(output_folder)
        elif bank_name in ["Andhra Bank"]:
            extract_tables_to_files(pdf_file_path, output_folder)
            merge_excel_files_andhra(output_folder)



# Run the main function with the specified PDF path
if __name__ == "__main__":
    pdf_path = '/media/nesru/karna/HYD/pdfplumber/sample_pdf/statement-bandhan-bank_compress.pdf'  # BOB - Working
    # pdf_path = '/media/nesru/karna/HYD/pdfplumber/pdf-sample/andhra-bank-statement_compress.pdf'     # AB - Working
    # pdf_path = '/home/player/Bank Statements/indusindaccountstatement-xxxxxxxx8783-6-12-2023-134949_compress.pdf'  # indusind Bank - Working
    # pdf_path = '/media/nesru/karna/HYD/pdfplumber/sample_pdf/axis-bank-statement-2024_compress.pdf'    #Axis Bank - Notworking #Added new function 60% working
    # pdf_path = '/media/nesru/karna/HYD/pdfplumber/sample_pdf/canara-bank-statement_compress.pdf'  # Canara Bank - Notworking  (WORKING 95%)
    # pdf_path = '/home/player/Bank Statements/union-bank-of-india-1-account-statement-pdf_compress.pdf'
    # pdf_path = '/media/player/karna1/HYD/table-extraction-oct30/4pg.pdf'  # Specify your PDF path here
    # pdf_path = '/home/player/Bank Statements/SBI4.pdf'
    # pdf_path = '/home/player/out_andhra_1.pdf'
    # pdf_path = '/media/nesru/karna/HYD/pdfplumber/sample_pdf/statement-of-account-for-mr-anup-dubey-from-june-1-2018-to-october-10-2018-showing-deposits-withdrawals.pdf' #HDFC
    # pdf_path = "/media/nesru/karna/HYD/pdfplumber/sample_pdf/andhra-bank-statement_compress.pdf"
    # pdf_path = "HDFC/statement-of-account-for-mr-anup-dubey-from-june-1-2018-to-october-10-2018-showing-deposits-withdrawals_page-0001.pdf"
    # pdf_path = "/media/nesru/karna/HYD/pdfplumber/pdf-sample/union-bank-of-india-1-account-statement-pdf_compress.pdf"
    main(pdf_path)