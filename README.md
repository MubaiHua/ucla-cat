## Symptom Monitoring System Auto Fill Script

## To users of this script
This script is only for a quick and easy way to fill the Symptom Monitoring Survey, please do not use it when you have any symptom of COVID-19
Please follow the UCLA guideline for COVID-19, and stay safe Bruins

## To obtain the activation link, please refer to activation.pdf

## First Time User
To Use this script, you need to have a Chrome browser

Open main.exe to start the script

Please enter the activation link you obtained, and then enter your UCLA Logon ID and password

The script will automatically install the Chrome Web Driver for you, and if it doesn't, please check update your Chrome's version

The info about Duo 2FA will be stored in duotoken.hotp, and your UCLA Logon ID and password will be stored in user_info.txt, please keep these 2 files in the same folder of the script

The script will install the Chrome Web Driver at its current folder, and if you want to move the Chrome Web Driver into a differnt folder, please don't forget
to change the path in user_info.txt

If the script doesn't successfully run at the first time, please try again

## Future updates
The script may get obselete when UCLA updates the Symptom Monitoring Survey, so stay updated

## Notes
The way to bypass DUO 2FA was incorperated from https://github.com/revalo/duo-bypass
And the package for auto install Chrome Web Driver was from https://github.com/yeongbin-jo/python-chromedriver-autoinstaller
This script was also inspired by https://github.com/SparkShen02/Easy-Duo-Authentication/
Massive thank you to all the contributors to the projects above
