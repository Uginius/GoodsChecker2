import json
import os
import re
import time
from datetime import datetime
from config import dir_date_template, date_pattern


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nIt takes {elapsed:.3f} sec, or {elapsed/60:.3f} min')
        return result

    return surrogate


def write_json_items(filename, data):
    with open(filename, "a") as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')


def write_html(src, filename):
    with open(filename, 'w', encoding='utf8') as write_file:
        write_file.write(src)


def get_last_dir():
    pages_dir_from_os = os.listdir('htmls')
    loaded_dirs = []
    for el in pages_dir_from_os:
        checking_dir = re.findall(dir_date_template, el)
        try:
            if checking_dir:
                dir_in_list = datetime.strptime(el, date_pattern)
                loaded_dirs.append(dir_in_list)
        except ValueError as ex:
            print(ex)
    final_dir = sorted(loaded_dirs)[-1].strftime(date_pattern)
    return final_dir


def last_json_file():
    jsf = {}
    for filename in os.listdir("json_results"):
        find_date = re.findall(dir_date_template, filename)
        if find_date:
            jsf[datetime.strptime(find_date[0], date_pattern)] = filename
    dates = jsf.keys()
    last = sorted(dates)[-1]
    return jsf[last]


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
