from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('http://www.yahoo.com')
assert 'Yahoo' in browser.title

elem = browser.find_element(By.NAME, 'p')  # Find the search box
elem.send_keys('seleniumhq' + Keys.RETURN)

browser.quit()



""" 
    <img name="psFMCQimage" style="display: block; border: 0px;" width="120" height="120" alt="Live chat online" 
    title="Live chat online" src="https://image.providesupport.com/image/1b8mhr0urq5uy1bzmuv7t6z0xv/online-994466233.gif">
"""