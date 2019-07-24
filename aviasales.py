# Задание 1. Доработать приложение по поиску авиабилетов, чтобы
# оно возвращало билеты по названию города, а не по IATA коду.
# Пункт отправления и пункт назначения должны передаваться в качестве
# параметров. Сделать форматированный вывод, который содержит в себе
# пункт отправления, пункт назначения, дату вылета, цену билета
# (можно добавить еще другие параметры по желанию)

import requests
import requests
import json
from argparse import ArgumentParser

# parsing arguments

parser = ArgumentParser()

parser.add_argument(
    '-o', '--origin', type=str,
    required=False, help='Origin name', default='MOW')
parser.add_argument(
    '-d', '--destination', type=str,
    required=True, help='Destination name')
args = parser.parse_args()

flight_params = {
    'origin': args.origin,
    'destination': args.destination,
    'one_way': 'true'}

# iata detection

def iata_recon(data):
    key = 'f2144820-33f5-4e27-befc-c6254065d2a0'
    r = requests.get(f'https://airlabs.co/api/v6/cities?&code={data}&api_key={key}')
    try:
        return(r.json()['response'][0]['name'])
    except:
        print(f'Something wrong with {data}')


origin = iata_recon(args.origin)
destination = iata_recon(args.destination)

# requesting
req = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
data = req.json()['best_prices']
data.sort(key=lambda k : k['depart_date'])

keys = ['origin','destination','depart_date','value']
data_filtered = [dict(zip(keys, [i[k] for k in keys])) for i in data]

for i in data_filtered[:10]:
    print(f'Flight from {origin} to {destination} at {i["depart_date"]} cost {i["value"]}')
