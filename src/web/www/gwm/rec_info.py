#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rec_info.py
@time: 16-7-15 上午11:35
"""

from api.helper import insert_table, update_table_row, get_table_one_row


def get_info(conn, rec_id):
    """
    获取用户收货信息
    """
    return get_table_one_row(conn, 'rec_info', {'id': rec_id})


def get_default_info(conn, uid):
    """
    获取用户收货默认信息
    """

    return get_table_one_row(conn, 'rec_info', {'uid': uid, 'default_status': 1})


def get_list(conn, uid):
    """
    获取用户收货信息列表
    """

    return get_table_one_row(conn, 'rec_info', {'uid': uid})


def edit(conn, rec_info_id, info):
    """
    编辑收货信息
    """
    return update_table_row(conn, 'rec_info', {'id': rec_info_id}, info)


def add(conn, info):
    """
    添加收货信息
    :param info:
    :return:
    """
    return insert_table(conn, 'rec_info', info)


def delete(conn, rec_id):
    """
    删除收货信息
    :param rec_id:
    :return:
    """
    return conn.execute('DELETE FROM rec_info WHERE id=%s', (rec_id,))


def update_rows(conn, uid, data):
    """
    批量修改数据
    :param uid:
    :param data:
    :return:
    """
    return update_table_row(conn, 'rec_info', {'uid': uid}, data)
