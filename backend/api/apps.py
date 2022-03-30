from copyreg import constructor
from django.apps import AppConfig
import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from google.protobuf.json_format import MessageToJson
from io import StringIO
import pandas as pd
import json
import os

from .mid import mediatorCall
from .features.timelog import timelogfun
from .features.tickets import ticket_func
from .features.covidcases import covidcasesfun
from .features.expense_managment import expense_management
from .features.token_generator import token_generator
from .getters.news import news_fun
from .getters.sports import sports_intent
from .getters.movies import movies_fun
from .getters.calendar import calendar_fun


class ApiConfig(AppConfig):
    name = 'api'


class Moderator(AppConfig):
    name = 'moderator'

    def moderator(msg):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'key.json')
        DIALOGFLOW_PROJECT_ID = 'maverick-final-calowo'
        DIALOGFLOW_LANGUAGE_CODE = 'en'
        SESSION_ID = 'me'

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(
            DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(
            text=msg, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        # try:
        #     if (msg == 'sports_schedule'):
        #         resp = sports_intent()
        #         print('call2')
        #     elif (msg == 'entertainment_schedule'):
        #         resp = movies_fun()
        #     else:
        #         temp = session_client.detect_intent(
        #             session=session, query_input=query_input)
        #         reply = dict()
        #         if temp.query_result.webhook_payload:
        #             reply = dict(temp.query_result.webhook_payload)
        #         resp = {'msg': None, 'data': None}
        #         if reply and reply.get('msg') or reply.get('data'):
        #             resp['msg'] = reply.get('msg', None)
        #             # print(type(reply['data']))
        #             if reply.get('data'):
        #                 resp['data'] = pd.DataFrame(dict(reply['data']))
        #                 resp['msg2'] = temp.query_result.fulfillment_text
        #             if reply.get('category', None):
        #                 resp['category'] = reply['category']
        #         else:
        #             resp['msg'] = temp.query_result.fulfillment_text
        #     return resp
        #     # df = pd.read_csv(StringIO(reply), sep='\s+')
        #     # return {'msg': None, 'data': df};
        # except InvalidArgument:
        #     raise
        try:
            qa = mediatorCall(msg)
            output = qa.run_query()
            return output
        except:
            return {'msg': "I don't know what to make of it. Please refer to ReadMe.", 'data': None}


class Webhook(AppConfig):
    name = "webhook"

    def moderator(intent, parameters):
        intents = intent.split("_")
        print('These are intents', intents)
        if (intents[0] == 'calendar' or intents[0] == 'calender'):
            fun = calendar_fun()
        elif (intents[0] == 'sports'):
            fun = sports_intent()
        elif (intents[0] == 'news' or intents[0] == 'catnews'):
            fun = news_fun()
        elif (intents[0] == 'expense'):
            fun = expense_management()
        elif (intents[0] == 'covid'):
            fun = covidcasesfun()
        elif (intents[0] == 'tickets'):
            fun = ticket_func()
        elif (intents[0] == 'timelog'):
            fun = timelogfun()
        else:
            return "idk what you talking about"
        resp = fun.get_result('_'.join(intents[1:]), parameters)
        return resp
