import os
import random
import time
import urllib.parse
from threading import Thread
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config import selenium_arguments, browser_path, blocklist, search_phrases, shops, today
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utilites import write_html


class PageGetter(Thread):
    def __init__(self, platform):
        super().__init__()
        self.shop = platform
        self.browser = None
        self.phrases = list(set(search_phrases) - set(blocklist[platform]))
        self.cur_phrase = None
        self.current_url = None
        self.html_dir = f'htmls/{today}/'
        self.has_pagination = 0
        self.html_data = None
        self.soup = None
        self.page_pos = None
        self.first_page_wait_time = 0

    def run(self):
        self.check_html_dir()
        self.initiate_browser()
        for self.cur_phrase in self.phrases:
            self.page_pos, self.has_pagination = 0, 0
            self.get_first_page()
            if self.has_pagination:
                self.get_other_pages()
        if self.browser:
            self.browser.close()

    def check_html_dir(self):
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)

    def initiate_browser(self):
        options = webdriver.ChromeOptions()
        for arg in selenium_arguments:
            options.add_argument(arg)
        self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def generate_url(self):
        platform = self.shop
        shop_url = shops[platform]
        pos = self.page_pos
        phrase = self.cur_phrase
        query = urllib.parse.quote_plus(phrase, safe='', encoding=None, errors=None)
        match platform:
            case 'akson':
                self.current_url = f'https://akson.ru/search/?q={query}'
            case 'baucenter':
                pagination = f'&PAGEN_1={pos}' if pos > 1 else ''
                self.current_url = f'{shop_url}search/?q={query}{pagination}'
            case 'dns':
                end = f'&p={pos}' if pos > 1 else ''
                self.current_url = f'https://www.dns-shop.ru/search/?q={query}{end}'
            case 'maxidom':
                link = f'https://www.maxidom.ru/search/catalog/?q={query}&category_search=0&amount=12'
                self.current_url = link + f'&PAGEN_2={pos}' if pos > 1 else link
            case 'sdvor':
                self.current_url = f'https://www.sdvor.com/moscow/search/{query}'
            case 'votonia':
                self.current_url = f'https://www.votonia.ru/search/{query}/'
        pag = self.has_pagination if self.has_pagination else 'FF'
        print(f'{platform:>9} {phrase:8} {pos:02}/{pag :02}, connect to {self.current_url}')

    def get_first_page(self):
        if self.shop == 'dns':
            self.first_page_wait_time = 10
        self.get_page()
        self.first_page_wait_time = 0
        self.soup = BeautifulSoup(self.browser.page_source, 'lxml')
        try:
            self.get_last_page_number()
        except Exception as ex:
            print(f'{self.shop}, getting last page number error...', ex)
            self.has_pagination = 0

    def get_page(self):
        self.generate_url()
        self.browser.get(url=self.current_url)
        time.sleep(self.first_page_wait_time)
        self.scroll_down()
        time.sleep(random.randint(3, 10))
        write_html(self.browser.page_source, f'{self.html_dir}/{self.shop}_{self.cur_phrase}_{self.page_pos:03d}.html')

    def get_other_pages(self):
        for self.page_pos in range(2, self.has_pagination + 1):
            self.get_page()

    def scroll_down(self):
        match self.shop:
            case 'akson':
                self.scroll_down_akson()
            case 'baucenter':
                self.scroll_down_classic()
            case 'sdvor':
                pass
            case 'votonia':
                self.scroll_down_votonia(wait=2)
        time.sleep(1)
        self.browser.execute_script(f"window.scrollTo(0, 0);")
        time.sleep(2)

    def scroll_down_classic(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.simple_to_bottom()
        self.browser.execute_script(f"window.scrollTo(0, {last_height - 1500});")

    def scroll_down_akson(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(1)
        for i in range(1, 5):
            self.browser.execute_script(f"window.scrollTo(0, {last_height - 500 * i});")
            time.sleep(1)
        self.simple_to_bottom(wait=3)

    def scroll_down_votonia(self, wait=10):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        while True:
            try:
                more_button = self.browser.find_elements_by_class_name("pager-info-block")
                # self.browser.find_element_by_css_selector('pager-info-block').click()
                more_button.click()
                time.sleep(wait)
            except Exception as ex:
                print(self.shop, ex)
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(wait)
            if new_height == last_height:
                break
            last_height = new_height

    def get_last_page_number(self):
        match self.shop:
            case 'akson':
                pass
            case 'baucenter':
                self.has_pagination = int(self.soup.find('nav', class_='pagination').find_all('a')[-2].text)
            case 'dns':
                pag_block = self.soup.find('ul', class_='pagination-widget__pages')
                self.has_pagination = int(pag_block.find_all('li')[-1]['data-page-number'])
            case 'maxidom':
                li = self.soup.find('div', class_='pager-catalogue__search').find_all('li')
                self.has_pagination = int(li[-2].text.strip())
            case 'sdvor':
                self.has_pagination = 0

    def simple_to_bottom(self, wait=1):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(wait)
        while True:
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(wait)
            if new_height == last_height:
                break
            last_height = new_height
