import time

from datetime import date
from datetime import timedelta

from enum import Enum

import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Course(Enum):
    FALLS_ROAD = 21184
    HAMPSHIRE_GREENS = 21183
    LAYTONSVILLE = 21182
    LITTLE_BENNET = 21181
    NEEDWOOD = 21180
    NORTHWEST = 21178
    POOLESVILLE = 21176
    RATTLEWOOD = 21175

# Set up browser service
def launch():
    service = Service(ChromeDriverManager().install())

    # Initiate the browser
    driver = webdriver.Chrome(service = service)

    return driver 

# Set up arguments
def get_args():
    
    parser = argparse.ArgumentParser(description='Snag a tee time')
    parser.add_argument('-u', type=str, required=True)
    parser.add_argument('-p', type=str, required=True)
    parser.add_argument('-count', type=int, required=True)

    return parser.parse_args()

args = get_args()

driver = launch()

# Open the Website
base_url = 'https://www.chronogolf.com/club/18159/widget?medium=widget&source=club'

# Set 7 days from now
base_url += '#?date='
base_url += str(date.today() + timedelta(days=7))

# Add the course id
base_url += '&course_id='
base_url += str(Course.NEEDWOOD.value)

# Set to 18 holes
base_url += '&nb_holes=18'

# 2 players
base_url += '&affiliation_type_ids='

count = args.count
for x in range(count):
    if x != 0 and x != count:
        base_url += ','

    base_url += '85113'

driver.get(base_url)
time.sleep(5)

driver.find_element(by=By.CLASS_NAME, value='widget-teetime-rate').click()
time.sleep(5)

driver.find_element(by=By.CLASS_NAME, value='fl-button').click()
time.sleep(5)

# Set the login info
login_email = args.u
login_password = args.p

driver.find_element(by=By.ID, value='sessionEmail').send_keys(login_email)
driver.find_element(by=By.ID, value='sessionPassword').send_keys(login_password)

time.sleep(5)

driver.find_element(by=By.XPATH, value="//input[@type='submit']").click()
time.sleep(5)

# Check the review terms
driver.find_element(by=By.TAG_NAME, value='reservation-review-terms').find_element(by=By.XPATH, value="//input[@type='checkbox']").click()