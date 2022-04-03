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

def main():
    user_file_exist = os.path.exists("user_info.txt")
    hotp_file_exist = os.path.exists("duotoken.hotp")

    if(user_file_exist== False or hotp_file_exist == False):
        print("Please follow the instruction and obtain the one-time activation link")
        while(True):
            try:
                link = input("Please paste your link here: ")
                host = "api" + link[link.index("-"):link.index("com")+3]
                code = link[link.index("/", 36, 60)+1:]
                break
            except KeyboardInterrupt:
                exit()
            except:
                print("Please enter a valid link")

        print("Please enter your UCLA Logon ID and password")
        id = input("Logon ID: ")
        password = input("Password: ")
        path = ""
        try:
            path = driverInstall()

        except:
            print("Fail to install chrome web driver")

        try:
            f = open("user_info.txt", "x")
            f.write(id+"\n")
            f.write(password+"\n")
            f.write(path+"\n")
            f.close()

        except:
            print("Please delete the file user_info.txt and redo the set up process")

        activate(host,code)
        time.sleep(3)

    print("Obtain the one-time passcode...")
    passcode = gen()

    print("Execute the script to fill the survey...")
    f = open("user_info.txt", "r")
    user_id = f.readline().strip()
    user_password = f.readline().strip()
    user_path = f.readline().strip()
    f.close()
    try:
        auto(user_id,user_password,passcode,user_path)
        print("Script execution success")
    except:
        print("Script execution failed")



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

  print("secret", secret)

  print("10 Next OneTime Passwords!")
  # Generate 10 Otps!
  hotp = pyotp.HOTP(secret)
  for _ in range(10):
      print(hotp.at(_))

  with open('duotoken.hotp', 'w') as file:
      file.write(secret.decode() + "\n")
      file.write("0")

  with open('response.json', 'w') as resp:
      resp.write(r.text)


def auto(username, password, code, PATH):
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
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

def driverInstall():
    path = chromedriver_autoinstaller.install(True)  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
    return path

if __name__ == '__main__':
    main()