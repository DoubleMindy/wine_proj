from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pprint
import argparse
import pandas
from collections import defaultdict

parser = argparse.ArgumentParser(description = 'Шаблонизация винного сайта')
parser.add_argument('-p', '--path', help = 'Путь к файлу')
args = parser.parse_args()

data_df = pandas.read_excel(args.path).rename(columns = {
    'Категория': 'wine_type', 
    'Название': 'wine_title', 
    'Сорт': 'wine_sort', 
    'Цена': 'wine_price',
    'Картинка': 'wine_pic', 
    'Акция': 'wine_sale'
    }).fillna(0)

data_df = data_df.to_dict(orient = 'records')

wines = defaultdict(list)
for item in data_df:
    wines[item['wine_type']].append(item)

# pprint.pprint(wine_dict, indent = 4)

current_year = datetime.datetime.today().year - 1920

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    wines = wines,
    cur_year = current_year
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
