# coding:utf-8

import itertools
from web.www.helper import *
from web.db import get_new_db


class Crawl(object):

    JOB_TYPE_HISTORY = 1
    JOB_TYPE_WEATHER = 2
    JOB_STATUS_READY = 1
    JOB_STATUS_DOING = 2
    JOB_STATUS_FINISH = 3

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

    @staticmethod
    def create_crawl_job_info(data):
        with get_new_db() as conn:
            return insert_table(conn, 'crawl_job', data)
