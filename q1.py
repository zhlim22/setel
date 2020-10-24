import unittest
import uuid, requests, json
from appium import webdriver
from time import sleep

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
    
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()