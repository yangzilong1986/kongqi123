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

    @staticmethod
    def get_job_list(city_name, year, month):
        with get_new_db() as conn:
            condition = {
                'city_name': city_name,
                # 'job_year': year,
                # 'job_month': month
            }
            # data = get_table_rows(conn, 'crawl_job', condition)

            table = 'crawl_job'
            keys = condition.keys()
            where = ' and '.join('`%s`=%%s' % (k,) for k in keys)
            param = [condition[k] for k in keys]
            sql = 'select * from ' + table + ' where ' + where + ' order by job_id desc limit 24'
            # print sql
            data = [dict(row) for row in conn.execute(sql, param).fetchall()]

            return data
