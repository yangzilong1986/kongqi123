# coding:utf-8
import itertools
from web.www.helper import *

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

    sql_select = 'SELECT * FROM  product '
    sql_count = 'SELECT count(*) as c FROM  product '
    sql = ''
    sql_val = ()
    result = {}
    if condition:
        sql_where, sql_val = helper.make_where(condition)
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
    rows = helper.to_list(conn.execute(sql_select + sql_order, sql_val).fetchall())
    total = conn.execute(sql_count, sql_val).fetchone()['c']

    pages = helper.get_page_count(total, per_page)

    for row in rows:
        img = get_product_cover_img(conn, row['id'])
        if img:
            row['img_url'] = img.get('img_url')

    result['items'] = rows
    result['total'] = total['c']
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result

