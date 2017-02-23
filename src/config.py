# -*- coding: utf-8 -*-
import os
import sys

MODE = 'dev'

BASE_PATH = os.path.join(os.path.dirname(__file__), '../../')

# 数据库 MySQL
if MODE == 'dev':
    DB_MYSQL = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': '1987527',
        'port': 3306,
        'db': 'pm25'
    }
    REDIS_CONFIG = {
        'host': '127.0.0.1',
        'port': 6379
    }
else:
    DB_MYSQL = {
        'host': '10.0.0.1',
        'user': 'root',
        'passwd': 'ayumihamasaki',
        'port': 3306,
        'db': 'pm25'
    }
    REDIS_CONFIG = {
        'host': '127.0.0.1',
        'port': 6379
    }

# 数据库连接字符串
SQLALCHEMY_DATABASE_URI_MYSQL = \
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % \
    (DB_MYSQL['user'], DB_MYSQL['passwd'], DB_MYSQL['host'], DB_MYSQL['port'], DB_MYSQL['db'])

# 数据库进程池大小 默认pool_size=5
SQLALCHEMY_POOL_SIZE = 5

# yahoo api
YAHOO_CONFIG = {
    'BASE_URL': 'https://query.yahooapis.com/v1/public/yql?',
    # (Consumer Key)
    'CLIENT_ID': 'dj0yJmk9SXpYbVZIa000dkpWJmQ9WVdrOWVIWjViamM0TXpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kMA--',
    # (Consumer Secret)
    'CLIENT_SECRET': 'bcc4568341c0fd845e97771c494a65675d82fc3c'
}

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detail': {
            'format': '%(asctime)s - %(name)s - File: %(filename)s - line: %(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO'
        },
        'file_alert_cron': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'detail',
            'level': 'DEBUG',
            'when': 'D',
            'filename': os.path.join(BASE_PATH, 'logs/file_alert_cron.log')
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_alert_cron'],
            'level': 'ERROR'
        },
        'alert_cron': {
            'handlers': ['console','file_alert_cron'],
            'level': 'DEBUG'
        },
    }
}

WEATHER_TYPES = {
    '0': 'tornado',
    '1': 'tropical storm',
    '2': 'hurricane',
    '3': 'severe thunderstorms',
    '4': 'thunderstorms',
    '5': 'mixed rain and snow',
    '6': 'mixed rain and sleet',
    '7': 'mixed snow and sleet',
    '8': 'freezing drizzle',
    '9': 'drizzle',
    '10': 'freezing rain',
    '11': 'showers',
    '12': 'showers',
    '13': 'snow flurries',
    '14': 'light snow showers',
    '15': 'blowing snow',
    '16': 'snow',
    '17': 'hail',
    '18': 'sleet',
    '19': 'dust',
    '20': 'foggy',
    '21': 'haze',
    '22': 'smoky',
    '23': 'blustery',
    '24': 'windy',
    '25': 'cold',
    '26': 'cloudy',
    '27': 'mostly cloudy (night)',
    '28': 'mostly cloudy (day)',
    '29': 'partly cloudy (night)',
    '30': 'partly cloudy (day)',
    '31': 'clear (night)',
    '32': 'sunny',
    '33': 'fair (night)',
    '34': 'fair (day)',
    '35': 'mixed rain and hail',
    '36': 'hot',
    '37': 'isolated thunderstorms',
    '38': 'scattered thunderstorms',
    '39': 'scattered thunderstorms',
    '40': 'scattered showers',
    '41': 'heavy snow',
    '42': 'scattered snow showers',
    '43': 'heavy snow',
    '44': 'partly cloudy',
    '45': 'thundershowers',
    '46': 'snow showers',
    '47': 'isolated thundershowers',
    '3200': 'not available',
}
'''
风力共有十三个等级，
0级指每秒    风速为0至0.2米,特征是静风,烟直上。
1级指每秒风速为0.3至1.5米，特    征是软风，烟能表示方向。
2级指每秒风速为1.6至3.3米，特征是轻风、树枝有微响。
3级指每秒风速3.4至5.4米，特征是微风，旌旗展开。
4级指每秒风速为5.5到7.9米，特征是和风，地面尘土和纸张能被风吹起。
5级指每秒风速为8至10.7米，特征是清劲风，小树摇动，水面有小波。
6级指每秒风速为10.8至13.8米，特征是强风，大树枝摇动，电线呼呼有响。
7级指每秒风速为13.9至17.1米，特征是疾风，全树摇动，迎风步行困难。
8级指每秒风速为17.2至20.7米，特征是大风，树枝折毁，步行向前阻力很大。
9级指每秒风速20.8至24.4米，特征是烈风，能吹毁小屋顶，汽船航行困难。
10级指每秒风速24.5至28.4米，特征是狂风，陆上少见，可吹毁建筑物。
11级指每秒风速28.5至32.6米，特征是暴风，摧毁力很大，汽船遇之极危险。
12级指每秒风速大于32.6米，特征是飓风，海浪滔天，摧毁力极大。

'''

class BaseConfig(object):
    """
    flask 站点 共享的配置属性
    """
    DEBUG = False
    CSRF_ENABLED = True


class MainConfig(BaseConfig):
    """
    主站 flask 配置
    """
    DEBUG = True
    CSRF_ENABLED = True
