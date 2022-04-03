import sys

from datetime import date
from datetime import datetime
from datetime import timedelta

from enum import Enum

import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return Course[s]
        except KeyError:
            raise ValueError()

# Set up browser service
def create_browser(args):
    service = Service(ChromeDriverManager().install())

    # Comment out/remove these options to load the browser and observe
    chrome_options = Options()
    
    if args.headless:
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')

    # Initiate the browser
    driver = webdriver.Chrome(service = service, chrome_options=chrome_options)

    # Always wait 10 seconds if needed
    driver.implicitly_wait(10)

    return driver 

# Set up arguments
def get_args():
    
    parser = argparse.ArgumentParser(description='Snag a tee time')

    # Required
    parser.add_argument('-u', type=str, required=True)
    parser.add_argument('-p', type=str, required=True)
    parser.add_argument('-course', type=Course.from_string, choices=list(Course), required=True)
    parser.add_argument('-count', type=int, required=True)
    parser.add_argument('-adv', type=int, default=7)
    parser.add_argument('-start', type=str, default='6:30 AM')
    parser.add_argument('-end', type=str, default='8:00 PM')

    # Optional
    parser.add_argument('--checkout', action='store_true')
    parser.add_argument('--headless', action='store_true')

    return parser.parse_args()

# Read the args from the cmd line
args = get_args()

# Launch the browser
driver = create_browser(args)

try:

    # Base url
    base_url = 'https://www.chronogolf.com/club/18159/widget?medium=widget&source=club'

    date_to_play = str(date.today() + timedelta(days=args.adv))

    # Look forward args.adv amount of days
    base_url += '#?date='
    base_url += date_to_play

    # Add the course id
    base_url += '&course_id='
    base_url += str(args.course.value)

    # Set to 18 holes
    base_url += '&nb_holes=18'

    # Add the amount of players
    base_url += '&affiliation_type_ids='

    count = args.count

    # This is a weird way to calculate number of players, hopefully this doesn't break/change in the future
    for x in range(count):
        if x != 0 and x != count:
            base_url += ','

        base_url += '85113'

    print('Going to url: ' + base_url)

    # Load the URL in the browser, this should get us half way there
    driver.get(base_url)

    # Find the widget on the page
    tee_time_widget = driver.find_element(by=By.CLASS_NAME, value='widget-teetimes')

    # Define the format and parse the provided date + times into datetime objects
    format = '%Y-%m-%d %I:%M %p'
    dt_to_play_start = datetime.strptime(date_to_play + ' ' + args.start, format)
    dt_to_play_end = datetime.strptime(date_to_play + ' ' + args.end, format)

    print('Finding a tee time between: ' + str(dt_to_play_start) + ' and ' + str(dt_to_play_end))     

    # Initialize it as none, in-case we don't find anything
    tee_time = None

    # Go through all of the tee times in the widget
    for tee_time_element in tee_time_widget.find_elements(by=By.CLASS_NAME, value='widget-teetime'):

        # Get the value of the tee time by the tag. This is the time of the tee time.
        # The expected format is '8:35 AM'. If that changes this will break and I'll be sad
        tee_time_value = tee_time_element.find_element(by=By.CLASS_NAME, value='widget-teetime-tag')\
            .get_attribute('innerHTML')\
            .strip()
        
        # Get the curr date by combining the date and the time we found
        dt_curr = datetime.strptime(date_to_play + ' ' + tee_time_value, format)
        
        # Check if it's within our range. If it is, go ahead and set it as the tee time we are working with
        if dt_curr >= dt_to_play_start and dt_curr <= dt_to_play_end:

            tee_time = tee_time_element.find_element(by=By.CLASS_NAME, value='widget-teetime-rate')
            print('Found tee time at ' + str(dt_curr))

            break

    if tee_time != None:
        tee_time.click()
    else:
        # Exit if we don't have anything.
        print('No tee time determined from provided parameters!')
        sys.exit()

    print('Clicking button to log in...')

    # Look for the login button
    driver\
        .find_element(by=By.CLASS_NAME, value='widget-step-confirmation')\
        .find_element(by=By.CLASS_NAME, value='fl-button').click()

    # Set the login info from args
    login_email = args.u
    login_password = args.p

    driver.find_element(by=By.ID, value='sessionEmail').send_keys(login_email)
    driver.find_element(by=By.ID, value='sessionPassword').send_keys(login_password)

    print('Logging in with provided credentials...')

    # Click the login submission button
    driver.find_element(by=By.XPATH, value="//input[@type='submit']").click()

    print('Agreeing to terms >:)')

    # Check the review terms. Hopefully they allow poorly written bots
    driver\
        .find_element(by=By.TAG_NAME, value='reservation-review-terms')\
        .find_element(by=By.XPATH, value="//input[@type='checkbox']").click()

    if args.checkout:
        print('Checking out...')
        driver\
            .find_element(by=By.TAG_NAME, value='reservation-review-submit-button')\
            .find_element(by=By.XPATH, value="//input[@type='submit']").click()
    else:
        # Just don't do anything
        print('Skipping checkout...')

finally:
    # Always exit the browser when complete
    driver.close()
