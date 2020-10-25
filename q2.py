from selenium import webdriver
from time import sleep
import unittest

class TestEcommerce(unittest.TestCase):
    # Setting links for Amazon and eBay
    amazon_link = "https://amazon.com"
    ebay_link = "https://ebay.com"

    def setUp(self):
        # Setup webdriver
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(10)

    def tearDown(self):
        # Close webdriver after test
        self.driver.quit()

    def test_amazon(self):
        # Open Amazon webpage
        self.driver.get(self.amazon_link)

        # Enter iPhone 11 into search box
        searchbox = self.driver.find_element_by_id("twotabsearchtextbox")
        searchbox.send_keys("iPhone 11")

        # Click on search button
        btn_search = self.driver.find_element_by_id("nav-search-submit-text")
        btn_search.click()

        # Wait for webpage to load
        sleep(2)

        # Get Name, Price and Link of products in search results
        list_product_name = [x.text for x in self.driver.find_elements_by_xpath("//span[@class='a-size-medium a-color-base a-text-normal']")]
        list_product_price = [x.get_attribute("innerHTML") for x in self.driver.find_elements_by_xpath("//span[@class='a-offscreen']")]
        list_product_link = [x.get_attribute('href') for x in self.driver.find_elements_by_xpath("//a[@class='a-link-normal a-text-normal']")]

        # Validating that results are correct
        for i in list_product_name:
            if i.find("iPhone") == -1 and i.find("11") == -1:
                print("Keywords 'iPhone' or '11' not found in the result: " + i)

        # Adding Name of website Key to list of search results
        results_amazon = [{'Name': name, 'Price': price, 'Link': link} for name,price,link in zip(list_product_name,list_product_price,list_product_link)]
        for i in results_amazon:
            i["Name of Website"] = "Amazon"

    # def test_ebay(self):
    #     self.driver.get(self.ebay_link)

if __name__ == '__main__':
    unittest.main()