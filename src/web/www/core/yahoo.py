# coding:utf-8

import urllib2
import urllib
import json
import itertools
from web.www.helper import *
from web.db import get_new_db
from config import YAHOO_CONFIG


class Yahoo(object):

    @staticmethod
    def factory():
        if hasattr(Yahoo, '_obj'):
            return Yahoo._obj

        obj = Yahoo()
        Yahoo._obj = obj

        return obj

    @staticmethod
    def get_woeid_by_name(name):
        base_url = YAHOO_CONFIG.get('BASE_URL')

        yql_query = "select * from geo.placefinder where text = '%s'" % name
        yql_url = base_url + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)

        result = data['query']['results']
        print result
        return result


    @staticmethod
    def get_weather(woeid):
        base_url = YAHOO_CONFIG.get('BASE_URL')

        yql_query = "select * from weather.forecast where woeid = %d" % woeid
        yql_url = base_url + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)

        result = data['query']['results']
        print result
        return result

