username = "mubaihua515"
password = "Hmb20020515"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("https://uclasurveys.co1.qualtrics.com/jfe/form/SV_aeH9BFhYVjkYTsO")
print(driver.title)

#ucla logon
usrname = driver.find_element(By.ID, "logon")
usrname.send_keys(username)
passwd = driver.find_element(By.ID, "pass")
passwd.send_keys(password)
sign_in_but = driver.find_element(By.CLASS_NAME, "primary-button")
sign_in_but.click()

#duo mobile
try:
    duo_frame = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID,"duo_iframe"))
    )
    driver.switch_to.frame(duo_frame)
    enter_a_psscode_button = driver.find_element(By.ID, "passcode")
    enter_a_psscode_button.click()
    enter_passcode_field = driver.find_element(By.NAME, "passcode")
    enter_passcode_field.send_keys("123456")
except:
    driver.quit()
    print("NOT FOUND")
    exit()