import pymongo
from pprint import pprint
import requests
import json

client = pymongo.MongoClient()
db = client["starwars"]

db.starships.drop()

def get_id(st):
    lurls = st['pilots']
    pilots_name = []
    object_ids = []
    for url in lurls:
        pilot = requests.get(url).json()['name']
        pilots_name.append(pilot)
        obj = db.characters.find_one({'name': pilot})['_id']
        # pprint(obj)
        object_ids.append(obj)
    # print(object_ids)
    # print( pilots_name)
    return object_ids


def get_all_data(url):
    result = []
    json_return = requests.get(url).json()
    result.extend(json_return['results'])
    next_url = json_return['next']
    while next_url:
        json_return = requests.get(next_url).json()
        result.extend(json_return['results'])
        next_url = json_return['next']

    return result


data = get_all_data("https://swapi.dev/api/starships/")
# results["pilots"]

for st in data:
    ids = get_id(st)
    st['pilots'] = ids


db.starships.insert_many(data)