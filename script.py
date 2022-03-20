import sys
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from keyring.errors import PasswordDeleteError

clockinFlag = sys.argv[1]

# directory

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(dir_path+'/automate.conf', 'r')
creds = f.readlines()
usrname = creds[0][0:-1].strip()
paswrd = creds[1].strip()
f.close()

# logs
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# defining loggers
logger = setup_logger('general log', dir_path+'/automate.log')


logger.info('starting')
option = webdriver.ChromeOptions()
option.add_argument("--width=2560")
option.add_argument("--height=1440")
option.add_argument('headless')

# login
browser = webdriver.Chrome(options=option)
browser.get("https://elevate.peoplestrong.com/altLogin.jsf")
username = browser.find_element_by_id('loginForm:username12')
username.send_keys(usrname)

password = browser.find_element_by_id('loginForm:password')
password.send_keys(paswrd)

submit = browser.find_element_by_id('loginForm:loginButton')
submit.click()

browser.get

logger.info('logged in')

# selecting out of office
try:
    xpath = '//a[contains( text( ), "Out of Office")]'
    ooo = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    ooo.click()
except Exception as e:
    logger.info("ooo not present: "+e)

logger.info(clockinFlag)
# clockin/clockout
if int(clockinFlag):
    logger.info("clocked in")
    clockin = WebDriverWait(browser, 3).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="includedAngularJS"]/app-root/div/div[1]/div/div/div/div/div/app-home/app-card/div/div/div[2]/app-punch-inout/div/div[1]/div/div/div[3]/div[1]/div[1]/a')))
    clockin.click()
    logger.info("clocked in")
else:
    logger.info("clocked out")
    clockout = WebDriverWait(browser, 3).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="includedAngularJS"]/app-root/div/div[1]/div/div/div/div/div/app-home/app-card/div/div/div[2]/app-punch-inout/div/div[1]/div/div/div[3]/div[1]/div[2]/a')))
    clockout.click()
    logger.info("clocked out")


# logger.info('marked attendance')
