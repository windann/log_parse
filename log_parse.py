# -*- encoding: utf-8 -*-

from collections import Counter
import re

<<<<<<< HEAD

def urls_with_inf(data):
    url_inf_list = []

    date_pattern = r'\d{2}\/\w{3}\/\d{4}\s\d{2}:\d{2}:\d{2}'
    type_request_pattern = r'"\w{3,7}'
    pattern = r'\w{2,4}p?\w:\/\/'
=======
# функция получения "чистых урлов" и запись всей информации (дата, тип запроса, сам урл) в словарь
def urls_with_inf():
    url_inf_list = []

    with open('log.log', 'r') as f:
        # вся информация из файла, типы запросов, урлы, дата и т.д
        data = f.read().split('\n')
        # шаблон даты
        date_pattern = r'\d{2}\/\w{3}\/\d{4}\s\d{2}:\d{2}:\d{2}'
        # шаблон типа запроса
        type_request_pattern = r'"\w{3,7}'
        # шаблон схемы
        pattern = r'http?\w:\/\/'
        
        repl = 'http://'
        elem_url_inf = {}

        for elem in data:
            # проверяем запрос ли это и записываем в словарь информацию о нём
            if re.search(date_pattern, elem) and re.search(type_request_pattern, elem) and re.search(pattern, elem):
                elem_url_inf['date'] = re.findall(date_pattern, elem)[0]
                elem_url_inf['request'] = re.findall(type_request_pattern, elem)[0].lstrip('"')
>>>>>>> cb069e7bd598c2500861b7b0e7db9cedce43d093

    for elem in data:
        elem_url_inf = {}
        if re.search(date_pattern, elem) and re.search(type_request_pattern, elem) and re.search(pattern, elem):
            elem_url_inf['date'] = re.findall(date_pattern, elem)[0]
            elem_url_inf['request'] = re.findall(type_request_pattern, elem)[0].lstrip('"')
            elem_url_inf['url'] = re.sub(pattern, '://', elem.split('?')[0].split()[3], count=0)
            elem_url_inf['time'] = elem.split()[6]
            url_inf_list.append(elem_url_inf)


    return url_inf_list

<<<<<<< HEAD

def start_at_func(start_at, urls,data):
=======
# возвращает список урлов, начиная с указанной даты
def start_at_func(start_at, urls):
>>>>>>> cb069e7bd598c2500861b7b0e7db9cedce43d093
    when_start = 0
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf(data)]

    for elem in urls_date:
        when_start += 1

        if start_at in elem:
            break

    return [url for url in urls[when_start:]]

<<<<<<< HEAD

def stop_at_func(stop_at, urls,data):
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf(data)]
=======
# возвращает список урлов, заканчивая указанной датой
def stop_at_func(stop_at, urls):
    urls_date = [elem['date'] + ' ' + elem['url'] for elem in urls_with_inf()]
>>>>>>> cb069e7bd598c2500861b7b0e7db9cedce43d093

    for j in range(len(urls_date[::-1]) - 1, 0, -1):
        when_finish = j

        if stop_at in urls_date[j]:
            break

    return [url for url in urls[:when_finish]]

# проходим по урлам в обратном порядке, если встречаем среди последних 4ёх символов точку, занчит это файл
# урл должен быть удалён
def ignore_files_func(urls):
    for url in urls:
        for i in range(len(url) - 1, len(url) - 5, -1):
            if url[i] == '.':
                urls.remove(url)

# прверяем наличие текущего урла в списке запрещённых
def ignore_urls_func(urls,ignore_urls):
    for ignore_url in ignore_urls:
        for url in urls:
            if url == ignore_url:
                urls.remove(url)


<<<<<<< HEAD
def slow_queries_func(data):
    urls_time = [(int(elem['time']), elem['url']) for elem in urls_with_inf(data)]
=======
def slow_queries_func():
    # запись в список кортежей время и запрос
    urls_time = [(int(elem['time']), elem['url']) for elem in urls_with_inf()]
    # сортировка по времени, начиная с самых медленных
>>>>>>> cb069e7bd598c2500861b7b0e7db9cedce43d093
    urls_time.sort(key=lambda x: x[0], reverse=True)

    slow_time_list = []
    slow_list = []
    # если текущий урл в списке самых медленных(после сортировки первые 5 элементов - самые медленные)
    # записываем все подходящие урлы в единый словарь
    # а в другой список записываем ещё и информацию о времени
    for elem_with_time in urls_time:
        for elem in urls_time[:5]:
            if elem_with_time[1] == elem[1]:
                slow_time_list.append(elem_with_time[1])
                slow_list.append(elem_with_time)
                
            
    # находим количество повторений таких урлов 
    c_s = Counter(slow_time_list)
    avg_list = []
    # проходим по словарю, где указаны количества повторений и по общему списку
    # в случае совпадения считаем всю сумму времени
    # затем из словаря берём количество вхождений и находим среднее
    for elem_k, elem_v in c_s.items():
        s_s = 0
        for slow_elem in slow_list:
            if elem_k == slow_elem[1]:
                s_s += slow_elem[0]
        avg_list.append(s_s // elem_v)
    # отсортированный список переворачиваем
    return sorted(avg_list)[::-1]


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
<<<<<<< HEAD
        pattern = r':\/\/www\.'
        new_urls = [url.replace('://www.','://') if re.search(pattern, url) else url for url in urls]
        print(new_urls)
        urls.clear()
        urls = new_urls.copy()
=======
        pattern = r':\/\/www.'
        repl = ''
        urls = [re.sub(pattern, repl, url, count=0) for url in urls]
>>>>>>> cb069e7bd598c2500861b7b0e7db9cedce43d093

    if ignore_files:
        ignore_files_func(urls)

    if ignore_urls:
        ignore_urls_func(urls, ignore_urls)

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
    return [elem[1] for elem in c]
<<<<<<< HEAD

print(parse())
=======
>>>>>>> cb069e7bd598c2500861b7b0e7db9cedce43d093
