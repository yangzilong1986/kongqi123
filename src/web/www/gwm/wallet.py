#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: wallet.py
@time: 16-9-2 下午4:33
"""

import decimal
import logging
from decimal import Decimal

from api import helper
from api.biz.buyer_relation import BuyerRelationApi
from api.models import WalletItem
from config import COMMISSION_CONF

log = logging.getLogger('api')


# 卖家的销售收入
WALLET_TYPE_SELL = 1
# 买家的代言分成
WALLET_TYPE_ENDORSE = 2

WALLET_STATUS_PENDING = 0


def do_commission(conn, order_id):
    """
    执行分成逻辑
    :param conn:
    :param order_id:
    :return:
    """
    # 订单基本信息
    order_info = conn.execute('SELECT * FROM `order` WHERE id = %s ', (order_id,)).fetchone()
    if order_info is None:
        log.error(u'order_id:%s, 订单信息不存在' % (order_id,))
        return
    # 获取上下级关系
    relation_info = BuyerRelationApi.get_relation_info(order_info['uid'], order_info['shop_id'])
    if relation_info is None:
        log.error(u'order_id:%s,uid:%s,shop_id:%s, get_relation_info is none',
                  (order_id, order_info['uid'], order_info['shop_id']))
        return

    # 卖家钱包加入
    shop_uid = order_info['shop_uid']

    items = conn.execute('SELECT * FROM order_item WHERE order_id = %s ', (order_id,)).fetchall()
    # todo: 检查进位情况
    total_endorse = 0
    for item in items:
        amount_1 = Decimal(COMMISSION_CONF[0]) * item['commission_amount']
        amount_2 = Decimal(COMMISSION_CONF[1]) * item['commission_amount']
        # 加入钱包
        total_endorse += amount_1 + amount_2

        add_wallet_item(conn, {
            'uid': relation_info['p1_uid'],
            'amount': amount_1,
            'order_id': order_id,
            'status': WALLET_STATUS_PENDING,
            'type': WALLET_TYPE_ENDORSE,
        })

        add_wallet_item(conn, {
            'uid': relation_info['p2_uid'],
            'amount': amount_2,
            'order_id': order_id,
            'status': WALLET_STATUS_PENDING,
            'type': WALLET_TYPE_ENDORSE,
        })

    # 卖家收入
    amount_seller = order_info['amount_total'] - total_endorse

    add_wallet_item(conn, {
        'uid': shop_uid,
        'amount': amount_seller,
        'order_id': order_id,
        'status': WALLET_STATUS_PENDING,
        'type': WALLET_TYPE_SELL,
    })


def calc_wallet_info(conn, uid):
    """
    重新计算钱包
    :param conn:
    :param uid:
    :return:
    """
    available = decimal.Decimal(0.00)
    total = decimal.Decimal(0.00)
    # todo:类型调整
    items = conn.execute('SELECT * FROM wallet_item WHERE uid=?', (uid,))
    for item in items:  # type: WalletItem
        # 可用余额
        if item['type'] in [1, 2, 3] and item['status'] == 1:
            available += item['money']
        # 总金额
        if item['type'] in [1, 2, 3] and item['status'] in [0, 1]:
            total += item['money']
    # 更新总表
    params = (uid, available, total, available, total,)
    conn.execute('INSERT INTO wallet (uid,available,total) VALUES(?,?,?) '
                 'ON DUPLICATE KEY UPDATE available=?,total=? ', params)
    return {'total': total, 'available': available}


def add_wallet_item(conn, info):
    """
    新增钱包记录
    :param conn:
    :param info:
    :return:
    """
    item_id = helper.insert_table(conn, 'wallet_item', info)
    calc_wallet_info(conn, info['uid'])
    return item_id


def get_wallet_info(conn, uid):
    """
    查询钱包状态
    :param conn:
    :param uid:
    :return:
    """
    default_info = {'total': 0, 'available': 0}
    row = conn.execute('SELECT total, available FROM wallet WHERE uid=%s LIMIT 1', (uid,)).fetchone()
    if row is None:
        return default_info
    return dict(row)


def update_wallet_item_status(conn, item_id, status):
    """
    修改钱包明细记录的状态 status:类型:0:待生效1:已生效2:作废
    """
    row = conn.execute('SELECT * FROM wallet_item WHERE id=%d LIMIT 1', (item_id,)).fetchone()
    if row is None:
        log.error('wallet_item_id:%s, get info none' % (item_id,))
        return
    conn.execute('UPDATE wallet_item SET status=%s WHERE id=%d', (status, item_id))
    calc_wallet_info(conn, row['uid'])


def get_wallet_item(conn, item_id):
    """
    获取钱包明细
    """
    return helper.get_table_one_row(conn, 'wallet_item', {'id': item_id})


def get_latest_request(conn, uid):
    """
    获取最新 的一条 提现请求
    """
    row = conn.execute('SELECT * FROM wallet_request WHERE uid=uid ORDER BY id DESC LIMIT 1',
                       (uid,)).fetchone()
    return row


def add_wallet_request(conn, info):
    """
    发起提现请求
    余额检查
    :param conn:
    :param info:
    :return:
    """
    return helper.insert_table(conn, 'wallet_request', info)


def get_list(conn, last_id, limit, condition=None):
    """
    获取钱包明细列表 钱包id降序（动态加载）
    condition = {'uid': xxx, 'type': 3}  # 提现列表
    :param conn:
    :param last_id: 页面传递过来的的最小id
    :param limit:
    :param condition:
    :return:
    """
    sql = 'SELECT * FROM  wallet_item WHERE id < %s' % (last_id, )
    sql_val = ()
    if condition:
        sql_where, sql_val = helper.make_where(condition)
        sql += ' and ' + sql_where
    sql += ' order by id desc limit %d' % (limit, )
    rows = helper.to_list(conn.execute(sql, sql_val).fetchall())
    return rows


def search(conn, filters, page, per_page, condition=None):
    """
    钱包明细
    """
    start_time = filters.get('start_time')
    end_time = filters.get('end_time')
    name = filters.get('name')
    src_id = filters.get('src_id')
    status = filters.get('status')
    result = {}

    sql_select = 'SELECT * FROM  wallet_item WHERE 1=1'
    sql_count = 'SELECT count(*) as c FROM  wallet_item WHERE 1=1'
    sql = ''
    sql_val = ()
    if condition:
        sql_where, sql_val = helper.make_where(condition)
        sql += ' and ' + sql_where

    if start_time:
        sql += ' and create_time >= %s'
        sql_val = sql_val + (start_time,)
    if end_time:
        sql += ' and create_time <= %s'
        sql_val = sql_val + (end_time,)
    if name:
        sql += ' and name like %s'
        sql_val = sql_val + ('%'+name+'%',)
    if src_id:
        sql += ' and src_id = %s'
        sql_val = sql_val + (src_id,)
    if status:
        sql += ' and status = %s'
        sql_val = sql_val + (status,)
    sql += ' order by id desc limit %d,%d' % ((page - 1) * per_page, per_page)

    sql_select += sql
    sql_count += sql

    rows = helper.to_list(conn.execute(sql_select, sql_val).fetchall())
    total = conn.execute(sql_select, sql_val).fetchone()['c']

    pages = helper.get_page_count(total, per_page)

    result['items'] = rows
    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result
