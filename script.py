import sys
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from keyring.errors import PasswordDeleteError

#directory

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(dir_path+'/automate.conf', 'r')
creds = f.readlines()
usrname = creds[0][0:-1].strip()
paswrd = creds[1].strip()
f.close()

#logs
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

#defining loggers
logger = setup_logger('general log', dir_path+'/automate.log')




logger.info('starting')
option = webdriver.ChromeOptions();
option.add_argument("--width=2560")
option.add_argument("--height=1440")
option.add_argument('headless');

#login
browser = webdriver.Chrome(options = option)
browser.get("https://elevate.darwinbox.in/")
username = browser.find_element_by_id('UserLogin_username')
username.send_keys(usrname)

password = browser.find_element_by_id('UserLogin_password')
password.send_keys(paswrd)

submit = browser.find_element_by_id('login-submit')
submit.click()

logger.info('logged in')

#checking smile page
try:
    xpath = '//*[@id="pulse_form"]/div/div/div/div[3]/button[1]'
    smile = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    smile.click()
except Exception as e:
    logger.info("work feel emoji not present")

#clockin/clockout
clockin = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dasboard-bigheader"]/header/div[4]/ul/li[1]/span')))
clockin.click()

enter = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="clokInClockout"]/div/div/div[2]/div[3]/button')))
enter.click()

browser.quit()    
logger.info('marked attendance')




