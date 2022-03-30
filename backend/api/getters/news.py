import nltk
import string
import json
import requests
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from keras.models import load_model
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
from datetime import datetime, timedelta, date
from .calendar import calendar_fun

nltk.download('wordnet')
nltk.download('stopwords')


class news_fun:

    def preprocess(self, text):
        final_text = []
        stopword = set(stopwords.words('english'))

        words = text.split()

        for i in words:
            if i not in stopword:
                final_text.append(i)

        lemmatizer = WordNetLemmatizer()
        final_text = list(
            map(lambda x: lemmatizer.lemmatize(x, 'v'), final_text))

        return ' '.join(final_text)

    def get_result(self, intent, parameters):
        if (intent == 'get'):
            return self.news_intent(parameters)
        elif (intent == 'get - yes - yes'):
            return self.set_remainder(parameters)

    def news_intent(self, params):
        if 'category' not in params:
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            mod = os.path.join(THIS_FOLDER, 'model.h5')
            model = tf.keras.models.load_model(
                mod, custom_objects={'KerasLayer': hub.KerasLayer})
            apiKey = '**************'
            response = requests.get(
                "https://newsapi.org/v2/top-headlines?country=in&apiKey="+apiKey)
            data = pd.DataFrame(json.loads(response.text)['articles'])[
                ['title', 'description', 'url', 'content']]
            data = data.dropna().reindex()
            X = pd.DataFrame()
            X = data.title + " " + data.description + " " + data.content
            X = pd.DataFrame(X)
            data.drop(['description', 'content'], axis=1, inplace=True)

            for i in range(X.shape[0]):
                X.iloc[i, 0] = self.preprocess(X.iloc[i, 0])

            X = tf.data.Dataset.from_tensor_slices((X.values))
            preds = model.predict(X)
            preds = np.argmax(preds, axis=1)
            data['category'] = preds
            d = ["sport", "general", "us", "business",
                 "health", "entertainment", "technology"]
            data.category = data.category.apply(lambda x: d[x])

            data = pd.DataFrame(data.groupby(['category'], as_index=False).first())[
                ['title', 'category', 'url']]
            output = {'msg': 'I have fetched latest news for you.',
                      'data': data.to_dict('list')}
            return output
        else:
            apiKey = "************"
            t = "https://newsapi.org/v2/top-headlines?country=in&category=" + \
                params['category'] + "&apiKey=" + apiKey
            response = requests.get(t)
            data = pd.DataFrame(json.loads(response.text)['articles'])[
                ['title', 'url']]
            output = {'msg': None, 'data': data.to_dict(
                'list'), 'category': params['category']}
            return output

    def set_remainder(self, params):
        c = calendar_fun()
        if 'news_cat' in params:
            return c.set_remainder(params)


# a = news_fun()
# b = a.news_intent({'category': 'sport'})
# c = b.to_dict()
# d = pd.DataFrame.from_dict(c)
