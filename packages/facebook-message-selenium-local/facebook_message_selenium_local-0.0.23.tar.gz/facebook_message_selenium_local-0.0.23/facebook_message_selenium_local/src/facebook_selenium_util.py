import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from message_local.MessageLocal import Recipient
from .facebook_message_constants import FacebookMessageSeleniumLocalConstants
from dotenv import load_dotenv
import os

load_dotenv()



class FacebookSeleniumUtil:
    @staticmethod
    def chrome_login_facebook_messenger(*, leave_open: bool = False) -> webdriver.Chrome:
        # Setup
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # if not our_get_env("DISABLE_HEADLESS_MODE", raise_if_not_found=False):
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-infobars')
        options.add_argument("--window-size=1920x1080")

        if leave_open:
            options.add_experimental_option("detach", True)

        browser = webdriver.Chrome(options=options)

        # Open Chrome and login to Facebook Messenger
        browser.get('https://www.facebook.com/messages')

        input_user = browser.find_element(By.ID, 'email')
        input_password = browser.find_element(By.ID, 'pass')
        login_button = browser.find_element(By.ID, 'loginbutton')

        # TODO get circles facebook username and password. For now, it is with personal circles account
        account = Recipient(profile_id='101011007', user_id='9686870', person_id='50053532')
        account_dict=account.get_user_dict_by_system_id(FacebookMessageSeleniumLocalConstants.FACEBOOK_SYSTEM_ID)

        user = account_dict['username']
        # TODO Please use the dedicated method we have for this in python-sdk
        password = os.getenv('PRODUCT_PASSWORD')

        input_user.send_keys(user)
        input_password.send_keys(password)
        login_button.click()
        time.sleep(5)

        return browser