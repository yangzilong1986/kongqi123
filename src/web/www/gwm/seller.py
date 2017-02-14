#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: seller.py
@time: 16-8-15 下午1:13
"""

import time

from api import helper
from api.helper import insert_table, update_table_row, get_table_one_row


def get_global_info(conn, uid):
    """
    获取全局信息
    :param uid:
    :return:
    """
    return get_table_one_row(conn, 'user_global', {'id': uid})


def get_reg_by_name(conn, name):
    """
    获取用户注册信息
    :param name:
    :return:
    """
    return get_table_one_row(conn, 'seller', {'name': name})


def get_reg(conn, uid):
    """
    获取用户注册信息
    :param uid:
    :return:
    """
    return get_table_one_row(conn, 'seller', {'uid': uid})


def check_login(conn, username, password):
    """
    登录校验
    """
    return get_table_one_row(conn, 'seller', {'name': username, 'password': password})


def check_password(conn, uid, password):
    """
    登录校验
    """
    return get_table_one_row(conn, 'seller', {'uid': uid, 'password': password})


def add_reg(conn, info):
    """
    添加用户注册信息
    :param info:
    :return:
    """

    uid = insert_table(conn, 'user_global', {'user_type': 1})
    info['uid'] = uid
    insert_table(conn, 'seller', info)
    return uid


def edit_reg(conn, uid, info):
    """
    编辑用户注册信息
    :param uid:
    :param info:
    :return:
    """
    return update_table_row(conn, 'seller', {'uid': uid}, info)


def change_password(conn, uid, new_password):
    """
    修改用户密码
    :param uid:
    :param new_password:
    :return:
    """

    return update_table_row(conn, {'uid': uid},
                            {'password': new_password, 'update_time': time.strftime("%Y-%m-%d %H:%M:%S")})


def get_detail(conn, uid):
    """
    获取用户详细信息
    :param uid:
    :return:
    """
    return get_table_one_row(conn, 'seller_detail', {'uid': uid})


def add_detail(conn, info):
    """
    添加用户详细信息
    :param info:
    :return:
    """
    insert_table(conn, 'seller_detail', info)
    return info['uid']


def edit_detail(conn, uid, info):
    """
    编辑用户详细信息
    :param uid:
    :param info:
    :return:
    """
    update_table_row(conn, 'seller_detail', {'uid': uid}, info)


def add_sub(conn, info):
    """
    添加子账号
    :param info:
    :return:
    """
    p_uid = info.get('p_uid')
    name = info.get('name')
    real_name = info.get('real_name')
    phone = info.get('phone')
    password = info.get('password')
    shop_id = info.get('shop_id')

    uid = insert_table('user_global', {'user_type': 1})

    # 用户类型 0:普通用户, 1:商户用户

    insert_table(conn, 'seller', dict(
        uid=uid,
        name=name,
        password=password
    ))

    insert_table(conn, 'seller_detail', dict(
        uid=uid,
        real_name=real_name,
        phone=phone,
        is_sub=1,
        p_uid=p_uid,
        shop_id=shop_id
    ))

    return uid


def delete_user(conn, uid):
    """
    删除用户（标记）
    """
    return update_table_row(conn, 'user_global', {'id': uid}, {'is_delete': 1})


def sub_user_list(conn, condition, page, per_page):
    """
    获取子账号列表
    """

    sql_where, sql_params = helper.make_where(condition)

    sql = 'SELECT * FROM  seller_detail '

    if sql_where:
        sql_where = ' WHERE ' + sql_where

    rows = conn.execute(sql + sql_where, sql_params).fetchall()

    total = helper.count_table(conn, 'seller_detail', condition)
    result = {}
    pages = helper.get_page_count(total, per_page)
    result['items'] = rows
    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result
