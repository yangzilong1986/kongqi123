# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from spider.items import HistoryCityItem

from sqlalchemy import Column, DateTime, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base = declarative_base()
metadata = Base.metadata
Base.to_dict = to_dict


class HistoryCity(Base):
    __tablename__ = 'history_city'

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(30), server_default=text("''::character varying"))
    city_url = Column(String(1024), server_default=text("''::character varying"))


class HistoryMonth(Base):
    hm_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String(30), server_default=text("''::character varying"))
    hm_year = Column(Integer)
    hm_month = Column(Integer)
    hm_aqi = Column(Integer)
    hm_aqi_min = Column(Integer)
    hm_aqi_max = Column(Integer)
    hm_quality = Column(String(30), server_default=text("''::character varying"))
    hm_pm25 = Column(Float)
    hm_pm10 = Column(Float)
    hm_so2 = Column(Float)
    hm_co = Column(Float)
    hm_no2 = Column(Float)
    hm_o3 = Column(Float)
    hm_rank = Column(Integer)
    hm_day_url = Column(String(255), server_default=text("''::character varying"))


class CitiesPipeline(object):

    def __init__(self, sqlalchemy_database_uri, sqlalchemy_pool_size):
        self.engine = create_engine(sqlalchemy_database_uri, pool_size=sqlalchemy_pool_size)
        self.db_session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlalchemy_database_uri=crawler.settings.get('SQLALCHEMY_DATABASE_URI_MYSQL'),
            sqlalchemy_pool_size=crawler.settings.get('SQLALCHEMY_POOL_SIZE', 8),
        )

    def open_spider(self, spider):
        self.session = self.db_session()

    def process_item(self, item, spider):
        try:
            if isinstance(item, CitiesItem):
                # 数据入库
                service_item = Cities(**item)
                self.session.add(service_item)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        return item

    def close_spider(self, spider):
        self.session.close()
