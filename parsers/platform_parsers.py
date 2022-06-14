from config import brand_list
from parsers.all_parsers import parse_platform_product


class FatherPlatformParser:
    def __init__(self, platform):
        self.soup = None
        self.goods_list = None
        self.cp = None
        self.search_index_number = 0
        self.shop = platform
        self.html_product = None
        self.parsed_dict = {}

    def run(self):
        try:
            self.get_goods_list()
        except Exception as ex:
            print('Goods list loading error', ex)
        if self.goods_list:
            self.parse_goods_list()

    def get_goods_list(self):
        match self.shop:
            case 'baucenter':
                catalog = self.soup.find('div', class_='catalog-list')
                self.goods_list = catalog.find_all('div', class_='catalog_item with-tooltip')
            case 'dns':
                self.goods_list = self.soup.find_all('div', attrs={'data-id': 'product'})
            case 'sdvor':
                self.goods_list = self.soup.find_all('sd-product-grid-item', class_='product-grid-item')

    def parse_goods_list(self):
        for self.html_product in self.goods_list:
            cp = parse_platform_product(platform=self.shop, html_product=self.html_product)
            if not cp:
                continue
            if not cp.trade_mark:
                continue
            if cp.trade_mark.upper() not in brand_list:
                continue
            if cp.url:
                self.parsed_dict.update(cp.json_items())
