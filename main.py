import os.path
import time
import pyotp
import requests
import base64
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

global ERR_CODE
global ERR_MSG
ERR_CODE = 'unknown_error'
ERR_MSG = '\nPlease run the program again or contact the developer team with your error (code: %s)' % ERR_CODE

def main():
    print("\nWelcome to UCLA CAT (COVID-symptom-survey Auto-filling Tool)\n")
    
    user_file_exist = os.path.exists("user_info.txt")
    hotp_file_exist = os.path.exists("duotoken.hotp")
    
    fill_success = False
    if not user_file_exist or not hotp_file_exist:
        register_success = register_user()
        
        if not register_success:
            ERR_CODE = 'user_registration_failed'
            print(ERR_MSG)
        else:
            fill_success = auto_fill_survey()
            
    else:
        fill_success = auto_fill_survey()
        
    if fill_success:
        print("\nSurvey auto-filling success! Enjoy your day :)\n")
        exit()
    else:
        exit()
    
                
def auto_fill_survey():
    print("Obtaining one-time passcodes...")
    passcode = gen()

    print("Auto-filling the survey...")
    
    f = open("user_info.txt", "r")
    user_id = f.readline().strip()
    user_password = f.readline().strip()
    user_path = f.readline().strip()
    f.close()
    
    try:
        auto(user_id,user_password,passcode,user_path)
        return True
        
    except:
        print('Failed to auto-fill the survey')
        ERR_CODE = 'survey_filling_failed'
        print(ERR_MSG)
        return False

def register_user():
    print("Registering a new user...\n")
    
    # input duo activation link
    print("Please obtain a Duo Mobile one-time activation link by following the instruction on https://github.com/MubaiHua/Symptom-Monitoring-System-Auto")
    while(True):
        try:
            link = input("Paste your link here: ")
            host = "api" + link[link.index("-"):link.index("com")+3]
            code = link[link.index("/", 36, 60)+1:]
            
            activate(host,code)
            break
        except:
            print("Please enter a valid link\n")

    # input logon id and password
    print("\nPlease enter your UCLA Logon ID and password (stored on your computer - we can't see it)")
    while True:
        id = input("Logon ID: ")
        password = input("Password: ")
        path = ""
    
        # verify duo login
        print("\nVerifying UCLA Logon sign in...")
        auth_success = False
        try:
            s=Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s)
            driver.get("https://uclasurveys.co1.qualtrics.com/jfe/form/SV_aeH9BFhYVjkYTsO")
            
            #ucla logon
            usrname = driver.find_element(By.ID, "logon")
            usrname.send_keys(id)
            passwd = driver.find_element(By.ID, "pass")
            passwd.send_keys(password)
            sign_in_but = driver.find_element(By.CLASS_NAME, "primary-button")
            sign_in_but.click()
        
            duo_frame = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID,"duo_iframe"))
            )
            
            auth_success = True
            
        except:
            driver.quit()
            print("\nFailed to sign in UCLA Logon...Please make sure your logon ID and password are correct")
            print("\nPlease re-enter your UCLA Logon ID and password")
        
        if auth_success:
            # write user information
            try:
                f = open("user_info.txt", "w")
                f.write(id+"\n")
                f.write(password+"\n")
                f.write(path+"\n")
                f.close()

            except:
                print("Failed to write user information")
                return False
            
            driver.quit()
            break  
    
    time.sleep(3)
    return True


#The QR Code is in the format: XXXXXXXXXX-YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
#copy 'XXXXXXXXXX' to "code"
#use https://www.base64decode.org/ to decode YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY and put it in 'host'
#decoded format should be in the format: api-XXXXX.duosecurity.com
def activate(host, code):
  url = 'https://{host}/push/v2/activation/{code}?customer_protocol=1'.format(host=host, code=code)
  headers = {'User-Agent': 'okhttp/2.7.5'}
  data = {'jailbroken': 'false',
          'architecture': 'arm64',
          'region': 'US',
          'app_id': 'com.duosecurity.duomobile',
          'full_disk_encryption': 'true',
          'passcode_status': 'true',
          'platform': 'Android',
          'app_version': '3.49.0',
          'app_build_number': '323001',
          'version': '11',
          'manufacturer': 'unknown',
          'language': 'en',
          'model': 'Pixel 3a',
          'security_patch_level': '2021-02-01'}

  r = requests.post(url, headers=headers, data=data)
  response = json.loads(r.text)

  try:
    secret = base64.b32encode(response['response']['hotp_secret'].encode())
  except KeyError:
    print(response)
    sys.exit(1)

#   print("secret", secret)

#   print("10 Next OneTime Passwords!")
  # Generate 10 Otps!
#   hotp = pyotp.HOTP(secret)
#   for _ in range(10):
#       print(hotp.at(_))

  with open('duotoken.hotp', 'w') as file:
      file.write(secret.decode() + "\n")
      file.write("0")

  with open('response.json', 'w') as resp:
      resp.write(r.text)


def auto(username, password, code, PATH):
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get("https://uclasurveys.co1.qualtrics.com/jfe/form/SV_aeH9BFhYVjkYTsO")

    #ucla logon
    usrname = driver.find_element(By.ID, "logon")
    usrname.send_keys(username)
    passwd = driver.find_element(By.ID, "pass")
    passwd.send_keys(password)
    sign_in_but = driver.find_element(By.CLASS_NAME, "primary-button")
    sign_in_but.click()
    print("UCLA Logon Sign-in Successful")

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
        # print("Survey filled successfully!")
        driver.quit()
    except:
        print("Fail to fill the survey")
        driver.quit()


def gen():

    if len(sys.argv) == 2:
        file = sys.argv[1]
    else:
        file = "duotoken.hotp"

    f = open(file, "r+")
    secret = f.readline()[0:-1]
    offset = f.tell()
    count = int(f.readline())

    # print("secret", secret)
    # print("count", count)

    hotp = pyotp.HOTP(secret)
    # print("Code:", hotp.at(count))

    f.seek(offset)
    f.write(str(count + 1))
    f.close()

    return(hotp.at(count))


if __name__ == '__main__':
    main()