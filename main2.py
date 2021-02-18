import unittest
import xmlrunner as xmlrunner
from lib.common_functions import *
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from testdata.config import *


class WebTests(unittest.TestCase):

    amazon_search = "Apple iPhone 11 Pro Max (64GB, Space Gray) - for Verizon (Renewed)"
    ebay_search = "Apple iPhone 11 Pro Max - 64GB - Midnight Green"
    @classmethod
    def setUpClass(self):
        logit("Init - Setting up web browser", 0)
        ## Todo: Take config from user on what browser to use and what OS the script is running and select the chromedriver based on that.
        self.driver = webdriver.Chrome("tools/chromedriver")
        self.driver.maximize_window()

    @classmethod
    def tearDownClass(self):
        logit("TearDown - End of Test Scenario", 0)
        # self.driver.quit()

    def test_1_open_amazon_and_fetch_results(self):
        logit("TestCase: 1 - Open Amazon and fetch results for Iphone 11", 0)
        ##Set their results global
        self.driver.get("http://amazon.com")
        waitfor(self, 10, By.ID, "twotabsearchtextbox")
        self.driver.find_element_by_id("twotabsearchtextbox").send_keys(self.amazon_search)
        waitfor(self, 10, By.ID, "nav-search-submit-button")
        self.driver.find_element_by_id("nav-search-submit-button").click()
        if waitfor(self, 10, By.PARTIAL_LINK_TEXT, self.amazon_search):
            print("Passed -  Found the required product")
        self.driver.find_element_by_partial_link_text(self.amazon_search).click()
        waitfor(self, 10, By.ID, "price_inside_buybox")
        price = normalize_text(str(self.driver.find_element_by_id("price_inside_buybox").text))
        global amazon_price
        amazon_price = float(price)
        print(str(amazon_price))

    def test_2_open_ebay_and_fetch_results(self):
        logit("TestCase: 2 - Open Ebay and fetch results for Iphone 11", 0)
        ## Set their results global
        self.driver.get("http://ebay.com")
        waitfor(self, 10, By.ID, "gh-ac")
        self.driver.find_element_by_id("gh-ac").send_keys(self.ebay_search)
        waitfor(self, 10, By.ID, "gh-btn")
        self.driver.find_element_by_id("gh-btn").click()
        if waitfor(self, 10, By.PARTIAL_LINK_TEXT, self.ebay_search):
            print("Passed -  Found the required product")
        self.driver.find_element_by_partial_link_text(self.ebay_search).click()
        waitfor(self, 10, By.ID, "prcIsum_bidPrice")
        price = normalize_text(str(self.driver.find_element_by_id("prcIsum_bidPrice").text))
        global ebay_price
        ebay_price = float(price)
        print(str(ebay_price))

    def test_3_combine_the_results(self):
        logit("TestCase: 3 - Fetch values from Global and handle data", 0)
        print("Amazon: " + str(amazon_price))
        print("Ebay: " + str(ebay_price))
        ##Fetch values from Global and handle data


if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output=reportlocation)
    unittest.main(testRunner=runner)
