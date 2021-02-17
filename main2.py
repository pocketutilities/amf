import unittest
import xmlrunner as xmlrunner
from lib.common_functions import *
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from testdata.config import *


class WebTests(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        logit("Init - Setting up web browser", 0)
        self.driver = webdriver.Chrome("tools/chromedriver")
        self.driver.maximize_window()


    @classmethod
    def tearDownClass(self):
        logit("TearDown - End of Test Scenario", 0)
        #self.driver.quit()

    def test_1_open_amazon_and_fetch_results(self):
        logit("TestCase: 1 - Open Amazon and fetch results for Iphone 11", 0)
        ##Set their results global
        self.driver.get("http://amazon.com")

    def test_2_open_ebay_and_fetch_results(self):
        logit("TestCase: 2 - Open Ebay and fetch results for Iphone 11", 0)
        ## Set their results global
        self.driver.get("http://amazon.com")

    def test_3_combine_the_results(self):
        logit("TestCase: 3 - Fetch values from Global and handle data", 0)
        ##Fetch values from Global and handle data


if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output=reportlocation)
    unittest.main(testRunner=runner)
