# coding:utf-8

import urllib2
import urllib
import json
import itertools
from web.www.helper import *
from web.db import get_new_db


class Yahoo(object):

    @staticmethod
    def factory():
        if hasattr(Yahoo, '_obj'):
            return Yahoo._obj

        obj = Yahoo()
        Yahoo._obj = obj

        return obj

    @staticmethod
    def get_weather():
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select wind from weather.forecast where woeid=2460286"
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)
        print data['query']['results']