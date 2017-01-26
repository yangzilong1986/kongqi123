from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from spider.model import HistoryCity, HistoryDay, HistoryMonth
from config import *


class Demo(object):
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE)
        self.db_session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def load_data_from_mysql(self):
        pass
