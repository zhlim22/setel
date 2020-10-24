import unittest
import uuid, requests, json
from appium import webdriver
from time import sleep
from appium.webdriver.common.touch_action import TouchAction

class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setting value of my user token
        cls.token = "f6b71ac9fc1d627bd818265c369b7eb468318d07"

        # Callinng api to create test project
        return_value = requests.post(
            "https://api.todoist.com/rest/v1/projects",
            data=json.dumps({
                "name": "Test Project"
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": "Bearer %s" % cls.token
            }).json()
        
        # Storing value of project id for clean up later
        cls.project_id = str(return_value["id"])
    
    @classmethod
    def tearDownClass(cls):
        # Delete the test project created in this test
        requests.delete("https://api.todoist.com/rest/v1/projects/%s" % cls.project_id, headers={"Authorization": "Bearer %s" % cls.token})

    def setUp(self):
        # Setting desired capabilities for android emulator for Todoist app
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.todoist'
        desired_caps['appActivity'] = 'com.todoist.activity.HomeActivity'

        # Setting url and desired capabilities to webdriver
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

        # Setting value of implicit wait time when locating elements
        self.driver.implicitly_wait(5)

        # Logging into the application
        # Click on Continue with email button on welcome screen
        btn_login_with_email = self.driver.find_element_by_id("com.todoist:id/btn_welcome_continue_with_email")
        btn_login_with_email.click()

        # Enter user email
        field_email = self.driver.find_element_by_id("com.todoist:id/email_exists_input")
        field_email.send_keys("dblee1111@gmail.com")

        # Click on Continue with email button on login screen
        btn_continue_with_email = self.driver.find_element_by_id("com.todoist:id/btn_continue_with_email")
        btn_continue_with_email.click()

        # Enter password
        field_password = self.driver.find_element_by_id("com.todoist:id/log_in_password")
        field_password.send_keys("abc12345")

        # Click on login button
        btn_login = self.driver.find_element_by_id("com.todoist:id/btn_log_in")
        btn_login.click()

        # Wait 5s for application to load
        sleep(5)

        # Ensure login is successful by checking if Today is shown
        # textview = self.driver.find_elements_by_class_name("android.widget.TextView")
        # listtext = [x.text for x in textview]
        # try:
        #     result = listtext.index("Today")
        # except ValueError:
        #     self.fail("Today page not shown after login, login may be unsuccessful")
    
    def tearDown(self):
        self.driver.quit()

    def test_create_project_and_task(self):
        # Click on the Change current view button
        btn_change_current_view = self.driver.find_element_by_accessibility_id("Change the current view")
        btn_change_current_view.click()

        # Wait for the side bar to load
        sleep(2)

        # Click on the expand button for Projects
        expand_project = self.driver.find_elements_by_id("com.todoist:id/collapse")[0]
        expand_project.click()

        # Wait for all the Projects to be shown
        sleep(2)

        # Get the list of projects and verify Test Project is created with API
        projects = self.driver.find_elements_by_id("com.todoist:id/name")
        project_texts = [x.text for x in projects]
        try:
            project_index = project_texts.index("Test Project")
        except ValueError:
            self.fail("Test Project not found under Projects, it may not been created successfully with the API")

        # Click on Test Project
        test_project = self.driver.find_elements_by_id("com.todoist:id/name")[project_index]
        test_project.click()

        # Click on Add button to create Task
        btn_add = self.driver.find_element_by_id("com.todoist:id/fab")
        btn_add.click()

        # Enter task name: Test task
        field_msg = self.driver.find_element_by_id("android:id/message")
        field_msg.send_keys("Test task")

        # Click on Send button
        btn_send = self.driver.find_element_by_id("android:id/button1")
        btn_send.click()
        self.driver.back()

        # Wait for task to be updated in server before calling API
        sleep(5)

        # Call API to retrieve active task
        return_value_task = requests.get(
            "https://api.todoist.com/rest/v1/tasks",
            params={
                "project_id": int(self.__class__.project_id)
            },
            headers={
                "Authorization": "Bearer %s" % self.__class__.token
            }).json()
        
        # Verify that Test task is created successfully
        list_content = [y["content"] for y in return_value_task]
        try:
            task_index = list_content.index("Test task")
            TestAppium.task_id = str(return_value_task[task_index]["id"])
        except ValueError:
            self.fail("Test task not found under Test Project")     
    
    def test_reopen_task(self):
        # Click on the Change current view button
        btn_change_current_view = self.driver.find_element_by_accessibility_id("Change the current view")
        btn_change_current_view.click()

        # Wait for the side bar to load
        sleep(2)

        # Click on the expand button for Projects
        expand_project = self.driver.find_elements_by_id("com.todoist:id/collapse")[0]
        expand_project.click()

        # Wait for all the Projects to be shown
        sleep(2)

        # Get the list of projects and verify Test Project is created with API
        projects = self.driver.find_elements_by_id("com.todoist:id/name")
        project_texts = [x.text for x in projects]
        try:
            project_index = project_texts.index("Test Project")
        except ValueError:
            self.fail("Test Project not found under Projects, it may not been created successfully with the API")

        # Click on Test Project
        test_project = self.driver.find_elements_by_id("com.todoist:id/name")[project_index]
        test_project.click()

        # Find Test task in the list
        tasks = self.driver.find_elements_by_id("com.todoist:id/text")
        tasks_text = [y.text for y in tasks]
        try:
            test_task_index = tasks_text.index("Test task")
        except ValueError:
            self.fail("Test task not found under Test Project")

        # Mark Test task as done
        test_task_checkmark = self.driver.find_elements_by_id("com.todoist:id/checkmark")[test_task_index]
        test_task_checkmark.click()

        # Wait for Test task to be updated in server
        sleep(5)

        # Reopen Test task using API
        requests.post("https://api.todoist.com/rest/v1/tasks/%s/reopen" % TestAppium.task_id, headers={"Authorization": "Bearer %s" % self.__class__.token})

        # Wait for Test task to be reopened in server
        sleep(3)

        # Pull down to refresh
        actions = TouchAction(self.driver)
        actions.long_press(x=500, y=500)
        actions.wait(ms=2000)
        actions.move_to(x=500, y=1500)
        actions.wait(ms=2000)
        actions.release()
        actions.perform()

        # Wait for refresh to be done
        sleep(3)

        # Check if Test task is reopened and appears in the list of tasks
        tasks = self.driver.find_elements_by_id("com.todoist:id/text")
        tasks_text = [y.text for y in tasks]
        try:
            test_task_index = tasks_text.index("Test task")
        except ValueError:
            self.fail("Test task is not reopened using API")


if __name__ == '__main__':
    unittest.main()