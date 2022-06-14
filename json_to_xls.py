import json
import math
from openpyxl import Workbook
from utilites import check_dir


class XlsConverter:
    def __init__(self, filename):
        self.load_filename = f'json_results/{filename}'
        self.goods_dict = {}
        self.workbook = Workbook()
        self.date = filename.split('.')[0]

    def run(self):
        self.open_json()
        self.initiate_workbook()
        self.combine_data_to_write()
        check_dir('xls_results')
        self.workbook.save(f"xls_results/{self.date}.xlsx")

    def open_json(self):
        with open(self.load_filename, 'r', encoding='utf8') as json_file:
            self.goods_dict = json.load(json_file)

    def combine_data_to_write(self):
        sw = self.workbook.active
        for shop in self.goods_dict:
            shop_goods = self.goods_dict[shop]
            for shop_id in shop_goods:
                merch = shop_goods[shop_id]
                qt = merch['vote_qt']
                rating = merch['vote_rating']
                if rating > 4 and qt > 1:
                    need = 0
                else:
                    need = math.ceil(qt * abs(4.1 - rating)) if rating else 2
                data = [shop, int(shop_id), merch['brand'], merch['name'], merch['url'], merch['status'],
                        merch['price'], rating, qt, need]
                sw.append(data)

    def initiate_workbook(self):
        title = ['Магазин', 'shop id', 'brand', 'Наименование', 'url', 'статус',
                 'price', 'рейтинг', 'количество голосов', 'требуется оценок']
        ws = self.workbook.active
        ws.append(title)
        print(ws[1])
        ws.column_dimensions['D'].width = 30
