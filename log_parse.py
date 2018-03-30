# -*- encoding: utf-8 -*-

from collections import Counter
import re
import datetime


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


def start_at_func(start_at, urls,data):
    when_start = 0
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf(data)]

    for elem in urls_date:
        when_start += 1

        if start_at in elem:
            break

    return [url for url in urls[when_start:]]


def stop_at_func(stop_at, urls,data):
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf(data)]

    for j in range(len(urls_date[::-1]) - 1, 0, -1):
        when_finish = j

        if stop_at in urls_date[j]:
            break

    return [url for url in urls[:when_finish]]


def ignore_files_func(urls):
    pattern = r'\.\w{2,3}$'

    return [url for url in urls if not re.search(pattern, url.split('/')[0])]


def ignore_urls_func(urls,ignore_urls):
    pattern = r'\w{2,4}p?\w:\/\/'
    new_ignore_urls = [re.sub(pattern, '://', url, count=0) for url in ignore_urls]
    return [re.sub(pattern, '://', url, count=0) for url in urls if url not in new_ignore_urls]


def slow_queries_func(data):
    urls_time = [(int(elem['time']), elem['url']) for elem in urls_with_inf(data)]
    urls_time.sort(key=lambda x: x[0], reverse=True)

    slow_time_list = []
    slow_list = []

    for elem_with_time in urls_time:
        for elem in urls_time[:5]:
            if elem_with_time[1] == elem[1]:
                slow_time_list.append(elem_with_time[1])
                slow_list.append(elem_with_time)

    c_s = Counter(slow_time_list)
    avg_list = []

    for elem_k, elem_v in c_s.items():
        s_s = 0
        for slow_elem in slow_list:
            if elem_k == slow_elem[1]:
                s_s += slow_elem[0]
        avg_list.append(s_s // elem_v)

    return sorted(avg_list)[::-1]

def new_slow_queries_func(data):



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

    if ignore_www:
        pattern = r':\/\/www\.'
        new_urls = [url.replace('://www.','://') if re.search(pattern, url) else url for url in urls]
        print(new_urls)
        urls.clear()
        urls = new_urls.copy()

    if ignore_files:
        new_urls = ignore_files_func(urls)
        urls.clear()
        urls = new_urls.copy()

    if ignore_urls:
        new_urls = ignore_urls_func(urls, ignore_urls)
        #print(new_urls)
        urls.clear()
        urls = new_urls.copy()

    if request_type:
        urls_type = [elem['request'] + ' ' + elem['url'] for elem in urls_with_inf(data)]
        urls = [type for type in urls_type if request_type in type]

    if start_at:
        urls = start_at_func(start_at, urls, data)

    if stop_at:
        urls = stop_at_func(stop_at, urls, data)

    if slow_queries:
        return slow_queries_func(data)

    c = Counter(urls).most_common(5)
    print(c)
    return [elem[1] for elem in c]

print(parse(ignore_urls=['http://www.sys.mail.ru/calendar/config/254/40263/','https://sys.mail.ru/calendar/config/254/40265/','http://sys.mail.ru/calendar/meeting/254/40265/']))