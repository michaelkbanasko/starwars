import pymongo
from pprint import pprint
import requests
import json

#connected to the database
client = pymongo.MongoClient()
db = client["starwars"]

#emptied the previous data in the database
db.starships.drop()

#created a function to get updated id
def get_id(st):
    lurls = st['pilots']
    pilots_name = []
    object_ids = []
    for url in lurls: #ging through each url in pilot and get the objectid
        pilot = requests.get(url).json()['name']
        pilots_name.append(pilot)
        obj = db.characters.find_one({'name': pilot})['_id']
        # pprint(obj)
        object_ids.append(obj)
    # print(object_ids)
    # print( pilots_name)
    return object_ids

# function to loop through all the pages and get the data
def get_all_data(url):
    result = []
    json_return = requests.get(url).json()
    result.extend(json_return['results'])
    next_url = json_return['next']
    while next_url: #keeps looping through the different pages
        json_return = requests.get(next_url).json()
        result.extend(json_return['results'])
        next_url = json_return['next']

    return result

# get the data from api
api = "https://swapi.dev/api/starships/"
data = get_all_data(api)
# results["pilots"]

# loop through each starship and update with objectId
for st in data:
    ids = get_id(st)
    st['pilots'] = ids

# Add this to the starships collection
db.starships.insert_many(data)