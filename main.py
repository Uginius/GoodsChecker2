from config import shops
from get_pages import PageGetter
from json_to_xls import XlsConverter
from parse_html_files import HtmlFilesParser
from utilites import time_track, get_last_dir, last_json_file


@time_track
def get_pages():
    pages_from_shop_list = [PageGetter(platform) for platform in shops]
    for page in pages_from_shop_list:
        print(f'****** start to get pages from {page.shop}')
        page.run()


@time_track
def parse_pages():
    pages_parser = HtmlFilesParser(get_last_dir())
    pages_parser.run()


@time_track
def convert_json_to_xls():
    conv = XlsConverter(last_json_file())
    conv.run()


if __name__ == '__main__':
    # get_pages()
    # parse_pages()
    convert_json_to_xls()
