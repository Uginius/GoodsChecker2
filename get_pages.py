import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from config import selenium_arguments, browser_path, blocklist, search_phrases, wait_time, shops
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utilites import write_html


class PageGetter:
    def __init__(self, platform):
        self.shop = platform
        self.browser = None
        self.phrases = list(set(search_phrases) - set(blocklist[platform]))
        self.cur_phrase = None
        self.current_url = None
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.html_dir = f'htmls/{self.date}/'
        self.has_pagination = 0
        self.html_data = None
        self.soup = None
        self.page_pos = None

    def run(self):
        self.check_html_dir()
        self.initiate_browser()
        for self.cur_phrase in self.phrases:
            self.page_pos = 1
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
        shop_url = shops[self.shop]
        query, pos = self.cur_phrase, self.page_pos
        match self.shop:
            case 'akson':
                self.current_url = f'https://akson.ru/search/?q={query}'
            case 'baucenter':
                pagination = f'&PAGEN_1={pos}' if pos > 1 else ''
                self.current_url = f'{shop_url}search/?q={query}{pagination}'
            case 'dns':
                self.current_url = f'https://www.dns-shop.ru/search/?q={query}&p={pos}'
            case 'maxidom':
                link = f'https://www.maxidom.ru/search/catalog/?q={query}&category_search=0&amount=12'
                self.current_url = link + f'&PAGEN_2={pos}' if pos > 1 else link
            case 'sdvor':
                self.current_url = f'https://www.sdvor.com/moscow/search/{query}'
            case 'votonia':
                self.current_url = f'https://www.votonia.ru/search/{query}/'
        print('connect to', self.current_url)

    def get_first_page(self):
        self.get_page()
        self.soup = BeautifulSoup(self.browser.page_source, 'lxml')
        try:
            self.get_last_page_number()
        except Exception as ex:
            print('getting last page number error...', ex)
            self.has_pagination = 0

    def get_page(self):
        self.generate_url()
        self.browser.get(url=self.current_url)
        self.scroll_down()
        time.sleep(wait_time)
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
                self.scroll_down_votonia()

    def scroll_down_classic(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        while True:
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(0.5)
            if new_height == last_height:
                break
            last_height = new_height
        self.browser.execute_script(f"window.scrollTo(0, {last_height - 1500});")

    def scroll_down_akson(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(1)
        for i in range(1, 5):
            self.browser.execute_script(f"window.scrollTo(0, {last_height - 500 * i});")
            time.sleep(1)
        while True:
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_down_votonia(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        while True:
            try:
                self.browser.find_element_by_css_selector('.pager-info-block').click()
            except Exception as ex:
                print(ex)
            time.sleep(1)
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(1)
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
