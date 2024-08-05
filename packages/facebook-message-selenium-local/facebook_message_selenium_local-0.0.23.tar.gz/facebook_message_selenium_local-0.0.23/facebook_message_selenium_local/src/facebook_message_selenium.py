from datetime import datetime
import random
from typing import List

from logger_local.MetaLogger import MetaLogger

from .facebook_message_constants import FacebookMessageSeleniumLocalConstants
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from .facebook_selenium_util import FacebookSeleniumUtil
from python_sdk_remote.utilities import our_get_env
from message_local.MessageLocal import MessageLocal, Recipient
import time

# TODO Please use this variable in the code like we do in sms-message-inforu package/repo
# IS_REALLY_SEND_WHATSAPP_SELENIUM = our_get_env('IS_REALLY_SEND_WHATSAPP_SELENIUM', 'False').lower() in ('true', '1')
IS_REALLY_SEND_FACEBOOK_MESSAGE_SELENIUM = our_get_env('IS_REALLY_SEND_FACEBOOK_SELENIUM', 'False').lower() in ('true', '1')

# TOO Please make sure that you take the good things from sms-message-inforu package/repo

class FacebookMessageSelenium(MessageLocal, metaclass=MetaLogger,
                              object=FacebookMessageSeleniumLocalConstants.FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False) -> None:
        #super().__init__(recipients=[Recipient()],original_body="setup",is_test_data=is_test_data)

        # Set up browser
        #if is_test_data:
        #self.options.add_experimental_option("detach", True) # Keeps the browser open after finished. Use for testing purposes

        self.browser = FacebookSeleniumUtil.chrome_login_facebook_messenger()

    def send(self, *, body: str = None, compound_message_dict: dict = None,
             recipients: list[Recipient] = None, cc: list[Recipient] = None, bcc: list[Recipient] = None,
             scheduled_timestamp_start: datetime = None,
             scheduled_timestamp_end: datetime = None, **kwargs) -> list[int]:
        self.logger.info("Sending messages")
        return_value = []
        for recipient in recipients:
            # TODO Make compatible with MessageLocal and implement:
            #  if not self.can_send(recipient=recipient, outgoing_body={"Message": body}):
            #     continue

            # TODO Shall we call user_external.get_user_dict_by_system_id(...)?
            # Response: That method wants a where clause. This method calls that method.
            user_external_dict = recipient.get_user_dict_by_system_id(
                FacebookMessageSeleniumLocalConstants.FACEBOOK_SYSTEM_ID)

            # TODO Do we want check if it empty? Why we don't send empty dict and check if it is None?
            # Response: If it is empty, there is an Exception thrown when trying to run the for loop.
            if user_external_dict == {"username": list, "user_external_id": list,
                                      "phone.full_number_normalized": list}:
                return []

            for username in user_external_dict["username"]:
                # Go to Messenger
                self.browser.get('https://www.facebook.com/messages/new')
                window = self.browser.find_element(By.XPATH, '/html/body')
                window.click()
                time.sleep(1)
                window = self.browser.find_element(By.XPATH, '/html/body')
                window.click()
                time.sleep(1)
                window = self.browser.find_element(By.XPATH, '/html/body')
                window.click()

                # Create a new chat with the username provided
                try:
                    # TODO Please do not use Magic Numbers, please use consts
                    time.sleep(random.randint(4, 6))
                    input_username = self.browser.find_element(By.XPATH, '//div[@role="main"]//input[@type="search"]')
                    input_username.send_keys(str(username))
                    time.sleep(random.randint(3, 6))
                    input_username.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
                    time.sleep(random.randint(2, 6))
                except NoSuchElementException:
                    time.sleep(random.randint(3, 6))
                    input_username = self.browser.find_element(By.XPATH, '//div[@role="presentation"]//input['
                                                                         '@type="search"]')
                    input_username.click()
                    input_username.send_keys(str(username))
                    time.sleep(random.randint(2, 6))
                    input_username.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
                    time.sleep(random.randint(2, 6))
                # Send provided message
                time.sleep(random.randint(2, 6))
                message_bar = self.browser.find_element(By.XPATH, '//div[@role="main"]//div[@role="textbox"]')
                message_bar.click()
                message_bar.send_keys(body, Keys.ENTER)
                time.sleep(random.randint(2, 6))

                # TODO Make compatible with MessageLocal and implement:
                #  self.after_send_attempt(http_status_code=HTTPStatus.OK.value, outgoing_body={"Message": body},
                #  recipient=recipient)
                return_value.append(
                    {"status": "success", "message": "Message sent successfully"})

        return return_value

    # TODO Add Tests to read()
    def read(self, *, username: str, number_messages: int = 1) -> []:
        self.logger.info("Reading message from:", username)

        # Find conversation with username
        search_bar = self.browser.find_element(By.XPATH,
                                               '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div/div/div/div/label/input')
        search_bar.click()
        search_bar.send_keys(username)
        time.sleep(1)
        search_bar.send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER)

        # Gather all the messages in the conversation
        messages = []
        temp_list = []
        try:
            i = 1
            while True:
                xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div[3]/div/div[' + str(
                    i) + ']'
                recent_message = self.browser.find_element(By.XPATH, xpath)
                messages.append(recent_message.text)
                i += 1
        except NoSuchElementException as e:
            for m in range(number_messages):
                temp_list.append(messages[number_messages - m - 1])

        # Take the last number_messages and return them
        return_value = list(reversed(temp_list))
        return return_value
