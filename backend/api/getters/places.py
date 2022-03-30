import json
import requests
import pandas as pd


def get_bars(city):
    headers = {'Accept': 'application/json',
               'user-key': '***********'}
    url = 'https://developers.zomato.com/api/v2.1/cities?q=' + city
    response = requests.get(url, headers=headers)

    city_id = json.loads(response.text)['location_suggestions'][0]['id']

    params = {'entity_id': '10', 'entity_type': 'city',
              'count': '3', 'collection_id': '3'}

    url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' + \
        str(city_id) + "&entity_type=city&count=3&establishment_type=7"

    response = requests.get(url, headers=headers)

    out = json.loads(response.text)['restaurants']

    data = {}
    data['Place'] = []
    data['Locality'] = []

    for i in range(3):
        data['Place'].append(out[i]["restaurant"]['name'])
        data['Locality'].append(out[i]["restaurant"]['location']['locality'])

    return {'msg': None, 'data': pd.DataFrame(data).to_dict('list')}


def get_tourism(city):

    cid = "*********"
    cs = "*************"

    t = "https://api.foursquare.com/v2/venues/explore?near=" + \
        city + "&limit=3" + "&section=outdoors"
    url = t + "&client_id=" + cid + "&client_secret=" + cs + "&v=20200704"

    response = requests.get(url)
    out = json.loads(response.text)['response']['groups'][0]['items']

    data = {}
    data['Place'] = []
    data['Locality'] = []

    for i in range(3):
        data['Place'].append(out[i]['venue']['name'])
        try:
            data['Locality'].append(out[i]['venue']['location']['address'])
        except:
            data['Locality'].append(city)

    return {'msg': None, 'data': pd.DataFrame(data).to_dict('list')}
