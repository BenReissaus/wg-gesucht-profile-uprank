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

    url = 'https://www.wg-gesucht.de/'
    delay = 30
    log_file = 'output.log'

    def __init__(self):
        self.logger = logging.getLogger('wg-gesucht')
        self.display = Display(visible=0, size=(800, 600))
        self.edit_url = 'https://www.wg-gesucht.de/gesuch-bearbeiten.html?edit={}'
        self.config = None
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
        self.load_config()

        self.edit_url = self.edit_url.format(self.config['application_id'])
        self.browser = webdriver.Chrome(self.config['path_to_driver'])
        self.username = self.config['username']
        self.password = self.config['password']
        self.display.start()

        self.initialize_logger()

    def load_config(self):
        dir = os.path.dirname(__file__)
        config_file_path = os.path.join(dir,"config.yml")
        self.config = yaml.safe_load(open(config_file_path))

    def initialize_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def load_web_page(self):
        self.browser.get(self.url)
        try:
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, "//div[@id='service-navigation']/div/a[2]")))
            self.logger.info("Page has loaded!")
        except TimeoutException:
            self.logger.warn("Loading took more than {} seconds!".format(self.delay))
            sys.exit(1)

    def login(self):
        # Click on Login Link
        self.browser.find_element(By.XPATH, "//div[@id='service-navigation']/div/a[2]").click()

        try:
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "login_email_username")))
            self.logger.info("Login modal has loaded!")
        except TimeoutException:
            self.logger.warn("Loading the modal took more than {} seconds!".format(self.delay))
            sys.exit(1)

        # Make sure the login input fields are loaded and visible by simulating a click
        assert 'login_email_username' in self.browser.page_source
        action = action_chains.ActionChains(self.browser)
        action.send_keys(keys.Keys.COMMAND+keys.Keys.ALT+'i')
        action.perform()
        time.sleep(3)
        action.send_keys(keys.Keys.ENTER)
        action.send_keys("document.querySelector('#login_email_username').click()"+keys.Keys.ENTER)
        action.perform()

        # Login
        self.browser.find_element_by_id('login_email_username').send_keys(self.username)
        self.browser.find_element_by_id('login_password').send_keys(self.password)
        self.browser.find_element_by_id('login_basic').submit()

        time.sleep(3)

    def update_title(self):
        title1 = u'Studium vorbei - suche WG in der Heimat !'
        title2 = u'Studium vorbei - suche WG in der Heimat!'
        try:
            title_element = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "title")))
            self.logger.info("Title input is ready!")
            current_title = title_element.get_attribute('value')
            title_element.clear()
            new_title = title1
            if current_title == title1:
                new_title = title2

            title_element.send_keys(new_title)
            self.logger.info("Set title to {}".format(new_title))

        except TimeoutException:
            self.logger.warn("Loading title input took more than {} seconds!".format(self.delay))
            sys.exit(1)

    def update_application(self):
        # Go to edit page of application
        self.browser.get(self.edit_url)

        # Leave and submit first page of application as is
        try:
            first_page = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, "create_ad")))
            self.logger.info("Ad submit button is ready!")
            first_page.submit()

        except TimeoutException:
            self.logger.warn("Loading ad submit button took more than {} seconds!".format(self.delay))
            sys.exit(1)

        # Update title on second page of application
        self.update_title()

        # Submit change
        self.browser.find_element_by_id('thisForm').submit()

    def shut_down(self):
        self.browser.close()
        self.display.stop()
        self.logger.info("Finished update!")


if __name__ == '__main__':
    upranking = Upranking()
    upranking.execute()
