from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# We are using FireFox WebDriver
driver = webdriver.Firefox()

# give website link it will Open the website
driver.get('https://gamegacor368.dev/')
# driver.get('https://adaokada.site/')

# Wait for the page to load completely
time.sleep(5)

# Handle popup/modal if it appears (e.g., pressing ESC or closing button)
# try:
#     webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#     print("Popup closed using ESC key.")
#     time.sleep(2)
# except Exception as e:
#     print("No popup detected or failed to close:", str(e))

try:
    register_button = driver.find_element(By.XPATH, '/html/body/div[3]/header/div/div[4]/div[1]/form/button[2]')
    register_button.click()
    print("Clicked on the registration button.")
except Exception as e:
    print("Failed to find or click the registration button:", str(e))

# Wait for the registration page to load
time.sleep(3)

# Fill out the registration form
try:
    """Scroll the username field into view """
    username_field = driver.find_element(By.XPATH, '//*[@id="input-username"]')
    driver.execute_script("arguments[0].scrollIntoView();", username_field)
    username_field = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[1]/input')
    username_field.click()
    username_field.send_keys('kasperboy'+ Keys.RETURN)


    user_password = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[2]/div[1]/input')
    user_password.click()
    user_password.send_keys('Password@123')

    user_confirm_password = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[2]/div[2]/input')
    user_confirm_password.click()
    user_confirm_password.send_keys('Password@123')


    user_email = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[2]/div[3]/input')
    user_email.click()
    user_email.send_keys('dummy123@gmail.com')

    user_phone_number = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[2]/div[4]/input')
    user_phone_number.click()
    user_phone_number.send_keys('7873277196')

    user_bank = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[3]/div[1]/select')
    user_bank.click()
    user_bank.send_keys('BRI')

    user_Account_number = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[3]/div[2]/input')
    user_Account_number.click()
    user_Account_number.send_keys('354625678912340')

    user_name_per_account = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/div[3]/div[3]/input')
    user_name_per_account.click()
    user_name_per_account.send_keys('kasperboy')

    print("Form filled successfully.")
except Exception as e:
    print("Failed to fill the registration form:", str(e))

# Submit the form
try:
    submit_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div/div/form/input[1]')
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)  
    submit_button.click()
    print("Form submitted.")
except Exception as e:
    print("Failed to submit the form:", str(e))

# wait and Close the browser
time.sleep(5)
driver.quit()

