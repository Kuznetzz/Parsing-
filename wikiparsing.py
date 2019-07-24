# Задание 2. В приложении парсинга википедии получить первую ссылку на
# другую страницу и вывести все значимые слова из неё. Результат записать
# в файл в форматированном виде

# Задание 3.*Научить приложение определять количество ссылок в статье.
# Спарсить каждую ссылку и результаты записать в отдельные файлы.

import yaml
import collections
import requests
import re
from urllib.parse import unquote

def return_wiki_html(topic):
    wiki_request = requests.get(f'{url}{topic}')
    return wiki_request.text

def return_words(topic):
    wiki_html = return_wiki_html(topic)
    words = re.findall('[а-яА-Я]{4,}', wiki_html)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    return words_counter.most_common(10)

def parse_to_file(link):
    count_words = return_words(link)

    dict_for_yaml = {}
    for i in count_words:
        dict_for_yaml[i[0]] = i[1]

    with open(f'{link}.yaml', 'w', encoding='utf-8') as to_write:
        yaml.dump(dict_for_yaml, to_write, default_flow_style=False, allow_unicode=True, sort_keys=False)


url = 'https://ru.wikipedia.org/wiki/'
topic = "Трамвай"


print(f'Parsing {url+topic}')
page = return_wiki_html(topic)
links = [i for i in  re.findall(r'href=\"/wiki/(.*?)\"', page) if ":" not in i ][1:]
print(f'Total {len(links)} links')
print(f'Parsing and saving results for fist 10 links :')
for i in links[:10]:
    print(f'Parsing {url+unquote(i)}')
    parse_to_file(unquote(i))
    print(f'parsing saved in {unquote(i)}.yaml')
print()
print(f'Process Done ')
