# coding:utf-8
"""
shop 店铺接口
"""
from math import ceil
from api import helper

from api.helper import insert_table, update_table_row, make_where, to_list, get_table_one_row

import logging
log = logging.getLogger('app')


def get_shop_info(conn, condition):
    """
    根据条件获取商铺信息
    """
    return get_table_one_row(conn, 'shop', condition)


def get_apply_info(conn, condition):
    """
    根据条件获取申请信息
    """
    return get_table_one_row(conn, 'apply_join', condition)


def get_apply_info_by_id(conn, apply_id):
    """
    根据主键id获取申请信息
    """
    return get_table_one_row(conn, 'apply_join', {'id': apply_id})


def get_apply_info_by_uid(conn, uid):
    """
    根据uid获取申请信息
    """
    return get_table_one_row(conn, 'apply_join', {'uid': uid})


def add_apply_info(conn, info):
    """
    添加入驻信息
    :param info:
    :return:
    """
    return insert_table(conn, 'apply_join', info)


def edit_apply_info(conn, apply_id, info):
    """
    编辑入驻信息
    :param apply_id:
    :param info:
    :return:
    """
    return update_table_row(conn, 'apply_join', {'id': apply_id}, info)


def get_shop_info_by_shop_id(conn, shop_id):
    """
    通过shop_id获取商铺信息
    :param shop_id:
    :return:
    """
    return get_table_one_row(conn, 'shop', {'id': shop_id})


def get_shop_info_by_uid(conn, uid):
    """
    通过uid获取商铺信息
    :param uid:
    :return:
    """
    return get_table_one_row(conn, 'shop', {'uid': uid})


def add_shop(conn, info):
    """
    添加商铺信息
    :param info:
    :return:
    """
    return insert_table(conn, 'shop', info)


def edit_shop(conn, shop_id, info):
    """
    编辑商铺信息
    :param shop_id:
    :param info:
    :return:
    """
    return update_table_row(conn, 'shop', {'id': shop_id}, info)


def search(conn, filters, page, per_page, condition=None):
    """
    商铺搜索
    条件：
        filters = {
            'join_type': '',
            'check_status': '',
            'keyword': ''  暂时支持公司名称
        }
    """
    join_type = filters.get('join_type')
    check_status = filters.get('check_status')
    keyword = filters.get('keyword')

    result = {}
    sql_where = ''
    sql_param = []
    if condition:
        sql_where, sql_param = helper.make_where(condition)

    if join_type:
        sql_where += ' and join_type=%s'
        sql_param += [join_type]

    if check_status:
        sql_where += ' and check_status=%s'
        sql_param += [check_status]

    if keyword:
        sql_where += ' and company_name like %s'
        sql_param += ['%' + keyword + '%']
    if sql_where.startswith(' and '):
        sql_where = sql_where[len(' and '):]

    if sql_where:
        sql_where = 'where ' + sql_where

    sql = 'select * from apply_join ' + sql_where \
          + (' order by `id` desc limit %d,%d' % ((page - 1) * per_page, per_page))
    rows = conn.execute(sql).fetchall()

    count_sql = 'SELECT count(*) AS c FROM apply_join ' + sql_where
    count_row = conn.execute(count_sql, sql_param).fetchone()
    total = count_row['c']

    pages = helper.get_page_count(total, per_page)

    result['items'] = rows
    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result


def stat_shop_count(conn, shop_id):
    """
    统计商铺相关数量（全部商品数量，热门推荐数量，代言报告数量）
    """
    product_all_count = conn.execute('SELECT count(*) AS c FROM product WHERE shop_id=%s AND is_delete=0',
                                     (shop_id,)).fetchone()['c']
    product_hot_count = conn.execute('SELECT count(*) AS c FROM product WHERE shop_id=%s AND is_delete=0 \
                                      AND is_recommend=1',
                                     (shop_id,)).fetchone()['c']
    report_all_count = conn.execute('SELECT count(*) AS c FROM endorse WHERE shop_id=%s AND is_delete=0',
                                    (shop_id,)).fetchone()['c']

    return {
        'product_all_count': product_all_count,
        'product_hot_count': product_hot_count,
        'report_all_count': report_all_count
    }


def shop_all(conn):
    return conn.execute('SELECT * FROM shop ORDER BY id DESC').fetchall()
