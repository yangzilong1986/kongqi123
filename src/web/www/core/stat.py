#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: stat.py
@time: 16-7-26 下午2:05
"""

import logging
from logging.config import dictConfig

from api import helper
from config import LOG_CONFIG
from tools.id_encode import encode_id

dictConfig(LOG_CONFIG)

logger = logging.getLogger('app')


def get_shop_stat(conn, shop_id):
    """
    获取商铺统计
    """
    return helper.get_table_one_row(conn, 'stat_shop', {'shop_id': shop_id})


def get_product_stat(conn, product_id):
    """
    获取商品统计
    """
    return helper.get_table_one_row(conn, 'stat_product', {'product_id': product_id})


def search(conn, filters, page, per_page, condition=None):
    """
    搜索
    分页：
        items: 信息列表
        has_next: 如果本页之后还有超过一个分页，则返回True
        has_prev: 如果本页之前还有超过一个分页，则返回True
        next_num: 返回下一页的页码
        prev_num: 返回上一页的页码
    """

    keyword = filters.get('keyword')
    price_min = filters.get('price_min')
    price_max = filters.get('price_max')
    sales_min = filters.get('sales_min')
    sales_max = filters.get('sales_max')

    result = {}

    where_sql, params = helper.make_where(condition)

    if keyword:
        where_sql += ' and name like %s '
        params += ['%' + keyword + '%']
    if price_min:
        where_sql += ' and price>=%s'
        params += [price_min]
    if price_max:
        where_sql += ' and price<=%s'
        params += [price_max]
    if sales_min:
        where_sql += ' and sales>=%s'
        params += [sales_min]
    if sales_max:
        where_sql += ' and sales<=%s'
        params += [sales_max]

    if where_sql.startswith(' and '):
        where_sql = where_sql[len(' and '):]

    if where_sql:
        where_sql = ' WHERE ' + where_sql

    sql = 'SELECT * FROM product ' + where_sql + (' order by id desc limit %d,%d' % ((page - 1) * per_page, per_page))
    rows = conn.execute(sql, params).fetchall()

    sql_count = 'SELECT count(*) AS c FROM product ' + where_sql
    row_count = conn.execute(sql_count, params).fetchone()
    total = row_count['c']

    pages = helper.get_page_count(total, per_page)

    from api.biz.core import product

    def convert_item(item):
        row = dict(item)
        row['_id'] = row['id']
        row['id'] = encode_id(row['_id'])
        row['product_stat'] = get_product_stat(conn, row['_id'])
        img_info = product.get_product_cover_img(conn, row['_id'])
        if img_info:
            row['img_url'] = img_info['img_url']
        return row

    result['items'] = map(convert_item, rows)

    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result


def daily_shop(conn, page, per_page):
    result = {}
    sql = 'select * from stat_day_shop order by id desc LIMIT %d,%d' % ((page - 1) * per_page, per_page)
    rows = conn.execute(sql).fetchall()

    count_row = conn.execute('SELECT count(*) AS c FROM stat_day_shop').fetchone()
    total = count_row['c']

    pages = helper.get_page_count(total, per_page)

    result['items'] = []
    for k, row in enumerate(rows):
        result['items'].append(row.__dict__)

    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1

    return result


def daily_user(conn, page, per_page):
    result = {}
    sql = 'select * from stat_day_user order by id desc LIMIT %d,%d' % ((page - 1) * per_page, per_page)
    rows = conn.execute(sql).fetchall()
    count_row = conn.execute('SELECT count(*) AS c FROM stat_day_user').fetchone()
    total = count_row['c']
    pages = helper.get_page_count(total, per_page)
    result['items'] = helper.to_list(rows)
    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1

    return result
