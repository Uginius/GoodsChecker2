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
        self.pag = None
        self.html_data = None
        self.soup = None
        self.page_pos = None

    def run(self):
        self.check_html_dir()
        self.initiate_browser()
        for self.cur_phrase in self.phrases:
            self.page_pos = 1
            self.get_first_page()
            if self.pag:
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
        match self.shop:
            case 'baucenter':
                pagination = f'&PAGEN_1={self.page_pos}' if self.page_pos > 1 else ''
                self.current_url = f'{shop_url}search/?q={self.cur_phrase}{pagination}'
            case 'sdvor':
                self.current_url = f'https://www.sdvor.com/moscow/search/{self.cur_phrase}'
        print('connect to', self.current_url)

    def get_first_page(self):
        self.get_page()
        self.soup = BeautifulSoup(self.html_data, 'lxml')
        try:
            self.get_last_page_number()
        except IndexError:
            self.pag = None

    def get_page(self):
        self.generate_url()
        self.browser.get(url=self.current_url)
        self.scroll_down()
        time.sleep(wait_time)
        self.html_data = self.browser.page_source
        write_html(self.html_data, f'{self.html_dir}/{self.shop}_{self.cur_phrase}_{self.page_pos:03d}.html')

    def get_other_pages(self):
        for self.page_pos in range(2, self.pag + 1):
            self.get_page()

    def scroll_down(self):
        match self.shop:
            case 'baucenter':
                self.scroll_down_classic()
            case 'sdvor':
                pass

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

    def get_last_page_number(self):
        match self.shop:
            case 'baucenter':
                self.last_page_number_bau()
            case 'sdvor':
                self.pag = None

    def last_page_number_bau(self):
        try:
            self.pag = int(self.soup.find('nav', class_='pagination').find_all('a')[-2].text)
        except AttributeError:
            self.pag = 1
