import requests
import pandas as pd

class covidcasesfun:
    def cases(state,district):
        url='https://api.covid19india.org/state_district_wise.json'
        res=requests.get(url)

        response= pd.DataFrame(pd.DataFrame(pd.read_json(res.text)[state]).iloc[0,0][district])[['active','confirmed','recovered']].iloc[0:1,:]
        res={'msg':None,'data':response}
        return res
