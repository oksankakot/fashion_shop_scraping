from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector


link = "https://www.farfetch.com/ca/shopping/women/dresses-1/items.aspx"


path_to_chromedriver = r"C:\Users\User\Desktop\chromedriver-win64\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(path_to_chromedriver)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(link)
temp_test = driver.find_element(By.TAG_NAME, "body")
elem = temp_test.get_attribute('innerHTML')


selectors = {
    'item_group_id': Selector(text=elem).css('div[itemid]').get(),
    'mpn': Selector(text=elem).css('div[itemid]').get(),
    'id': Selector(text=elem).xpath('//*[@itemID or @data-ffref]').extract(),
    'title': Selector(text=elem).xpath('//*[@data-component="ProductCardDescription"]').extract(),
    'image_link': Selector(text=elem).xpath('//*[@data-component="ProductCardImagePrimary"]').extract(),
    'link': Selector(text=elem).xpath('//*[@data-component="ProductCardLink"]').extract(),
    'gender': Selector(text=elem).css('a[data-testid="header-department-141259"]').get(),
    'brand': Selector(text=elem).xpath('//*[@data-component="ProductCardBrandName"]').extract(),
    'availability': Selector(text=elem).xpath('//*[@data-component="ProductCardSizesAvailable"]').extract(),
    'price': Selector(text=elem).xpath('//*[@data-component="Price"]').extract()
}
print(selectors)
