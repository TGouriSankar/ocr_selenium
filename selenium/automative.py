# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# import time

# # Set up your WebDriver (use the path to your WebDriver)
# driver = webdriver.Firefox()

# # Open the website
# driver.get('https://yuyu4dok.com/')

# # Wait for the page to load
# time.sleep(10)

# # Click on the registration button using the provided XPath
# register_button = driver.find_element(By.XPATH, '/html/body/div[3]/header/div/div[4]/div[1]/form/button[2]')
# register_button.click()

# # Wait for the registration page to load
# time.sleep(3)

# # Fill out the registration form (replace XPaths and values with actual ones from the website)
# name_field = driver.find_element(By.XPATH, 'xpath_for_name_field')
# name_field.send_keys('Your Name')

# password_field = driver.find_element(By.XPATH, 'xpath_for_password_field')
# password_field.send_keys('YourPassword')

# confirm_password_field = driver.find_element(By.XPATH, 'xpath_for_confirm_password_field')
# confirm_password_field.send_keys('YourPassword')

# # Add other form fields here in the same way

# # Submit the form
# submit_button = driver.find_element(By.XPATH, 'xpath_for_submit_button')
# submit_button.click()

# # Wait to observe the result (or you can add assertions here)
# time.sleep(5)

# # Close the browser
# driver.quit()



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up your WebDriver for Firefox
driver = webdriver.Firefox()

# Open the website
# driver.get('https://yuyu4dok.com/')
driver.get('https://adaokada.site/')

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
    register_button = driver.find_element(By.XPATH, '/html/body/div[3]/header/div/div[4]/div[1]/form/button[2]')
    register_button.click()
    print("Clicked on the registration button.")
except Exception as e:
    print("Failed to find or click the registration button:", str(e))

# Wait for the registration page to load
time.sleep(3)

# Fill out the registration form (replace XPaths and values with actual ones from the website)
try:
    # Fill Username
    # username_field = driver.find_element(By.XPATH, '//*[@id="reg_username"]')
    # username_field.click()
    # username_field.send_keys('kasperboy')

    username_field = driver.find_element(By.ID, 'reg_username')
    driver.execute_script("arguments[0].scrollIntoView();", username_field)
    username_field.click()
    username_field.send_keys('kasperboy')

    print("Form filled successfully.")
except Exception as e:
    print("Failed to fill the registration form:", str(e))

# Submit the form
# try:
#     submit_button = driver.find_element(By.XPATH, '//*[@id="buttonRegister"]')  
#     submit_button.click()
#     print("Form submitted.")
# except Exception as e:
#     print("Failed to submit the form:", str(e))

# Wait to observe the result (or you can add assertions here)
time.sleep(5)

# Close the browser
driver.quit()
