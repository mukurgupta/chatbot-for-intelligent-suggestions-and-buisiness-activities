import urllib.request
import urllib.parse
import urllib.error
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json


def sports_intent():

    parent_url = "https://www.betexplorer.com/next/"
    sports = ["soccer", "tennis", "hockey", "basketball",
              "handball", "volleyball", "baseball"]

    schedule = {}
    schedule['league'] = []
    schedule['match'] = []

    for sport in sports:
        url = parent_url + sport + "/"
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req) as request_object:
            html = request_object.read()

        soup = BeautifulSoup(html, "html.parser")
        html = soup.prettify('utf-8')

        for t_body in soup.findAll('tbody'):
            flag = 0
            for t_r in t_body.findAll('tr', attrs={'data-def': "1"}):
                flag = 1
            if flag:
                for t_r in t_body.findAll('tr', attrs={'class': 'js-tournament'}):
                    schedule['league'].append(t_r.text.strip())
                    break

                for class_obj in t_body.findAll('td', attrs={'class': 'table-main__tt'}):
                    for a in class_obj.findAll('a'):
                        pair = ''
                        t = 1
                        for span in a.findAll('span'):
                            pair = pair + " "+span.text.strip()
                            if t:
                                pair = pair + " vs "
                                t -= 1
                        schedule['match'].append(pair)
                        break
                    break

    top_league = ['USA: National Football League', 'INDIA: Indian Premier League', 'Germany: Bundesliga', 'England: Premier League', 'Australia: Australian Football League',
                  'Japan: NPB', 'Australia: Big Bash League', 'USA: Major League Baseball', 'Spain: LaLiga', 'Spain: LaLiga2', 'USA: NBA', 'USA: WNBA']
    data = pd.DataFrame(schedule)

    data.league = data.league.apply(lambda x: x if x in top_league else np.nan)
    data = data.dropna()
    data = data.sort_values(by=['league'])

    output = {'msg': 'I have also found some sports fixtures for you. Have a look and tell me if you want some beers?', 'data': data}
    return output
