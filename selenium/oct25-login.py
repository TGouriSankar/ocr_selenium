from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# We are using FireFox WebDriver
driver = webdriver.Firefox()

# Open the website
# driver.get('https://pstoto99tiga.com/')
driver.get('https://pafigacor168.club/')

# Wait for the page to load completely
time.sleep(5)

# Handle popup/modal if it appears (e.g., pressing ESC or closing button)
try:
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("Popup closed using ESC key.")
    time.sleep(2)
except Exception as e:
    print("No popup detected or failed to close:", str(e))

# Fill in the login form
try:
    login_name = driver.find_element(By.XPATH, '/html/body/div[3]/header/div/div[4]/div[1]/form/div[2]/input')
    login_name.click()
    login_name.send_keys('kasperboy')

    login_password = driver.find_element(By.XPATH, '/html/body/div[3]/header/div/div[4]/div[1]/form/div[4]/input')
    login_password.click()
    login_password.send_keys('Password@123')

    print("filled login username and password.")
except Exception as e:
    print("Failed to find or click the registration button:", str(e))

# Attempt to login
time.sleep(3)
try:
    login_button = driver.find_element(By.XPATH, '/html/body/div[3]/header/div/div[4]/div[1]/form/button[1]')
    driver.execute_script("arguments[0].scrollIntoView();", login_button)
    login_button.click()
    print("Click on login button.")
except Exception as e:
    print("Failed to submit the form:", str(e))

# Wait for login action to process
time.sleep(5)

# Check if login was successful
try:
    # Look for an element only present after successful login
    driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul[2]/li[2]/a')
    print("Login successful: Account exists.")
except:
    print("Login failed: Account does not exist.")

# Close the browser
driver.quit()
