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
    def get_city_by_name(name):
        with get_new_db() as conn:
            condition = {
                'city_name': name
            }
            return get_table_one_row(conn, 'history_city', condition)

    @staticmethod
    def get_history_city_all():
        with get_new_db() as conn:
            return get_table_all(conn, 'history_city')

    @staticmethod
    def total_history(filters, group_name):
        city_name = filters.get('city_name')
        date_start = filters.get('date_start')
        date_end = filters.get('date_end')

        sql_select = 'SELECT %s, count(*) cnt FROM  history_day ' % (group_name, )
        sql = ''
        sql_val = ()

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

        sql_group = ' group by %s' % (group_name, )
        sql_select += sql

        # log.debug('sql:' + sql_select + ' | ' + str(sql_val))
        # SELECT weather_am, count(*) FROM `weather_day` WHERE city_name = '上海' group by `weather_am`
        with get_new_db() as conn:
            result = conn.execute(sql_select + sql_group, sql_val).fetchall()

            return result

    @staticmethod
    def all_day(filters, condition=None):
        city_name = filters.get('city_name')
        date_start = filters.get('date_start')
        date_end = filters.get('date_end')

        sql_select = 'SELECT * FROM  history_day '
        sql = ''
        sql_val = ()

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

        sql_order = ' order by hd_date asc'

        sql_select += sql

        # log.debug('sql:' + sql_select + ' | ' + str(sql_val))
        with get_new_db() as conn:
            result = conn.execute(sql_select + sql_order, sql_val).fetchall()
            return [dict(row.items()) for row in result]

    @staticmethod
    def all_city(filters, condition=None):
        hd_date = filters.get('date')

        sql_select = 'SELECT * FROM  history_day '
        sql = ''
        sql_val = ()

        if condition:
            sql_where, sql_val = make_where(condition)
            sql += ' and ' + sql_where

        if hd_date:
            sql += ' and hd_date = %s'
            sql_val += (hd_date,)

        if sql.startswith(' and '):
            sql = sql[len(' and '):]
        if sql:
            sql = 'where ' + sql

        sql_order = ' order by hd_id asc'

        sql_select += sql

        # log.debug('sql:' + sql_select + ' | ' + str(sql_val))
        with get_new_db() as conn:
            result = conn.execute(sql_select + sql_order, sql_val).fetchall()
            return [dict(row.items()) for row in result]

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

