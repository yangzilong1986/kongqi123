#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: commission.py
@time: 16-8-25 下午2:38
"""

from api import helper

"""
分成,即将废弃的接口 迁移到 钱包 模块

"""


def get_info(conn, condition):
    """
    获取分成信息
    :param condition:
    :return:
    """
    if not condition:
        return
    where_sql, where_param = helper.make_where(condition)
    row = conn.execute('SELECT * FROM commission WHERE  ' + where_sql + ' LIMIT 1', where_param).fetchone()
    return row


def add(conn, info):
    return helper.insert_table(conn, 'commission', info)


def get_sum_first_money(conn, condition):
    """
    获取一级分成统计
    :param condition:
    :return:
    """

    where_sql, where_params = helper.make_where(condition)
    row = conn.execute('SELECT sum(first_amount) AS c FROM commission WHERE ' + where_sql).fetchone()
    return row['c']


def get_sum_second_money(conn, condition):
    """
    获取二级分成统计
    :param condition:
    :return:
    """
    where_sql, where_params = helper.make_where(condition)
    row = conn.execute('SELECT sum(second_amount) AS c FROM commission WHERE ' + where_sql).fetchone()
    return row['c']


def get_count(conn, condition):
    """
    获取分成统计
    :param condition:
    :return:
    """
    where_sql, where_params = helper.make_where(condition)
    row = conn.execute('SELECT count(*) AS c FROM commission WHERE ' + where_sql).fetchone()
    return row['c']
