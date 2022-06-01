import json
from openpyxl import Workbook


class XlsConverter:
    def __init__(self, filename):
        self.load_filename = f'json_results/{filename}'
        self.goods_dict = {}

    def run(self):
        self.open_json()

    def open_json(self):
        with open(self.load_filename, 'r') as json_file:
            self.goods_dict = json.load(json_file)
