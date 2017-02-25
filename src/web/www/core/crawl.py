# coding:utf-8

import itertools
from web.www.helper import *
from web.db import get_new_db


class Crawl(object):

    @staticmethod
    def factory():
        if hasattr(Crawl, '_obj'):
            return Crawl._obj

        obj = Crawl()
        Crawl._obj = obj

        return obj

    @staticmethod
    def get_crawl_job_info(city_name, year, month, spider):
        with get_new_db() as conn:
            condition = {
                'city_name': city_name,
                'job_year': year,
                'job_month': month,
                'job_spider': spider
            }
            return get_table_one_row(conn, 'crawl_job', condition)