#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common import action_chains, keys
from pyvirtualdisplay import Display
import sys
import time
import yaml
import os
import logging

class Upranking:

    WG_GESUCHT_URL = 'https://www.wg-gesucht.de'
    EDIT_URL = 'https://www.wg-gesucht.de/gesuch-bearbeiten.html?action=update_request&request_id={}'
    LOGIN_BUTTON_XPATH = "//a[contains(.,'Login')]"
    DELAY = 30
    LOAD_TRIES = 3

    def __init__(self, debug=False):
        self.logger = None
        self.browser = None
        self.username = None
        self.password = None
        self.application_id = None
        self.title1 = None
        self.title2 = None
        self.debug = debug

        if self.debug:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

    def execute(self):
        self.initialize()
        self.load_web_page()
        self.login()
        self.update_application()
        self.shut_down()

    def initialize(self):
        self.initialize_logger()
        self.initialize_chrome_driver()
        self.load_config_values()

    def initialize_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger = logging.getLogger('wg-gesucht')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(sh)

    def initialize_chrome_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        if not self.debug:
            chrome_options.add_argument('--headless')

        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def load_config_values(self):
        self.username = os.environ['username']
        self.password = os.environ['password']
        self.application_id = os.environ['application_id']
        self.title1 = os.environ['title1']
        self.title2 = os.environ['title2']

        self.logger.info("Successfully loaded config values.")

    def wait_till_element_loaded(self, element_name, xpath_type, xpath_value):

        tries = 0
        while (tries < self.LOAD_TRIES):
            try:
                condition = EC.presence_of_element_located((xpath_type, xpath_value))
                element = WebDriverWait(self.browser, self.DELAY).until(condition)
                self.logger.info("'{}' has loaded.".format(element_name))
            except TimeoutException:
                self.logger.warn("Loading '{}' took more than {} seconds!".format(element_name, self.DELAY))
            else:
                return element
            finally:
                tries += 1
        else:
            self.logger.warn("Failed loading '{}' {} times. Exiting.".format(element_name, self.LOAD_TRIES))
            self.shut_down()
            sys.exit(1)

    def load_web_page(self):
        self.browser.get(self.WG_GESUCHT_URL)
        self.wait_till_element_loaded("Web Page", By.XPATH, self.LOGIN_BUTTON_XPATH)

    def login(self):

        # click on login link
        self.browser.find_element(By.XPATH, self.LOGIN_BUTTON_XPATH).click()
        self.logger.info("Clicked on login button.")

        # make sure the login input fields are loaded and visible by simulating a click
        assert 'login_email_username' in self.browser.page_source
        action = action_chains.ActionChains(self.browser)
        action.send_keys(keys.Keys.COMMAND+keys.Keys.ALT+'i')
        action.perform()
        time.sleep(3)

        action.send_keys(keys.Keys.ENTER)
        action.send_keys("document.querySelector('#login_email_username').click()"+keys.Keys.ENTER)
        action.perform()
        self.logger.info("Clicked in username input field.")

        # login
        self.browser.find_element_by_id('login_email_username').send_keys(self.username)
        self.browser.find_element_by_id('login_password').send_keys(self.password)
        self.browser.find_element_by_id('login_basic').submit()

        self.logger.info("Inserted all credentials and submitted login request.")

        self.wait_till_element_loaded("Login Icon", By.XPATH, "//div[contains(@class, 'profile_image_menu')]")

        self.logger.info("Logged in.")

    def update_title(self):
        self.wait_till_element_loaded("Title input", By.ID, "ad_title")
        title_element = self.browser.find_element_by_id('ad_title')

        current_title = title_element.get_attribute('value')
        title_element.clear()
        new_title = self.title1
        if current_title == self.title1:
            new_title = self.title2

        title_element.send_keys(new_title)
        self.logger.info("Set title to '{}'".format(new_title))


    def update_application(self):
        self.browser.get(self.EDIT_URL.format(self.application_id))
        self.update_title()
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.browser.find_element_by_id('update_request').click()

        self.logger.info("Finished update.")

    def shut_down(self):
        self.browser.close()

        if self.debug:
            self.display.stop()

if __name__ == '__main__':
    upranking = Upranking() if os.environ.get('debug_wg_gesucht') != "true" else Upranking(debug=True)
    upranking.execute()

