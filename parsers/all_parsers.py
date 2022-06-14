from config import brand_list
from parsers.product import Product


def parse_platform_product(platform, html_product):
    product = None
    match platform:
        case 'baucenter':
            product = bau_goods_parser(html_product)
        case 'dns':
            product = dns_goods_parser(html_product)
        case 'sdvor':
            product = sdvor_goods_parser(html_product)
    return product


def bau_goods_parser(html_product):
    cp = Product()
    tm = html_product['data-brand']
    if tm.upper() not in brand_list:
        return None
    cp.trade_mark = tm
    cp.id = int(html_product['data-article'])
    cp.name = html_product['data-name']
    link = html_product.find('a', attrs={'data-gtm-event': 'product_click'})['href']
    cp.url = f"https://baucenter.ru{link}"
    try:
        stock = html_product.find('div', class_='stock-list').p.text
        cp.status = ' '.join(stock.split())
    except AttributeError:
        cp.status = 'Отсутствуют в продаже'
    try:
        cp.price = float(html_product['data-price'])
    except AttributeError:
        cp.price = 'Нет данных'
    votes = html_product.find('div', class_='catalog_item_rating')
    if votes.text.strip():
        cp.vote_qt = votes.text.strip()
        percent = int(votes.find('div', class_='raiting-votes')['style'].split(':')[1][:-2])
        cp.vote_rating = (percent * 5) / 100
    return cp


def sdvor_goods_parser(html_product):
    cp = Product()
    cp.id = int(html_product.find('span', class_='code-value').text)
    link = html_product.find('a', class_='product-name')
    name = link.text.strip().split()
    cp.name = ' '.join(name)
    cp.url = 'https://www.sdvor.com' + link['href']
    try:
        price = html_product.find('div', class_='price').text.strip().split()[:-1]
        cp.price = float(''.join(price))
    except AttributeError:
        cp.price = None
    if 'Фотон'.upper() in cp.name.upper():
        cp.trade_mark = 'ФОТОН'
    elif 'Изолента'.upper() in cp.name.upper():
        cp.trade_mark = 'SafeLine'
    try:
        status = html_product.find('span', class_='shops-text check-availability').text
        if status == 'Проверить наличие':
            cp.status = 'Есть в наличии'
        else:
            cp.status = 'Нет данных'
    except Exception:
        cp.status = 'Нет в наличии'
    rating = html_product.find('div', class_='rating')
    if rating:
        stars = rating.find('sd-star-rating')['style'].split(':')[1][:-1]
        cp.vote_rating = float(stars)
        cp.vote_qt = int(rating.text.split()[0])
    return cp


def dns_goods_parser(html_product):
    cp = Product()
    cp.id = int(html_product['data-code'])
    cp.name = html_product.find('span').text
    cp.url = f"https://www.dns-shop.ru{html_product.find('a')['href']}"
    try:
        cp.status = html_product.find('div', class_='order-avail-wrap').text.strip()
    except AttributeError:
        cp.status = 'Отсутствуют в продаже'
    try:
        price = html_product.find('div', class_='product-buy__price').text.split('₽')[0].split()
        cp.price = int(''.join(price))
    except AttributeError:
        cp.price = 'Продажи прекращены'
    if 'ФОТОН' in cp.name.upper():
        cp.trade_mark = 'ФОТОН'
    votes = html_product.find('a', class_='catalog-product__rating ui-link ui-link_black')
    cp.vote_rating = votes['data-rating']
    cp.vote_rating = float(cp.vote_rating)
    cp.vote_qt = votes.text.strip()
    if cp.vote_qt == 'нет отзывов':
        cp.vote_qt = 0
    cp.vote_qt = int(cp.vote_qt)
    return cp
