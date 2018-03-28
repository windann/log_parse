# -*- encoding: utf-8 -*-

from collections import Counter
import re


def urls_with_inf():
    url_inf_list = []

    with open('log.log', 'r') as f:
        # вся информация из файла, типы запросов, урлы, дата и т.д
        data = f.read().split('\n')
        date_pattern = r'\d{2}\/\w{3}\/\d{4}\s\d{2}:\d{2}:\d{2}'
        type_request_pattern = r'"\w{3,7}'
        pattern = r'http?\w:\/\/'
        repl = 'http://'
        elem_url_inf = {}

        for elem in data:

            if re.search(date_pattern, elem) and re.search(type_request_pattern, elem) and re.search(pattern, elem):
                elem_url_inf['date'] = re.findall(date_pattern, elem)[0]
                elem_url_inf['request'] = re.findall(type_request_pattern, elem)[0].lstrip('"')

                if '?' in elem.split()[3]:
                    for i in range(len(elem.split()[3]) - 1, 0, -1):
                        if elem.split()[3][i] == '?':
                            break
                    # добавляем чистый урл с приведённой к единой схеме запроса
                    elem_url_inf['url'] = re.sub(pattern, repl, elem.split()[3][:i], count=0)
                else:
                    elem_url_inf['url'] = re.sub(pattern, repl, elem.split()[3], count=0)

                elem_url_inf['time'] = elem.split()[6]
                url_inf_list.append(elem_url_inf)
                elem_url_inf = {}

    return url_inf_list


def start_at_func(start_at, urls):
    when_start = 0
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf()]

    for elem in urls_date:
        when_start += 1

        if start_at in elem:
            break

    return [url for url in urls[when_start:]]


def stop_at_func(stop_at, urls):
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf()]

    for j in range(len(urls_date[::-1]) - 1, 0, -1):
        when_finish = j

        if stop_at in urls_date[j]:
            break

    return [url for url in urls[:when_finish]]


def ignore_files_func(urls):
    for url in urls:
        for i in range(len(url) - 1, len(url) - 4, -1):
            if url[i] == '.':
                urls.remove(url)


def ignore_urls_func(urls,ignore_urls):
    for ignore_url in ignore_urls:
        for url in urls:
            if url == ignore_url:
                urls.remove(url)


def slow_queries_func():
    urls_time = [(int(elem['time']), elem['url']) for elem in urls_with_inf()]
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


def parse(ignore_urls=[],
          start_at=None,
          stop_at=None,
          request_type=None,
          ignore_www=False,
          slow_queries=False,
          ignore_files=False):

    urls = [elem['url'] for elem in urls_with_inf()]

    if ignore_www:
        pattern = r'www.'
        repl = ''
        urls = [re.sub(pattern, repl, url, count=0) for url in urls]

    if ignore_files:
        ignore_files_func(urls)

    if ignore_urls:
        ignore_urls_func(urls, ignore_urls)

    if request_type:
        urls_type = [elem['request'] + ' ' + elem['url'] for elem in urls_with_inf()]
        urls = [type for type in urls_type if request_type in type]

    if start_at:
        urls = start_at_func(start_at, urls)

    if stop_at:
        urls = stop_at_func(stop_at, urls)

    if slow_queries:
        return slow_queries_func()

    c = Counter(urls).most_common(5)
    return [elem[1] for elem in c]