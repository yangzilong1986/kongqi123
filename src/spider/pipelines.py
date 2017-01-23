# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from items import HistoryCityItem, HistoryMonthItem, HistoryDayItem
from model import HistoryCity, HistoryDay, HistoryMonth


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base = declarative_base()
metadata = Base.metadata
Base.to_dict = to_dict


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
            if isinstance(item, HistoryCityItem):
                # 数据入库
                service_item = HistoryCity(**item)

                row_sql = "select count(*) cnt from history_city where city_name = :city_name"
                row_data = {"city_name": service_item.city_name}
                row = self.session.execute(row_sql, row_data).fetchone()

                if not row['cnt']:
                    self.session.add(service_item)
                    self.session.commit()
            elif isinstance(item, HistoryMonthItem):
                service_item = HistoryMonth(**item)

                row_sql = "select * from history_city where city_name = :city_name"
                row_data = {"city_name": service_item.city_name}
                row = self.session.execute(row_sql, row_data).fetchone()
                if 'city_id' in row:
                    service_item.city_id = row['city_id']
                # print u"----- HistoryMonthItem:%s" % json.dumps(dict(service_item), indent=4, ensure_ascii=False)

                row_sql = "select count(*) cnt from history_month " \
                          "where city_name = :city_name and hm_year = :hm_year and hm_month = :hm_month"
                row_data = {
                    "city_name": service_item.city_name,
                    "hm_year": service_item.hm_year,
                    "hm_month": service_item.hm_month
                }
                row = self.session.execute(row_sql, row_data).fetchone()
                if not row['cnt']:
                    self.session.add(service_item)
                    self.session.commit()
            elif isinstance(item, HistoryDayItem):
                service_item = HistoryDay(**item)

                row_sql = "select * from history_city where city_name = :city_name"
                row_data = {"city_name": service_item.city_name}
                row = self.session.execute(row_sql, row_data).fetchone()
                if 'city_id' in row:
                    service_item.city_id = row['city_id']
                # print u"----- HistoryMonthItem:%s" % json.dumps(dict(service_item), indent=4, ensure_ascii=False)

                row_sql = "select count(*) cnt from history_day " \
                          "where city_name = :city_name and hd_date = :hd_date"
                row_data = {
                    "city_name": service_item.city_name,
                    "hd_date": service_item.hd_date,
                }
                row = self.session.execute(row_sql, row_data).fetchone()
                if not row['cnt']:
                    self.session.add(service_item)
                    self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        return item

    def close_spider(self, spider):
        self.session.close()
