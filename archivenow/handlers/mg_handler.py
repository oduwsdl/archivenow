# encoding: utf-8
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

class MG_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'Megalodon.jp'
        self.api_required = False

    def push(self, uri_org, p_args=[], session=requests.Session()):

        msg = ""

        options = Options()
        options.headless = True # Run in background
        driver = webdriver.Firefox(options = options)
        driver.get("https://megalodon.jp/?url=" + uri_org)

        try:
            addButton = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[8]/form/div[1]/input[2]")

            addButton.click() # Click the add button
        except :
            print("Unable to archive this page at this time.")
            raise


        stillOnPage = True
        while stillOnPage:
            try:
                button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div/h3")

            except:
                stillOnPage = False

            try:
                error = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div/a/h3")
                msg = "We apologize for the inconvenience. Currently, acquisitions that are considered \"robots\" in the acquisition of certain conditions are prohibited."
                raise
                sys.exit()

            except:
                pass

        # The page takes a while to archive, so keep checking if the loading page is still displayed.
        loading = True
        while loading:
            try:
                loadingPage = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/a/img")
                loading = False

            except:
                loading = True

        # After the loading screen is gone and the page is archived, the current URL
        # will be the URL to the archived page.
        if msg == "":
            print(driver.current_url)

        return msg
        