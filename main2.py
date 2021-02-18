import unittest
import xmlrunner as xmlrunner
from lib.common_functions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from testdata.config import *


class WebTests(unittest.TestCase):
    products = []
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
        self.driver.quit()

    def test_1_open_amazon_and_fetch_results(self):
        logit("TestCase: 1 - Open Amazon and fetch results for Iphone 11", 0)
        self.driver.get("http://amazon.com")
        waitfor(self, 10, By.ID, "twotabsearchtextbox")
        logit("[Passed] - SearchBox appeared - Page loaded", 0)
        self.driver.find_element_by_id("twotabsearchtextbox").send_keys(self.amazon_search)
        waitfor(self, 10, By.ID, "nav-search-submit-button")
        logit("[Passed] - Search Button is visible", 0)
        self.driver.find_element_by_id("nav-search-submit-button").click()
        if waitfor(self, 10, By.PARTIAL_LINK_TEXT, self.amazon_search, 0):
            logit("[Passed] -  Found the required product in the results", 0)
        else:
            logit("[Failed] - Couldn't find the required result in the page", 0)
            self.fail("[Failed] - Couldn't find the required result in the page")
        logit("Fetching product details", 0)
        link_element = self.driver.find_element_by_partial_link_text(self.amazon_search)
        link = link_element.get_attribute("href")
        link_element.click()
        waitfor(self, 10, By.ID, "price_inside_buybox")
        price = normalize_text(str(self.driver.find_element_by_id("price_inside_buybox").text))
        self.products = self.products.append(dic_add("Amazon.com", price, self.amazon_search, link))

    def test_2_open_ebay_and_fetch_results(self):
        logit("TestCase: 2 - Open Ebay and fetch results for Iphone 11", 0)
        self.driver.get("http://ebay.com")
        waitfor(self, 10, By.ID, "gh-ac")
        logit("[Passed] - SearchBox appeared - Page loaded", 0)
        self.driver.find_element_by_id("gh-ac").send_keys(self.ebay_search)
        waitfor(self, 10, By.ID, "gh-btn")
        logit("[Passed] - Search Button is visible", 0)
        self.driver.find_element_by_id("gh-btn").click()
        if waitfor(self, 10, By.PARTIAL_LINK_TEXT, self.ebay_search, 0):
            logit("[Passed] -  Found the required product in the results", 0)
        else:
            logit("[Failed] - Couldn't find the required result in the page", 0)
        logit("Fetching product details", 0)
        link_element = self.driver.find_element_by_partial_link_text(self.ebay_search)
        link = link_element.get_attribute("href")
        link_element.click()
        waitfor(self, 10, By.ID, "prcIsum_bidPrice")
        price = normalize_text(str(self.driver.find_element_by_id("prcIsum_bidPrice").text))
        self.products = self.products.append(dic_add("Ebay.com", price, self.ebay_search, link))

    def test_3_sort_and_report_the_results_based_on_price(self):
        logit("TestCase: 3 - Sort the results based on the price and report", 0)
        print("Before Sorting " + str(self.products))
        self.products = sorted(self.products, key=lambda k: float(k['price']))
        for entry in self.products:
            print("-----------------")
            print(entry['website'])
            print(entry['price'])
            print(entry['name'])
            print(entry['link'])


if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output=reportlocation)
    unittest.main(testRunner=runner)
