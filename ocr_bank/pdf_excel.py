import os
from pdf2image import convert_from_path
from ultralyticsplus import YOLO
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from paddleocr import PPStructure, save_structure_res

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



# Main function to coordinate steps
def main(pdf_path):
    output_folder = f'/media/nesru/karna/HYD/{os.path.splitext(os.path.basename(pdf_path))[0]}'
    pdf_file_path = detect_tables_and_create_pdf(pdf_path, output_folder)
    
    if pdf_file_path:
        extract_tables_to_files(pdf_file_path, output_folder)


# Run the main function with the specified PDF path
if __name__ == "__main__":
    pdf_path = '/home/nesru/Documents/Bk state/1/rajul post search/Priyank Mehta/F.Y.2015-16.pdf'  # Specify your PDF path here
    main(pdf_path)


