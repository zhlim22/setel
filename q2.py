from selenium import webdriver
from time import sleep
import unittest
from pprint import pprint

class TestEcommerce(unittest.TestCase):
    # Setting links for Amazon and eBay
    amazon_link = "https://amazon.com"
    ebay_link = "https://ebay.com"
    results_amazon = []
    results_ebay = []

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

        # Merging the lists into a dictionary
        TestEcommerce.results_amazon = [{'Name': name, 'Price': price, 'Link': link} for name,price,link in zip(list_product_name,list_product_price,list_product_link)]

        # Validating and removing results without keyword 'iPhone' and '11'
        TestEcommerce.results_amazon = [i for i in TestEcommerce.results_amazon if not (i['Name'].find("iPhone") == -1 and i['Name'].find("11") == -1)]

        # Adding Name of website Key to list of search results
        for i in TestEcommerce.results_amazon:
            i["Name of Website"] = "Amazon"
        
    def test_ebay(self):
        self.driver.get(self.ebay_link)

        # Enter iPhone 11 into search box
        searchbox = self.driver.find_element_by_id("gh-ac")
        searchbox.send_keys("iPhone 11")

        # Click on search button
        btn_search = self.driver.find_element_by_id("gh-btn")
        btn_search.click()

        # Wait for webpage to load
        sleep(2)

        # Get Name, Price and Link of products in search results
        list_product_name = [x.text for x in self.driver.find_elements_by_xpath("//h3[@class='s-item__title']")]
        list_product_price = [x.text for x in self.driver.find_elements_by_xpath("//span[@class='s-item__price']")]
        list_product_link = [x.get_attribute('href') for x in self.driver.find_elements_by_xpath("//a[@class='s-item__link']")]
        
        # Merging the lists into a dictionary
        TestEcommerce.results_ebay = [{'Name': name, 'Price': price, 'Link': link} for name,price,link in zip(list_product_name,list_product_price,list_product_link)]

        # Validating and removing results without keyword 'iPhone' and '11'
        TestEcommerce.results_ebay = [i for i in TestEcommerce.results_ebay if not (i['Name'].find("iPhone") == -1 and i['Name'].find("11") == -1)]

        # Adding Name of website Key to list of search results
        for i in TestEcommerce.results_ebay:
            i["Name of Website"] = "eBay"

    def test_print_results(self):
        # Combining the list of results
        combined_results = TestEcommerce.results_amazon + TestEcommerce.results_ebay

        # Sorting the results based on Price in ascending order
        combined_results = sorted(combined_results, key = lambda i: float(i['Price'].strip("$").replace(",","").split(" ", 1)[0]))

        # Printing the list of results
        pprint(combined_results)



if __name__ == '__main__':
    unittest.main()