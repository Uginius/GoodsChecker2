import datetime
import sys

brand_list = ['ФОТОН', 'КОНТАКТ', 'РЕКОРД', 'SAFELINE']

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
date_pattern = "%Y-%m-%d"
today = datetime.datetime.now().strftime(date_pattern)
dir_date_template = r'202\d-\d{2}-\d{2}'

match sys.platform:
    case 'linux':
        browser_path = 'chromedriver_linux64/chromedriver'
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
    case 'darwin':
        browser_path = 'drivers/chromedriver'
        user_agent = None
    case 'win32':
        browser_path = 'drivers/chromedriver.exe'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    case _:
        print("ERROR: can't found selenium driver")
        user_agent = None

selenium_arguments = [f'user-agent={user_agent}', '--disable-blink-features=AutomationControlled']
req_headers = {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'user-agent': user_agent}

