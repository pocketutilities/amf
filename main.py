import unittest
from common_functions import *
from todoist_functions import *
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import By

#if __name__ == '__main__':

#print(fetch_all_projects())
#print(create_project("testproject2"))

#Check if app is already installed or Install the App on the emulator
#Launch the app and Login to the application



#print(verify_project_created("testproject1"))



class InterviewTests(unittest.TestCase):



    def setUp(self):
        print("inside setup")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = ''
        desired_caps['deviceName'] = 'R5CN80KH18R'
        desired_caps['appPackage'] = 'com.todoist'
        desired_caps['appActivity'] = 'com.todoist.activity.HomeActivity'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


    def tearDown(self):
        print("inside quit")
        #self.driver.quit()

    def test_1_verify_if_app_is_ready(self):
        print("Case: Test if the app main screen is launched and if the continue with email button appears")
        waitfor(self,10,By.ID,"btn_welcome_continue_with_email")

    def test_2_login(self):
        waitfor(self,10,By.ID,"btn_welcome_continue_with_email")
        self.driver.find_element_by_id("btn_welcome_continue_with_email").click()
        waitfor(self,10,By.ID,"email_exists_input")
        self.driver.find_element_by_id("email_exists_input").send_keys(Auth_Email)
        waitfor(self, 10, By.ID, "btn_continue_with_email")
        self.driver.find_element_by_id("btn_continue_with_email").click()
        waitfor(self,10,By.ID,"log_in_password")
        self.driver.find_element_by_id("log_in_password").send_keys(Auth_Password)
        waitfor(self,10,By.ID,"btn_log_in")
        self.driver.find_element_by_id("btn_log_in").click()
        sleep(20)





if __name__=="__main__":
    unittest.main()