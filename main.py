import unittest
from common_functions import *
from todoist_functions import *
from time import sleep
from time import time
from appium import webdriver
from appium.webdriver.common.mobileby import By

print(str(time()))

prjname = str(time())

# if __name__ == '__main__':

# print(fetch_all_projects())


# Check if app is already installed or Install the App on the emulator
# Launch the app and Login to the application


# print(verify_project_created("testproject1"))


class InterviewTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("inside setup")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = ''
        desired_caps['deviceName'] = 'R5CN80KH18R'
        desired_caps['appPackage'] = 'com.todoist'
        desired_caps['appActivity'] = 'com.todoist.activity.HomeActivity'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    @classmethod
    def tearDownClass(self):
        print("inside quit")
    #    #self.driver.quit()

    def test_0_create_project_with_API(self):
        print(create_project(prjname))


    def test_1_verify_if_app_is_ready(self):
        print("Case: Test if the app main screen is launched and if the continue with email button appears")
        waitfor(self, 10, By.ID, "btn_welcome_continue_with_email")

    def test_2_login(self):
        waitfor(self, 10, By.ID, "btn_welcome_continue_with_email")
        self.driver.find_element_by_id("btn_welcome_continue_with_email").click()
        # The app might display pick up use dialog from previous authentication, Cancel for fresh login
        ##May Show choose from
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
        waitfor(self, 10, By.CLASS_NAME,"android.widget.ImageButton")

    def test_3_verify_if_project_exists(self):
        print("Test Case id: 1 - Verify that test project created from API exists on the UI")
        waitfor(self, 10, By.CLASS_NAME, "android.widget.ImageButton")
        sleep(2)
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
        waitfor(self, 10, By.XPATH, "//*[@text='Projects']")
        self.driver.find_element_by_xpath("//*[@text='Projects']").click()
        #alternate method self.driver.find_elements(By.CLASS_NAME,"android.widget.RelativeLayout").__getitem__(3).click()
        waitfor(self, 10, By.XPATH, "//*[@text='"+prjname+"']")
        self.driver.find_element_by_xpath("//*[@text='"+prjname+"']").click()
        waitfor(self, 10, By.XPATH,"//*[@text='How to best use projects']") # This verifies that we have reached to projects page
        print("Test Case id: 1 [Result] Passed")









if __name__ == "__main__":
    unittest.main()
