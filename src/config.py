# -*- coding: utf-8 -*-

MODE = 'dev'

# 数据库 MySQL
if MODE == 'dev':
    DB_MYSQL = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': '1987527',
        'port': 3306,
        'db': 'pm25'
    }
else:
    DB_MYSQL = {
        'host': '10.0.0.1',
        'user': 'root',
        'passwd': 'ayumihamasaki',
        'port': 3306,
        'db': 'pm25'
    }

SQLALCHEMY_DATABASE_URI_MYSQL = \
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % \
    (DB_MYSQL['user'], DB_MYSQL['passwd'], DB_MYSQL['host'], DB_MYSQL['port'], DB_MYSQL['db'])

# 默认 pool_size=5
SQLALCHEMY_POOL_SIZE = 5


# yahoo api
YAHOO_CONFIG = {
    'BASE_URL': 'https://query.yahooapis.com/v1/public/yql?',
    # (Consumer Key)
    'CLIENT_ID': 'dj0yJmk9SXpYbVZIa000dkpWJmQ9WVdrOWVIWjViamM0TXpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kMA--',
    # (Consumer Secret)
    'CLIENT_SECRET': 'bcc4568341c0fd845e97771c494a65675d82fc3c'
}


import os
from logging.config import dictConfig
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

WEB_WWW = {
    'debug': True
}

LOG_CONFIG = {

}
"""
def log_conf(name=None):
    dictConfig(LOG_CONFIG)

log_conf()

"""

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
    SECRET_KEY = '76751a270d0785eea367301db62752f3'
