import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from datetime import datetime, timedelta, date
import pandas as pd
from .places import get_bars, get_tourism

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class calendar_fun:

    def __init__(self):
        print('calender function is being called')
        FLOW = OAuth2WebServerFlow(
            client_id='*************',
            client_secret='***********',
            scope='https://www.googleapis.com/auth/calendar',
            user_agent='maverick/2.0')

        storage = Storage('calendar.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(FLOW, storage, flags)

        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build('calendar', 'v3', http=http,
                             developerKey='************')

    def get_result(self, intent, parameters):
        print(intent)
        if (intent == 'get_events'):
            return self.get_events(parameters)
        elif (intent == 'book_flight'):
            return self.book_flight(parameters)
        elif (intent == 'create_event'):
            return self.create_event(parameters)
        elif (intent == 'book_flight - bars' or 'book_flight - places'):
            return self.get_flight_places(intent, parameters)

    def get_events(self, params):
        # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        timeS = params['date'][:10] + 'T00:00:00+05:30'
        timeE = str(pd.to_datetime(
            params['date'][:10], format='%Y-%m-%d') + timedelta(days=1))[:10] + 'T00:00:00+05:30'
        events_result = self.service.events().list(calendarId='primary', timeMin=timeS,
                                                   timeMax=timeE, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        events_list = []
        if not events:
            return {'msg': 'No upcoming events found.', 'data': None}
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            events_list.append(
                [event['summary'], event.get('location', ''), start, end])
        data = pd.DataFrame(events_list, columns=[
                            'Name', 'Location', 'Start Time', 'Ending Time'])
        # return data
        return {'msg': None, 'data': data.to_dict('list')}
        # return data.to_string()
        # return data.to_string()

    def create_event(self, params):
        GMT_TIME = '+05:30'
        startdate = params['date'][:11] + params['time'][11:]
        t = params['time'][11:16]
        final = str(pd.to_datetime(t, format='%H:%M') +
                    timedelta(hours=0.5))[11:]
        endtime = params['date'][:11] + final + GMT_TIME
        event = {'summary': params['event_title'],
                 'start': {
                     'dateTime': startdate,
        },
            'end': {
                     'dateTime': endtime,
        },
        }
        if params.get('location'):
            event['location'] = params['location']
        try:
            self.service.events().insert(calendarId='primary',
                                         sendUpdates='all', body=event).execute()
            return {'msg': 'Event added successfully.', 'data': None}
        except:
            return{'msg': 'Error in adding event', 'data': None}

    def book_flight(self, params):
        title = "Trip to " + params['geo-city']
        startdate = params['date'][:10]
        endDate = str(pd.to_datetime(
            params['date'][:10], format='%Y-%m-%d') + timedelta(days=1))[:10]
        event = {'summary': title,
                 'start': {
                     'date': startdate,
                 },
                 'end': {
                     'date': endDate,
                 },
                 'location': params['geo-city']
                 }
        self.service.events().insert(calendarId='primary',
                                     sendUpdates='all', body=event).execute()
        return {'msg': None, 'data': None}

    def get_flight_places(self, intent, params):
        if (intent == 'book_flight - bars'):
            return get_bars(params['flight_place'])
        else:
            print('getting tourism', params['flight_place'])
            return get_tourism(params['flight_place'])

    def set_remainder(self, params):
        if params['news_cat'] == 'sports':
            title = "Sports match"
        elif params['news_cat'] == 'entertainment':
            title = "Movie release"
        startdate = str(date.today() + timedelta(days=1))
        endDate = str(date.today() + timedelta(days=2))
        event = {'summary': title,
                 'start': {
                     'date': startdate,
                 },
                 'end': {
                     'date': endDate,
                 }
                 }
        self.service.events().insert(calendarId='primary',
                                     sendUpdates='all', body=event).execute()
        return {'msg': None, 'data': None}
