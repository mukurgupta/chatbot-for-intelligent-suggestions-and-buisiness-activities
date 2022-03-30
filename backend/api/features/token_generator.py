import requests
import json


class token_generator:
    def __init__(self):
        self.client_id = '***********'
        self.client_secret = '************'
        self.grant_type = 'refresh_token'

        self.timelog_token = '************'

        self.expense_refresh_token = '***************'
        self.expense_organization_id = '************'

        self.desk_refresh_token = '****************'
        self.desk_organization_id = '**********'
        self.desk_scope = 'Desk.settings.READ,Desk.basic.READ,Desk.tickets.ALL,Desk.contacts.READ'

    def expense(self):
        url = 'https://accounts.zoho.in/oauth/v2/token?refresh_token='+self.expense_refresh_token + \
            '&client_id='+self.client_id+'&client_secret=' + \
            self.client_secret+'&grant_type='+self.grant_type
        response = requests.post(url)
        response_json = json.loads(response.text)
        oauth_token = response_json['access_token']
        return {'access_token': oauth_token, 'organization_id': self.expense_organization_id}

    def ticket(self):
        url = 'https://accounts.zoho.in/oauth/v2/token?refresh_token='+self.desk_refresh_token+'&grant_type=' + \
            self.grant_type+'&client_id='+self.client_id+'&client_secret=' + \
            self.client_secret+'&scope='+self.desk_scope
        response = requests.post(url)
        response_json = json.loads(response.text)
        oauth_token = response_json['access_token']
        return {'access_token': oauth_token, 'organization_id': self.desk_organization_id}

    def timelog(self):
        return self.timelog_token
