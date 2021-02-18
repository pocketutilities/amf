import unittest
import xmlrunner as xmlrunner
from lib.common_functions import *
from lib.todoist_functions import *
from time import time
from appium import webdriver
from appium.webdriver.common.mobileby import By


class InterviewTests(unittest.TestCase):

    #Todo: This should ideally come under test data but we are taking dynamic values to make sure our script don't collide on re-run
    prjname = str(time())
    taskname = "task_" + prjname

    @classmethod
    def setUpClass(self):
        logit("Init - Setting up Android Device", 0)
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
        logit("TearDown - End of Test Scenario", 0)
        self.driver.quit()

    def test_1_api_create_project(self):
        logit("TestCase: 1 - Verify that project can be created via API", 0)
        logit(create_project(self.prjname), 0)
        if verify_project_created(self.prjname):
            logit("Project [" + self.prjname + "] is successfully created via API", 0)
            logit("[Passed]", 0)
        else:
            self.fail("[Error] Couldn't create Project [" + self.prjname + "] via API, Please check")

    def test_2_android_verify_if_app_is_launched(self):
        logit("TestCase: 2 - Test if the app main screen is launched", 0)
        waitfor(self, 10, By.ID, "btn_welcome_continue_with_email")
        logit("[Passed]", 0)

    def test_3_android_login(self):
        logit("TestCase: 3 - Test if the app login works", 0)
        waitfor(self, 10, By.ID, "btn_welcome_continue_with_email")
        self.driver.find_element_by_id("btn_welcome_continue_with_email").click()
        #Todo: The app might display pick up use dialog from previous authentication, Cancel for fresh login.
        #More such scenarios might need to be explored for a very robust script
        if waitfor(self, 5, By.ID, "com.google.android.gms:id/credentials_hint_picker_title", 0):
            logit("[Passed] - Choose from ids dialog appeared", 0)
            waitfor(self, 2, By.ID, "com.google.android.gms:id/cancel")
            self.driver.find_element_by_id("com.google.android.gms:id/cancel").click()
        waitfor(self, 10, By.ID, "email_exists_input")
        self.driver.find_element_by_id("email_exists_input").send_keys(Auth_Email)
        waitfor(self, 10, By.ID, "btn_continue_with_email")
        self.driver.find_element_by_id("btn_continue_with_email").click()
        waitfor(self, 10, By.ID, "log_in_password")
        logit("[Passed] - Navigated to Password screen")
        self.driver.find_element_by_id("log_in_password").send_keys(Auth_Password)
        waitfor(self, 10, By.ID, "btn_log_in")
        self.driver.find_element_by_id("btn_log_in").click()
        waitfor(self, 10, By.CLASS_NAME, "android.widget.ImageButton")
        logit("[Passed] - Logged in Successfully", 0)

    def test_4_android_verify_if_project_exists(self):
        logit("TestCase: 4 - Verify that test project created from API exists on the UI", 0)
        waitfor(self, 10, By.CLASS_NAME, "android.widget.ImageButton")
        sleep(2)
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
        waitfor(self, 10, By.XPATH, "//*[@text='Projects']")
        logit("[Passed] - Menu link is opened, Projects category is visible",0)
        self.driver.find_element_by_xpath("//*[@text='Projects']").click()
        # alternate method self.driver.find_elements(By.CLASS_NAME,"android.widget.RelativeLayout").__getitem__(
        # 3).click()
        waitfor(self, 10, By.XPATH, "//*[@text='" + self.prjname + "']")
        logit("[Passed] - The newly created project is visible", 0)
        self.driver.find_element_by_xpath("//*[@text='" + self.prjname + "']").click()
        waitfor(self, 3, By.XPATH,
                "//*[@text='How to best use projects']", 1)  # This verifies that we have reached to projects page
        logit("[Passed] - Able to open new project screen", 0)

    def test_5_android_create_task(self):
        logit("TestCase: 5 - Android UI - Create Task", 0)
        waitfor(self, 10, By.XPATH, "//*[@text='How to best use projects']")
        self.driver.find_element_by_id("fab").click()
        sleep(1)
        waitfor(self, 10, By.CLASS_NAME, "android.widget.EditText")
        logit("[Passed] - The Create Task dialog has appeared successfully", 0)
        self.driver.find_element_by_class_name("android.widget.EditText").send_keys(self.taskname)
        waitfor(self, 2, By.ID, "android:id/button1")
        self.driver.find_element_by_id("android:id/button1").click()
        # Todo: An extra check might be good here
        logit("[Passed] - The Task has been created successfully", 0)

    def test_6_api_verify_task(self):
        logit("TestCase: 6 - API - Verify Task", 0)
        sleep(10)
        ##Todo: Let's give the backend server 10 seconds to Sync - Mobile Internet speed might be slow because of which sync might take time. A dynamic sync time calculation would help here.
        data = get_all_active_items()
        found = False
        # logit("To Verify Taskname: "+self.taskname + " - ProjectID  " + str(get_project_id(self.prjname)),1)
        for item in data["items"]:
            # logit(str(item),1)
            # logit("observe: Taskname " + str(item['content']) + " - ProjectID  " + str(item["project_id"]),1)

            if str(item['content']) == str(self.taskname) and str(item["project_id"]) == str(
                    get_project_id(self.prjname)):
                found = True
                break

        if found:
            logit("[Passed] - Found the task in the correct project", 0)
        else:
            logit("[Failed] to find the task in the correct project", 0)
            self.fail("Failed to find the task in the correct project", 0)

    def test_7_android_complete_the_task(self):
        logit("TestCase: 7 - Android - Put the task to completion", 0)
        ##Useless click on the task to close the tray
        self.driver.find_element_by_id("com.todoist:id/content_toolbar_container").click()
        sleep(2)  ###Animations can take time from one device to another - Safe option with static wait.
        ##CHILD-PARENT-CHILD2 METHOD , Could use Sibling as well
        self.driver.find_element_by_xpath(
            "//*[@text='" + self.taskname + "']/../*[@resource-id='com.todoist:id/checkmark']").click()
        sleep(10)
        ##Some Dynamic wait disappearance method can be written here like waitfor waits , we can check for disappearance.
        if waitfor(self, 2, By.XPATH, "//*[@text='" + self.taskname + "']", 0) == False:
            logit("[Passed] - The Task has been set to complete", 0)
        else:
            logit("[Error]: Issue while putting Task to complete", 0)
            self.fail("[Error]: Issue while putting Task to complete")

    def test_8_API_reopen_task(self):
        logit("TestCase: 8 - API - Reopen the task", 0)
        reopen_item(self.taskname, self.prjname)
        # Todo: an extra check might be good here
        logit("[Passed]", 0)

    def test_9_Android_verify_reopened_task(self):
        logit("TestCase: 9 - Android - Verify if the reopened task appears on the page", 0)
        waitfor(self, 20, By.XPATH, "//*[@text='" + self.taskname + "']")
        logit("[Passed], The server has synced with the UI - Reopen Confirmed", 0)


if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output=reportlocation)
    unittest.main(testRunner=runner)
