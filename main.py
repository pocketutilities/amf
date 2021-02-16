import unittest
from common_functions import *
from time import sleep
from appium import webdriver

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
        print("inside first test")


if __name__=="__main__":
    unittest.main()