import sys

brand_list = ['ФОТОН', 'КОНТАКТ', 'РЕКОРД', 'SAFELINE']

wait_time = 3
shops = {
    'akson': 'https://akson.ru/',
    'baucenter': 'https://baucenter.ru/',
    'dns': 'https://www.dns-shop.ru/',
    'maxidom': 'https://www.maxidom.ru/',
    'sdvor': 'https://www.sdvor.com/moscow',
    'votonia': 'https://www.votonia.ru/'
}
blocklist = {
    'akson': ['рекорд'],
    'baucenter': [],
    'dns': ['контакт', 'safeline', 'рекорд'],
    'maxidom': [],
    'sdvor': ['контакт', 'рекорд'],
    'votonia': ['контакт', 'рекорд', 'safeline'],
}

search_phrases = ['фотон', 'контакт', 'рекорд', 'safeline']
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
selenium_arguments = [
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    '--disable-blink-features=AutomationControlled'
]

match sys.platform:
    case 'linux':
        browser_path = 'drivers/chromedriver_linux64_99.0.4844.51/chromedriver'
    case 'darwin':
        browser_path = 'drivers/chromedriver'
    case 'win32':
        browser_path = 'drivers/chromedriver.exe'
    case _:
        print("ERROR: can't found selenium driver")

req_headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
