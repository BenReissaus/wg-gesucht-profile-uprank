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

    WG_GESUCHT_URL = 'https://www.wg-gesucht.de/'
    EDIT_URL = 'https://www.wg-gesucht.de/gesuch-bearbeiten.html?edit={}'
    LOGIN_BUTTON_XPATH = "//a[contains(.,'Login')]"
    DELAY = 30
    LOAD_TRIES = 3
    LOG_FILE_NAME = 'output.log'

    def __init__(self):
        self.logger = logging.getLogger('wg-gesucht')
        self.display = Display(visible=0, size=(800, 600))
        self.browser = None
        self.username = None
        self.password = None

    def execute(self):
        self.initialize()
        self.load_web_page()
        self.login()
        self.update_application()
        self.shut_down()

    def initialize(self):
        self.logger.info("Started Upranking program...")
        self.display.start()
        self.load_config_values()
        self.initialize_logger()

    def load_config_values(self):
        dir = os.path.dirname(__file__)
        config_file_path = os.path.join(dir,"config.yml")
        config = yaml.safe_load(open(config_file_path))

        self.EDIT_URL = self.EDIT_URL.format(config['application_id'])
        self.browser = webdriver.Chrome(config['path_to_driver'])
        self.username = config['username']
        self.password = config['password']

        self.logger.info("Successfully loaded config values.")

    def initialize_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh = logging.FileHandler(self.LOG_FILE_NAME)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(fh)

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

        time.sleep(3)

        self.logger.info("Logged in.")

    def update_title(self):
        title1 = u'Studium vorbei - suche WG in der Heimat !'
        title2 = u'Studium vorbei - suche WG in der Heimat!'
        self.wait_till_element_loaded("Title input", By.ID, "title")
        title_element = self.browser.find_element_by_id('title')

        current_title = title_element.get_attribute('value')
        title_element.clear()
        new_title = title1
        if current_title == title1:
            new_title = title2

        title_element.send_keys(new_title)
        self.logger.info("Set title to '{}'".format(new_title))


    def update_application(self):
        self.browser.get(self.EDIT_URL)
        self.wait_till_element_loaded("First edit page", By.ID, "create_ad")

        # leave first edit page untouched
        self.browser.find_element_by_id('create_ad').submit()

        self.update_title()
        self.browser.find_element_by_id('thisForm').submit()

        self.logger.info("Finished update!")

    def shut_down(self):
        self.browser.close()
        self.display.stop()

if __name__ == '__main__':
    upranking = Upranking()
    upranking.execute()
