from PIL import Image
from paddleocr import PaddleOCR

# Initialize PaddleOCR
image_path = '/media/player/karna1/HYD/selenium/full_page.png' 
image = Image.open(image_path)

# Get the dimensions of the image
width, height = image.size

# Calculate the crop coordinates
left = int(width * 0.4)           # Exclude left 30%
top = int(height * 0.1)           # Exclude top 10%
right = int(width * 0.6)          # Exclude right 40% (keep 60%)

# Calculate the new bottom coordinate to keep only 20% of the height
bottom = top + int(height * 0.08)  # Keep the height from top to 20% down

# Crop the image
cropped_image = image.crop((left, top, right, bottom))

# Save or display the cropped image
cropped_image.save('cropped_image.png')  # Save the cropped image


def ocr_with_paddle(img):
    finaltext = ''
    ocr = PaddleOCR(lang='en', use_angle_cls=True)
    # img_path = 'exp.jpeg'
    result = ocr.ocr(img)
    
    for i in range(len(result[0])):
        text = result[0][i][1][0]
        finaltext += ' '+ text
    return print(finaltext)

img = 'cropped_image.png'
ocr_with_paddle(img)
