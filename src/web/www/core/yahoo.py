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
        base_url = YAHOO_CONFIG.get('BASE_URL')

        yql_query = "select * from geo.places where text = '%s'" % name
        yql_url = base_url + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
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
        base_url = YAHOO_CONFIG.get('BASE_URL')

        yql_query = "select * from weather.forecast where woeid = %d and u = 'c'" % woeid
        yql_url = base_url + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
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

