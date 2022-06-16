import json


class Product:
    def __init__(self):
        self.id = None
        self.rosel_id = None
        self.shop_name = None
        self.name = ''
        self.url = None
        self.trade_mark = None
        self.status = None
        self.price = 0
        self.index = None
        self.vote_rating = None
        self.vote_qt = None

    def out_items(self):
        return self.id, self.name, self.url, self.status, self.price

    def json_items(self):
        return {
            self.id: {
                'brand': self.trade_mark,
                'name': self.name,
                'url': self.url,
                'status': self.status,
                'price': self.price,
                'vote_rating': self.vote_rating,
                'vote_qt': self.vote_qt,
                'rosel_id': self.rosel_id,
                # 'index': self.index
            }
        }

    def json_items_write(self):
        with open('json_result_data.json', "a") as file:
            json.dump(self.json_items(), file, ensure_ascii=False)
            file.write('\n')
