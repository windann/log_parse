# -*- encoding: utf-8 -*-

from collections import Counter
import re
from datetime import datetime


def urls_with_inf(data):
    url_inf_list = []

    date_pattern = r'\d{2}\/\w{3}\/\d{4}\s\d{2}:\d{2}:\d{2}'
    type_request_pattern = r'"\w{3,7}'
    pattern = r'\w{2,4}p?\w:\/\/'

    for elem in data:
        elem_url_inf = {}
        if re.search(date_pattern, elem) and re.search(type_request_pattern, elem) and re.search(pattern, elem):
            elem_url_inf['date'] = re.findall(date_pattern, elem)[0]
            elem_url_inf['request'] = re.findall(type_request_pattern, elem)[0].lstrip('"')
            elem_url_inf['url'] = re.sub(pattern, '://', elem.split('?')[0].split()[3], count=0)
            elem_url_inf['time'] = elem.split()[6]
            url_inf_list.append(elem_url_inf)

    return url_inf_list


def start_at_func(start_at, data):
    urls_date = [(datetime.strptime(elem['date'], '%d/%b/%Y %H:%M:%S'),elem['url']) for elem in urls_with_inf(data)]
    return [url[1] for url in urls_date if url[0] >= start_at]


def stop_at_func(stop_at, data):
    urls_date = [(datetime.strptime(elem['date'].split()[0], '%d/%b/%Y %H:%M:%S'), elem['url']) for elem in urls_with_inf(data)]
    return [url[1] for url in urls_date if url[0] <= stop_at]


def ignore_files_func(urls):
    pattern = r'\.\w{2,3}$'
    return [url for url in urls if not re.search(pattern, url.split('/')[0])]


def ignore_urls_func(urls,ignore_urls):
    pattern = r'\w{2,4}p?\w:\/\/'
    new_ignore_urls = [re.sub(pattern, '://', url, count=0) for url in ignore_urls]
    return [re.sub(pattern, '://', url, count=0) for url in urls if url not in new_ignore_urls]


def request_type_func(data, urls, request_type):
    urls_type = [(elem['request'], elem['url']) for elem in urls_with_inf(data)]
    return [url[1] for url in urls_type if url[1] in urls and url[0] == request_type]


def slow_queries_func(urls,data):
    new_urls = []
    new_urls_time = []
    urls_time = [(elem['url'],int(elem['time'])) for elem in urls_with_inf(data)]
    for url_t in urls_time:
        if url_t[0] in urls:
            new_urls_time.append(url_t)
            new_urls.append(url_t[0])

    c_t = dict(Counter(new_urls))
    avg_list = []

    for url,kol in c_t.items():
        summ = 0
        for url_t in new_urls_time:
            if url == url_t[0]:
                summ += url_t[1]

        avg_list.append(summ//kol)
        avg_list.sort(reverse=True)

    return avg_list[:5]


def parse(ignore_urls=[],
          start_at=None,
          stop_at=None,
          request_type=None,
          ignore_www=False,
          slow_queries=False,
          ignore_files=False):
    with open('log.log', 'r') as f:
        # вся информация из файла, типы запросов, урлы, дата и т.д
        data = f.read().split('\n')

    urls = [elem['url'] for elem in urls_with_inf(data)]

    if start_at:
        urls = start_at_func(start_at, data)

    if stop_at:
        urls = stop_at_func(stop_at, data)

    if ignore_www:
        pattern = r':\/\/www\.'
        urls = [url.replace('://www.','://') if re.search(pattern, url) else url for url in urls]

    if ignore_files:
        urls = ignore_files_func(urls)

    if ignore_urls:
        urls = ignore_urls_func(urls, ignore_urls)

    if request_type:
        urls = request_type_func(data,urls,request_type)

    if slow_queries:
        return slow_queries_func(urls,data)

    c = Counter(urls).most_common(5)

    return [elem[1] for elem in c]



