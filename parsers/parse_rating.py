import time
import requests
from random import randint
from threading import Thread
from bs4 import BeautifulSoup
from config import req_headers


class RatingParser(Thread):
    def __init__(self, shop_goods):
        super().__init__()
        self.goods = shop_goods
        self.merch = None

    def run(self):
        ll = len(self.goods)
        for num, shop_id in enumerate(self.goods):
            self.merch = self.goods[shop_id]
            vote_qt = self.merch['vote_qt']
            if vote_qt or vote_qt == 0:
                continue
            url = self.set_url(shop_id)
            print(f"{num + 1:03}/{ll}: Connecting to {url}")
            req = requests.get(url, headers=req_headers)
            time.sleep(randint(0, 3))
            self.get_product_data(BeautifulSoup(req.text, 'lxml'))

    def set_url(self, shop_id):
        return self.merch['url']

    def get_product_data(self, url):
        pass

    def out_goods_data(self):
        return self.goods


class MaxidomRatingUpdate(RatingParser):
    def __init__(self, shop_goods):
        super().__init__(shop_goods)

    def set_url(self, shop_id):
        return f"https://www.maxidom.ru/ajax/mneniya_pro/getReviewsHtml.php?SKU_ID={shop_id}"

    def get_product_data(self, soup):
        merch = self.merch
        try:
            merch['vote_rating'] = float(soup.find('div', class_='score__number').text)
        except ValueError:
            merch['vote_rating'] = 0
        try:
            score_block = soup.find('div', class_='score-rating').find_all('div', class_='scale__number')
            votes_list = [int(votes.text) for votes in score_block]
            merch['vote_qt'] = sum(votes_list)
        except ValueError:
            merch['vote_qt'] = 0


class VotoniaRatingUpdate(RatingParser):
    def __init__(self, shop_goods):
        super().__init__(shop_goods)

    def get_product_data(self, soup):
        merch = self.merch
        try:
            merch['vote_rating'] = float(soup.find('div', class_='review_info_line').b.text.strip('"'))
        except AttributeError:
            merch['vote_rating'] = 0
        try:
            merch['vote_qt'] = int(soup.find('a', attrs={'href': '#tab-review'}).text.split()[1].strip('()'))
        except AttributeError:
            merch['vote_qt'] = 0
