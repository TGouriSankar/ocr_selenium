

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from paddleocr import PaddleOCR
import re

# We are using FireFox WebDriver
driver = webdriver.Firefox()

# give website link it will Open the website
driver.get('https://qqmegahxl.com/')
# driver.get('https://adaokada.site/')

# Wait for the page to load completely
time.sleep(5)

# Handle popup/modal if it appears (e.g., pressing ESC or closing button)
try:
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("Popup closed using ESC key.")
    time.sleep(2)
except Exception as e:
    print("No popup detected or failed to close:", str(e))

try:
    register_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/form/a')
    register_button.click()
    print("Clicked on the registration button.")
except Exception as e:
    print("Failed to find or click the registration button:", str(e))

# Wait for the registration page to load
time.sleep(3)

# Fill out the registration form
try:
    """Scroll the username field into view """
    # username_field = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[2]/table/tbody/tr[1]/td/div/input')
    # driver.execute_script("arguments[0].scrollIntoView();", username_field)
    username_field = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[2]/table/tbody/tr[1]/td/div/input')
    username_field.click()
    username_field.send_keys('kasperboy'+ Keys.RETURN)

    user_email = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[2]/table/tbody/tr[2]/td/div/input')
    user_email.click()
    user_email.send_keys('dummy123@gmail.com')

    user_phone_number = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[2]/table/tbody/tr[4]/td/div/input[2]')
    user_phone_number.click()
    user_phone_number.send_keys('7873277196')

    username_field = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[3]/table/tbody/tr[1]/td/div/input')
    username_field.click()
    username_field.send_keys('kasperboy'+ Keys.RETURN)

    user_password = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[3]/table/tbody/tr[2]/td/div/input')
    user_password.click()
    user_password.send_keys('Password@123')

    user_confirm_password = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[3]/table/tbody/tr[3]/td/div/input')
    user_confirm_password.click()
    user_confirm_password.send_keys('Password@123')


    user_bank = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[1]/td/select')
    user_bank.click()
    user_bank.send_keys('BRI')

    user_name_per_account = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[2]/td/div/input')
    user_name_per_account.click()
    user_name_per_account.send_keys('kasperboy')

    user_Account_number = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[3]/td/div/input')
    user_Account_number.click()
    user_Account_number.send_keys('354625678912340')

    # Locate the CAPTCHA image element
    captcha_element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[6]/td/div/img[1]')
    location = captcha_element.location
    size = captcha_element.size

    # Take a full screenshot and crop the CAPTCHA area

    captcha_field = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[3]/td/div/input')
    driver.execute_script("arguments[0].scrollIntoView();", captcha_field)
    driver.save_screenshot("full_page.png")
    captcha_image = Image.open("full_page.png")

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
            finaltext += text
        # Keep only digits
        finaltext = re.sub(r'\D', '', finaltext)
        return finaltext


    img = 'cropped_image.png'
    captcha_code = ocr_with_paddle(img)
    print(captcha_code)

    # upload the CAPTCHA code element
    captcha_code = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[6]/td/div/input')
    captcha_code.click()
    captcha_code.send_keys(captcha_code)

    print("Form filled successfully.")
except Exception as e:
    print("Failed to fill the registration form:", str(e))


time.sleep(10)
# Submit the form
try:
    submit_button = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[7]/button')
    # driver.execute_script("arguments[0].scrollIntoView();", submit_button)  
    submit_button.click()
    print("Form submitted.")
except Exception as e:
    print("Failed to submit the form:", str(e))

# wait and Close the browser
time.sleep(5)
driver.quit()

