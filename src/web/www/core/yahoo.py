# coding:utf-8

import urllib2
import urllib
import json
import redis
import itertools
import datetime
import time
from config import YAHOO_CONFIG, REDIS_CONFIG, WEATHER_TYPES_CN, WEEK_TYPE
from web.www.helper import *
from web.db import get_new_db
from web.www.core import generate_md5

redis_client = redis.Redis(host=REDIS_CONFIG.get('host'), port=REDIS_CONFIG.get('port'))


class Yahoo(object):
    @staticmethod
    def factory():
        '''
        http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D%22shanghai%22&diagnostics=true
        https://developer.yahoo.com/weather/documentation.html
        :return:
        '''
        if hasattr(Yahoo, '_obj'):
            return Yahoo._obj

        obj = Yahoo()
        Yahoo._obj = obj

        return obj

    @staticmethod
    def get_woeid_by_name(name):
        result = Yahoo.get_geo_places_info(name)
        if not result:
            return False
        if 'place' not in result:
            return False
        if not result['place']:
            return False
        if 'woeid' not in result['place'][0]:
            return False
        woeid = int(result['place'][0]['woeid'])
        if not woeid:
            return False

        return woeid

    @staticmethod
    def get_geo_places_info(name):
        '''
        {
            "query": {
                "count": 2,
                "created": "2017-02-21T03:00:38Z",
                "lang": "zh-CN",
                "results": {
                    "place": [
                        {
                            "lang": "en-US",
                            "xmlns": "http://where.yahooapis.com/v1/schema.rng",
                            "yahoo": "http://www.yahooapis.com/v1/base.rng",
                            "uri": "http://where.yahooapis.com/v1/place/2151849",
                            "woeid": "2151849",
                            "placeTypeName": {
                                "code": "7",
                                "content": "Town"
                            },
                            "name": "Shanghai",
                            "country": {
                                "code": "CN",
                                "type": "Country",
                                "woeid": "23424781",
                                "content": "China"
                            },
                            "admin1": {
                                "code": "",
                                "type": "Municipality",
                                "woeid": "12578012",
                                "content": "Shanghai"
                            },
                            "admin2": {
                                "code": "",
                                "type": "Prefecture",
                                "woeid": "26198093",
                                "content": "Shanghai"
                            },
                            "admin3": null,
                            "locality1": {
                                "type": "Town",
                                "woeid": "2151849",
                                "content": "Shanghai"
                            },
                            "locality2": null,
                            "postal": null,
                            "centroid": {
                                "latitude": "31.247709",
                                "longitude": "121.472618"
                            },
                            "boundingBox": {
                                "southWest": {
                                    "latitude": "30.975",
                                    "longitude": "121.10157"
                                },
                                "northEast": {
                                    "latitude": "31.514999",
                                    "longitude": "121.804611"
                                }
                            },
                            "areaRank": "1",
                            "popRank": "1",
                            "timezone": {
                                "type": "Time Zone",
                                "woeid": "56043597",
                                "content": "Asia/Shanghai"
                            }
                        },
                        {
                            "lang": "en-US",
                            "xmlns": "http://where.yahooapis.com/v1/schema.rng",
                            "yahoo": "http://www.yahooapis.com/v1/base.rng",
                            "uri": "http://where.yahooapis.com/v1/place/12578012",
                            "woeid": "12578012",
                            "placeTypeName": {
                                "code": "8",
                                "content": "Municipality"
                            },
                            "name": "Shanghai",
                            "country": {
                                "code": "CN",
                                "type": "Country",
                                "woeid": "23424781",
                                "content": "China"
                            },
                            "admin1": {
                                "code": "",
                                "type": "Municipality",
                                "woeid": "12578012",
                                "content": "Shanghai"
                            },
                            "admin2": null,
                            "admin3": null,
                            "locality1": null,
                            "locality2": null,
                            "postal": null,
                            "centroid": {
                                "latitude": "31.113159",
                                "longitude": "121.416611"
                            },
                            "boundingBox": {
                                "southWest": {
                                    "latitude": "30.6014",
                                    "longitude": "120.932701"
                                },
                                "northEast": {
                                    "latitude": "31.848",
                                    "longitude": "122.233856"
                                }
                            },
                            "areaRank": "1",
                            "popRank": "1",
                            "timezone": {
                                "type": "Time Zone",
                                "woeid": "56043597",
                                "content": "Asia/Shanghai"
                            }
                        }
                    ]
                }
            }
        }
        {
            "query": {
                "count": 0,
                "created": "2017-02-21T03:03:50Z",
                "lang": "zh-CN",
                "results": null
            }
        }
        {
            "error": {
                "lang": "en-US",
                "description": "Invalid identfier p. me AND me.ip are the only supported identifier in this context"
            }
        }
        '''

        name_md5 = generate_md5(name)
        redis_key = "yahoo_geo_place_city_%s" % name_md5
        result = redis_client.get(redis_key)
        if not result:
            print 'load result from remote.'
            base_url = YAHOO_CONFIG.get('BASE_URL')
            yql_query = "select * from geo.places where text = '%s'" % name
            print yql_query, type(yql_query)
            yql_url = base_url + urllib.urlencode({'q': yql_query.encode('utf-8')}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            if not result:
                return False
            redis_client.set(redis_key, result)
        else:
            print 'load result from cache.'

        data = json.loads(result)
        if 'query' not in data:
            return False
        if 'results' not in data['query']:
            return False
        result = data['query']['results']
        if result == 'null':
            return False

        # print result
        return result

    @staticmethod
    def get_weather(woeid):
        '''
        {
            "query": {
                "count": 1,
                "created": "2017-02-21T03:23:10Z",
                "lang": "zh-cn",
                "results": {
                    "channel": {
                        "units": {
                            "distance": "km",
                            "pressure": "mb",
                            "speed": "km/h",
                            "temperature": "C"
                        },
                        "title": "Yahoo! Weather - Shanghai, Shanghai, CN",
                        "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2151849/",
                        "description": "Yahoo! Weather for Shanghai, Shanghai, CN",
                        "language": "en-us",
                        "lastBuildDate": "Tue, 21 Feb 2017 11:23 AM CST",
                        "ttl": "60",
                        "location": {
                            "city": "Shanghai",
                            "country": "China",
                            "region": " Shanghai"
                        },
                        "wind": {
                            "chill": "37",
                            "direction": "85",
                            "speed": "35.40"
                        },
                        "atmosphere": {
                            "humidity": "66",
                            "pressure": "34845.95",
                            "rising": "0",
                            "visibility": "25.91"
                        },
                        "astronomy": {
                            "sunrise": "6:29 am",
                            "sunset": "5:46 pm"
                        },
                        "image": {
                            "title": "Yahoo! Weather",
                            "width": "142",
                            "height": "18",
                            "link": "http://weather.yahoo.com",
                            "url": "http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif"
                        },
                        "item": {
                            "title": "Conditions for Shanghai, Shanghai, CN at 10:00 AM CST",
                            "lat": "31.247709",
                            "long": "121.472618",
                            "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2151849/",
                            "pubDate": "Tue, 21 Feb 2017 10:00 AM CST",
                            "condition": {
                                "code": "28",
                                "date": "Tue, 21 Feb 2017 10:00 AM CST",
                                "temp": "6",
                                "text": "Mostly Cloudy"
                            },
                            "forecast": [
                                {
                                    "code": "28",
                                    "date": "21 Feb 2017",
                                    "day": "Tue",
                                    "high": "10",
                                    "low": "3",
                                    "text": "Mostly Cloudy"
                                },
                                {
                                    "code": "11",
                                    "date": "22 Feb 2017",
                                    "day": "Wed",
                                    "high": "11",
                                    "low": "6",
                                    "text": "Showers"
                                },
                                {
                                    "code": "28",
                                    "date": "23 Feb 2017",
                                    "day": "Thu",
                                    "high": "7",
                                    "low": "3",
                                    "text": "Mostly Cloudy"
                                },
                                {
                                    "code": "30",
                                    "date": "24 Feb 2017",
                                    "day": "Fri",
                                    "high": "8",
                                    "low": "3",
                                    "text": "Partly Cloudy"
                                },
                                {
                                    "code": "30",
                                    "date": "25 Feb 2017",
                                    "day": "Sat",
                                    "high": "11",
                                    "low": "2",
                                    "text": "Partly Cloudy"
                                },
                                {
                                    "code": "30",
                                    "date": "26 Feb 2017",
                                    "day": "Sun",
                                    "high": "12",
                                    "low": "5",
                                    "text": "Partly Cloudy"
                                },
                                {
                                    "code": "30",
                                    "date": "27 Feb 2017",
                                    "day": "Mon",
                                    "high": "12",
                                    "low": "6",
                                    "text": "Partly Cloudy"
                                },
                                {
                                    "code": "30",
                                    "date": "28 Feb 2017",
                                    "day": "Tue",
                                    "high": "13",
                                    "low": "6",
                                    "text": "Partly Cloudy"
                                },
                                {
                                    "code": "30",
                                    "date": "01 Mar 2017",
                                    "day": "Wed",
                                    "high": "14",
                                    "low": "6",
                                    "text": "Partly Cloudy"
                                },
                                {
                                    "code": "34",
                                    "date": "02 Mar 2017",
                                    "day": "Thu",
                                    "high": "11",
                                    "low": "5",
                                    "text": "Mostly Sunny"
                                }
                            ],
                            "description": "<![CDATA[<img src=\"http://l.yimg.com/a/i/us/we/52/28.gif\"/>
        <BR />
        <b>Current Conditions:</b>
        <BR />Mostly Cloudy
        <BR />
        <BR />
        <b>Forecast:</b>
        <BR /> Tue - Mostly Cloudy. High: 10Low: 3
        <BR /> Wed - Showers. High: 11Low: 6
        <BR /> Thu - Mostly Cloudy. High: 7Low: 3
        <BR /> Fri - Partly Cloudy. High: 8Low: 3
        <BR /> Sat - Partly Cloudy. High: 11Low: 2
        <BR />
        <BR />
        <a href=\"http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2151849/\">Full Forecast at Yahoo! Weather</a>
        <BR />
        <BR />
        (provided by <a href=\"http://www.weather.com\" >The Weather Channel</a>)
        <BR />
        ]]>",
                            "guid": {
                                "isPermaLink": "false"
                            }
                        }
                    }
                }
            }
        }
        {
            "query": {
                "count": 1,
                "created": "2017-02-21T03:24:42Z",
                "lang": "zh-CN",
                "results": {
                    "channel": {
                        "units": {
                            "distance": "km",
                            "pressure": "mb",
                            "speed": "km/h",
                            "temperature": "C"
                        }
                    }
                }
            }
        }
        {
            "error": {
                "lang": "en-US",
                "description": "Invalid identfier p. me AND me.ip are the only supported identifier in this context"
            }
        }
        :param woeid:
        :return:
        '''
        redis_key = "yahoo_weather_forecast_woeid_%d" % woeid
        result = redis_client.get(redis_key)
        if not result:
            print 'load result from remote.'
            base_url = YAHOO_CONFIG.get('BASE_URL')
            yql_query = "select * from weather.forecast where woeid = %d and u = 'c'" % woeid
            yql_url = base_url + urllib.urlencode({'q': yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            if not result:
                return False
            redis_client.set(redis_key, result, 60 * 60)
        else:
            print 'load result from cache.'

        data = json.loads(result)
        if 'query' not in data:
            return False
        if 'results' not in data['query']:
            return False
        if 'channel' not in data['query']['results']:
            return False
        result = data['query']['results']['channel']
        if result == 'null':
            return False

        print result
        return result

    @staticmethod
    def get_today_weather(woeid):
        weather_channel = Yahoo.get_weather(woeid)
        if not weather_channel:
            return False
        if 'item' not in weather_channel:
            return False

        '''
        "units": {
            "distance": "km",
            "pressure": "mb",
            "speed": "km/h",
            "temperature": "C"
        },
        风：冷风级别9，风向，风速3.22
        "wind": {
            "chill": "37",
            "direction": "85",
            "speed": "35.40"
        },
        大气情况：湿度，能见度，压强
        "atmosphere": {
            "humidity": "66",
            "pressure": "34845.95",
            "rising": "0",
            "visibility": "25.91"
        },
        天文：日出6:49am，日落5:25pm
        "astronomy": {
            "sunrise": "6:29 am",
            "sunset": "5:46 pm"
        },
        "item": {
            "title": "Conditions for Shanghai, Shanghai, CN at 10:00 AM CST",
            "lat": "31.247709",
            "long": "121.472618",
            "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2151849/",
            "pubDate": "Tue, 21 Feb 2017 10:00 AM CST",
            "condition": {
                "code": "28",
                "date": "Tue, 21 Feb 2017 10:00 AM CST",
                "temp": "6",
                "text": "Mostly Cloudy"
            },
            ...
        }
        '''

        data = {}
        if 'wind' in weather_channel:
            data = dict(data.items() + weather_channel['wind'].items())

        if 'atmosphere' in weather_channel:
            data = dict(data.items() + weather_channel['atmosphere'].items())

        if 'astronomy' in weather_channel:
            data = dict(data.items() + weather_channel['astronomy'].items())

        if 'condition' in weather_channel['item']:
            data = dict(data.items() + weather_channel['item']['condition'].items())
            t = time.strptime(data['date'], '%a, %d %b %Y %I:%M %p %Z')
            data['date2'] = t.tm_hour
            data['text2'] = WEATHER_TYPES_CN['3200']
            if data['code'] in WEATHER_TYPES_CN:
                data['text2'] = WEATHER_TYPES_CN[data['code']]
        return data

    @staticmethod
    def get_forecast_weather(woeid):
        weather_channel = Yahoo.get_weather(woeid)
        if not weather_channel:
            return False
        if 'item' not in weather_channel:
            return False

        if 'forecast' not in weather_channel['item']:
            return False

        for data in weather_channel['item']['forecast']:
            #  25 Feb 2017
            t = time.strptime(data['date'], '%d %b %Y')
            data['date2'] = time.strftime('%Y-%m-%d', t)
            data['day2'] = WEEK_TYPE[data['day']]
            data['text2'] = WEATHER_TYPES_CN['3200']
            if data['code'] in WEATHER_TYPES_CN:
                data['text2'] = WEATHER_TYPES_CN[data['code']]

        return weather_channel['item']['forecast']
