# coding:utf-8
"""
 买家接口
 """
from math import ceil

from api import helper
from api.helper import insert_table, update_table_row, make_where, to_list


def get_info_by_openid(conn, openid):
    """
    获取微信用户信息
    :param openid:
    :return:
    """
    return conn.execute('SELECT * FROM buyer_weixin WHERE openid=%s LIMIT 1 ', (openid,)).fetchone()


def get_info_by_uid(conn, uid):
    """
    根据uid获取微信用户信息
    :param uid:
    :return:
    """
    return conn.execute('SELECT * FROM buyer_weixin WHERE uid=%s LIMIT 1 ', (uid,)).fetchone()


def add_info(conn, info):
    """
    添加微信用户信息
    :param info:
    :return:
    """

    uid = insert_table(conn, 'user_global', {'user_type': 0})
    info['uid'] = uid
    insert_table(conn, 'buyer_weixin', info)
    return uid


def edit_info(conn, uid, info):
    """
    编辑微信用户信息
    :param uid:
    :param info:
    :return:
    """
    return update_table_row(conn, 'buyer_weixin', {'uid': uid}, info)


def edit_weixin(conn, uid, weixin):
    """
    编辑微信用户微信号
    :param uid:
    :param weixin:
    :return:
    """

    return update_table_row(conn, 'buyer_weixin', {'uid': uid}, {'weixin': weixin})


def get_list(conn, condition, page, per_page):
    """
    获取买家列表
    """

    sql_where, sql_val = make_where(condition)
    sql = 'SELECT * FROM  buyer_weixin WHERE ' + sql_where
    sql += (' order by uid desc limit %d,%d' % ((page - 1) * per_page, per_page))

    count_sql = 'SELECT count(*) AS c FROM  buyer_weixin WHERE ' + sql_where
    rows = to_list(conn.execute(sql, sql_val).fetchall())
    count_row = conn.execute(count_sql, sql_val).fetchone()

    result = {}

    pages = helper.get_page_count(count_row['c'], per_page)


    result['items'] = rows
    result['total'] = count_row['c']
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result
