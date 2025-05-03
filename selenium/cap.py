# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from PIL import Image
# import time

# # Initialize Selenium and open the page
# driver = webdriver.Firefox()
# driver.get('https://qqmegahxl.com/')

# # Wait for the page and CAPTCHA to load
# time.sleep(5)

# # Handle popup/modal if it appears (e.g., pressing ESC or closing button)
# try:
#     ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#     print("Popup closed using ESC key.")
#     time.sleep(2)
# except Exception as e:
#     print("No popup detected or failed to close:", str(e))

# try:
#     register_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/form/a')
#     register_button.click()
#     print("Clicked on the registration button.")
# except Exception as e:
#     print("Failed to find or click the registration button:", str(e))

# # Wait for the registration page to load
# time.sleep(3)

# # Locate the CAPTCHA image element
# captcha_element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[6]/td/div/img[1]')
# location = captcha_element.location
# size = captcha_element.size

# # Take a full screenshot and crop the CAPTCHA area
# captcha_field = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[3]/td/div/input')
# driver.execute_script("arguments[0].scrollIntoView();", captcha_field)
# driver.save_screenshot("full_page.png")

# # Adjust location offsets (if needed) for better cropping accuracy
# captcha_image = Image.open("full_page.png")
# # left = location['x']
# # top = location['y']
# # right = location['x'] + size['width']
# # bottom = location['y'] + size['height']

# # Adjusted cropping
# left = location['x'] - 50  # Slightly shift to the left for better capture
# top = location['y'] - 50  # Slightly move up for better capture
# right = location['x'] + size['width'] + 5  # Slightly expand to the right
# bottom = location['y'] + size['height'] + 500  # Slightly expand downward


# captcha_image = captcha_image.crop((left, top, right, bottom))
# captcha_image.save("captcha.png")

# print("Captcha image saved as 'captcha.png'")



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import keras_ocr
import time

# Initialize Selenium and open the page
driver = webdriver.Firefox()
driver.get('https://qqmegahxl.com/')

# Wait for the page and CAPTCHA to load
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

# Locate the CAPTCHA image element
captcha_element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[6]/td/div/img[1]')
location = captcha_element.location
size = captcha_element.size

# Take a full screenshot and crop the CAPTCHA area

captcha_field = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[3]/td/div/input')
driver.execute_script("arguments[0].scrollIntoView();", captcha_field)
driver.save_screenshot("full_page.png")
captcha_image = Image.open("full_page.png")
# captcha_image = captcha_image.crop((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))
# captcha_image.save("captcha.png")

# Initialize KerasOCR pipeline
pipeline = keras_ocr.pipeline.Pipeline()
captcha_text = pipeline.recognize([captcha_image])[0][0][0]  # Assuming single text result
print(captcha_text)

# Fill in the CAPTCHA text in the input box
# captcha_input = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/div[4]/table/tbody/tr[6]/td/div/input')
# captcha_input.send_keys(captcha_text)

# Close the browser after processing
time.sleep(2)
driver.quit()

