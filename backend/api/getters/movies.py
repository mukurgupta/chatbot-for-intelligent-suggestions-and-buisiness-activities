import requests
import json
from datetime import datetime
import pandas as pd

no_of_pages = 6
Language = 'English'
Date_today = '2020-07-03'
no_of_items_finally = 4


def movie_extractor(page):
    url = 'https://api.themoviedb.org/3/movie/upcoming?'
    api_key = '*************'
    language = 'en-US'
    page = page
    final_url = url+'api_key='+api_key+'&language='+language+'&page='+str(page)
    response = requests.get(final_url)
    response_json = json.loads(response.text)
    result_list = response_json['results']
    return result_list


def release_date_sorter(elem):
    return datetime.strptime(elem['release_date'], '%Y-%m-%d')


def movies_fun():
    # Getting the No of Pages
    upcoming_movie_list = []
    for i in range(1, no_of_pages):
        try:
            upcoming_movie_list.extend(movie_extractor(i))
        except:
            break
    # Sorting the Movies based on release Date
    upcoming_movie_list.sort(key=release_date_sorter)
    # Filtering movies based on today's date and Language
    language_dictionary = {
        'Czech': 'cs',
        'Danish': 'da',
        'German': 'de',
        'English': 'en',
        'Spanish': 'es',
        'Estonion': 'et',
        'French': 'fr',
        'Galician': 'gl',
        'Hindi': 'hi',
        'Indonesian': 'id',
        'Italian': 'it',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Norwegian': 'no',
        'Polish': 'pl',
        'Portugese': 'pt',
        'Tamil': 'ta',
        'Thai': 'th',
        'Vietnamese': 'vi',
        'Chinese': 'zh'
    }
    filtered_list = []
    for element in upcoming_movie_list:
        if((datetime.strptime(element['release_date'], '%Y-%m-%d') > datetime.strptime(Date_today, '%Y-%m-%d'))):
            if(element['original_language'] == language_dictionary[Language]):
                filtered_list.append(element)
    final_list = []
    for i in range(0, no_of_items_finally):
        try:
            temp = {}
            temp['title'] = filtered_list[i]['title']
            temp['overview'] = filtered_list[i]['overview']
            temp['release_date'] = filtered_list[i]['release_date']
            final_list.append(temp)
        except:
            break
    # Final Dataframe
    data = pd.DataFrame(final_list)
    return {'msg': 'I have also found some movies. Have a look and tell me if you want some beers?', 'data': data}
