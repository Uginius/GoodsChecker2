import time

from bs4 import BeautifulSoup

from config import selenium_arguments, browser_path, wait_time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utilites import time_track


class VotoniaRatingUpdate:
    def __init__(self, shop_goods):
        self.goods = shop_goods
        self.browser = None

    def run(self):
        self.initiate_browser()
        self.get_products()
        if self.browser:
            self.browser.close()

    def initiate_browser(self):
        options = webdriver.ChromeOptions()
        for arg in selenium_arguments:
            options.add_argument(arg)
        self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def out_goods_data(self):
        return self.goods

    @time_track
    def get_products(self):
        goods = self.goods
        for shop_id in goods:
            merch = goods[shop_id]
            url = merch['url'] + '#tab-review'
            self.browser.get(url=url)
            time.sleep(2)
            soup = BeautifulSoup(self.browser.page_source, 'lxml').find('div', id='pj_product_info')
            try:
                merch['vote_rating'] = float(soup.find('div', class_='review_info_line').b.text.strip('"'))
            except AttributeError:
                merch['vote_rating'] = 0
            try:
                merch['vote_qt'] = int(soup.find('a', attrs={'href': '#tab-review'}).text.split()[1].strip('()'))
            except AttributeError:
                merch['vote_qt'] = None
            pass
