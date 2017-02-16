# coding:utf-8

import itertools
from web.www.helper import *
from web.db import get_new_db


class History(object):

    @staticmethod
    def factory():
        if hasattr(History, '_obj'):
            return History._obj

        obj = History()
        History._obj = obj

        return obj

    @staticmethod
    def search_day(filters, page, per_page, condition=None):
        city_name = filters.get('city_name')
        date_start = filters.get('date_start')
        date_end = filters.get('date_end')

        sql_select = 'SELECT * FROM  history_day '
        sql_count = 'SELECT count(*) as c FROM  history_day '
        sql = ''
        sql_val = ()
        result = {}
        if condition:
            sql_where, sql_val = make_where(condition)
            sql += ' and ' + sql_where

        if city_name:
            sql += ' and city_name = %s'
            sql_val += (city_name,)
        if date_start:
            sql += ' and hd_date >= %s'
            sql_val += (date_start,)
        if date_end:
            sql += ' and hd_date <= %s'
            sql_val += (date_end,)

        if sql.startswith(' and '):
            sql = sql[len(' and '):]
        if sql:
            sql = 'where ' + sql

        sql_order = ' order by hd_date desc limit %d,%d' % ((page - 1) * per_page, per_page)

        sql_select += sql
        sql_count += sql

        # log.debug('sql:' + sql_select + ' | ' + str(sql_val))
        # log.debug('sql:' + sql_count + ' | ' + str(sql_val))
        with get_new_db() as conn:
            rows = conn.execute(sql_select + sql_order, sql_val).fetchall()
            total = conn.execute(sql_count, sql_val).fetchone()
            pages = get_page_count(total['c'], per_page)

            result['items'] = rows
            result['total'] = total['c']
            result['pages'] = pages
            result['has_next'] = page < pages
            result['has_prev'] = page > 1
            result['next_num'] = page + 1
            result['prev_num'] = page - 1

            return result

