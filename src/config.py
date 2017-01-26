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
