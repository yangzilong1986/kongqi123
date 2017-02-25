# coding:utf-8
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI_MYSQL, SQLALCHEMY_POOL_SIZE
from web.www.core.spider import SpiderClient
from web.www.core.history import History
from web.www.core.crawl import Crawl

def init_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE)
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = db_session()
    return session


def run_export_spider_job():
    session = init_database()
    sp = SpiderClient.list_spider()
    if not sp:
        print 'bad sp'
        return False
    if 'spiders' not in sp:
        print 'no spiders'
        return False

    current = datetime.datetime.now()

    history_client = History.factory()
    history_cities = history_client.get_history_city_all()


if __name__ == '__main__':
    from web.runhelp import main

    main(__file__, __name__)
