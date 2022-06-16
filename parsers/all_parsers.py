from config import brand_list
from parsers.product import Product


def parse_platform_product(platform, html_product):
    product = None
    match platform:
        case 'akson':
            product = akson_goods_parser(html_product)
        case 'baucenter':
            product = bau_goods_parser(html_product)
        case 'dns':
            product = dns_goods_parser(html_product)
        case 'maxidom':
            product = maxidom_goods_parser(html_product)
        case 'sdvor':
            product = sdvor_goods_parser(html_product)
        case 'votonia':
            product = votonia_goods_parser(html_product)
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
        if 'Интернет-магазин' in cp.status:
            cp.status = 'в наличии'
    except AttributeError:
        cp.status = 'Отсутствуют в продаже'
    try:
        cp.price = float(html_product['data-price'])
    except AttributeError:
        cp.price = 'Нет данных'
    votes = html_product.find('div', class_='catalog_item_rating')
    if votes.text.strip():
        cp.vote_qt = int(votes.text.strip())
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
            cp.status = 'в наличии'
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
        if cp.status == 'Товара нет в наличии':
            cp.status = 'Нет в наличии'
        if 'В наличии:' in cp.status or 'В магазинах:' in cp.status:
            cp.status = 'в наличии'
    except AttributeError:
        cp.status = 'Отсутствуют в продаже'
    try:
        price = html_product.find('div', class_='product-buy__price').text.split('₽')[0].split()
        cp.price = int(''.join(price))
    except AttributeError:
        cp.price = 'Продажи прекращены'
        return None
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


def akson_goods_parser(html_prod):
    cp = Product()
    cp.name = html_prod.find('a', class_='info-title text-body-regular text-color-headline').text
    not_rosel_brand, cp.trade_mark = check_brand_for_akson(cp.name.upper())
    if not_rosel_brand:
        return
    cp.id = int(html_prod.find('div', class_='info-code mb-1 text-body-regular text-color-secondary').text.split()[1])
    cp.url = f"https://akson.ru{html_prod.find('a')['href']}"
    try:
        button_text = html_prod.find('button').text
        if button_text == 'В корзину':
            cp.status = 'в наличии'
    except AttributeError:
        cp.status = 'Отсутствуют в продаже'
    try:
        price = html_prod.find('span', class_='info-price__value text-header-l-bold').text.split()
        cp.price = float(''.join(price))
    except AttributeError:
        cp.price = 'Продажи прекращены'
    rate = html_prod.find('span', class_='rating')
    stars = rate.find('span', class_='stars__block stars__block_fill')['style']
    percent = int(stars.split(':')[1][:-2])
    cp.vote_rating = (percent * 5) / 100
    cp.vote_qt = int(rate.text.split('(')[1].split(')')[0])
    pass
    return cp


def check_brand_for_akson(name):
    trade_mark = None
    brandlist = ['ФОТОН', 'РЕКОРД', 'КОНТАКТ', 'SafeLine']
    for brand in brandlist:
        if brand.upper() in name:
            trade_mark = brand
            break
    stop_words = ['Бетон', 'Планка', 'Профиль', 'Фотообои', 'Очаг', 'Разъем', 'Фоторамка', 'Портал', 'Секатор']
    for word in stop_words:
        no_our_brand = word.upper() in name
        if no_our_brand:
            return True, None
    return False, trade_mark


def maxidom_goods_parser(html_product):
    cp = Product()
    art_block = html_product.find_all('small', class_="sku")
    split_rosel_id = art_block[0].text.split()[1].replace('.', '')
    split_id = art_block[1].text.split()[-1]
    cp.id = int(split_id)
    if '/' in split_rosel_id:
        split_rosel_id = split_rosel_id.split('/')[0]
    try:
        cp.rosel_id = int(split_rosel_id)
    except ValueError:
        cp.rosel_id = None
    cp.trade_mark = art_block[2].text.split(':')[1].strip()
    link = html_product.find(attrs={'itemprop': 'name'})
    cp.name = link.text
    cp.url = 'https://www.maxidom.ru' + link['href']
    cp.status = html_product.find('div', class_='item-controls').span.text.strip()
    cp.price = float(html_product.find('span', class_='price-list').text.split(',-')[0].strip().replace(' ', ''))
    return cp


def votonia_goods_parser(html_product):
    cp = Product()
    cp.id = html_product['data-id']
    link = html_product.find('a', class_='product_link')
    cp.name = link.text.strip()
    cp.url = 'https://www.votonia.ru' + link['href']
    cp.price = float(html_product['data-market'])
    cp.trade_mark = 'Фотон'
    cp.status = html_product.find('div', class_='reach_line reach1').text.strip()
    return cp
