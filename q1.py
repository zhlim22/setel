import unittest
import uuid, requests, json
from appium import webdriver
from time import sleep

class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token = "f6b71ac9fc1d627bd818265c369b7eb468318d07"
        return_value = requests.post(
            "https://api.todoist.com/rest/v1/projects",
            data=json.dumps({
                "name": "Movies to watch"
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": "Bearer %s" % cls.token
            }).json()
        cls.project_id = str(return_value["id"])
        print(cls.project_id)
    
    @classmethod
    def tearDownClass(cls):
        requests.delete("https://api.todoist.com/rest/v1/projects/%s" % cls.project_id, headers={"Authorization": "Bearer %s" % cls.token})

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.todoist'
        desired_caps['appActivity'] = 'com.todoist.activity.HomeActivity'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
    
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()