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
