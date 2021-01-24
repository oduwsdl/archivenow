import os
import requests
import sys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class IS_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Archive.is'
        self.api_required = False 

    def push(self, uri_org, p_args=[], session=requests.Session()):

        msg = ""

        try:

            options = Options()
            options.headless = True # Run in background
            driver = webdriver.Firefox(options = options)
            driver.get("https://archive.is")

            elem = driver.find_element_by_id("url") # Find the form to place a URL to be archived

            elem.send_keys(uri_org) # Place the URL in the input box

            saveButton = driver.find_element_by_xpath("/html/body/center/div/form[1]/div[3]/input") # Find the submit button

            saveButton.click() # Click the submit button

            # After clicking submit, there may be an additional page that pops up and asks if you are sure you want
            # to archive that page since it was archived X amount of time ago. We need to wait for that page to 
            # load and click submit again.
            delay = 30 # seconds
            try:
                nextSaveButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/div[4]/center/div/div[2]/div/form/div/input")))
                nextSaveButton.click()

            except TimeoutException:
                pass

            # The page takes a while to archive, so keep checking if the loading page is still displayed.
            loading = True
            while loading:
                
                if not 'wip' in driver.current_url:
                    loading = False

            # After the loading screen is gone and the page is archived, the current URL
            # will be the URL to the archived page.
            print(driver.current_url)

            driver.quit()

        except:

            '''
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print((fname, exc_tb.tb_lineno, sys.exc_info() ))
            '''

            msg = "Unable to complete request."

        return msg
