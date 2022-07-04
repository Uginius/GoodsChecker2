import json
import os
from bs4 import BeautifulSoup
from config import shops
from parsers.platform_parsers import FatherPlatformParser
from utilites import check_dir


class HtmlFilesParser:
    def __init__(self, last_date):
        self.last_dir = 'htmls/' + last_date
        self.files = os.listdir(self.last_dir)
        self.shop, self.parser, self.soup = None, None, None
        self.goods = {pl: {} for pl in shops}
        self.json_results_dir = f'json_results/'
        check_dir(self.json_results_dir)
        self.json_file = f'{self.json_results_dir}{last_date}.json'

    def run(self):
        for filename in self.files:
            if filename == '.DS_Store':
                continue
            self.shop = filename.split('_')[0]
            self.open_file(filename)
            self.parse_page()
        self.write_json()

    def open_file(self, name):
        filename = f'{self.last_dir}/{name}'
        print(f'******* open {filename}')
        with open(filename, 'r', encoding='utf8') as read_file:
            src = read_file.read()
        self.soup = BeautifulSoup(src, 'lxml')

    def parse_page(self):
        par = FatherPlatformParser(self.shop)
        par.soup = self.soup
        par.run()
        self.goods[self.shop].update(par.parsed_dict)

    def write_json(self):
        json_file = self.json_file
        with open(json_file, 'w', encoding='utf8') as write_file:
            json.dump(self.goods, write_file, ensure_ascii=False)
