import unittest
from common_functions import *
from todoist_functions import *
from time import sleep
from time import time
from appium import webdriver
from appium.webdriver.common.mobileby import By


class InterviewTests(unittest.TestCase):
    prjname = str(time())

    @classmethod
    def setUpClass(self):
        print("inside setup")
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '',
            'deviceName': 'R5CN80KH18R',
            'appPackage': 'com.todoist',
            'appActivity': 'com.todoist.activity.HomeActivity'
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    @classmethod
    def tearDownClass(self):
        print("inside quit")
        # self.driver.quit()

    def test_1_create_project_via_API(self):
        print("TestCase: 1 - Verify that project can be created via API")
        print(create_project(self.prjname))
        if verify_project_created(self.prjname):
            print("Project [" + self.prjname + "] is successfully created via API")
            print("[Result] Passed")
        else:
            self.fail("[Error] Couldn't create Project [" + self.prjname + "] via API, Please check")

    def test_2_verify_if_app_is_ready(self):
        print("TestCase: 2 - Test if the app main screen is launched")
        waitfor(self, 10, By.ID, "btn_welcome_continue_with_email")
        print("[Result] Passed")

    def test_3_login(self):
        print("TestCase: 3 - Test if the app login works")
        waitfor(self, 10, By.ID, "btn_welcome_continue_with_email")
        self.driver.find_element_by_id("btn_welcome_continue_with_email").click()
        # The app might display pick up use dialog from previous authentication, Cancel for fresh login
        if waitfor(self, 5, By.ID, "com.google.android.gms:id/credentials_hint_picker_title", 0):
            print("Debug: Choose from dialog was shown")
            waitfor(self, 2, By.ID, "com.google.android.gms:id/cancel")
            self.driver.find_element_by_id("com.google.android.gms:id/cancel").click()
        waitfor(self, 10, By.ID, "email_exists_input")
        self.driver.find_element_by_id("email_exists_input").send_keys(Auth_Email)
        waitfor(self, 10, By.ID, "btn_continue_with_email")
        self.driver.find_element_by_id("btn_continue_with_email").click()
        waitfor(self, 10, By.ID, "log_in_password")
        self.driver.find_element_by_id("log_in_password").send_keys(Auth_Password)
        waitfor(self, 10, By.ID, "btn_log_in")
        self.driver.find_element_by_id("btn_log_in").click()
        waitfor(self, 10, By.CLASS_NAME, "android.widget.ImageButton")
        print("[Result] Passed")

    def test_4_verify_if_project_exists(self):
        print("TestCase: 4 - Verify that test project created from API exists on the UI")
        waitfor(self, 10, By.CLASS_NAME, "android.widget.ImageButton")
        sleep(2)
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
        waitfor(self, 10, By.XPATH, "//*[@text='Projects']")
        self.driver.find_element_by_xpath("//*[@text='Projects']").click()
        # alternate method self.driver.find_elements(By.CLASS_NAME,"android.widget.RelativeLayout").__getitem__(
        # 3).click()
        waitfor(self, 10, By.XPATH, "//*[@text='" + self.prjname + "']")
        self.driver.find_element_by_xpath("//*[@text='" + self.prjname + "']").click()
        waitfor(self, 10, By.XPATH,
                "//*[@text='How to best use projects']")  # This verifies that we have reached to projects page
        print("[Result] Passed")


if __name__ == "__main__":
    unittest.main()
