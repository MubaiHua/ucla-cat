import duo_activate
import duo_gen
import atom
import os.path
import time

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
        except:
            print("Please enter a valid link")

    print("Please enter your UCLA Logon ID and password")
    id = input("Logon ID: ")
    password = input("Password: ")

    print("Please enter the path of your Chrome Web Driver")
    path = input("path: ")

    try:
        f = open("user_info.txt", "x")
        f.write(id+"\n")
        f.write(password+"\n")
        f.write(path+"\n")
        f.close()

    except:
        print("Please delete the file user_info.txt and redo the set up process")

    duo_activate.activate(host,code)
    time.sleep(3)

print("Obtain the one-time passcode...")
passcode = duo_gen.gen()

print("Execute the script to fill the survey...")
f = open("user_info.txt", "r")
user_id = f.readline().strip()
user_password = f.readline().strip()
user_path = f.readline().strip()
f.close()
try:
    atom.auto(user_id,user_password,passcode,user_path)
    print("Script execution success")
except:
    print("Script execution failed")