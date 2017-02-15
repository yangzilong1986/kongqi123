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
    def search(filters, page, per_page, condition=None):
        keyword = filters.get('keyword')
        price_min = filters.get('price_min')
        price_max = filters.get('price_max')
        sales_min = filters.get('sales_min')
        sales_max = filters.get('sales_max')

        sql_select = 'SELECT * FROM  product '
        sql_count = 'SELECT count(*) as c FROM  product '
        sql = ''
        sql_val = ()
        result = {}
        if condition:
            sql_where, sql_val = make_where(condition)
            sql += ' and ' + sql_where

        if keyword:
            sql += ' and name like %s'
            sql_val += ('%' + keyword + '%',)
        if price_min:
            sql += ' and price >= %s'
            sql_val += (price_min,)
        if price_max:
            sql += ' and price <= %s'
            sql_val += (price_max,)
        if sales_min:
            sql += ' and price >= %s'
            sql_val += (sales_min,)
        if sales_max:
            sql += ' and price <= %s'
            sql_val += (sales_max,)

        if sql.startswith(' and '):
            sql = sql[len(' and '):]
        if sql:
            sql = 'where ' + sql

        sql_order = ' order by id desc limit %d,%d' % ((page - 1) * per_page, per_page)

        sql_select += sql
        sql_count += sql

        # log.debug('sql:' + sql_select + ' | ' + str(sql_val))
        # log.debug('sql:' + sql_count + ' | ' + str(sql_val))
        with get_new_db() as conn:
            rows = to_list(conn.execute(sql_select + sql_order, sql_val).fetchall())
            total = conn.execute(sql_count, sql_val).fetchone()['c']
            pages = get_page_count(total, per_page)

            for row in rows:
                pass

            result['items'] = rows
            result['total'] = total['c']
            result['pages'] = pages
            result['has_next'] = page < pages
            result['has_prev'] = page > 1
            result['next_num'] = page + 1
            result['prev_num'] = page - 1

            return result

