#PATH = 'C:\Program Files (x86)\chromedriver.exe'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def auto(username, password, code, PATH):
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
    print("UCLA Logon Successful")

    #duo mobile
    try:
        duo_frame = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,"duo_iframe"))
        )
        driver.switch_to.frame(duo_frame)
        enter_a_psscode_button = driver.find_element(By.ID, "passcode")
        enter_a_psscode_button.click()
        enter_passcode_field = driver.find_element(By.NAME, "passcode")
        enter_passcode_field.send_keys(code)
        enter_a_psscode_button.click()
        driver.switch_to.default_content()
        print("Duo Mobile 2FA Authentication Successful")
    except:
        driver.quit()
        print("Duo Authentication Failed")

    # fill the survey
    try:
    #page 1
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        next_button.click()

        #page 2
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        next_button.click()

        #page 3
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        no_button = driver.find_element(By.ID, "QID215-2-label")
        no_button.click()
        next_button.click()

        #page 4
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        yes_button = driver.find_element(By.ID, "QID207-4-label")
        yes_button.click()
        next_button.click()

        #page 5
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        no_button = driver.find_element(By.ID, "QID2-1-label")
        no_button.click()
        next_button.click()

        #page 6
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        no_button = driver.find_element(By.ID, "QID12-2-label")
        no_button.click()
        next_button.click()

        #page 7
        next_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, "NextButton"))
        )
        no_button = driver.find_element(By.ID, "QID289-2-label")
        no_button.click()
        next_button.click()

        #page 8 for user without test result
        page = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "Questions"))
        )
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.ID, "EndOfSurvey"))
            )
        except: 
            next_button = WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID, "NextButton"))
            )
            yes_button = driver.find_element(By.ID, "QID293-1-label")
            yes_button.click()
            next_button.click()
        print("Survey filled successfully!")
        driver.quit()
    except:
        print("Fail to fill the survey")
        driver.quit()
